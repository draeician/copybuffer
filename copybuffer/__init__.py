#!/usr/bin/env python3

import argparse
from PIL import Image
import pyperclip
import os
import sys
import tempfile
import subprocess
import shutil
import tiktoken
import mimetypes
from pathlib import Path

__VERSION__ = "1.6.1"

def is_xclip_installed():
    return shutil.which("xclip") is not None

def is_xsel_installed():
    return shutil.which("xsel") is not None

def is_pyperclip_installed():
    try:
        import pyperclip
        return True
    except ImportError:
        return False

def check_dependencies():
    missing_dependencies = []

    if not is_xclip_installed() and not is_xsel_installed():
        missing_dependencies.append("xclip or xsel")

    if not is_pyperclip_installed():
        missing_dependencies.append("pyperclip")

    return missing_dependencies

def install_dependencies():
    print("Please install the following dependencies:")
    dependencies = check_dependencies()
    for dep in dependencies:
        print(f"- {dep}")

def copy_file_contents_to_clipboard(file_contents_list, include_header=False, discord_attachment=False, file_paths=None, debug=False):
    try:
        combined_contents = ""
        for i, file_contents in enumerate(file_contents_list):
            if include_header and file_paths:
                header = f"=== File: {file_paths[i]} ===\n"
                file_contents = header + file_contents

            if discord_attachment and file_paths:
                file_contents = f"[Attached file: {file_paths[i]}\nContent:\n```\n{file_contents}\n```\n]"

            combined_contents += file_contents + "\n"
            if debug:
                print(f"Debug: Combined contents so far:\n{combined_contents}")  # Debug print

        pyperclip.copy(combined_contents)
        if debug:
            print(f"Debug: Final combined contents copied to clipboard:\n{combined_contents}")  # Debug print
        return combined_contents
    except Exception as e:
        print(f"Error: An unexpected error occurred. {str(e)}")
        return None

def copy_to_clipboard():
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

def get_file_stats(file_path):
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

def format_file_stats(file_path, stats, token_count=None):
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
                    f"\nToken Statistics:",
                    f"Token Count: {token_count:,}",
                    f"Avg Bytes per Token: {stats['size'] / token_count:.2f}",
                    f"Tokens per Word: {token_count / stats['word_count']:.2f}" if stats['word_count'] > 0 else "Tokens per Word: N/A"
                ])
        else:
            output.append(f"\nError reading text statistics: {stats['text_stats_error']}")
    else:
        output.append("\nNote: Binary file - text statistics not applicable")
    
    return '\n'.join(output)

def main():
    parser = argparse.ArgumentParser(description="Copy file contents, images, or STDIN input to clipboard.")
    parser.add_argument("--version", action="store_true", help="Display the application version.")
    parser.add_argument("files", nargs="*", help="Files to copy (reads from STDIN if not provided)")
    parser.add_argument("-i", "--include-header", action="store_true", help="Include the filename as a header in copied text")
    parser.add_argument("-d", "--directory", action="store_true", help="Copy contents of all files in directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Display the copied contents")
    parser.add_argument("-a", "--attachment", action="store_true", help="Format output as Discord attachment")
    parser.add_argument("-t", "--tokens", action="store_true", help="Display token statistics for the file")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    # Check dependencies before proceeding
    missing_dependencies = check_dependencies()
    if missing_dependencies:
        print("Missing dependencies:")
        for dep in missing_dependencies:
            print(f"- {dep}")
        install_dependencies()
        return

    if args.version:
        print(f"copybuffer version {__VERSION__}")
        return

    # If no files provided, check STDIN
    if not args.files:
        content = sys.stdin.read().strip()
        if args.debug:
            print(f"Debug: Read from STDIN: {content}")
        combined_contents = copy_file_contents_to_clipboard([content], args.include_header, args.attachment, debug=args.debug)
        if combined_contents:
            print("STDIN copied to the clipboard successfully!")
            if args.verbose:
                print("Copied contents:\n" + combined_contents)
        return

    # Process files
    file_contents_list = []
    valid_file_paths = []
    for file_path in args.files:
        try:
            with open(file_path, 'r') as file:
                file_content = file.read().strip()
                file_contents_list.append(file_content)
                valid_file_paths.append(file_path)
                if args.debug:
                    print(f"Debug: Read file {file_path}")
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found")
            continue
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue

    if file_contents_list:
        combined_contents = copy_file_contents_to_clipboard(
            file_contents_list, 
            args.include_header, 
            args.attachment, 
            valid_file_paths,
            args.debug
        )
        if combined_contents:
            print("Files copied to clipboard successfully!")
            if args.verbose:
                print("Copied contents:\n" + combined_contents)

    if args.tokens:
        enc = tiktoken.get_encoding(encoding)
        for file_path in args.files:
            try:
                stats = get_file_stats(file_path)
                token_count = None
                
                if not stats['is_binary']:
                    with open(file_path, 'r') as file:
                        content = file.read()
                        tokens = enc.encode(content)
                        token_count = len(tokens)
                
                print(format_file_stats(file_path, stats, token_count))
                
            except FileNotFoundError:
                print(f"Error: File '{file_path}' not found")
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
        return

# Add back the encoding variable
encoding = "cl100k_base"

if __name__ == '__main__':
    main()

