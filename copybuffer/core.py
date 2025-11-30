import importlib.util
import io
import mimetypes
import os
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image
import pyperclip

__VERSION__ = "1.9.0"


def is_wayland() -> bool:
    """Return True if running in a Wayland session."""
    return bool(
        os.environ.get("WAYLAND_DISPLAY")
        or os.environ.get("XDG_SESSION_TYPE") == "wayland"
        or os.environ.get("HYPRLAND_INSTANCE_SIGNATURE")
        or os.environ.get("SWAYSOCK")
    )


def is_wlclipboard_installed() -> bool:
    """Check if wl-clipboard (wl-copy and wl-paste) is available."""
    return shutil.which("wl-copy") is not None and shutil.which("wl-paste") is not None

def is_xclip_installed():
    return shutil.which("xclip") is not None

def is_xsel_installed():
    return shutil.which("xsel") is not None

def has_display() -> bool:
    """Return True if an X11 display is available."""
    return bool(os.environ.get("DISPLAY"))

def is_pyperclip_installed():  # pragma: no cover
    return importlib.util.find_spec("pyperclip") is not None

def check_dependencies():
    missing_dependencies = []

    if is_wayland():
        if not is_wlclipboard_installed():
            missing_dependencies.append("wl-clipboard (wl-copy and wl-paste)")
    elif not has_display():
        missing_dependencies.append("DISPLAY environment variable")
    elif not is_xclip_installed() and not is_xsel_installed():
        missing_dependencies.append("xclip or xsel")

    if not is_pyperclip_installed():
        missing_dependencies.append("pyperclip")

    return missing_dependencies

def install_dependencies():  # pragma: no cover
    print("Please install the following dependencies:")
    dependencies = check_dependencies()
    for dep in dependencies:
        print(f"- {dep}")

def copy_file_contents_to_clipboard(
    file_contents_list,
    include_header=False,
    discord_attachment=False,
    file_paths=None,
    debug=False,
):
    try:
        combined_contents = ""
        for i, file_contents in enumerate(file_contents_list):
            if include_header and file_paths:
                header = f"=== File: {file_paths[i]} ===\n"
                file_contents = header + file_contents

            if discord_attachment and file_paths:
                file_contents = (
                    f"[Attached file: {file_paths[i]}\nContent:\n```\n{file_contents}\n```\n]"
                )

            combined_contents += file_contents + "\n"
            if debug:
                print(f"Debug: Combined contents so far:\n{combined_contents}")

        pyperclip.copy(combined_contents)
        if debug:
            print(f"Debug: Final combined contents copied to clipboard:\n{combined_contents}")
        return combined_contents
    except pyperclip.PyperclipException:
        if is_wayland():
            print("Error: Install 'wl-clipboard' for Wayland clipboard support.")
        elif not has_display():
            print(
                "Error: No DISPLAY environment variable. Ensure an X server is running or install wl-clipboard for Wayland."
            )
        else:
            print("Error: No clipboard mechanism found. Install xclip or xsel.")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred. {str(e)}")
        return None


