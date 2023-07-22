#!/usr/bin/env python3
# filename: cb.py
# author: draeician (July 22, 2023)
# purpose: allow for a file to be placed in the system clipboard quickly and easily

import sys
import subprocess

def copy_file_contents_to_clipboard(file_path, include_header=False):
    """
    Copies the contents of a file to the clipboard using the xclip command.

    Args:
        file_path (str): The path of the file to copy.
        include_header (bool): Flag to indicate whether to include a header with the filename.

    Returns:
        bool: True if the file exists and its contents are copied successfully, False otherwise.
    """
    try:
        # Verify if the file exists
        with open(file_path, 'r') as file:
            file_contents = file.read().strip()

        # Include header if specified
        if include_header:
            header = f"=== File: {file_path} ===\n"
            file_contents = header + file_contents

        # Use the xclip command to copy the file contents to the clipboard
        subprocess.run(['xclip', '-selection', 'clipboard'], input=file_contents, encoding='utf-8', check=True)

        return True
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Error: Failed to copy file contents to clipboard. Command returned non-zero exit status {e.returncode}.")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Please provide the file path as a command-line argument.")
    else:
        file_path = sys.argv[1]
        include_header = False
        if "--header" in sys.argv:
            include_header = True
        copy_file_contents_to_clipboard(file_path, include_header)

