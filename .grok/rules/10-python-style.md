# Python coding style (copybuffer)

Apply on any `*.py` edit under this repository.

## Language and packaging

- Target Python 3.9+ (`tool.ruff.target-version = "py39"`).
- Package lives in flat `copybuffer/` (not `src/`).
- Prefer existing production dependencies; do not add new ones without an explicit task.
- Entry point: `cb` → `copybuffer.main:main` (also `python -m copybuffer`).
- Version constant is `__VERSION__` in `copybuffer/core.py` (not `__version__`).

## Style

1. PEP 8 / Ruff-friendly layout; 4-space indent; line length 88.
2. Type hints on public functions; return types included.
3. Google-style docstrings for public callables.
4. f-strings for formatting.
5. `snake_case` functions and variables; `PascalCase` classes/dataclasses.
6. Prefer explicit `is None` checks for singletons.
7. Narrow `except` clauses; preserve causes when re-raising.
8. Use `with` for resources; no bare `open` without context managers.

## Subprocess and safety

- Always pass argv **lists** to `subprocess` — never `shell=True`.
- Do not use `pip install --break-system-packages`.
- Install with `pipx` or a project venv; ad-hoc via `python3 -m copybuffer`.

## Domain-specific

- Clipboard backends: Linux text uses `--backend` / `COPYBUFFER_BACKEND`
  (`auto`, `osc52`, `wayland`, `xclip`, `xsel`). `auto` prefers Wayland
  (`wl-copy`) or X11 (`xclip`/`xsel`) and falls back to OSC 52 on `/dev/tty`.
  Do not use OSC 52 for images. macOS/Windows `auto` stays on pyperclip.
- Wayland detection: `WAYLAND_DISPLAY`, `XDG_SESSION_TYPE=wayland`,
  `HYPRLAND_INSTANCE_SIGNATURE`, or `SWAYSOCK`.
- Directory discovery: honor `.gitignore` via pathspec; optional recursion (`-r`).
- Image formats: PNG, JPG, JPEG, BMP, GIF (and existing GIF-specific path in core).
- Heredoc generation (`-p` / `--append`) must produce safe shell-quoted scripts.
- Discord formatting is `-a/--attachment` only — never overload with append semantics.
- Token counting uses `tiktoken` when reporting stats; do not hard-require network.

## Structure preference

Keep changes local to existing modules until size or clarity demands a split:

| Module | Responsibility |
|--------|----------------|
| `main.py` | argparse, file discovery, orchestration |
| `core.py` | clipboard, images, heredoc, deps, `__VERSION__` |

If splitting, preserve the public CLI flag surface.

## Tests

- Prefer pure-function unit tests for discovery, ignore rules, heredoc, and helpers.
- Mock clipboard and display detection; avoid requiring a live graphical session.
- Do not weaken tests to pass a bad change.
- Name tests clearly; one concern per test function.
