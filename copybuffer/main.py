import argparse
import mimetypes
import sys

import pyperclip
import tiktoken

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
        "-d", "--directory", action="store_true", help="Copy contents of all files in directory"
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
        "--image", action="store_true", help="Force treating input files as images"
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
        combined_contents = copy_file_contents_to_clipboard(
            [content], args.include_header, args.attachment, debug=args.debug
        )
        if combined_contents:
            print("STDIN copied to the clipboard successfully!")
            if args.verbose:
                print("Copied contents:\n" + combined_contents)
        return

    # Process files
    file_contents_list = []
    valid_file_paths = []
    for file_path in args.files:
        mime_type, _ = mimetypes.guess_type(file_path)
        if args.debug:
            print(f"Debug: MIME type for {file_path}: {mime_type}")
        if args.image or (mime_type and mime_type.startswith("image/")):
            if copy_image_to_clipboard(file_path):
                print(f"Image '{file_path}' copied to clipboard successfully!")
            continue
        try:
            with open(file_path, "r") as file:
                file_content = file.read().strip()
                file_contents_list.append(file_content)
                valid_file_paths.append(file_path)
                if args.debug:
                    print(f"Debug: Read file {file_path}")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            continue
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

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

    if args.tokens:
        enc = tiktoken.get_encoding(encoding)
        for file_path in args.files:
            try:
                stats = get_file_stats(file_path)
                token_count = None

                if not stats["is_binary"]:
                    with open(file_path, "r") as file:
                        content = file.read()
                        tokens = enc.encode(content)
                        token_count = len(tokens)

                print(format_file_stats(file_path, stats, token_count))

            except FileNotFoundError:
                print(f"Error: File '{file_path}' not found")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        return


__all__ = ["main"]
