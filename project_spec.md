# copybuffer (`cb`) — Project Specification

Single source of truth for product scope and conventions. Agent priority:

`project_spec.md` > `AGENTS.md` > `.crules/modes/*` > tool entrypoints (`GROK.md`, `.codex/`)

## Overview

Python CLI utility that copies file contents, directory contents, or STDIN to the
system clipboard. Supports text, images, Discord-friendly formatting, and heredoc
script generation for recreating files on paste.

- **Package**: `copybuffer` (flat layout)
- **CLI**: `cb` → `copybuffer.main:main` (also intended: `python -m copybuffer` once `__main__` exists)
- **Version (master)**: `pyproject.toml` → `[project].version` (**1.11.1**)
- **Runtime mirror**: `copybuffer.core.__VERSION__` (must match master)
- **Author**: Draeician / Andrew Falgout — MIT License

## Core features

1. **Input sources**
   - One or more file paths
   - Directory expansion (`-d` non-recursive, `-r` recursive)
   - STDIN when no files are given
   - Images (PNG, JPG/JPEG, BMP, GIF first frame)

2. **Output options**
   - Direct clipboard copy (text or image)
   - Optional filename headers (`-i`)
   - Discord attachment formatting (`-a`)
   - Heredoc shell script for recreate-on-paste (`-p`) or append (`--append`)
   - Token statistics (`-t`, tiktoken)
   - Verbose (`-v`) and debug (`--debug`)

3. **Discovery**
   - Honors `.gitignore` via `pathspec` (plus default `.git` ignores)
   - Optional `--image` to include images found while expanding directories

## CLI surface

| Flag | Purpose |
|------|---------|
| `files…` | Paths to copy; STDIN if omitted |
| `--version` | Print `copybuffer version X.Y.Z` |
| `-i, --include-header` | Prefix content with filename header |
| `-d, --directory` | Expand directory args (non-recursive) |
| `-r, --recursive` | Expand directory args recursively |
| `-v, --verbose` | Print copied contents |
| `-a, --attachment` | Discord attachment formatting (**not** append) |
| `-p, --paste` | Emit heredoc script that recreates files |
| `--append` | Heredoc that appends instead of overwriting |
| `-t, --tokens` | Show token statistics |
| `--image` | Include images when expanding directories |
| `--debug` | Debug logging |
| `--backend` | Text clipboard backend: `auto`, `osc52`, `wayland`, `xclip`, `xsel` (overrides `COPYBUFFER_BACKEND`) |

### Usage examples

```bash
cb filename.txt
echo "text" | cb
cb -d directory/
cb -r directory/
cb -a filename.txt
cb -i filename.txt
cb -p path/to/file1.txt path/to/file2.txt
cb --append path/to/file1.txt
cb --backend osc52 filename.txt
cb image.png
cb --version
```

## Stack

| Layer | Choice |
|-------|--------|
| Language | Python 3.9+ (ruff target `py39`) |
| Packaging | hatchling + `pyproject.toml` |
| Runtime deps | `pyperclip`, `Pillow`, `tiktoken`, `pathspec` |
| X11 clipboard | `xclip` or `xsel` + display (DISPLAY is a hint, not proof) |
| Wayland clipboard | `wl-clipboard` (`wl-copy`) |
| Remote/SSH text clipboard | OSC 52 written to `/dev/tty` (text only) |
| Dev deps | `pytest`, `pytest-cov`, `black`, `flake8` |
| Install | `pipx install .` preferred |

### Wayland detection

Treat as Wayland when any of: `WAYLAND_DISPLAY`, `XDG_SESSION_TYPE=wayland`,
`HYPRLAND_INSTANCE_SIGNATURE`, `SWAYSOCK`.

## Layout

```
copybuffer/           # package
  __init__.py         # re-exports core + main
  main.py             # argparse, discovery, orchestration
  core.py             # clipboard, images, heredoc, deps, __VERSION__
tests/                # pytest
  test_discover_files.py
  test_heredoc.py
  test_images.py
  test_wayland.py
  test_clipboard_backends.py
AGENTS.md             # canonical multi-agent instructions
GROK.md               # Grok entrypoint
.grok/                # Grok rules + agent profiles
.crules/              # Skeleton Swarm modes + tasks
.codex/               # Legacy Codex swarm (kept; prefer .crules for new work)
```

## Conventions

- Minimum code that solves the request; no speculative scope growth.
- Prefer list-form `subprocess` (never `shell=True`).
- Never `pip install --break-system-packages`.
- Conventional commits + SemVer; bump both version sources together.
- Keep CLI flags stable; document breaking renames.
- Tests: mock clipboard/display when possible; do not weaken assertions.

## Out of scope (unless explicitly requested)

- Full GUI clipboard manager
- Network clipboard sync / multi-device daemon
- Non-clipboard “everything bucket” product expansion

## Agent workflow

See `AGENTS.md`. Default personas: **Coder** (implementation), **Manager**
(planning, version, commit/release). Task pipeline: `.crules/tasks/{wip,review,done}/`.

## Continuity files

| File | Use |
|------|-----|
| `summary.txt` | Short project status snapshot |
| `instructions.txt` | Pending user-facing instruction log |
| `CHANGELOG.md` | User-visible version history |
