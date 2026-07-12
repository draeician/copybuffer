"""Tests for heredoc script generation utilities.

Expected results:
- _choose_unique_heredoc_delimiter never returns a delimiter present in the contents.
- generate_heredoc_script creates shell scripts that reproduce files exactly
  in both overwrite and append modes, supporting multiple files and special paths.
- Write-permission checks abort the script before writing when the destination
  is not writable.
- Linux metadata restores mode/owner only with safe existence/permission guards.
"""

from pathlib import Path
import os
import re
import secrets
import stat
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from copybuffer.core import (
    generate_heredoc_script,
    get_linux_file_metadata,
    _choose_unique_heredoc_delimiter,
    _shell_single_quote,
)


def test_choose_unique_heredoc_delimiter_unique(monkeypatch):
    tokens = iter(["abcd", "efef"])
    monkeypatch.setattr(secrets, "token_hex", lambda n: next(tokens))
    contents = "prefix EOF_CB_ABCD suffix"
    delim = _choose_unique_heredoc_delimiter(contents)
    assert delim == "EOF_CB_EFEF"
    assert delim not in contents


@pytest.mark.parametrize("append", [False, True])
def test_generate_heredoc_script(tmp_path, append):
    file_paths = [
        "file1.txt",
        "dir with space/file2.txt",
        "weird 'quote'/file3.txt",
        "nested/deeper/path/file4.txt",
    ]
    contents = [
        "alpha",
        "beta with $dollar and `backticks`",
        "gamma\nmulti-line\ncontent",
        "delta\nwith nested dirs",
    ]

    if append:
        for path in file_paths:
            full_path = tmp_path / path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text("start\n")

    script_text = generate_heredoc_script(file_paths, contents, append=append)

    redir = ">>" if append else ">"
    assert f"cat {redir} 'file1.txt'" in script_text
    assert _shell_single_quote("dir with space/file2.txt") in script_text
    assert _shell_single_quote("weird 'quote'/file3.txt") in script_text
    assert _shell_single_quote("nested/deeper/path/file4.txt") in script_text
    assert "no write permission" in script_text
    assert 'mkdir -p -- "$(dirname --' in script_text

    delims = re.findall(r"<< '([^']+)'", script_text)
    assert len(delims) == len(file_paths)
    assert len(set(delims)) == len(file_paths)
    for delim, content in zip(delims, contents):
        assert delim not in content

    script_file = tmp_path / "run.sh"
    script_file.write_text(script_text)
    subprocess.run(["bash", str(script_file)], cwd=tmp_path, check=True)

    for path, content in zip(file_paths, contents):
        full_path = tmp_path / path
        result = full_path.read_text()
        expected = content + "\n"
        if append:
            expected = "start\n" + expected
        assert result == expected


def test_generate_heredoc_script_with_linux_metadata(tmp_path):
    file_paths = ["owned.txt"]
    contents = ["payload"]
    metadata_list = [
        {"owner": "pasteuser", "group": "pastegroup", "mode": 0o640},
    ]

    script_text = generate_heredoc_script(
        file_paths, contents, metadata_list=metadata_list
    )

    assert "chmod 0640 --" in script_text
    assert "[ -O \"$_cb_dest\" ]" in script_text or '[ -O "$_cb_dest" ]' in script_text
    assert "id -u 'pasteuser'" in script_text
    assert "getent group 'pastegroup'" in script_text
    assert "chown 'pasteuser':'pastegroup'" in script_text

    # Running without that user should still write content and skip chown cleanly.
    script_file = tmp_path / "run.sh"
    script_file.write_text(script_text)
    subprocess.run(["bash", str(script_file)], cwd=tmp_path, check=True)
    assert (tmp_path / "owned.txt").read_text() == "payload\n"
    # Mode may be applied (we own the new file); ownership stays as current user.
    mode = stat.S_IMODE((tmp_path / "owned.txt").stat().st_mode)
    assert mode == 0o640


def test_generate_heredoc_aborts_when_not_writable(tmp_path):
    """Script must exit before writing when the destination is not writable."""
    if os.geteuid() == 0:
        pytest.skip("root can write almost anywhere; cannot simulate EACCES")

    locked = tmp_path / "locked"
    locked.mkdir()
    target = locked / "secret.txt"
    target.write_text("original\n")
    # Remove write from directory and file for the current user.
    os.chmod(target, 0o444)
    os.chmod(locked, 0o555)

    try:
        script_text = generate_heredoc_script(
            ["locked/secret.txt"], ["should-not-appear"]
        )
        script_file = tmp_path / "run.sh"
        script_file.write_text(script_text)
        result = subprocess.run(
            ["bash", str(script_file)],
            cwd=tmp_path,
            capture_output=True,
            text=True,
        )
        assert result.returncode != 0
        assert "no write permission" in result.stderr
        assert target.read_text() == "original\n"
    finally:
        os.chmod(locked, 0o755)
        os.chmod(target, 0o644)


def test_get_linux_file_metadata(tmp_path, monkeypatch):
    if not sys.platform.startswith("linux"):
        monkeypatch.setattr(sys, "platform", "win32")
        assert get_linux_file_metadata(tmp_path / "x") is None
        return

    sample = tmp_path / "meta.txt"
    sample.write_text("hi")
    os.chmod(sample, 0o600)
    meta = get_linux_file_metadata(sample)
    assert meta is not None
    assert meta["mode"] == 0o600
    assert isinstance(meta["owner"], str) and meta["owner"]
    assert isinstance(meta["group"], str) and meta["group"]


def test_get_linux_file_metadata_non_linux(monkeypatch, tmp_path):
    monkeypatch.setattr(sys, "platform", "darwin")
    sample = tmp_path / "meta.txt"
    sample.write_text("hi")
    assert get_linux_file_metadata(sample) is None
