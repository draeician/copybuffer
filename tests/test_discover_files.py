from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from copybuffer.main import discover_files


def _as_relative_paths(entries):
    return [entry.display_path for entry in entries]


def test_discover_files_recursive_expands_nested(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    base = Path("project")
    nested_dir = base / "nested" / "deeper"
    (tmp_path / base).mkdir()
    (tmp_path / nested_dir).mkdir(parents=True)
    (tmp_path / base / "top.txt").write_text("root")
    (tmp_path / nested_dir / "inner.txt").write_text("deep")

    text_entries, image_entries, missing, directory_errors = discover_files(
        [str(base)], include_directory=False, recursive=True, allow_images=False
    )

    assert missing == []
    assert directory_errors == []
    assert _as_relative_paths(text_entries) == [
        "project/nested/deeper/inner.txt",
        "project/top.txt",
    ]
    assert image_entries == []


def test_discover_files_honors_gitignore_and_images(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / ".gitignore").write_text("ignored_dir/\n*.bin\n")

    target_dir = Path("data")
    ignored = target_dir / "ignored_dir"
    (tmp_path / ignored).mkdir(parents=True)
    (tmp_path / target_dir).mkdir(exist_ok=True)
    (tmp_path / target_dir / "kept.txt").write_text("keep")
    (tmp_path / ignored / "skip.txt").write_text("skip")
    (tmp_path / target_dir / "artifact.bin").write_text("binary")
    (tmp_path / target_dir / "picture.png").write_text("fake image")

    text_entries, image_entries, missing, directory_errors = discover_files(
        [str(target_dir)], include_directory=True, recursive=True, allow_images=False
    )

    assert missing == []
    assert directory_errors == []
    assert _as_relative_paths(text_entries) == ["data/kept.txt"]
    assert image_entries == []

    text_entries, image_entries, _, _ = discover_files(
        [str(target_dir)], include_directory=True, recursive=True, allow_images=True
    )

    assert _as_relative_paths(text_entries) == ["data/kept.txt"]
    assert _as_relative_paths(image_entries) == ["data/picture.png"]
