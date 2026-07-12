# Git, versioning, and release

Follow `.crules/modes/GIT_POLICY.md` in full for commits and releases.

## Conventional commits

`feat` | `fix` | `docs` | `chore` | `refactor` — imperative subject, ≤72 chars.

## Version sources (must match)

1. `pyproject.toml` — **master** (`[project].version`)
2. `copybuffer/core.py` — `__VERSION__`
3. Git tags on release (`vX.Y.Z`)

Bump from the highest observed value (monotonic). Default: feat→minor,
fix/docs/chore/refactor→patch, breaking→major.

## Pre-commit

- Heuristic secret scan on staged files.
- No credentials or private clipboard dumps committed.
- After version edit, verify:

```bash
python3 -m copybuffer --version
```

Both metadata files and CLI output must report the same version.

## Shortcuts

User says **commit** / **branch** / **release** → Manager persona + `GIT_POLICY.md`.
