# Agent System Status: [CUSTOMIZED]

Canonical instruction file for Grok Build, Codex, Claude Code, Cursor, and human contributors.

Read this file completely before changing code. When instructions conflict:

`project_spec.md` > `AGENTS.md` > `.crules/modes/*` > tool-specific entrypoints (`GROK.md`, `.codex/AGENTS.md`, native IDE rules)

## Project identity

This repository is **copybuffer**: a Python CLI utility for copying file contents,
directory contents, or STDIN to the system clipboard (text and images).

- Package: `copybuffer` (flat layout under `copybuffer/`)
- CLI entry points: `cb` → `copybuffer.main:main`; also `python -m copybuffer`
- Packaging: `pyproject.toml` (hatchling) — **master** version source
- Runtime version constant: `copybuffer.core.__VERSION__` (must match pyproject)
- Dependencies: `pyperclip`, `Pillow`, `tiktoken`, `pathspec`
- Linux clipboard helpers: `xclip`/`xsel` (X11) or `wl-clipboard` (Wayland)
- Authoritative product scope: `project_spec.md`
- Legacy Codex swarm (still present): `.codex/` — prefer `.crules/` + `.grok/` for new work

## Required reading before implementation

1. `AGENTS.md` (this file)
2. `project_spec.md`
3. Active task under `.crules/tasks/wip/` (if present)
4. Relevant swarm mode under `.crules/modes/` when acting as Manager or Coder
5. `README.md` / `CHANGELOG.md` when changing user-facing CLI behavior
6. Existing tests under `tests/` for the area you touch

## Swarm SOP (crules)

This repo uses the **Skeleton Swarm** workflow from crules (aligned with `ap` / `ol`).

| Path | Role |
|------|------|
| `.crules/modes/MANAGER.md` | Orchestrate, version, task pipeline — do not implement product code |
| `.crules/modes/CODER.md` | Implement atomic, tested changes from tasks / user request |
| `.crules/modes/GIT_POLICY.md` | Conventional commits, branching, secret scan, release |
| `.crules/modes/BOOTSTRAPPER.md` | Only when `AGENTS.md` status is `[TEMPLATE]` |
| `.crules/tasks/{wip,review,done}/` | Markdown task files with acceptance criteria |
| `project_spec.md` | Single source of truth for scope and conventions |
| `.grok/rules/` | Always-on Grok project rules (SOP + style) |
| `.grok/agents/` | Optional Grok agent profiles (manager / coder / swarm) |

Default persona for implementation work: **Coder**.
Default persona for planning, commits, releases, backlog: **Manager**.

Shortcut keywords (act as Manager, then follow `GIT_POLICY.md`):

- **commit** — secret scan, version bump, verify CLI version, conventional commit
- **branch** — create `feat/` / `fix/` / `docs/` / `chore/` / `refactor/` branch
- **release** — verify version, changelog summary, tag, push tags

## Hard boundaries

1. Keep CLI surface stable: document any flag rename/removal as breaking.
  Known flags include: file args, `-i/--include-header`, `-d/--directory`,
  `-r` (recursive), `-v/--verbose`, `-a/--attachment` (Discord), `-p/--paste`
  (heredoc), `--append`, `--debug`, `--backend`, `--version`.
2. Do not repurpose `-a/--attachment` for append — use `--append` for heredoc append mode.
3. Never use `pip install --break-system-packages`. Prefer `pipx`, project `.venv`,
   or `python3 -m copybuffer`.
4. Never commit secrets, credentials, or private clipboard dumps.
5. Do not expand scope into a full GUI clipboard manager, network sync service,
   or multi-user daemon unless the user explicitly requests it and tasks cover it.
6. Prefer list-form `subprocess` — never `shell=True`.
7. Honor `.gitignore` when scanning directories (pathspec); do not copy ignored paths by default.
8. Platform clipboard behavior: detect Wayland vs X11 correctly; prefer
   `wl-clipboard` on Wayland and `xclip`/`xsel` on X11 when DISPLAY is set.
   Treat DISPLAY as a hint, not proof. Linux `auto` text copy may fall back
   to OSC 52 on `/dev/tty`. OSC 52 is text-only.

## Coding style (Python)

- Target Python 3.9+ (`tool.ruff.target-version = "py39"`; modern union syntax OK).
- Type hints on public functions; Google-style docstrings for public callables.
- Prefer existing deps (`pyperclip`, `Pillow`, `tiktoken`, `pathspec`) over new
  production dependencies unless a task adds them.
- No `shell=True` in `subprocess` — pass argv lists.
- `snake_case` functions/vars; `PascalCase` only for classes/dataclasses.
- Match existing `copybuffer/` module patterns (`main.py` CLI + discovery,
  `core.py` clipboard/image/heredoc helpers) before introducing modules.
- Dev tooling: pytest, black, flake8 (see `pyproject.toml` optional `dev`).

## Versioning and packaging

- Version strings must agree across:
  - `pyproject.toml` (`[project].version`) — **master**
  - `copybuffer/core.py` (`__VERSION__`)
  - Git tags when releasing (`vX.Y.Z`)
- Verify with: `python3 -m copybuffer --version` (or installed `cb --version`).
- Bump rules: `feat` → minor, `fix`/`docs`/`chore`/`refactor` → patch,
  `BREAKING CHANGE` / `!` → major. Versions only increase (monotonic).
- On commit: base version = highest of pyproject, `__VERSION__`, and tags.

## Testing discipline

- Prefer the smallest test that proves the change (pytest under `tests/`).
- Mock clipboard / subprocess / display detection; unit suite should not require
  a live graphical session when avoidable.
- Run relevant tests before claiming done, e.g.:
  - `python -m pytest tests/ -q`
  - or the project venv: `.venv/bin/python -m pytest tests/ -q`
- Do not weaken assertions to green a bad implementation.
- For CLI changes: cover argparse paths, discovery/ignore, heredoc, and
  platform clipboard routing when those areas are touched.
- Existing suites: `test_discover_files.py`, `test_heredoc.py`, `test_images.py`,
  `test_wayland.py`.

## Git discipline

- Follow `.crules/modes/GIT_POLICY.md`.
- Conventional commits; imperative subject; max ~72 chars.
- Prefer feature branches; do not force-push `main`.
- Track `AGENTS.md`, `GROK.md`, `project_spec.md`, `.grok/`, and `.crules/` in git.
- Legacy `.codex/` remains for Codex workflows; do not delete without an explicit request.
- Personal IDE dumps (e.g. `.cursorrules` if gitignored) stay local unless asked.

## Work discipline

- Minimum code that solves the stated problem. Nothing speculative.
- Touch only what you must. Clean up only your own mess.
- Surface tradeoffs; do not hide confusion.
- Define success criteria; loop until verified.
- When a task file exists, update acceptance criteria and Coder Notes before
  moving it `wip` → `review` → `done`.
- Cross-session continuity: `summary.txt`, `instructions.txt`.

## Grok-specific layout

| Path | Purpose |
|------|---------|
| `GROK.md` | Thin Grok entrypoint → points here |
| `.grok/rules/*.md` | Auto-loaded project rules |
| `.grok/agents/*.md` | Named agent profiles (`manager`, `coder`, `swarm`) |

Use `grok inspect` to confirm rules and agents load.
