#!/usr/bin/env python3

import argparse
from PIL import Image
import pyperclip
import os
import sys
import tempfile
import subprocess
import shutil

__VERSION__ = "v1.0-2-g3cbb90b"

def is_xclip_installed():
    return shutil.which("xclip") is not None

def copy_image_to_clipboard(image_path):
    if not is_xclip_installed():
        print("Error: xclip is not installed. Please install it using 'sudo apt-get install xclip'.")
        return False

    try:
        # Open the image
        image = Image.open(image_path)

        # If it's a GIF, take the first frame and convert to RGB
        if image_path.lower().endswith('.gif'):
            image = image.convert('RGB')

        # Create a temporary file to hold the image
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_path = temp_file.name

        # Save the image to the temporary file
        image.save(temp_path)

        # Use xclip to copy the image to the clipboard
        command = f"xclip -selection clipboard -t image/png -i {temp_path}"
        subprocess.run(command, shell=True)

        return True
    except Exception as e:
        print(f"Error: An unexpected error occurred while copying the image. {str(e)}")
        return False


def copy_file_contents_to_clipboard(file_paths, include_header=False):
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
                file_path = os.path.abspath(file_path)
                try:
                    with open(file_path, 'r') as file:
                        file_contents = file.read().strip()
                except FileNotFoundError:
                    print(f"Error: File '{file_path}' not found.")
                    copied_all_files = False

            if include_header:
                header = f"=== File: {file_path} ===\\n"
                file_contents = header + file_contents

            all_file_contents += file_contents + "\\n\\n"

        pyperclip.copy(all_file_contents)
        return copied_all_files
    except Exception as e:
        print(f"Error: An unexpected error occurred. {str(e)}")
        return False

def main():
    debug = False
    parser = argparse.ArgumentParser(description="Copy file contents or images to clipboard.")
    parser.add_argument("--version", action="store_true", help="Display the application version.")
    parser.add_argument("--header", action="store_true", help="Include header for text files.")
    parser.add_argument("file_paths", metavar='N', nargs='*', help="Paths of the files or images to copy.")  # Changed nargs='*'
    args = parser.parse_args()

    if args.version:
        print(f"This is the CopyBuffer application, version {__VERSION__}")
        return

    if debug:
        print(args.file_paths)

    for file_path in args.file_paths:
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            copy_successful = copy_image_to_clipboard(file_path)
        else:
            copy_successful = copy_file_contents_to_clipboard(args.file_paths, args.header)

        if copy_successful:
            print(f"{file_path} copied to the clipboard successfully!")

if __name__ == '__main__':
    main()

