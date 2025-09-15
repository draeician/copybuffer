from pathlib import Path
from PIL import Image
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
