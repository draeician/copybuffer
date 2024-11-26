#!/usr/bin/env python3

import argparse
from PIL import Image
import pyperclip
import os
import sys
import tempfile
import subprocess
import shutil
import tiktoken

__VERSION__ = "1.6.1"

def is_xclip_installed():
    return shutil.which("xclip") is not None

def is_xsel_installed():
    return shutil.which("xsel") is not None

def is_pyperclip_installed():
    try:
        import pyperclip
        return True
    except ImportError:
        return False

def check_dependencies():
    missing_dependencies = []

    if not is_xclip_installed() and not is_xsel_installed():
        missing_dependencies.append("xclip or xsel")

    if not is_pyperclip_installed():
        missing_dependencies.append("pyperclip")

    return missing_dependencies

def install_dependencies():
    print("Please install the following dependencies:")
    dependencies = check_dependencies()
    for dep in dependencies:
        print(f"- {dep}")

def copy_file_contents_to_clipboard(file_contents_list, include_header=False, discord_attachment=False, file_paths=None, debug=False):
    try:
        combined_contents = ""
        for i, file_contents in enumerate(file_contents_list):
            if include_header and file_paths:
                header = f"=== File: {file_paths[i]} ===\n"
                file_contents = header + file_contents

            if discord_attachment and file_paths:
                file_contents = f"[Attached file: {file_paths[i]}\nContent:\n```\n{file_contents}\n```\n]"

            combined_contents += file_contents + "\n"
            if debug:
                print(f"Debug: Combined contents so far:\n{combined_contents}")  # Debug print

        pyperclip.copy(combined_contents)
        if debug:
            print(f"Debug: Final combined contents copied to clipboard:\n{combined_contents}")  # Debug print
        return combined_contents
    except Exception as e:
        print(f"Error: An unexpected error occurred. {str(e)}")
        return None

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
    main()

