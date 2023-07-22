#!/usr/bin/env python3

#!/usr/bin/env python3

import sys
import subprocess

def copy_file_contents_to_clipboard(file_path):
    """
    Copies the contents of a file to the clipboard using the xclip command.

    Args:
        file_path (str): The path of the file to copy.

    Returns:
        bool: True if the file exists and its contents are copied successfully, False otherwise.
    """
    try:
        # Verify if the file exists
        with open(file_path, 'r') as file:
            file_contents = file.read().strip()

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
        copy_file_contents_to_clipboard(file_path)

