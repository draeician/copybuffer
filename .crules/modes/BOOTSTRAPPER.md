# Role: Bootstrapper

## When to run

Only when root `AGENTS.md` status is `[TEMPLATE]`.

If status is `[CUSTOMIZED]`, do **not** run this mode. Hand off to Manager or Coder.

## Goal

Turn a bare or partially agentic repository into a Grok-ready Skeleton Swarm
project without inventing product features.

## Checklist

1. Confirm packaging (`pyproject.toml` / `setup.py`), package path, CLI entry, version fields.
2. Write a customized root `AGENTS.md` and set status to `[CUSTOMIZED]`.
3. Add thin `GROK.md` entrypoint.
4. Create `.grok/rules/` (SOP, language style, git/version) and `.grok/agents/`
   (`swarm`, `manager`, `coder`).
5. Create `.crules/modes/{MANAGER,CODER,GIT_POLICY,BOOTSTRAPPER}.md`.
6. Create `.crules/tasks/{wip,review,done}/` with `.gitkeep` placeholders.
7. Ensure `project_spec.md` reflects the real tree (not stale aspirational text).
8. Align `.gitignore` so agent files and `project_spec.md` can be tracked;
   keep venvs and secrets ignored.
9. Smoke: `python3 -m <package> --help` / `--version` when a CLI exists.
10. Optionally run `grok inspect` to confirm rules load.

## Stop conditions

- Do not implement product roadmap items during bootstrap.
- Do not delete legacy agent trees (`.codex/`, `.cursor/`, etc.) without an explicit user request.
- Prefer regenerating multi-IDE rules via `crules` when that tool is in use.
