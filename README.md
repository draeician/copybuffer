# Clipboard Manager (cb)

## Description
A versatile command-line utility for copying file contents, directory contents, or STDIN input to the system clipboard. Supports both text and image files, with special features for Discord formatting and debug output. The command is installed as `cb` and maps to `copybuffer.main:main`, so it can also be invoked with `python -m copybuffer`.

## Features
- Copy text from files to clipboard
- Copy text from STDIN to clipboard
- Copy contents of all files in a directory (non-recursive by default)
- Recursively expand directories when needed
- Honor `.gitignore` patterns while scanning directories
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
- xclip or xsel (Linux X11, preferred when `DISPLAY` is set and the tool works)
- wl-clipboard (Wayland only)
- A terminal that supports OSC 52, for SSH/remote sessions without a working graphical clipboard

  On CachyOS/Hyprland systems, `wl-clipboard` is preferred for native
  clipboard access. Wayland detection checks for `WAYLAND_DISPLAY`,
  `XDG_SESSION_TYPE=wayland`, `HYPRLAND_INSTANCE_SIGNATURE`, or `SWAYSOCK`.
  If `wl-copy` is missing or fails, `auto` may fall back to OSC 52.

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

# Copy directory contents (non-recursive)
cb -d directory/

# Copy directory contents recursively
cb -r directory/

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
- `-d, --directory`: Copy contents of all files in directory (non-recursive)
- `-r, --recursive`: Recursively copy contents of provided directories
- `-v, --verbose`: Display the copied contents
- `-a, --attachment`: Format output as Discord attachment
- `-p, --paste`: Copy a heredoc shell script that recreates the given files when pasted
- `--append`: Use with `--paste` behavior to append to files instead of overwriting
- `--image`: Include image files discovered when expanding directories
- `--debug`: Enable debug mode
- `--backend {auto,osc52,wayland,xclip,xsel}`: Select the text clipboard backend. Overrides `COPYBUFFER_BACKEND`. Default: `auto`
- `--version`: Display application version

### Clipboard backends (Linux text)

`cb` copies text with an explicit backend. Images never use OSC 52.

| Selection | How |
|-----------|-----|
| `--backend auto\|osc52\|wayland\|xclip\|xsel` | Command-line flag |
| `COPYBUFFER_BACKEND=osc52` | Environment variable |

The flag overrides the environment variable. `auto` is the default.

**Automatic selection** prefers a native graphical backend when its environment and executable are present: Wayland (`wl-copy`) when a Wayland session is detected, otherwise `xclip` or `xsel` when `DISPLAY` is set *and the display looks reachable*. `DISPLAY` is only a hint — a value such as `localhost:12.0` does not prove X11 works. Copybuffer probes the X11 socket or TCP port (250ms) before running `xclip`, and caps graphical helpers at 2 seconds, so a dead SSH forward does not stall the command. If that graphical backend fails, `auto` falls back to OSC 52 when `/dev/tty` is writable. Explicit `xclip`, `xsel`, or `wayland` do not fall back; they fail with a nonzero exit status. Explicit `osc52` skips X11 and Wayland.

```bash
# Force OSC 52 (useful over SSH)
cb --backend osc52 filename.txt
printf 'test' | COPYBUFFER_BACKEND=osc52 cb
```

**OSC 52 over SSH.** Copybuffer encodes the text as UTF-8, then Base64, and writes this control sequence to `/dev/tty` (not stdout, so it still works at the end of a pipeline):

```text
ESC ] 52 ; c ; BASE64_DATA BEL
```

`SSH_TTY` is not required. The session needs a writable controlling terminal (`/dev/tty`). The local terminal emulator must allow OSC 52 clipboard writes (iTerm2, kitty, Alacritty, Windows Terminal, xterm with `allowWindowOps`, and others). tmux users typically need `set -s set-clipboard on`. Some terminals (notably many VTE-based ones) ignore OSC 52.

**Payload size.** Copybuffer does not chunk OSC 52 payloads. Terminals and multiplexers often cap the sequence (commonly tens to hundreds of kilobytes; tmux, screen, and some emulators truncate or drop larger pastes). If a large copy appears truncated, use a native graphical backend or split the payload.

**Security.** OSC 52 lets the application running in the terminal set the *local* clipboard. Over SSH that means a remote `cb` (or any remote program that emits the sequence) can overwrite clipboard contents on your workstation. Disable or restrict OSC 52 in the terminal if you do not trust the remote session, and avoid `--backend osc52` on untrusted hosts. Copybuffer's OSC 52 path is text-only; it will not place images on the clipboard that way.

macOS and Windows keep the existing pyperclip/`pbcopy` behavior when `--backend auto` is used.

### Image Support
Supports copying image files directly to clipboard. Image files are detected automatically
based on their MIME type, or you can force image handling with the `--image` flag:
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
- Uses `.gitignore` rules from the current working directory
- Optionally includes headers with -i flag
- Can format as Discord attachments with -a flag
- Use `-r` to walk directories recursively and include nested files

### Debug Mode
Enable detailed output for troubleshooting:
```bash
cb --debug filename.txt
```

### Version Information
```bash
# Display version information
cb --version
# Output: copybuffer version 1.11.1
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
2. Verify clipboard system access (on Linux, try `--backend osc52` over SSH)
3. Check file permissions
4. Ensure proper Python version
5. If `cb` prints success but paste is empty, upgrade past 1.10.0: that release could report success when `xclip` failed on a dead `DISPLAY`

## License
This project is open source and available under the MIT License.

## Contact
For issues or suggestions: draeician@gmail.com
