# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a simple Python script that allows you to quickly and easily copy the contents of one or more files to the system clipboard. This script makes use of the `pyperclip` library, which provides cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library

## Usage
1. Clone this repository or download the `cb.py` script to your local machine.

2. Open a terminal or command prompt in the directory containing `cb.py`.

3. To copy the contents of one or more files to the clipboard, use the following command:

    ```bash
    python cb.py [--header] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

5. After running the command, you can paste the clipboard contents into any application that supports pasting.

## Example
To copy the contents of two files, `file1.txt` and `file2.txt`, to the clipboard and include headers for each file, use the following command:

```bash

python cb.py --header file1.txt file2.txt


This will copy the contents of file1.txt and file2.txt to the clipboard, including headers if the --header flag is used.

Additional Notes
The cb.py script has been updated to support multiple file paths as arguments, allowing you to copy the contents of several files to the clipboard at once.

The script now includes an option to include a header with the filename before each file's contents when copying to the clipboard.

The requirements.txt file has been added to specify the required pyperclip library for the script. Install it using pip before running the script.

Feel free to modify the script according to your needs or contribute to its development by submitting pull requests.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Author
draeician
Acknowledgments
Special thanks to the developers of the pyperclip library for providing a simple cross-platform clipboard access solution.
