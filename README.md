
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Features

- **Copy Text File Contents**: Copy the contents of one or multiple text files to the clipboard.
- **Copy Image Files**: Copy image files (PNG, JPG, JPEG, BMP, GIF) to the clipboard.
- **Include Headers**: Add headers to the copied text indicating the file path.
- **Discord Attachment Formatting**: Format the copied text as a Discord attachment for easy sharing.
- **Token Count Display**: Display the token count of the text using Tiktoken.
- **Export Clipboard Contents**: Export the final clipboard contents to the screen.

## Requirements

- Python 3.x
- [Pillow](https://python-pillow.org/)
- [pyperclip](https://github.com/asweigart/pyperclip)
- [tiktoken](https://github.com/openai/tiktoken)
- [xclip](https://github.com/astrand/xclip) or [xsel](https://github.com/kfish/xsel) for Linux (optional for image copy)

## Installation

1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).

2. Install the required Python libraries using `pip`:

    ```bash
    pip install pillow pyperclip tiktoken
    ```

3. Install `xclip` (or `xsel`) for clipboard handling on Linux:

    ```bash
    sudo apt-get install xclip
    ```

    Or, if you prefer `xsel`:

    ```bash
    sudo apt-get install xsel
    ```

## Usage

### Copying Text Files
1. Clone this repository or download the `cb.py` script to your local machine.
2. Open a terminal or command prompt in the directory containing `cb.py`.
3. To copy the contents of one or more files to the clipboard, use the following command:

    ```bash
    python cb.py [--header] [-a|--attachment] [-e|--export] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.
    - `-e` or `--export`: (Optional) Export the final clipboard contents to the screen.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will concatenate and copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a -e file1.txt file2.txt
```

### Copying Images
To copy an image to the clipboard, use the same command as for text files, providing the image path:

```bash
python cb.py <image_path>
```

Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
You can also copy data from standard input by using `-` as the file path:

```bash
echo "Some text" | python cb.py -
```

This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Exporting Clipboard Contents
To export the current contents of the clipboard to the screen without copying new content:

```bash
python cb.py -e
```

This will print the contents currently in the clipboard.

#### Example
```bash
python cb.py -e
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Debugging Steps
If the script is not working as expected, follow these steps to troubleshoot the issue:

1. **Verify Clipboard Access**:
   Ensure `xclip` or `xsel` is working correctly by manually testing clipboard access:
   ```sh
   echo "test" | xclip -selection clipboard
   xclip -selection clipboard -o
   ```

2. **Check Python Environment**:
   Ensure the required Python packages are installed and versions match:
   ```sh
   pip freeze | egrep -i 'pyperclip|pillow|tiktoken'
   ```

3. **Verify X Server/Display Access**:
   Ensure the X server is running and accessible:
   ```sh
   echo $DISPLAY
   ```

4. **Check System Logs**:
   Look for any relevant errors or warnings in the system logs:
   ```sh
   tail -f /var/log/syslog
   ```

5. **Ensure Script Permissions**:
   Verify the script has execution permissions:
   ```sh
   chmod +x cb.py
   ./cb.py cb.py
   ```

6. **Reinstall Dependencies**:
   Reinstall the required packages to ensure there are no issues:
   ```sh
   sudo apt-get install --reinstall xclip xsel
   pip install --force-reinstall pyperclip Pillow tiktoken
   ```

## Example Use Cases

### Copying Text Files for Documentation
Quickly copy the contents of multiple documentation files with headers for easy pasting into reports or wikis.

```bash
python cb.py --header docs/intro.txt docs/setup.txt docs/usage.txt
```

### Preparing Code Snippets for Discord
Format code snippets as Discord attachments for sharing in developer channels.

```bash
python cb.py --attachment code/example.py
```

### Counting Tokens in a File
Use the token count feature to analyze the length of text in a file.

```bash
python cb.py --token path/to/longtextfile.txt
```

### Copying Images for Quick Sharing
Copy images to the clipboard for quick pasting into documents or image editors.

```bash
python cb.py images/logo.png
```

### Using Standard Input
Copy text piped from another command.

```bash
cat notes.txt | python cb.py -
```

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