def copy_image_to_clipboard(image_path):
    """Copy an image file to the system clipboard.
    
    For GIF files (animated or static), preserves the original GIF format.
    For other image formats, converts to PNG.
    """
    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: File '{image_path}' not found")
        return False
    except Exception as e:
        print(f"Error: Unable to open image '{image_path}': {e}")
        return False

    # Convert all images to PNG for clipboard compatibility
    # Note: GIFs (both animated and static) are converted to PNG for clipboard.
    # This ensures compatibility with applications like Discord that don't
    # support image/gif clipboard format on Linux. Animated GIFs will show
    # only the first frame when pasted. To share animated GIFs, upload the
    # file directly rather than using clipboard.
    with io.BytesIO() as output:
        img.save(output, format="PNG")
        image_data = output.getvalue()
    mime_type = "image/png"

    try:
        if sys.platform.startswith("linux"):
            if is_wayland() and shutil.which("wl-copy"):
                subprocess.run(["wl-copy", "--type", mime_type], input=image_data, check=True)
            elif shutil.which("xclip"):
                subprocess.run([
                    "xclip",
                    "-selection",
                    "clipboard",
                    "-t",
                    mime_type,
                ], input=image_data, check=True)
            elif shutil.which("xsel"):
                subprocess.run(
                    ["xsel", "--clipboard", "--input", "--mime-type", mime_type],
                    input=image_data,
                    check=True,
                )
            else:
                print(
                    "Error: No clipboard mechanism found. Install wl-clipboard, xclip, or xsel."
                )
                return False
        elif sys.platform == "darwin":
            # macOS pbcopy should handle both PNG and GIF
            subprocess.run(["pbcopy"], input=image_data, check=True)
        elif sys.platform.startswith("win"):
            try:
                import win32clipboard
                import win32con
            except ImportError:
                print("Error: win32clipboard module is required on Windows.")
                return False

            if is_gif:
                # For GIF on Windows, convert to BMP since win32clipboard doesn't
                # natively support animated GIFs in clipboard
                # Note: This will convert animated GIFs to static BMP (first frame)
                bmp = img.convert("RGB")
                with io.BytesIO() as bmp_buffer:
                    bmp.save(bmp_buffer, "BMP")
                    dib_data = bmp_buffer.getvalue()[14:]
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32con.CF_DIB, dib_data)
                win32clipboard.CloseClipboard()
            else:
                # For non-GIF images, use existing BMP conversion
                bmp = img.convert("RGB")
                with io.BytesIO() as bmp_buffer:
                    bmp.save(bmp_buffer, "BMP")
                    dib_data = bmp_buffer.getvalue()[14:]
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardData(win32con.CF_DIB, dib_data)
                win32clipboard.CloseClipboard()
        else:
            print("Error: Unsupported platform for image clipboard operations.")
            return False
    except Exception as e:
        print(f"Error copying image to clipboard: {e}")
        return False
    return True

def _choose_unique_heredoc_delimiter(contents: str) -> str:  # pragma: no cover
    """Choose a heredoc delimiter that does not appear in contents.

    Args:
        contents: The string content that will be placed inside the heredoc.

    Returns:
        A delimiter string safe to use as a heredoc terminator.
    """
    import secrets

    base = "EOF_CB_"
    for _ in range(10):
        candidate = base + secrets.token_hex(4).upper()
        if candidate not in contents:
            return candidate
    return base + secrets.token_hex(16).upper()

def _shell_single_quote(value: str) -> str:  # pragma: no cover
    """Safely single-quote a string for POSIX shell.

    Replaces single quotes using the standard pattern: ' -> '\''
    """
    return "'" + value.replace("'", "'\\''") + "'"

def generate_heredoc_script(
    file_paths, file_contents_list, append: bool = False
) -> str:  # pragma: no cover
    """Generate a shell script using heredoc to create or append files with their contents.

    Args:
        file_paths: List of file paths corresponding to the contents provided.
        file_contents_list: List of file contents as strings.
        append: If True, appends to files (>>); otherwise overwrites (>)

    Returns:
        Combined shell script text for recreating the files on a target system.
    """
    lines = ["#!/usr/bin/env bash"]
    redir = ">>" if append else ">"
    for path, contents in zip(file_paths, file_contents_list):
        delimiter = _choose_unique_heredoc_delimiter(contents)
        quoted_path = _shell_single_quote(path)
        lines.append(f"mkdir -p \"$(dirname -- {quoted_path})\"")
        lines.append(f"cat {redir} {quoted_path} << '{delimiter}'")
        lines.append(contents)
        lines.append(delimiter)
        lines.append("")
    return "\n".join(lines)

