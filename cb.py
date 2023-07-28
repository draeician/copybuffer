#!/usr/bin/env python3
# filename: cb.py
# author: draeician (July 27, 2023)
# purpose: allow for files to be placed in the system clipboard quickly and easily

import argparse
import subprocess
import os
import sys
import pyperclip

def copy_file_contents_to_clipboard(file_paths, include_header=False):
    """
    Copies the contents of files to the clipboard using the pyperclip library.

    Args:
        file_paths (list): List of file paths to copy.
        include_header (bool): Flag to indicate whether to include a header with the filename.

    Returns:
        bool: True if all files exist and their contents are copied successfully, False otherwise.
    """
    try:
        copied_all_files = True
        all_file_contents = ""

        for file_path in file_paths:
            file_contents = ""
            if file_path == '-':
                for line in sys.stdin:
                    file_contents += line
                file_path = "STDIN"
            else:
                # Get the absolute path of the file
                file_path = os.path.abspath(file_path)

                # Verify if the file exists
                try:
                    with open(file_path, 'r') as file:
                        file_contents = file.read().strip()
                except FileNotFoundError:
                    print(f"Error: File '{file_path}' not found.")
                    copied_all_files = False

            # Include header if specified
            if include_header:
                header = f"=== File: {file_path} ===\n"
                file_contents = header + file_contents

            # Add the file contents to the combined string
            all_file_contents += file_contents + "\n\n"

        # Use pyperclip to copy the combined file contents
        pyperclip.copy(all_file_contents)

        return copied_all_files
    except Exception as e:
        print(f"Error: An unexpected error occurred. {str(e)}")
        return False

def main():
    # define debug mode
    debug = False

    parser = argparse.ArgumentParser(description="Copy file contents to clipboard.")
    parser.add_argument("file_paths", metavar='N', nargs="+", help="Paths of the files to copy.")
    parser.add_argument("--header", action="store_true", help="Include header.")
    args = parser.parse_args()

    if debug:
        print(args.file_paths)

    copy_successful = copy_file_contents_to_clipboard(args.file_paths, args.header)
    if copy_successful:
        print("File contents copied to the clipboard successfully!")

if __name__ == '__main__':
    main()

