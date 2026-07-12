# Swarm SOP (always on)

You operate in a multi-agent (Skeleton Swarm) repository. Native Grok rules
are loaded; also obey root `AGENTS.md`.

## Priority

`project_spec.md` > `AGENTS.md` > `.crules/modes/*` > this file

## Personas

| Mode | When | File |
|------|------|------|
| Manager | planning, backlog, commit/branch/release | `.crules/modes/MANAGER.md` |
| Coder | implementation and tests | `.crules/modes/CODER.md` |
| Git policy | any VCS mutation | `.crules/modes/GIT_POLICY.md` |

Default for coding requests: **Coder**. Default for “commit” / “release” / roadmap: **Manager**.

## Session checklist

1. Read `AGENTS.md` and `project_spec.md` when starting non-trivial work.
2. Track non-trivial work as Markdown under `.crules/tasks/wip/` with acceptance criteria.
3. Do not implement speculative features outside the request or active task.
4. Never use `--break-system-packages`. Prefer `pipx`, venv, or `python3 -m copybuffer`.
5. Preserve CLI flag meanings: `-a` is Discord attachment; append mode is `--append`.

## Important files

| File | Use |
|------|-----|
| `project_spec.md` | Scope, CLI surface, features |
| `AGENTS.md` | Hard boundaries and coding rules |
| `GROK.md` | Grok entrypoint |
| `CHANGELOG.md` | Version history |
| `summary.txt` / `instructions.txt` | Cross-session continuity |
| `.grok/agents/` | Optional named agent profiles |
| `.codex/` | Legacy Codex tasking (prefer `.crules/` for new work) |

## Verification

Before claiming done:

- Smoke: `python3 -m copybuffer --help` and/or `python3 -m copybuffer --version`
- If version touched: CLI version matches `pyproject.toml` and `copybuffer.core.__VERSION__`
- If logic touched: relevant `pytest` under `tests/`
