# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
# Clipboard Manager (cb.py)

## Description
Clipboard Manager is a versatile Python script that allows you to quickly and easily copy the contents of one or more files or images to the system clipboard. In addition to text files, it now supports various image formats, including PNG, JPEG, BMP, and GIF. For animated GIFs, only the first frame is copied to the clipboard. This script makes use of the `pyperclip` library and `xclip` (or `xsel`), providing cross-platform clipboard access.

## Requirements
- Python 3.x
- `pyperclip` library
- `xclip` or `xsel` (for handling images on Linux)

## Installation
1. Ensure you have Python 3 installed. You can download it from the [official Python website](https://www.python.org/).
2. Install the required Python libraries. You can do this using `pip`:

    ```bash
    pip install pyperclip Pillow
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
    python cb.py [--header] [-a|--attachment] <file_path(s)>
    ```

    - `<file_path(s)>`: Provide one or more file paths separated by spaces.
    - `--header`: (Optional) Include a header with the filename before each file's contents.
    - `-a` or `--attachment`: (Optional) Format the output as a Discord attachment.

4. The contents of the specified file(s) will be copied to the system clipboard. If multiple file paths are provided, the script will copy the contents of each file in sequence.

#### Example
```bash
python cb.py --header -a file1.txt file2.txt
```

### Copying Images
1. To copy an image to the clipboard, use the same command as for text files, providing the image path:

    ```bash
    python cb.py <image_path>
    ```

    - Supported image formats: PNG, JPEG, BMP, GIF (first frame only for animated GIFs)

2. The image will be copied to the system clipboard, ready to be pasted into other applications.

#### Example
```bash
python cb.py image.png
```

### Copying from Standard Input
1. You can also copy data from standard input by using `-` as the file path:

    ```bash
    echo "Some text" | python cb.py -
    ```

2. This can be useful for piping output from other commands into the clipboard.

#### Example
```bash
cat somefile.txt | python cb.py -
```

### Checking the Version
You can check the version of the script by using the `--version` flag:

```bash
python cb.py --version
```

## Error Handling
The script will print meaningful error messages if something goes wrong, such as if a file is not found or a dependency is missing. Make sure all dependencies are installed properly before running the script.

## Development and Contributions
Feel free to fork this repository and submit pull requests for any features or bug fixes you would like to see included.

## License
This project is licensed under the MIT License.
