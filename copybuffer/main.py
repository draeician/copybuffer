import argparse
import mimetypes
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple

import pyperclip
import tiktoken
from pathspec import PathSpec

DEFAULT_IGNORE_PATTERNS = [
    ".git",
    ".git/",
    ".git/**",
]

from .core import (
    __VERSION__,
    check_dependencies,
    copy_file_contents_to_clipboard,
    copy_image_to_clipboard,
    generate_heredoc_script,
    get_file_stats,
    format_file_stats,
    install_dependencies,
    encoding,
)


@dataclass
class FileEntry:
    abs_path: Path
    display_path: str


def _load_gitignore_spec(base_dir: Path) -> PathSpec | None:
    gitignore_path = base_dir / ".gitignore"
    lines: List[str] = list(DEFAULT_IGNORE_PATTERNS)
    if gitignore_path.is_file():
        lines.extend(gitignore_path.read_text().splitlines())
    if not lines:
        return None
    return PathSpec.from_lines("gitwildmatch", lines)


def _is_ignored(path: Path, spec: PathSpec | None, base_dir: Path) -> bool:
    if spec is None:
        return False
    try:
        relative = path.resolve().relative_to(base_dir)
    except ValueError:
        relative = path.resolve()
    return spec.match_file(str(relative))


def _classify_path(
    path: Path,
    display_path: str,
    allow_images: bool,
) -> Tuple[List[FileEntry], List[FileEntry]]:
    mime_type, _ = mimetypes.guess_type(str(path))
    entry = FileEntry(abs_path=path, display_path=display_path)
    if mime_type and mime_type.startswith("image/"):
        if allow_images:
            return [], [entry]
        return [], []
    return [entry], []


def _discover_directory(
    original_argument: str,
    directory: Path,
    recursive: bool,
    allow_images: bool,
    spec: PathSpec | None,
    base_dir: Path,
    debug: bool = False,
) -> Tuple[List[FileEntry], List[FileEntry]]:
    text_entries: List[FileEntry] = []
    image_entries: List[FileEntry] = []
    iterator: Iterable[Path]
    if recursive:
        iterator = directory.rglob("*")
    else:
        iterator = directory.iterdir()

    for child in iterator:
        if _is_ignored(child, spec, base_dir):
            if debug:
                print(f"Debug: Skipping ignored path {child}")
            continue

        try:
            is_dir = child.is_dir()
        except OSError:
            continue

        if is_dir:
            # Skip directories; files within will be handled via rglob.
            continue

        if not child.is_file():
            continue

        try:
            relative = child.relative_to(directory)
            display_path = str(Path(original_argument) / relative)
        except ValueError:
            display_path = str(child)

        text, images = _classify_path(child, display_path, allow_images)
        text_entries.extend(text)
        image_entries.extend(images)

    text_entries.sort(key=lambda entry: entry.display_path)
    image_entries.sort(key=lambda entry: entry.display_path)
    return text_entries, image_entries


def discover_files(
    inputs: Sequence[str],
    include_directory: bool,
    recursive: bool,
    allow_images: bool,
    base_dir: Path | None = None,
    debug: bool = False,
) -> Tuple[List[FileEntry], List[FileEntry], List[str], List[str]]:
    base_dir = (base_dir or Path.cwd()).resolve()
    spec = _load_gitignore_spec(base_dir)

    text_entries: List[FileEntry] = []
    image_entries: List[FileEntry] = []
    missing: List[str] = []
    directory_errors: List[str] = []
    seen: set[Path] = set()

    for raw_path in inputs:
        provided_path = Path(raw_path)
        if provided_path.is_absolute():
            candidate = provided_path.resolve()
        else:
            candidate = (base_dir / provided_path).resolve()

        if not candidate.exists():
            missing.append(raw_path)
            continue

        if candidate.is_dir():
            effective_recursive = recursive or (not include_directory)
            dir_text, dir_images = _discover_directory(
                raw_path,
                candidate,
                effective_recursive,
                allow_images,
                spec,
                base_dir,
                debug,
            )
            for entry in dir_text:
                if entry.abs_path in seen:
                    continue
                seen.add(entry.abs_path)
                text_entries.append(entry)
            for entry in dir_images:
                if entry.abs_path in seen:
                    continue
                seen.add(entry.abs_path)
                image_entries.append(entry)
            continue

        if _is_ignored(candidate, spec, base_dir):
            if debug:
                print(f"Debug: Skipping ignored path {candidate}")
            continue

        try:
            display_path = str(candidate.relative_to(base_dir))
        except ValueError:
            display_path = raw_path

        if candidate in seen:
            continue
        seen.add(candidate)

        text, images = _classify_path(candidate, display_path, True)
        text_entries.extend(text)
        image_entries.extend(images)

    return text_entries, image_entries, missing, directory_errors


