# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip`, providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` (for handling images on Linux)

## Usage

### Copying Text Files
1. Clone this repository or download the `cb.py` script to your local machine.
2. Open a terminal or command prompt in the directory containing `cb.py`.
3. To copy the contents of one or more files to the clipboard, use the following command:

    ```bash
    python cb.py [--header] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.