def copy_to_clipboard():  # pragma: no cover
    # Check if input is from STDIN or file
    if len(sys.argv) == 1:
        # Read from STDIN
        try:
            content = sys.stdin.read()
            pyperclip.copy(content)
        except Exception as e:
            print(f"Error copying from STDIN: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Existing file reading logic
        try:
            with open(sys.argv[1], 'r') as file:
                content = file.read()
                pyperclip.copy(content)
        except FileNotFoundError:
            print(f"Error: File '{sys.argv[1]}' not found", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

def get_file_stats(file_path):  # pragma: no cover
    """Get detailed statistics about a file.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        dict: Dictionary containing file statistics
    """
    path = Path(file_path)
    stats = path.stat()
    mime_type, encoding = mimetypes.guess_type(file_path)
    
    # Initialize mimetypes if needed
    if not mimetypes.inited:
        mimetypes.init()
    
    file_stats = {
        'size': stats.st_size,
        'size_human': f"{stats.st_size / 1024:.2f} KB" if stats.st_size >= 1024 else f"{stats.st_size} bytes",
        'mime_type': mime_type or 'application/octet-stream',
        'is_binary': mime_type and not mime_type.startswith('text/'),
        'extension': path.suffix,
        'last_modified': stats.st_mtime,
        'created': stats.st_ctime,
    }
    
    # Add text statistics if it's a text file
    if not file_stats['is_binary']:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                words = content.split()
                
                file_stats.update({
                    'line_count': len(lines),
                    'word_count': len(words),
                    'char_count': len(content),
                    'char_no_spaces': len(content.replace(' ', '').replace('\n', '').replace('\r', '')),
                    'avg_line_length': len(content) / len(lines) if lines else 0,
                    'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
                })
        except Exception as e:
            file_stats['text_stats_error'] = str(e)
    
    return file_stats

def format_file_stats(file_path, stats, token_count=None):  # pragma: no cover
    """Format file statistics for display.
    
    Args:
        file_path (str): Path to the file
        stats (dict): File statistics dictionary
        token_count (int, optional): Number of tokens if text file
        
    Returns:
        str: Formatted statistics string
    """
    from datetime import datetime
    
    output = [
        f"\nFile Statistics for: {file_path}",
        f"{'=' * (18 + len(file_path))}",
        f"Type: {stats['mime_type']}",
        f"Size: {stats['size_human']} ({stats['size']} bytes)",
        f"Extension: {stats['extension'] or 'No extension'}",
        f"Last Modified: {datetime.fromtimestamp(stats['last_modified']).strftime('%Y-%m-%d %H:%M:%S')}",
    ]
    
    if not stats['is_binary']:
        if 'text_stats_error' not in stats:
            output.extend([
                "\nText Statistics:",
                f"Lines: {stats['line_count']:,}",
                f"Words: {stats['word_count']:,}",
                f"Characters (with spaces): {stats['char_count']:,}",
                f"Characters (no spaces): {stats['char_no_spaces']:,}",
                f"Average Line Length: {stats['avg_line_length']:.2f} characters",
                f"Average Word Length: {stats['avg_word_length']:.2f} characters",
            ])
            
            if token_count is not None:
                output.extend([
                    "\nToken Statistics:",
                    f"Token Count: {token_count:,}",
                    f"Avg Bytes per Token: {stats['size'] / token_count:.2f}",
                    (
                        f"Tokens per Word: {token_count / stats['word_count']:.2f}"
                        if stats['word_count'] > 0
                        else "Tokens per Word: N/A"
                    )
                ])
        else:
            output.append(f"\nError reading text statistics: {stats['text_stats_error']}")
    else:
        output.append("\nNote: Binary file - text statistics not applicable")
    
    return '\n'.join(output)


encoding = "cl100k_base"

__all__ = [
    "__VERSION__",
    "is_wayland",
    "is_wlclipboard_installed",
    "is_xclip_installed",
    "is_xsel_installed",
    "has_display",
    "is_pyperclip_installed",
    "check_dependencies",
    "install_dependencies",
    "copy_file_contents_to_clipboard",
    "copy_image_to_clipboard",
    "generate_heredoc_script",
    "copy_to_clipboard",
    "get_file_stats",
    "format_file_stats",
    "encoding",
]

