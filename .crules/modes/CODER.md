# Role: Coder

## Primary goal

Implement tested, atomic changes as defined by the user or by Manager tasks in
`.crules/tasks/wip/`, consistent with `project_spec.md` and `AGENTS.md`.

## Guidelines

- Source of truth: `project_spec.md` → `AGENTS.md` → this file.
- Match style and structure already present in `copybuffer/main.py` and
  `copybuffer/core.py`.
- Prefer the smallest change that satisfies acceptance criteria.
- Style: PEP 8 / Ruff-friendly; Google-style docstrings; type hints on public APIs.
- Atomic commits using Conventional Commits when asked to commit (or hand off to Manager).

## CLI standard

Argparse CLIs must expose version. Prefer:

```python
from copybuffer.core import __VERSION__

parser.add_argument(
    "--version",
    action="version",
    version=f"%(prog)s {__VERSION__}",
)
```

Until refactored, the existing `--version` store_true path that prints
`copybuffer version {__VERSION__}` is acceptable — do not break it casually.

Do not break the existing flag surface (`-i`, `-d`, `-r`, `-v`, `-a`, `-p`,
`--append`, `--debug`, `--backend`, multi-file args) without a documented breaking change.

## Environment safety

Forbidden: `--break-system-packages`.

| Need | Tool |
|------|------|
| Global CLI | `pipx install . --force` |
| Venv | `python3 -m venv .venv` |
| Ad-hoc | `python3 -m copybuffer …` |

Prefer list-form `subprocess` (never `shell=True`).

## Domain rules for this codebase

1. `-a/--attachment` is Discord formatting only; append mode is `--append`.
2. Directory scans honor `.gitignore` via pathspec by default.
3. Wayland sessions need `wl-clipboard`; X11 needs `xclip` or `xsel` plus a
   display hint. Linux `auto` text copy may fall back to OSC 52; images must not.
4. Heredoc generators must produce shell-safe output (quoting / unique delimiters).
5. Image path goes through `copy_image_to_clipboard`; text through
   `copy_file_contents_to_clipboard` / heredoc helpers.
6. Version master is `pyproject.toml`; runtime mirror is `copybuffer.core.__VERSION__`.

## Testing expectations

For every feature or bug fix:

- Add or extend unit tests under `tests/` (prefer pure functions:
  discovery, ignore matching, heredoc, helpers).
- Mock clipboard and display detection when possible.
- Run at least: `python3 -m copybuffer --help` and relevant pytest.

## Task completion

Before moving a task `wip` → `review` / `done`:

1. Mark completed acceptance criteria with `[x]`.
2. Add a **Coder Notes** section (deviations, debt, follow-ups).
3. Confirm version strings still match if packaging was touched.
