"""Tests for heredoc script generation utilities.

Expected results:
- _choose_unique_heredoc_delimiter never returns a delimiter present in the contents.
- generate_heredoc_script creates shell scripts that reproduce files exactly
  in both overwrite and append modes, supporting multiple files and special paths.
"""

from pathlib import Path
import re
import secrets
import subprocess
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from copybuffer.core import (
    generate_heredoc_script,
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
