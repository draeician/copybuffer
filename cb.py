#!/usr/bin/env python3

import argparse
import importlib.util
import os
import shutil
import sys

import pyperclip

__VERSION__ = "1.8.0"


def is_wayland() -> bool:
    """Return True if running in a Wayland session."""
    return bool(
        os.environ.get("WAYLAND_DISPLAY")
        or os.environ.get("XDG_SESSION_TYPE") == "wayland"
        or os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
        or os.environ.get("SWAYSOCK")
    )


def is_wlclipboard_installed() -> bool:
    return shutil.which("wl-copy") is not None and shutil.which("wl-paste") is not None

def is_xclip_installed():
    return shutil.which("xclip") is not None

def is_xsel_installed():
    return shutil.which("xsel") is not None

def has_display() -> bool:
    """Return True if an X11 display is available."""
    return bool(os.environ.get("DISPLAY"))

def is_pyperclip_installed():  # pragma: no cover
    return importlib.util.find_spec("pyperclip") is not None

def check_dependencies():
    missing_dependencies = []

    if is_wayland():
        if not is_wlclipboard_installed():
            missing_dependencies.append("wl-clipboard (wl-copy and wl-paste)")
    elif not has_display():
        missing_dependencies.append("DISPLAY environment variable")
    elif not is_xclip_installed() and not is_xsel_installed():
        missing_dependencies.append("xclip or xsel")

    if not is_pyperclip_installed():
        missing_dependencies.append("pyperclip")

    return missing_dependencies

def install_dependencies():
    print("Please install the following dependencies:")
    dependencies = check_dependencies()
    for dep in dependencies:
        print(f"- {dep}")

def copy_file_contents_to_clipboard(
    file_contents_list,
    include_header=False,
    discord_attachment=False,
    file_paths=None,
    debug=False,
):
    try:
        combined_contents = ""
        for i, file_contents in enumerate(file_contents_list):
            if include_header and file_paths:
                header = f"=== File: {file_paths[i]} ===\n"
                file_contents = header + file_contents

            if discord_attachment and file_paths:
                file_contents = (
                    f"[Attached file: {file_paths[i]}\nContent:\n```\n{file_contents}\n```\n]"
                )

            combined_contents += file_contents + "\n"
            if debug:
                print(f"Debug: Combined contents so far:\n{combined_contents}")

        pyperclip.copy(combined_contents)
        if debug:
            print(f"Debug: Final combined contents copied to clipboard:\n{combined_contents}")
        return combined_contents
    except pyperclip.PyperclipException:
        if is_wayland():
            print("Error: Install 'wl-clipboard' for Wayland clipboard support.")
        elif not has_display():
            print(
                "Error: No DISPLAY environment variable. Ensure an X server is running or install wl-clipboard for Wayland."
            )
        else:
            print("Error: No clipboard mechanism found. Install xclip or xsel.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred. {str(e)}")
        return None

def _choose_unique_heredoc_delimiter(contents: str) -> str:
    """Choose a heredoc delimiter that does not appear in contents.

    Args:
        contents: The string content that will be placed inside the heredoc.

    Returns:
        A delimiter string safe to use as a heredoc terminator.
    """
    import secrets

    base = "EOF_CB_"
    # Try a few times to find a delimiter not present in contents
    for _ in range(10):
        candidate = base + secrets.token_hex(4).upper()
        if candidate not in contents:
            return candidate
    # Fallback: extremely unlikely to collide
    return base + secrets.token_hex(16).upper()

def _shell_single_quote(value: str) -> str:
    """Safely single-quote a string for POSIX shell.

    Replaces single quotes using the standard pattern: ' -> '\''
    """
    return "'" + value.replace("'", "'\\''") + "'"

def generate_heredoc_script(file_paths, file_contents_list, append=False) -> str:
    """Generate a shell script using heredoc to create or append files with their contents.

    Uses a single-quoted heredoc delimiter to avoid shell expansion and interpolation.

    Args:
        file_paths: List of file paths corresponding to the contents provided.
        file_contents_list: List of file contents as strings.
        append: If True, appends to files (>>). If False, overwrites (>)

    Returns:
        Combined shell script text for recreating the files on a target system.
    """
    lines = ["#!/usr/bin/env bash"]
    redir = ">>" if append else ">"
    for path, contents in zip(file_paths, file_contents_list):
        delimiter = _choose_unique_heredoc_delimiter(contents)
        quoted_path = _shell_single_quote(path)
        # Ensure parent directory exists on target system
        lines.append(f"mkdir -p \"$(dirname -- {quoted_path})\"")
        # Use single-quoted delimiter to disable interpolation
        lines.append(f"cat {redir} {quoted_path} << '{delimiter}'")
        lines.append(contents)
        lines.append(delimiter)
        lines.append("")
    return "\n".join(lines)

def copy_to_clipboard():
    # Check if input is from STDIN or file
    if len(sys.argv) == 1:
        # Read from STDIN
        try:
            content = sys.stdin.read()
            pyperclip.copy(content)
        except Exception as e:
            print(f"Error copying from STDIN: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Existing file reading logic
        try:
            with open(sys.argv[1], 'r') as file:
                content = file.read()
                pyperclip.copy(content)
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Copy file contents, images, or STDIN input to clipboard.")
    parser.add_argument("--version", action="store_true", help="Display the application version.")
    parser.add_argument("files", nargs="*", help="Files to copy (reads from STDIN if not provided)")
    parser.add_argument("-i", "--include-header", action="store_true", help="Include the filename as a header in copied text")
    parser.add_argument("-d", "--directory", action="store_true", help="Copy contents of all files in directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Display the copied contents")
    parser.add_argument("-a", "--attachment", action="store_true", help="Format output as Discord attachment")
    parser.add_argument("-p", "--paste", action="store_true", help="Format output as a shell heredoc script to create files on paste")
    parser.add_argument("--append", action="store_true", help="Like --paste, but append to the target files instead of overwriting")
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
        combined_contents = copy_file_contents_to_clipboard([content], args.include_header, args.attachment, debug=args.debug)
        if combined_contents:
            print("STDIN copied to the clipboard successfully!")
            if args.verbose:
                print("Copied contents:\n" + combined_contents)
        return

    # Process files
    file_contents_list = []
    valid_file_paths = []
    for file_path in args.files:
        try:
            with open(file_path, 'r') as file:
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
            script_text = generate_heredoc_script(valid_file_paths, file_contents_list, append=args.append)
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
                args.debug
            )
            if combined_contents:
                print("Files copied to clipboard successfully!")
                if args.verbose:
                    print("Copied contents:\n" + combined_contents)

# Add back the encoding variable
encoding = "cl100k_base"

if __name__ == '__main__':
    main()  # Use main() instead of copy_to_clipboard()