def main():  # pragma: no cover
    parser = argparse.ArgumentParser(
        description="Copy file contents, images, or STDIN input to clipboard."
    )
    parser.add_argument("--version", action="store_true", help="Display the application version.")
    parser.add_argument(
        "files", nargs="*", help="Files to copy (reads from STDIN if not provided)"
    )
    parser.add_argument(
        "-i", "--include-header", action="store_true", help="Include the filename as a header in copied text"
    )
    parser.add_argument(
        "-d",
        "--directory",
        action="store_true",
        help="Copy contents of all files in provided directories (non-recursive)",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Recursively copy contents of provided directories",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Display the copied contents"
    )
    parser.add_argument(
        "-a", "--attachment", action="store_true", help="Format output as Discord attachment"
    )
    parser.add_argument(
        "-p",
        "--paste",
        action="store_true",
        help="Format output as a shell heredoc script to create files on paste",
    )
    parser.add_argument(
        "--append",
        action="store_true",
        help="Like --paste, but append to the target files instead of overwriting",
    )
    parser.add_argument(
        "-t", "--tokens", action="store_true", help="Display token statistics for the file"
    )
    parser.add_argument(
        "--image", action="store_true", help="Include image files discovered in directories"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    # Check dependencies before proceeding
    missing_dependencies = check_dependencies()
    if missing_dependencies:
        print("Missing dependencies:")
        for dep in missing_dependencies:
            print(f"- {dep}")
        install_dependencies()
        return

    if args.version:
        print(f"copybuffer version {__VERSION__}")
        return

    # If no files provided, check STDIN
    if not args.files:
        if args.paste or args.append:
            print("Error: --paste/--append require file paths to determine output destinations.")
            return
        content = sys.stdin.read().strip()
        if args.debug:
            print(f"Debug: Read from STDIN: {content}")
        
        # Handle token counting for STDIN
        if args.tokens:
            # Calculate text statistics
            lines = content.splitlines()
            words = content.split()
            char_count = len(content)
            char_no_spaces = len(content.replace(' ', '').replace('\n', '').replace('\r', ''))
            
            # Calculate token count
            enc = tiktoken.get_encoding(encoding)
            tokens = enc.encode(content)
            token_count = len(tokens)
            
            # Display statistics
            avg_line_length = char_count / len(lines) if lines else 0.00
            avg_word_length = sum(len(word) for word in words) / len(words) if words else 0.00
            avg_bytes_per_token = char_count / token_count if token_count > 0 else 0.00
            tokens_per_word = token_count / len(words) if words and len(words) > 0 else 0.00
            
            output = [
                "\nSTDIN Input Statistics",
                "=" * 25,
                "\nText Statistics:",
                f"Lines: {len(lines):,}",
                f"Words: {len(words):,}",
                f"Characters (with spaces): {char_count:,}",
                f"Characters (no spaces): {char_no_spaces:,}",
                f"Average Line Length: {avg_line_length:.2f} characters",
                f"Average Word Length: {avg_word_length:.2f} characters",
                "\nToken Statistics:",
                f"Token Count: {token_count:,}",
                f"Avg Bytes per Token: {avg_bytes_per_token:.2f}" if token_count > 0 else "Avg Bytes per Token: N/A",
                f"Tokens per Word: {tokens_per_word:.2f}" if words and len(words) > 0 else "Tokens per Word: N/A",
            ]
            print('\n'.join(output))
        
        combined_contents = copy_file_contents_to_clipboard(
            [content], args.include_header, args.attachment, debug=args.debug
        )
        if combined_contents:
            print("STDIN copied to the clipboard successfully!")
            if args.verbose:
                print("Copied contents:\n" + combined_contents)
        return

    text_entries, image_entries, missing, directory_errors = discover_files(
        args.files, args.directory, args.recursive, args.image, debug=args.debug
    )

    for missing_path in missing:
        print(f"Error: File '{missing_path}' not found")

    for directory_path in directory_errors:
        print(
            f"Error: Directory '{directory_path}' requires --directory (-d) or --recursive (-r)."
        )

    file_contents_list: List[str] = []
    valid_file_paths: List[str] = []
    for entry in text_entries:
        try:
            with entry.abs_path.open("r") as file:
                file_content = file.read().strip()
        except FileNotFoundError:
            print(f"Error: File '{entry.display_path}' not found")
            continue
        except Exception as e:
            print(f"Error reading {entry.display_path}: {e}")
            continue

        file_contents_list.append(file_content)
        valid_file_paths.append(entry.display_path)
        if args.debug:
            print(f"Debug: Read file {entry.abs_path}")

    for image_entry in image_entries:
        if args.debug:
            print(f"Debug: Processing image {image_entry.abs_path}")
        if copy_image_to_clipboard(str(image_entry.abs_path)):
            print(
                f"Image '{image_entry.display_path}' copied to clipboard successfully!"
            )

    if file_contents_list:
        if args.paste or args.append:
            script_text = generate_heredoc_script(
                valid_file_paths, file_contents_list, append=args.append
            )
            try:
                pyperclip.copy(script_text)
                if args.verbose:
                    print("Copied heredoc script:\n" + script_text)
                print("Heredoc script copied to clipboard successfully!")
            except Exception as e:
                print(f"Error: An unexpected error occurred. {str(e)}")
        else:
            combined_contents = copy_file_contents_to_clipboard(
                file_contents_list,
                args.include_header,
                args.attachment,
                valid_file_paths,
                args.debug,
            )
            if combined_contents:
                print("Files copied to clipboard successfully!")
                if args.verbose:
                    print("Copied contents:\n" + combined_contents)

    all_entries = text_entries + image_entries
    if args.tokens:
        if not all_entries:
            return
        enc = tiktoken.get_encoding(encoding)
        for entry in all_entries:
            try:
                stats = get_file_stats(str(entry.abs_path))
                token_count = None

                if not stats["is_binary"]:
                    with entry.abs_path.open("r") as file:
                        content = file.read()
                        tokens = enc.encode(content)
                        token_count = len(tokens)

                print(format_file_stats(entry.display_path, stats, token_count))

            except FileNotFoundError:
                print(f"Error: File '{entry.display_path}' not found")
            except Exception as e:
                print(f"Error processing {entry.display_path}: {e}")
        return


__all__ = ["main", "discover_files"]
