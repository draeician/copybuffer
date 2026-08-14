import base64
import importlib.util
import io
import mimetypes
import os
import shutil
import socket
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional, Sequence, Tuple, Union

from PIL import Image
import pyperclip

__VERSION__ = "1.11.0"


def detect_encoding(data: bytes) -> Tuple[Union[str, None], bool]:
    """Detect the encoding of byte data.
    
    Checks for BOMs first, then tries chardet if available, then falls back to common encodings.
    
    Args:
        data: Byte data to detect encoding for
        
    Returns:
        Tuple of (encoding_name, has_bom) where has_bom indicates if a BOM was found
    """
    # Check for BOMs first (most reliable indicator)
    if len(data) >= 2:
        # UTF-16-LE BOM: FF FE
        if data[:2] == b'\xff\xfe':
            return 'utf-16-le', True
        # UTF-16-BE BOM: FE FF
        if data[:2] == b'\xfe\xff':
            return 'utf-16-be', True
        # UTF-8 BOM: EF BB BF
        if len(data) >= 3 and data[:3] == b'\xef\xbb\xbf':
            return 'utf-8', True
    
    # Try chardet if available
    try:
        import chardet
        result = chardet.detect(data)
        if result and result.get('encoding') and result.get('confidence', 0) > 0.7:
            encoding = result['encoding']
            # Normalize encoding names
            if encoding.lower() in ('utf-16', 'utf16'):
                # chardet might return 'utf-16' but we need to determine endianness
                # Try both and see which works
                try:
                    data.decode('utf-16-le')
                    return 'utf-16-le', False
                except UnicodeDecodeError:
                    try:
                        data.decode('utf-16-be')
                        return 'utf-16-be', False
                    except UnicodeDecodeError:
                        return 'utf-16', False
            return encoding, False
    except ImportError:
        pass
    
    # Fallback: try common encodings in order
    encodings_to_try = [
        'utf-8',
        'utf-16-le',
        'utf-16-be',
        'utf-16',
        'latin-1',
    ]
    
    for encoding in encodings_to_try:
        try:
            # Try to decode with this encoding
            data.decode(encoding)
            return encoding, False
        except (UnicodeDecodeError, LookupError):
            continue
    
    return None, False


def read_with_encoding(file_path: Union[Path, str]) -> Tuple[str, str]:
    """Read a file and detect its encoding.
    
    Args:
        file_path: Path to the file to read
        
    Returns:
        Tuple of (content, encoding_used)
        
    Raises:
        UnicodeDecodeError: If encoding detection fails and all fallbacks fail
    """
    path = Path(file_path)
    data = path.read_bytes()
    
    detected_encoding, has_bom = detect_encoding(data)
    if detected_encoding is None:
        # Last resort: try utf-8 with errors='replace'
        return data.decode('utf-8', errors='replace'), 'utf-8'
    
    # Strip BOM bytes if present (before decoding)
    if has_bom:
        if detected_encoding == 'utf-16-le' and data[:2] == b'\xff\xfe':
            data = data[2:]
        elif detected_encoding == 'utf-16-be' and data[:2] == b'\xfe\xff':
            data = data[2:]
        elif detected_encoding == 'utf-8' and data[:3] == b'\xef\xbb\xbf':
            data = data[3:]
    
    # Handle truncated UTF-16 data (must be even number of bytes)
    if detected_encoding in ('utf-16-le', 'utf-16-be', 'utf-16'):
        if len(data) % 2 != 0:
            # Truncated UTF-16 data - strip last byte and decode with error handling
            data = data[:-1]
    
    # Decode with detected encoding
    # Use 'replace' for UTF-16 to handle any remaining truncation issues
    if detected_encoding in ('utf-16-le', 'utf-16-be', 'utf-16'):
        content = data.decode(detected_encoding, errors='replace')
    else:
        content = data.decode(detected_encoding)
    
    return content, detected_encoding


