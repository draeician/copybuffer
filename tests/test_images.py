from pathlib import Path
from PIL import Image
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from copybuffer import core


def create_temp_image(tmp_path):
    img = Image.new("RGB", (1, 1), color="red")
    path = tmp_path / "test.jpg"
    img.save(path, format="JPEG")
    return path


def test_copy_image_wayland(monkeypatch, tmp_path):
    path = create_temp_image(tmp_path)
    captured = {}

    def fake_run(cmd, input=None, check=None):
        captured["cmd"] = cmd
        captured["input"] = input

    monkeypatch.setattr(core, "is_wayland", lambda: True)
    monkeypatch.setattr(core.shutil, "which", lambda cmd: "/usr/bin/" + cmd)
    monkeypatch.setattr(core.subprocess, "run", fake_run)

    assert core.copy_image_to_clipboard(str(path))
    assert captured["cmd"][0] == "wl-copy"
    assert captured["cmd"][1:] == ["--type", "image/png"]
    assert captured["input"].startswith(b"\x89PNG")


def test_copy_image_xclip(monkeypatch, tmp_path):
    path = create_temp_image(tmp_path)
    captured = {}

    def fake_run(cmd, input=None, check=None):
        captured["cmd"] = cmd
        captured["input"] = input

    def fake_which(cmd):
        return "/usr/bin/xclip" if cmd == "xclip" else None

    monkeypatch.setattr(core, "is_wayland", lambda: False)
    monkeypatch.setattr(core.shutil, "which", fake_which)
    monkeypatch.setattr(core.subprocess, "run", fake_run)

    assert core.copy_image_to_clipboard(str(path))
    assert captured["cmd"][:4] == ["xclip", "-selection", "clipboard", "-t"]
    assert captured["cmd"][4] == "image/png"
    assert captured["input"].startswith(b"\x89PNG")


def test_copy_image_rejects_osc52(tmp_path, capsys):
    path = create_temp_image(tmp_path)
    assert core.copy_image_to_clipboard(str(path), backend="osc52") is False
    out = capsys.readouterr().out
    assert "OSC 52 supports text only" in out


def test_copy_image_does_not_fall_back_to_osc52(monkeypatch, tmp_path, capsys):
    path = create_temp_image(tmp_path)
    tty = tmp_path / "tty"
    tty.write_text("", encoding="utf-8")
    monkeypatch.setattr(core, "CONTROLLING_TTY", str(tty))
    monkeypatch.setattr(core, "is_wayland", lambda: False)
    monkeypatch.setattr(
        core.shutil, "which", lambda cmd: "/usr/bin/xclip" if cmd == "xclip" else None
    )

    def fake_run(cmd, input=None, check=None):
        raise subprocess.CalledProcessError(1, cmd, stderr=b"Can't open display")

    monkeypatch.setattr(core.subprocess, "run", fake_run)
    osc_calls = []

    def fake_osc(_text):
        osc_calls.append(True)
        raise AssertionError("OSC 52 must not be used for images")

    monkeypatch.setattr(core, "_copy_via_osc52", fake_osc)
    monkeypatch.setattr(
        core, "write_to_controlling_tty", lambda data: osc_calls.append(data)
    )

    assert core.copy_image_to_clipboard(str(path)) is False
    assert osc_calls == []
    assert tty.read_text(encoding="utf-8") == ""
    out = capsys.readouterr().out
    assert "OSC 52" not in out
    assert "Error copying image to clipboard" in out
