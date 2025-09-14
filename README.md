# Clipboard Manager (cb)

## Description
A versatile command-line utility for copying file contents, directory contents, or STDIN input to the system clipboard. Supports both text and image files, with special features for Discord formatting and debug output.

## Features
- Copy text from files to clipboard
- Copy text from STDIN to clipboard
- Copy contents of all files in a directory
- Copy images to clipboard
- Include headers with filenames
- Format output for Discord
- Generate heredoc shell script to recreate files on paste
- Append mode for heredoc script generation
- Verbose output option
- Debug mode

## Requirements
- Python 3.x
- pyperclip
- PIL (for image support)
- xclip or xsel (Linux only)
- wl-clipboard (Wayland only)

  On CachyOS/Hyprland systems, `wl-clipboard` is required. Wayland detection
  checks for `WAYLAND_DISPLAY`, `XDG_SESSION_TYPE=wayland`,
  `HYPRLAND_INSTANCE_SIGNATURE`, or `SWAYSOCK`.

## Installation
1. Install package with pipx:
```bash
pipx install .
```
## Uninstall
```bash
pipx uninstall copybuffer)
```

2. For Linux systems, install clipboard handlers:
```bash
sudo apt-get install xclip
# or
sudo apt-get install xsel
# For Wayland sessions
sudo apt-get install wl-clipboard
```

## Usage

### Basic Usage
```bash
# Copy file contents
cb filename.txt

# Copy from STDIN
echo "hello" | cb

# Copy directory contents
cb -d directory/

# Copy with Discord formatting
cb -a filename.txt

# Copy with headers
cb -i filename.txt

# Copy as heredoc script for recreating files on paste
cb -p path/to/file1.txt path/to/file2.txt

# Copy as heredoc script that appends to target files
cb --append path/to/file1.txt
```

### Options
- `file`: File to copy (optional - reads from STDIN if not provided)
- `-i, --include-header`: Include filename as header in copied text
- `-d, --directory`: Copy contents of all files in directory
- `-v, --verbose`: Display the copied contents
- `-a, --attachment`: Format output as Discord attachment
- `-p, --paste`: Copy a heredoc shell script that recreates the given files when pasted
- `--append`: Use with `--paste` behavior to append to files instead of overwriting
- `--debug`: Enable debug mode
- `--version`: Display application version

### Image Support
Supports copying image files directly to clipboard:
- PNG
- JPG/JPEG
- BMP
- GIF (first frame)

```bash
cb image.png
```

### Directory Mode
Copy contents of all text files in a directory:
```bash
cb -d /path/to/directory
```
- Automatically skips image files
- Optionally includes headers with -i flag
- Can format as Discord attachments with -a flag

### Debug Mode
Enable detailed output for troubleshooting:
```bash
cb --debug filename.txt
```

### Version Information
```bash
# Display version information
cb --version
# Output: copybuffer version 1.8.0
```

## Error Handling
The script provides clear error messages for common issues:
- Missing dependencies
- File not found
- Permission errors
- Invalid file types
- Directory access errors

## Examples

### Copy with Headers
```bash
cb -i document.txt
# Output includes: === document.txt ===
```

### Discord Formatting
```bash
cb -a code.py
# Output format: [Attached file: code.py\nContent:\n```\n...\n```\n]
```

### Heredoc Script Generation
```bash
# Overwrite or create files on the target system
cb -p path/to/file1 path/to/nested/dir/file2

# Append to files on the target system
cb --append path/to/file1

# Notes:
# - A random, content-safe delimiter is used to avoid collisions
# - Single-quoted heredocs prevent shell interpolation
```

### Verbose Directory Copy
```bash
cb -d -v -i /path/to/docs
# Shows all processed files and copied content
```

## Troubleshooting
If you encounter issues:
1. Check dependencies with --debug flag
2. Verify clipboard system access
3. Check file permissions
4. Ensure proper Python version

## License
This project is open source and available under the MIT License.

## Contact
For issues or suggestions: draeician@gmail.com