def read_stdin_with_encoding() -> Tuple[str, str]:
    """Read from stdin and detect encoding.
    
    Returns:
        Tuple of (content, encoding_used)
        
    Raises:
        UnicodeDecodeError: If encoding detection fails and all fallbacks fail
    """
    data = sys.stdin.buffer.read()
    
    detected_encoding, has_bom = detect_encoding(data)
    if detected_encoding is None:
        # Last resort: try utf-8 with errors='replace'
        return data.decode('utf-8', errors='replace'), 'utf-8'
    
    # Strip BOM bytes if present (before decoding)
    if has_bom:
        if detected_encoding == 'utf-16-le' and data[:2] == b'\xff\xfe':
            data = data[2:]
        elif detected_encoding == 'utf-16-be' and data[:2] == b'\xfe\xff':
            data = data[2:]
        elif detected_encoding == 'utf-8' and data[:3] == b'\xef\xbb\xbf':
            data = data[3:]
    
    # Handle truncated UTF-16 data (must be even number of bytes)
    if detected_encoding in ('utf-16-le', 'utf-16-be', 'utf-16'):
        if len(data) % 2 != 0:
            # Truncated UTF-16 data - strip last byte and decode with error handling
            data = data[:-1]
    
    # Decode with detected encoding
    # Use 'replace' for UTF-16 to handle any remaining truncation issues
    if detected_encoding in ('utf-16-le', 'utf-16-be', 'utf-16'):
        content = data.decode(detected_encoding, errors='replace')
    else:
        content = data.decode(detected_encoding)
    
    return content, detected_encoding


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
    """Return True if DISPLAY is set to a nonempty value.

    A set DISPLAY is only a hint that X11 *might* work. It does not prove
    that the display is reachable or that an authorization cookie exists.
    """
    return bool(os.environ.get("DISPLAY"))


TEXT_BACKENDS = ("auto", "osc52", "wayland", "xclip", "xsel")
CONTROLLING_TTY = "/dev/tty"
# Dead SSH X11 forwards (DISPLAY=localhost:N.0) can block in XOpenDisplay
# for tens of seconds. Probe first, then cap helper runtime.
X11_PROBE_TIMEOUT = 0.25
GRAPHICAL_BACKEND_TIMEOUT = 2.0


class ClipboardError(Exception):
    """Raised when a clipboard backend fails to copy text."""


def is_pyperclip_installed():  # pragma: no cover
    return importlib.util.find_spec("pyperclip") is not None

def check_dependencies():
    """Return missing *hard* dependencies.

    Linux graphical clipboard tools are preferred at copy time but are not
    required: OSC 52 can still succeed over a writable controlling terminal.
    ``DISPLAY`` is not treated as proof that X11 works, and its absence is
    not a hard failure.
    """
    missing_dependencies = []

    if not is_pyperclip_installed():
        missing_dependencies.append("pyperclip")

    return missing_dependencies

def install_dependencies():  # pragma: no cover
    print("Please install the following dependencies:")
    dependencies = check_dependencies()
    for dep in dependencies:
        print(f"- {dep}")


def resolve_text_backend(
    cli_backend: Optional[str] = None,
    environ: Optional[dict] = None,
) -> str:
    """Resolve the text clipboard backend.

    Command-line ``--backend`` takes precedence over ``COPYBUFFER_BACKEND``.
    Unset or empty values default to ``auto``.

    Args:
        cli_backend: Value from ``--backend``, or None if the flag was omitted.
        environ: Environment mapping; defaults to ``os.environ``.

    Returns:
        One of ``TEXT_BACKENDS``.

    Raises:
        ClipboardError: If the selected name is not a supported backend.
    """
    mapping = os.environ if environ is None else environ
    if cli_backend is not None and str(cli_backend).strip() != "":
        selected = str(cli_backend).strip().lower()
    else:
        selected = str(
            mapping.get("COPYBUFFER_BACKEND", "auto") or "auto"
        ).strip().lower()
        if not selected:
            selected = "auto"
    if selected not in TEXT_BACKENDS:
        raise ClipboardError(
            f"Unknown clipboard backend '{selected}'. "
            f"Choose from: {', '.join(TEXT_BACKENDS)}"
        )
    return selected


def _tcp_port_open(host: str, port: int, timeout: float) -> bool:
    """Return True if a TCP connect to ``host:port`` succeeds within timeout."""
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def x11_display_reachable(timeout: float = X11_PROBE_TIMEOUT) -> bool:
    """Return whether DISPLAY looks like a reachable X11 server.

    A set DISPLAY is not proof of a working server. Unix sockets are checked
    with ``exists()``. TCP displays (typical SSH forwarding,
    ``localhost:12.0``) get a short connect timeout so a dead tunnel cannot
    stall ``cb`` inside ``xclip``.

    Args:
        timeout: Seconds to wait for a TCP connect.

    Returns:
        True if the display socket or TCP port appears reachable.
    """
    display = (os.environ.get("DISPLAY") or "").strip()
    if not display:
        return False
    host, sep, rest = display.rpartition(":")
    if not sep or not rest:
        return False
    display_num = rest.split(".", 1)[0]
    try:
        number = int(display_num)
    except ValueError:
        return False
    if host.startswith("[") and host.endswith("]"):
        host = host[1:-1]
    if not host or host == "unix":
        return os.path.exists(f"/tmp/.X11-unix/X{number}")
    return _tcp_port_open(host, 6000 + number, timeout)


