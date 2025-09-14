import pyperclip

import copybuffer


def test_is_wayland_detection(monkeypatch):
    monkeypatch.setenv("WAYLAND_DISPLAY", "wayland-0")
    assert copybuffer.is_wayland()
    monkeypatch.delenv("WAYLAND_DISPLAY", raising=False)

    monkeypatch.setenv("XDG_SESSION_TYPE", "wayland")
    assert copybuffer.is_wayland()
    monkeypatch.setenv("XDG_SESSION_TYPE", "x11")

    monkeypatch.setenv("HYPRLAND_INSTANCE_SIGNATURE", "1")
    assert copybuffer.is_wayland()
    monkeypatch.delenv("HYPRLAND_INSTANCE_SIGNATURE", raising=False)

    monkeypatch.setenv("SWAYSOCK", "/run/user/1000/sway-ipc.sock")
    assert copybuffer.is_wayland()
    monkeypatch.delenv("SWAYSOCK", raising=False)

    assert not copybuffer.is_wayland()


def test_is_wlclipboard_installed(monkeypatch):
    monkeypatch.setattr(copybuffer.shutil, "which", lambda cmd: "/usr/bin/" + cmd)
    assert copybuffer.is_wlclipboard_installed()


def test_check_dependencies_wayland_missing(monkeypatch):
    monkeypatch.setenv("WAYLAND_DISPLAY", "wayland-0")
    monkeypatch.setattr(copybuffer, "is_wlclipboard_installed", lambda: False)
    deps = copybuffer.check_dependencies()
    assert "wl-clipboard (wl-copy and wl-paste)" in deps


def test_check_dependencies_wayland_present(monkeypatch):
    monkeypatch.setenv("WAYLAND_DISPLAY", "wayland-0")
    monkeypatch.setattr(copybuffer, "is_wlclipboard_installed", lambda: True)
    deps = copybuffer.check_dependencies()
    assert "wl-clipboard" not in "".join(deps)


def test_check_dependencies_xclip_missing(monkeypatch):
    monkeypatch.setattr(copybuffer, "is_wayland", lambda: False)
    monkeypatch.setattr(copybuffer, "is_xclip_installed", lambda: False)
    monkeypatch.setattr(copybuffer, "is_xsel_installed", lambda: False)
    monkeypatch.setenv("DISPLAY", ":1")
    deps = copybuffer.check_dependencies()
    assert deps == ["xclip or xsel"]


def test_check_dependencies_missing_pyperclip(monkeypatch):
    monkeypatch.setattr(copybuffer, "is_wayland", lambda: False)
    monkeypatch.setattr(copybuffer, "is_xclip_installed", lambda: True)
    monkeypatch.setattr(copybuffer, "is_xsel_installed", lambda: True)
    monkeypatch.setattr(copybuffer, "is_pyperclip_installed", lambda: False)
    monkeypatch.setenv("DISPLAY", ":1")
    deps = copybuffer.check_dependencies()
    assert deps == ["pyperclip"]


def test_check_dependencies_missing_display(monkeypatch):
    monkeypatch.setattr(copybuffer, "is_wayland", lambda: False)
    monkeypatch.setattr(copybuffer, "is_xclip_installed", lambda: True)
    monkeypatch.setattr(copybuffer, "is_xsel_installed", lambda: True)
    monkeypatch.delenv("DISPLAY", raising=False)
    deps = copybuffer.check_dependencies()
    assert "DISPLAY environment variable" in deps


def test_copy_file_contents_success(monkeypatch):
    captured = {}

    def fake_copy(text):
        captured["text"] = text

    monkeypatch.setattr(pyperclip, "copy", fake_copy)
    result = copybuffer.copy_file_contents_to_clipboard(
        ["hello"],
        include_header=True,
        discord_attachment=True,
        file_paths=["f.txt"],
        debug=True,
    )
    assert captured["text"]
    assert "=== File: f.txt ===" in captured["text"]
    assert result


def test_copy_file_contents_wayland_error(monkeypatch, capsys):
    def raising_copy(_):
        raise pyperclip.PyperclipException()

    monkeypatch.setattr(pyperclip, "copy", raising_copy)
    monkeypatch.setattr(copybuffer, "is_wayland", lambda: True)
    copybuffer.copy_file_contents_to_clipboard(["data"])
    assert "wl-clipboard" in capsys.readouterr().out


def test_copy_file_contents_no_display(monkeypatch, capsys):
    def raising_copy(_):
        raise pyperclip.PyperclipException()

    monkeypatch.setattr(pyperclip, "copy", raising_copy)
    monkeypatch.setattr(copybuffer, "is_wayland", lambda: False)
    monkeypatch.delenv("DISPLAY", raising=False)
    copybuffer.copy_file_contents_to_clipboard(["data"])
    assert "DISPLAY" in capsys.readouterr().out


def test_is_xclip_and_xsel_installed(monkeypatch):
    monkeypatch.setattr(copybuffer.shutil, "which", lambda cmd: "/usr/bin/" + cmd)
    assert copybuffer.is_xclip_installed()
    assert copybuffer.is_xsel_installed()

