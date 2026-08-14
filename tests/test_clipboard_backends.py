"""Tests for Linux text clipboard backends, OSC 52, and failure propagation."""

import base64
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from copybuffer import core

# copybuffer.__init__ shadows the submodule with the main() function.
main_mod = sys.modules["copybuffer.main"]


def _clear_wayland(monkeypatch):
    for key in ("WAYLAND_DISPLAY", "HYPRLAND_INSTANCE_SIGNATURE", "SWAYSOCK"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("XDG_SESSION_TYPE", "x11")


def _which_only(*names):
    allowed = set(names)

    def fake_which(cmd):
        return f"/usr/bin/{cmd}" if cmd in allowed else None

    return fake_which


def _completed(argv, returncode, stderr=b"", stdout=b""):
    return subprocess.CompletedProcess(list(argv), returncode, stdout, stderr)


def _run_with_stderr(returncode, message=b""):
    def fake_run(argv, input=None, stdout=None, stderr=None, **kwargs):
        if message and stderr is not None:
            stderr.write(message)
        return _completed(argv, returncode, stderr=message)

    return fake_run


def _point_tty(monkeypatch, tmp_path, name="tty"):
    tty = tmp_path / name
    tty.write_text("", encoding="utf-8")
    monkeypatch.setattr(core, "CONTROLLING_TTY", str(tty))
    return tty


def _force_x11_reachable(monkeypatch, reachable=True):
    monkeypatch.setattr(core, "x11_display_reachable", lambda timeout=0.25: reachable)


def test_resolve_cli_backend_overrides_environment(monkeypatch):
    monkeypatch.setenv("COPYBUFFER_BACKEND", "osc52")
    assert core.resolve_text_backend("xclip") == "xclip"
    assert core.resolve_text_backend("auto") == "auto"
    assert core.resolve_text_backend(None) == "osc52"


def test_resolve_empty_env_defaults_to_auto(monkeypatch):
    monkeypatch.delenv("COPYBUFFER_BACKEND", raising=False)
    assert core.resolve_text_backend(None) == "auto"
    monkeypatch.setenv("COPYBUFFER_BACKEND", "")
    assert core.resolve_text_backend(None) == "auto"


def test_resolve_invalid_env_backend(monkeypatch):
    monkeypatch.setenv("COPYBUFFER_BACKEND", "pbcopy")
    with pytest.raises(core.ClipboardError, match="Unknown clipboard backend"):
        core.resolve_text_backend(None)


def test_build_osc52_sequence_framing_and_base64():
    text = "hello"
    sequence = core.build_osc52_sequence(text)
    payload = base64.b64encode(text.encode("utf-8")).decode("ascii")
    assert sequence == f"\x1b]52;c;{payload}\x07"
    assert sequence.startswith("\x1b]52;c;")
    assert sequence.endswith("\x07")
    encoded = sequence[len("\x1b]52;c;") : -1]
    assert base64.b64decode(encoded) == b"hello"


def test_build_osc52_sequence_unicode_and_multiline():
    text = "héllo 🎯\nsecond line"
    sequence = core.build_osc52_sequence(text)
    encoded = sequence[len("\x1b]52;c;") : -1]
    assert base64.b64decode(encoded).decode("utf-8") == text
    assert "\n" not in encoded
    assert sequence.endswith("\x07")


def test_explicit_osc52_writes_to_tty_not_stdout(monkeypatch, tmp_path, capsys):
    tty = _point_tty(monkeypatch, tmp_path)
    text = "pipe-safe 🎯\nmultiline"
    core.copy_text_to_clipboard(text, backend="osc52")
    written = tty.read_text(encoding="utf-8")
    assert written == core.build_osc52_sequence(text)
    captured = capsys.readouterr()
    assert "\x1b]52;c;" not in captured.out
    assert "\x1b]52;c;" not in captured.err
    assert captured.out == ""


def test_explicit_osc52_skips_x11_and_wayland(monkeypatch, tmp_path):
    tty = _point_tty(monkeypatch, tmp_path)
    monkeypatch.setenv("DISPLAY", "localhost:12.0")
    monkeypatch.setenv("WAYLAND_DISPLAY", "wayland-0")
    monkeypatch.setattr(core.shutil, "which", lambda cmd: f"/usr/bin/{cmd}")
    calls = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        return _completed(argv, 0)

    monkeypatch.setattr(core.subprocess, "run", fake_run)
    core.copy_text_to_clipboard("only-osc", backend="osc52")
    assert calls == []
    assert "only-osc" in base64.b64decode(
        tty.read_text(encoding="utf-8")[len("\x1b]52;c;") : -1]
    ).decode("utf-8")


def test_osc52_fails_without_writable_tty(monkeypatch, tmp_path, capsys):
    missing = tmp_path / "missing-dir" / "tty"
    monkeypatch.setattr(core, "CONTROLLING_TTY", str(missing))
    with pytest.raises(core.ClipboardError, match="no writable controlling terminal"):
        core.copy_text_to_clipboard("test", backend="osc52")
    result = core.copy_file_contents_to_clipboard(["test"], backend="osc52")
    assert result is None
    out = capsys.readouterr().out
    assert "no writable controlling terminal" in out
    assert "successfully" not in out


def test_xclip_nonzero_status_is_failure(monkeypatch, tmp_path, capsys):
    _clear_wayland(monkeypatch)
    _force_x11_reachable(monkeypatch, True)
    monkeypatch.setenv("DISPLAY", "localhost:12.0")
    monkeypatch.setattr(core.shutil, "which", _which_only("xclip"))
    monkeypatch.setattr(core, "CONTROLLING_TTY", str(tmp_path / "missing" / "tty"))
    monkeypatch.setattr(
        core.subprocess,
        "run",
        _run_with_stderr(1, b"Error: Can't open display: localhost:12.0\n"),
    )
    with pytest.raises(core.ClipboardError, match="xclip backend failed"):
        core.copy_text_to_clipboard("test", backend="xclip")
    result = core.copy_file_contents_to_clipboard(["test"], backend="xclip")
    assert result is None
    out = capsys.readouterr().out
    assert "xclip" in out
    assert "successfully" not in out


def test_invalid_display_auto_falls_back_to_osc52(monkeypatch, tmp_path, capsys):
    _clear_wayland(monkeypatch)
    _force_x11_reachable(monkeypatch, True)
    tty = _point_tty(monkeypatch, tmp_path)
    monkeypatch.setenv("DISPLAY", "localhost:12.0")
    monkeypatch.setattr(core.shutil, "which", _which_only("xclip"))
    calls = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        return _completed(
            argv,
            1,
            stderr=b"Error: Can't open display: localhost:12.0\n",
        )

    monkeypatch.setattr(core.subprocess, "run", fake_run)
    result = core.copy_file_contents_to_clipboard(["test"])
    assert result is not None
    assert calls == [["xclip", "-selection", "clipboard"]]
    written = tty.read_text(encoding="utf-8")
    assert written == core.build_osc52_sequence(result)
    out = capsys.readouterr().out
    assert "successfully" not in out


def test_unreachable_display_skips_xclip_and_uses_osc52(monkeypatch, tmp_path):
    _clear_wayland(monkeypatch)
    _force_x11_reachable(monkeypatch, False)
    tty = _point_tty(monkeypatch, tmp_path)
    monkeypatch.setenv("DISPLAY", "localhost:12.0")
    monkeypatch.setattr(core.shutil, "which", _which_only("xclip"))
    calls = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        return _completed(argv, 0)

    monkeypatch.setattr(core.subprocess, "run", fake_run)
    core.copy_text_to_clipboard("no-hang", backend="auto")
    assert calls == []
    assert tty.read_text(encoding="utf-8") == core.build_osc52_sequence("no-hang")


def test_xclip_timeout_falls_back_to_osc52(monkeypatch, tmp_path):
    _clear_wayland(monkeypatch)
    _force_x11_reachable(monkeypatch, True)
    tty = _point_tty(monkeypatch, tmp_path)
    monkeypatch.setenv("DISPLAY", "localhost:12.0")
    monkeypatch.setattr(core.shutil, "which", _which_only("xclip"))

    def fake_run(argv, **kwargs):
        raise subprocess.TimeoutExpired(argv, core.GRAPHICAL_BACKEND_TIMEOUT)

    monkeypatch.setattr(core.subprocess, "run", fake_run)
    core.copy_text_to_clipboard("after-timeout", backend="auto")
    assert tty.read_text(encoding="utf-8") == core.build_osc52_sequence(
        "after-timeout"
    )


def test_x11_display_reachable_unix_missing(monkeypatch):
    monkeypatch.setenv("DISPLAY", ":99")
    monkeypatch.setattr(core.os.path, "exists", lambda path: False)
    assert core.x11_display_reachable() is False


def test_x11_display_reachable_unix_present(monkeypatch):
    monkeypatch.setenv("DISPLAY", ":0")
    monkeypatch.setattr(
        core.os.path, "exists", lambda path: path == "/tmp/.X11-unix/X0"
    )
    assert core.x11_display_reachable() is True


def test_x11_display_reachable_tcp_refused(monkeypatch):
    monkeypatch.setenv("DISPLAY", "localhost:12.0")
    monkeypatch.setattr(core, "_tcp_port_open", lambda host, port, timeout: False)
    monkeypatch.setattr(core.shutil, "which", _which_only("xclip"))
    monkeypatch.setattr(core, "is_wayland", lambda: False)
    assert core.x11_display_reachable() is False
    assert core.preferred_linux_graphical_backend() is None


def test_x11_display_reachable_tcp_open(monkeypatch):
    monkeypatch.setenv("DISPLAY", "localhost:12.0")
    seen = {}

    def fake_open(host, port, timeout):
        seen["host"] = host
        seen["port"] = port
        return True

    monkeypatch.setattr(core, "_tcp_port_open", fake_open)
    assert core.x11_display_reachable() is True
    assert seen == {"host": "localhost", "port": 6012}


def test_explicit_xclip_does_not_fall_back_to_osc52(monkeypatch, tmp_path):
    tty = _point_tty(monkeypatch, tmp_path)
    monkeypatch.setenv("DISPLAY", "localhost:12.0")
    monkeypatch.setattr(core.shutil, "which", _which_only("xclip"))

    def fake_run(argv, **kwargs):
        return _completed(argv, 1, stderr=b"Error: Can't open display\n")

    monkeypatch.setattr(core.subprocess, "run", fake_run)
    with pytest.raises(core.ClipboardError, match="xclip backend failed"):
        core.copy_text_to_clipboard("test", backend="xclip")
    assert tty.read_text(encoding="utf-8") == ""


def test_all_backends_fail_returns_none_and_error(monkeypatch, tmp_path, capsys):
    _clear_wayland(monkeypatch)
    _force_x11_reachable(monkeypatch, True)
    monkeypatch.setenv("DISPLAY", "localhost:12.0")
    monkeypatch.setattr(core.shutil, "which", _which_only("xclip"))
    monkeypatch.setattr(core, "CONTROLLING_TTY", str(tmp_path / "nope" / "tty"))

    def fake_run(argv, **kwargs):
        return _completed(
            argv, 1, stderr=b"Error: Can't open display: localhost:12.0\n"
        )

    monkeypatch.setattr(core.subprocess, "run", fake_run)
    result = core.copy_file_contents_to_clipboard(["test"])
    assert result is None
    out = capsys.readouterr().out
    assert "successfully" not in out
    assert "xclip backend failed" in out
    assert "OSC 52" in out


def test_successful_xclip_does_not_use_osc52(monkeypatch, tmp_path, capsys):
    _clear_wayland(monkeypatch)
    _force_x11_reachable(monkeypatch, True)
    tty = _point_tty(monkeypatch, tmp_path)
    monkeypatch.setenv("DISPLAY", ":0")
    monkeypatch.setattr(core.shutil, "which", _which_only("xclip"))
    captured = {}

    def fake_run(argv, input=None, **kwargs):
        captured["argv"] = argv
        captured["input"] = input
        captured["capture_output"] = kwargs.get("capture_output", False)
        captured["stdout"] = kwargs.get("stdout")
        captured["stderr"] = kwargs.get("stderr")
        return _completed(argv, 0)

    monkeypatch.setattr(core.subprocess, "run", fake_run)
    result = core.copy_file_contents_to_clipboard(["hello"])
    assert result == "hello\n"
    assert captured["argv"] == ["xclip", "-selection", "clipboard"]
    assert captured["input"] == b"hello\n"
    assert captured["capture_output"] is False
    assert captured["stdout"] is subprocess.DEVNULL
    assert captured["stderr"] is not subprocess.PIPE
    assert captured["stderr"] is not subprocess.DEVNULL
    assert tty.read_text(encoding="utf-8") == ""
    assert "successfully" not in capsys.readouterr().out


def test_successful_wayland_preferred_over_xclip(monkeypatch, tmp_path):
    tty = _point_tty(monkeypatch, tmp_path)
    monkeypatch.setenv("WAYLAND_DISPLAY", "wayland-0")
    monkeypatch.setenv("DISPLAY", ":0")
    monkeypatch.setattr(core.shutil, "which", lambda cmd: f"/usr/bin/{cmd}")
    captured = {}

    def fake_run(argv, input=None, **kwargs):
        captured["argv"] = argv
        captured["input"] = input
        return _completed(argv, 0)

    monkeypatch.setattr(core.subprocess, "run", fake_run)
    core.copy_text_to_clipboard("wayland-text", backend="auto")
    assert captured["argv"][0] == "wl-copy"
    assert captured["input"] == b"wayland-text"
    assert tty.read_text(encoding="utf-8") == ""


def test_auto_without_display_uses_osc52(monkeypatch, tmp_path):
    _clear_wayland(monkeypatch)
    tty = _point_tty(monkeypatch, tmp_path)
    monkeypatch.delenv("DISPLAY", raising=False)
    monkeypatch.setattr(core.shutil, "which", _which_only("xclip"))
    calls = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        return _completed(argv, 0)

    monkeypatch.setattr(core.subprocess, "run", fake_run)
    core.copy_text_to_clipboard("ssh-text", backend="auto")
    assert calls == []
    assert tty.read_text(encoding="utf-8") == core.build_osc52_sequence("ssh-text")


def test_macos_auto_uses_pyperclip(monkeypatch):
    copied = {}

    def fake_copy(text):
        copied["text"] = text

    monkeypatch.setattr(core.pyperclip, "copy", fake_copy)
    core.copy_text_to_clipboard("mac-text", backend="auto", platform="darwin")
    assert copied["text"] == "mac-text"


def test_windows_auto_uses_pyperclip(monkeypatch):
    copied = {}

    def fake_copy(text):
        copied["text"] = text

    monkeypatch.setattr(core.pyperclip, "copy", fake_copy)
    core.copy_text_to_clipboard("win-text", backend="auto", platform="win32")
    assert copied["text"] == "win-text"


def test_copy_file_contents_success_headers(monkeypatch):
    captured = {}

    def fake_copy(text, backend="auto", debug=False):
        captured["text"] = text
        captured["backend"] = backend

    monkeypatch.setattr(core, "copy_text_to_clipboard", fake_copy)
    result = core.copy_file_contents_to_clipboard(
        ["hello"],
        include_header=True,
        discord_attachment=True,
        file_paths=["f.txt"],
        debug=True,
        backend="xclip",
    )
    assert captured["text"]
    assert captured["backend"] == "xclip"
    assert "=== File: f.txt ===" in captured["text"]
    assert result


def test_main_stdin_no_false_success_nonzero_exit(monkeypatch, tmp_path, capsys):
    _clear_wayland(monkeypatch)
    _force_x11_reachable(monkeypatch, True)
    monkeypatch.setenv("DISPLAY", "localhost:12.0")
    monkeypatch.delenv("COPYBUFFER_BACKEND", raising=False)
    monkeypatch.setattr(sys, "argv", ["cb"])
    monkeypatch.setattr(main_mod, "check_dependencies", lambda: [])
    monkeypatch.setattr(main_mod, "read_stdin_with_encoding", lambda: ("test", "utf-8"))
    monkeypatch.setattr(core.shutil, "which", _which_only("xclip"))
    monkeypatch.setattr(core, "CONTROLLING_TTY", str(tmp_path / "missing" / "tty"))

    def fake_run(argv, **kwargs):
        return _completed(
            argv,
            1,
            stderr=b"Error: Can't open display: localhost:12.0\n",
        )

    monkeypatch.setattr(core.subprocess, "run", fake_run)
    assert main_mod.main() == 1
    out = capsys.readouterr().out
    assert "STDIN copied to the clipboard successfully!" not in out
    assert "successfully" not in out
    assert "xclip backend failed" in out


def test_main_cli_backend_overrides_env(monkeypatch, tmp_path, capsys):
    tty = _point_tty(monkeypatch, tmp_path)
    monkeypatch.setenv("COPYBUFFER_BACKEND", "xclip")
    monkeypatch.setenv("DISPLAY", "localhost:12.0")
    monkeypatch.setattr(sys, "argv", ["cb", "--backend", "osc52"])
    monkeypatch.setattr(main_mod, "check_dependencies", lambda: [])
    monkeypatch.setattr(
        main_mod, "read_stdin_with_encoding", lambda: ("cli-wins", "utf-8")
    )
    calls = []

    def fake_run(argv, **kwargs):
        calls.append(argv)
        return _completed(argv, 1, stderr=b"should not be used\n")

    monkeypatch.setattr(core.subprocess, "run", fake_run)
    monkeypatch.setattr(core.shutil, "which", _which_only("xclip"))
    assert main_mod.main() == 0
    assert calls == []
    written = tty.read_text(encoding="utf-8")
    assert written.startswith("\x1b]52;c;")
    decoded = base64.b64decode(written[len("\x1b]52;c;") : -1]).decode("utf-8")
    assert "cli-wins" in decoded
    out = capsys.readouterr().out
    assert "STDIN copied to the clipboard successfully!" in out
    assert "\x1b]52;c;" not in out


def test_main_help_documents_backend(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["cb", "--help"])
    with pytest.raises(SystemExit) as excinfo:
        main_mod.main()
    assert excinfo.value.code == 0
    out = capsys.readouterr().out
    assert "--backend" in out
    assert "osc52" in out
    assert "COPYBUFFER_BACKEND" in out