def preferred_linux_graphical_backend() -> Optional[str]:
    """Return the preferred native Linux graphical backend, or None.

    Wayland is preferred when its environment and ``wl-copy`` are present.
    Otherwise ``DISPLAY`` is a hint to try ``xclip``, then ``xsel``, but
    only when the display looks reachable.
    """
    if is_wayland() and shutil.which("wl-copy"):
        return "wayland"
    if has_display() and x11_display_reachable():
        if shutil.which("xclip"):
            return "xclip"
        if shutil.which("xsel"):
            return "xsel"
    return None


def build_osc52_sequence(text: str) -> str:
    """Build an OSC 52 clipboard sequence for ``text``.

    The payload is the original text encoded as UTF-8 bytes, then Base64.
    Framing is ``ESC ] 52 ; c ; BASE64_DATA BEL`` with no extra spaces.

    Args:
        text: Clipboard text to encode.

    Returns:
        The OSC 52 control sequence as a Unicode string (ASCII payload).
    """
    encoded = base64.b64encode(text.encode("utf-8")).decode("ascii")
    return f"\x1b]52;c;{encoded}\x07"


def write_to_controlling_tty(data: str) -> None:
    """Write ``data`` to the controlling terminal, not stdout.

    OSC 52 must go to ``/dev/tty`` so the sequence still reaches the
    terminal when ``cb`` is used at the end of a pipeline. ``SSH_TTY`` is
    not required.

    Args:
        data: Text to write to the controlling terminal.

    Raises:
        ClipboardError: If the controlling terminal cannot be opened for writing.
    """
    try:
        with open(CONTROLLING_TTY, "w", encoding="utf-8") as tty:
            tty.write(data)
            tty.flush()
    except OSError as exc:
        raise ClipboardError(
            "OSC 52 backend failed: no writable controlling terminal at "
            f"{CONTROLLING_TTY}"
        ) from exc


def _run_clipboard_command(backend: str, argv: Sequence[str], data: bytes) -> None:
    """Run a clipboard helper and raise if it fails.

    Do not use ``capture_output=True``. ``xclip`` and ``wl-copy`` daemonize
    to own the selection and keep inherited pipes open, so waiting on those
    pipes stalls until ``GRAPHICAL_BACKEND_TIMEOUT``. Stderr is copied to a
    temp file instead so a failed helper can still be diagnosed.

    Args:
        backend: Backend name used in error messages.
        argv: Command and arguments (list form, never ``shell=True``).
        data: Bytes to send on stdin.

    Raises:
        ClipboardError: If the executable is missing, times out, or is nonzero.
    """
    try:
        with tempfile.TemporaryFile() as err_file:
            result = subprocess.run(
                list(argv),
                input=data,
                stdout=subprocess.DEVNULL,
                stderr=err_file,
                check=False,
                timeout=GRAPHICAL_BACKEND_TIMEOUT,
            )
            err_file.seek(0)
            err = err_file.read().decode("utf-8", errors="replace").strip()
    except subprocess.TimeoutExpired as exc:
        raise ClipboardError(
            f"{backend} backend failed: timed out after "
            f"{GRAPHICAL_BACKEND_TIMEOUT}s waiting for the display"
        ) from exc
    except OSError as exc:
        raise ClipboardError(f"{backend} backend failed: {exc}") from exc
    if result.returncode != 0:
        if err:
            raise ClipboardError(f"{backend} backend failed: {err}")
        raise ClipboardError(
            f"{backend} backend failed with exit status {result.returncode}"
        )


def _copy_via_wayland(text: str) -> None:
    if shutil.which("wl-copy") is None:
        raise ClipboardError("wayland backend failed: wl-copy is not installed")
    _run_clipboard_command("wayland", ["wl-copy"], text.encode("utf-8"))


def _copy_via_xclip(text: str) -> None:
    if shutil.which("xclip") is None:
        raise ClipboardError("xclip backend failed: xclip is not installed")
    _run_clipboard_command(
        "xclip",
        ["xclip", "-selection", "clipboard"],
        text.encode("utf-8"),
    )


