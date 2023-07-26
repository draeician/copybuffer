#!/usr/bin/env python3
# filename: cb.py
# author: draeician (July 22, 2023)
# purpose: allow for a file to be placed in the system clipboard quickly and easily

import argparse
import subprocess
import os
import pyperclip

def copy_file_contents_to_clipboard(file_path, include_header=False):
    """
    Copies the contents of a file to the clipboard using the pyperclip library.

    Args:
        file_path (str): The path of the file to copy.
        include_header (bool): Flag to indicate whether to include a header with the filename.

    Returns:
        bool: True if the file exists and its contents are copied successfully, False otherwise.
    """
    try:
        # Get the absolute path of the file
        file_path = os.path.abspath(file_path)

        # Verify if the file exists
        with open(file_path, 'r') as file:
            file_contents = file.read().strip()

        # Include header if specified
        if include_header:
            header = f"=== File: {file_path} ===\n"
            file_contents = header + file_contents

        # Use pyperclip to copy the file contents
        pyperclip.copy(file_contents)

        return True
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return False
    except Exception as e:
        print(f"Error: An unexpected error occurred. {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Copy file contents to clipboard.")
    parser.add_argument("file_path", help="Path of the file to copy.")
    parser.add_argument("--header", action="store_true", help="Include a header with the filename.")
    args = parser.parse_args()

    copy_successful = copy_file_contents_to_clipboard(args.file_path, args.header)
    if copy_successful:
        print("File contents copied to the clipboard successfully!")

if __name__ == '__main__':
    main()

