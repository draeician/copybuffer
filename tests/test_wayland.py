from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from copybuffer import core


def test_is_wayland_detection(monkeypatch):
    monkeypatch.setenv("WAYLAND_DISPLAY", "wayland-0")
    assert core.is_wayland()
    monkeypatch.delenv("WAYLAND_DISPLAY", raising=False)

    monkeypatch.setenv("XDG_SESSION_TYPE", "wayland")
    assert core.is_wayland()
    monkeypatch.setenv("XDG_SESSION_TYPE", "x11")

    monkeypatch.setenv("HYPRLAND_INSTANCE_SIGNATURE", "1")
    assert core.is_wayland()
    monkeypatch.delenv("HYPRLAND_INSTANCE_SIGNATURE", raising=False)

    monkeypatch.setenv("SWAYSOCK", "/run/user/1000/sway-ipc.sock")
    assert core.is_wayland()
    monkeypatch.delenv("SWAYSOCK", raising=False)

    assert not core.is_wayland()


def test_is_wlclipboard_installed(monkeypatch):
    monkeypatch.setattr(core.shutil, "which", lambda cmd: "/usr/bin/" + cmd)
    assert core.is_wlclipboard_installed()


def test_check_dependencies_wayland_missing_is_not_hard(monkeypatch):
    monkeypatch.setenv("WAYLAND_DISPLAY", "wayland-0")
    monkeypatch.setattr(core, "is_wlclipboard_installed", lambda: False)
    monkeypatch.setattr(core, "is_pyperclip_installed", lambda: True)
    deps = core.check_dependencies()
    assert deps == []


def test_check_dependencies_wayland_present(monkeypatch):
    monkeypatch.setenv("WAYLAND_DISPLAY", "wayland-0")
    monkeypatch.setattr(core, "is_wlclipboard_installed", lambda: True)
    monkeypatch.setattr(core, "is_pyperclip_installed", lambda: True)
    deps = core.check_dependencies()
    assert "wl-clipboard" not in "".join(deps)


def test_check_dependencies_xclip_missing_is_not_hard(monkeypatch):
    monkeypatch.setattr(core, "is_wayland", lambda: False)
    monkeypatch.setattr(core, "is_xclip_installed", lambda: False)
    monkeypatch.setattr(core, "is_xsel_installed", lambda: False)
    monkeypatch.setattr(core, "is_pyperclip_installed", lambda: True)
    monkeypatch.setenv("DISPLAY", ":1")
    deps = core.check_dependencies()
    assert deps == []


def test_check_dependencies_missing_pyperclip(monkeypatch):
    monkeypatch.setattr(core, "is_wayland", lambda: False)
    monkeypatch.setattr(core, "is_xclip_installed", lambda: True)
    monkeypatch.setattr(core, "is_xsel_installed", lambda: True)
    monkeypatch.setattr(core, "is_pyperclip_installed", lambda: False)
    monkeypatch.setenv("DISPLAY", ":1")
    deps = core.check_dependencies()
    assert deps == ["pyperclip"]


def test_check_dependencies_missing_display_is_not_hard(monkeypatch):
    monkeypatch.setattr(core, "is_wayland", lambda: False)
    monkeypatch.setattr(core, "is_xclip_installed", lambda: True)
    monkeypatch.setattr(core, "is_xsel_installed", lambda: True)
    monkeypatch.setattr(core, "is_pyperclip_installed", lambda: True)
    monkeypatch.delenv("DISPLAY", raising=False)
    deps = core.check_dependencies()
    assert deps == []
    assert "DISPLAY" not in "".join(deps)


def test_copy_file_contents_success(monkeypatch):
    captured = {}

    def fake_copy(text, backend="auto", debug=False):
        captured["text"] = text

    monkeypatch.setattr(core, "copy_text_to_clipboard", fake_copy)
    result = core.copy_file_contents_to_clipboard(
        ["hello"],
        include_header=True,
        discord_attachment=True,
        file_paths=["f.txt"],
        debug=True,
    )
    assert captured["text"]
    assert "=== File: f.txt ===" in captured["text"]
    assert result


def test_is_xclip_and_xsel_installed(monkeypatch):
    monkeypatch.setattr(core.shutil, "which", lambda cmd: "/usr/bin/" + cmd)
    assert core.is_xclip_installed()
    assert core.is_xsel_installed()