def _copy_via_xsel(text: str) -> None:
    if shutil.which("xsel") is None:
        raise ClipboardError("xsel backend failed: xsel is not installed")
    _run_clipboard_command(
        "xsel",
        ["xsel", "--clipboard", "--input"],
        text.encode("utf-8"),
    )


def _copy_via_osc52(text: str) -> None:
    write_to_controlling_tty(build_osc52_sequence(text))


def _copy_via_pyperclip(text: str) -> None:
    try:
        pyperclip.copy(text)
    except pyperclip.PyperclipException as exc:
        raise ClipboardError(f"pyperclip backend failed: {exc}") from exc


def _copy_named_backend(backend: str, text: str) -> None:
    if backend == "wayland":
        _copy_via_wayland(text)
    elif backend == "xclip":
        _copy_via_xclip(text)
    elif backend == "xsel":
        _copy_via_xsel(text)
    elif backend == "osc52":
        _copy_via_osc52(text)
    else:
        raise ClipboardError(
            f"Unknown clipboard backend '{backend}'. "
            f"Choose from: {', '.join(TEXT_BACKENDS)}"
        )


def copy_text_to_clipboard(
    text: str,
    backend: str = "auto",
    debug: bool = False,
    platform: Optional[str] = None,
) -> None:
    """Copy text using the selected clipboard backend.

    On Linux, ``auto`` prefers a native graphical backend when its
    environment and executable are available. ``DISPLAY`` is only a hint;
    if that backend fails, OSC 52 is tried when a controlling terminal is
    writable. Explicit backends do not fall back. OSC 52 is text-only.

    macOS and Windows ``auto`` keep the existing pyperclip path.

    Args:
        text: Text to place on the clipboard.
        backend: One of ``TEXT_BACKENDS``.
        debug: If True, print fallback diagnostics.
        platform: Override ``sys.platform`` (tests).

    Raises:
        ClipboardError: If the selected backend fails and no fallback succeeds.
    """
    selected = (backend or "auto").strip().lower()
    if selected not in TEXT_BACKENDS:
        raise ClipboardError(
            f"Unknown clipboard backend '{selected}'. "
            f"Choose from: {', '.join(TEXT_BACKENDS)}"
        )
    backend = selected
    plat = sys.platform if platform is None else platform

    if backend != "auto":
        _copy_named_backend(backend, text)
        return

    if not plat.startswith("linux"):
        _copy_via_pyperclip(text)
        return

    graphical = preferred_linux_graphical_backend()
    errors = []
    if graphical:
        try:
            _copy_named_backend(graphical, text)
            return
        except ClipboardError as exc:
            errors.append(str(exc))
            if debug:
                print(f"Debug: {exc}; falling back to OSC 52")
    try:
        _copy_via_osc52(text)
    except ClipboardError as exc:
        errors.append(str(exc))
        raise ClipboardError("; ".join(errors)) from exc


def copy_file_contents_to_clipboard(
    file_contents_list,
    include_header=False,
    discord_attachment=False,
    file_paths=None,
    debug=False,
    backend: str = "auto",
):
    """Combine file contents and copy the result to the clipboard.

    Success is returned only when a clipboard backend actually succeeds.
    Backend failures are captured and reported; a failed ``xclip`` process
    is not treated as success.

    Args:
        file_contents_list: Text fragments to combine.
        include_header: Prefix each fragment with a filename header.
        discord_attachment: Wrap fragments in Discord attachment formatting.
        file_paths: Parallel filenames for headers/attachments.
        debug: Print combined contents while building the payload.
        backend: Text clipboard backend (see ``TEXT_BACKENDS``).

    Returns:
        The combined text on success, or None if every backend failed.
    """
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

        copy_text_to_clipboard(combined_contents, backend=backend, debug=debug)
        if debug:
            print(f"Debug: Final combined contents copied to clipboard:\n{combined_contents}")
        return combined_contents
    except ClipboardError as e:
        print(f"Error: {e}")
        return None
    except Exception as e:
        print(f"Error: An unexpected error occurred. {str(e)}")
        return None


