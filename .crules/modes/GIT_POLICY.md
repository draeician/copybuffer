# Git Policy

## Conventional Commits

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Allowed types

| Type | Purpose |
|------|---------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `chore` | Maintenance (deps, tooling, agent files) |
| `refactor` | Neither fix nor feature |

### Version bump rules

| Type | Default bump |
|------|----------------|
| `feat` | minor |
| `fix` / `docs` / `chore` / `refactor` | patch |
| `BREAKING CHANGE` or `type!` | major |

- Subject: imperative, lowercase start preferred, no trailing period, ≤72 chars.
- Body: explain *why*, wrap ~80 chars.
- Cross-file consistency: every bump updates `pyproject.toml` **and**
  `copybuffer/core.py` (`__VERSION__`) to the same string before commit.

### Change-type floor

If staged changes add new public modules, CLI flags, or functions that users
call, treat as at least `feat` / minor unless the user overrides.

## Branching

Prefer work on a branch — avoid drive-by commits on `main` for large changes.

| Pattern | Use |
|---------|-----|
| `feat/name` | Features |
| `fix/name` | Fixes |
| `docs/topic` | Docs |
| `chore/desc` | Tooling / agent infra |
| `refactor/desc` | Restructures |

Lowercase, hyphen-separated; short-lived; delete after merge.

## Secret prevention

Never commit:

- `.env`, `.env.*`
- `*.pem`, `*.key`, `*.p12`, `*.pfx`
- `credentials.json`, service account keys
- Hardcoded API keys, tokens, passwords
- Private clipboard dumps or personal secrets pasted into fixtures

### Pre-commit secret scan (Manager)

On staged files, check:

1. **Names**: `.env`, `.pem`, `.key`, `credentials.json`, `secret*`, `*.p12`
2. **Content regexes** (case-insensitive key assignments, PEM headers,
   `ghp_…`, `sk-…`, `AKIA…`)
3. **Outcome**: block commit on match unless user explicitly overrides a false positive

Ensure `.gitignore` covers `.env`, `venv/`, `.venv/` as needed.

## Commit shortcut workflow

1. Secret scan staged set.
2. Stage relevant agent/spec updates if they are part of the change
   (`.crules/`, `project_spec.md`, `AGENTS.md`, `.grok/`).
3. Reconcile versions to highest + apply SemVer bump when releasing a change
   that warrants it (user may request patch/minor/major).
4. Verify `python3 -m copybuffer --version`.
5. Commit with HEREDOC message; do not push unless asked.

## Release protocol

1. Verify runtime version matches metadata.
2. Summarise `feat` / `fix` commits since last tag.
3. Tag `vX.Y.Z` matching metadata.
4. Push branch/tags only with explicit user request.
5. Provide GitHub Release blurb from the summary.