def copy_image_to_clipboard(image_path, backend: str = "auto"):
    """Copy an image file to the system clipboard.

    OSC 52 is text-only and is never used for images, including as a
    fallback when a graphical backend fails.

    Args:
        image_path: Path to the image file.
        backend: Text-backend selection from the CLI. ``osc52`` is rejected.
            ``auto`` keeps the existing graphical cascade. Explicit
            ``wayland`` / ``xclip`` / ``xsel`` use only that helper.
    """
    if backend == "osc52":
        print("Error: OSC 52 supports text only; cannot copy images.")
        return False

    try:
        img = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: File '{image_path}' not found")
        return False
    except Exception as e:
        print(f"Error: Unable to open image '{image_path}': {e}")
        return False

    # Determine image format
    is_gif = img.format and img.format.upper() == 'GIF'
    
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

            def _run_image_cmd(argv):
                subprocess.run(argv, input=image_data, check=True)

            if backend == "wayland":
                if not shutil.which("wl-copy"):
                    print("Error: wayland backend failed: wl-copy is not installed")
                    return False
                _run_image_cmd(["wl-copy", "--type", mime_type])
            elif backend == "xclip":
                if not shutil.which("xclip"):
                    print("Error: xclip backend failed: xclip is not installed")
                    return False
                _run_image_cmd(
                    ["xclip", "-selection", "clipboard", "-t", mime_type]
                )
            elif backend == "xsel":
                if not shutil.which("xsel"):
                    print("Error: xsel backend failed: xsel is not installed")
                    return False
                _run_image_cmd(
                    ["xsel", "--clipboard", "--input", "--mime-type", mime_type]
                )
            elif is_wayland() and shutil.which("wl-copy"):
                _run_image_cmd(["wl-copy", "--type", mime_type])
            elif shutil.which("xclip"):
                _run_image_cmd(
                    ["xclip", "-selection", "clipboard", "-t", mime_type]
                )
            elif shutil.which("xsel"):
                _run_image_cmd(
                    ["xsel", "--clipboard", "--input", "--mime-type", mime_type]
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

def _shell_single_quote(value: str) -> str:
    """Safely single-quote a string for POSIX shell.

    Replaces single quotes using the standard pattern: ' -> '\\'' .
    """
    return "'" + value.replace("'", "'\\''") + "'"


def get_linux_file_metadata(path) -> dict | None:
    """Return Linux owner/group/mode for a path, or None if unavailable.

    Only works on Linux. Uses the numeric uid/gid resolved to names via
    :mod:`pwd` and :mod:`grp`. Mode is the permission bits only (e.g. ``0o644``).

    Args:
        path: Filesystem path to inspect.

    Returns:
        Dict with keys ``owner``, ``group``, ``mode`` (int), or None.
    """
    if not sys.platform.startswith("linux"):
        return None
    try:
        import grp
        import pwd
        import stat as stat_mod

        st = Path(path).stat()
        owner = pwd.getpwuid(st.st_uid).pw_name
        group = grp.getgrgid(st.st_gid).gr_name
        mode = stat_mod.S_IMODE(st.st_mode)
        return {"owner": owner, "group": group, "mode": mode}
    except (OSError, KeyError, AttributeError):
        return None


def _emit_write_permission_check(quoted_path: str) -> list[str]:
    """Emit bash that aborts if the destination is not writable.

    Checks the nearest existing ancestor of the destination directory, then
    the destination itself if it already exists. On failure prints to stderr
    and exits non-zero so no content is written.
    """
    # Use a subshell-friendly block with local-ish temps via unique vars
    # scoped per-file by using dest path only in quoted form.
    return [
        f"_cb_dest={quoted_path}",
        '_cb_dir="$(dirname -- "$_cb_dest")"',
        '_cb_check="$_cb_dir"',
        'while [ ! -e "$_cb_check" ] && [ "$_cb_check" != "/" ] && [ "$_cb_check" != "." ]; do',
        '  _cb_check="$(dirname -- "$_cb_check")"',
        "done",
        'if [ ! -w "$_cb_check" ]; then',
        '  echo "Error: no write permission for \'$_cb_check\' (needed for \'$_cb_dest\')" >&2',
        "  exit 1",
        "fi",
        'if [ -e "$_cb_dest" ] && [ ! -w "$_cb_dest" ]; then',
        '  echo "Error: no write permission for \'$_cb_dest\'" >&2',
        "  exit 1",
        "fi",
    ]


def _emit_linux_perm_restore(quoted_path: str, owner: str, group: str, mode: int) -> list[str]:
    """Emit bash to restore mode/owner only when safe.

    - ``chmod`` runs only if the pasting user owns the file or is root.
    - ``chown`` runs only if the owner name exists on the target system
      (group is included when that group exists).
    """
    quoted_owner = _shell_single_quote(owner)
    quoted_group = _shell_single_quote(group)
    mode_oct = format(mode, "04o")
    return [
        f"_cb_dest={quoted_path}",
        # chmod only when root or we own the file (-O)
        'if [ "$(id -u)" -eq 0 ] || [ -O "$_cb_dest" ]; then',
        f'  chmod {mode_oct} -- "$_cb_dest" 2>/dev/null || true',
        "fi",
        # chown only when the source owner account exists here
        f"if id -u {quoted_owner} >/dev/null 2>&1; then",
        f"  if getent group {quoted_group} >/dev/null 2>&1; then",
        f"    chown {quoted_owner}:{quoted_group} -- \"$_cb_dest\" 2>/dev/null || true",
        "  else",
        f"    chown {quoted_owner} -- \"$_cb_dest\" 2>/dev/null || true",
        "  fi",
        "fi",
    ]


def generate_heredoc_script(
    file_paths,
    file_contents_list,
    append: bool = False,
    metadata_list=None,
) -> str:
    """Generate a shell script using heredoc to create or append files.

    On Linux, when per-file metadata is provided (or collectable), the script
    also:

    1. Verifies write access to the destination (or nearest existing parent)
       and aborts with an error before writing if not writable.
    2. After writing, ``chmod`` only if the pasting user owns the file or is root.
    3. After writing, ``chown`` only if the original owner username exists.

    Args:
        file_paths: Destination paths used in the generated script.
        file_contents_list: File contents as strings (parallel to paths).
        append: If True, appends to files (>>); otherwise overwrites (>).
        metadata_list: Optional parallel list of dicts from
            :func:`get_linux_file_metadata` (keys: owner, group, mode).
            Entries may be None. Ownership/mode restore is emitted only for
            non-None entries (Linux capture). Write checks always run.

    Returns:
        Combined shell script text for recreating the files on a target system.
    """
    lines = ["#!/usr/bin/env bash"]
    redir = ">>" if append else ">"
    n = len(file_paths)
    meta = list(metadata_list) if metadata_list is not None else [None] * n
    if len(meta) < n:
        meta.extend([None] * (n - len(meta)))

    for idx, (path, contents) in enumerate(zip(file_paths, file_contents_list)):
        delimiter = _choose_unique_heredoc_delimiter(contents)
        quoted_path = _shell_single_quote(path)
        file_meta = meta[idx]

        # Abort before writing if the destination (or its parent) is not writable.
        lines.extend(_emit_write_permission_check(quoted_path))

        lines.append(f'mkdir -p -- "$(dirname -- {quoted_path})"')
        lines.append(f"cat {redir} {quoted_path} << '{delimiter}'")
        lines.append(contents)
        lines.append(delimiter)

        # Ownership/mode restore only when Linux metadata was captured at copy time.
        if file_meta:
            lines.extend(
                _emit_linux_perm_restore(
                    quoted_path,
                    file_meta["owner"],
                    file_meta["group"],
                    file_meta["mode"],
                )
            )
        lines.append("")
    return "\n".join(lines)

def copy_to_clipboard():  # pragma: no cover
    # Check if input is from STDIN or file
    if len(sys.argv) == 1:
        # Read from STDIN
        try:
            content, _ = read_stdin_with_encoding()
            copy_text_to_clipboard(content)
        except Exception as e:
            print(f"Error copying from STDIN: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Existing file reading logic
        try:
            content, _ = read_with_encoding(sys.argv[1])
            copy_text_to_clipboard(content)
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
            content, _ = read_with_encoding(file_path)
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
    "detect_encoding",
    "read_with_encoding",
    "read_stdin_with_encoding",
    "is_wayland",
    "is_wlclipboard_installed",
    "is_xclip_installed",
    "is_xsel_installed",
    "has_display",
    "TEXT_BACKENDS",
    "CONTROLLING_TTY",
    "x11_display_reachable",
    "ClipboardError",
    "is_pyperclip_installed",
    "check_dependencies",
    "install_dependencies",
    "resolve_text_backend",
    "preferred_linux_graphical_backend",
    "build_osc52_sequence",
    "write_to_controlling_tty",
    "copy_text_to_clipboard",
    "copy_file_contents_to_clipboard",
    "copy_image_to_clipboard",
    "get_linux_file_metadata",
    "generate_heredoc_script",
    "copy_to_clipboard",
    "get_file_stats",
    "format_file_stats",
    "encoding",
]
