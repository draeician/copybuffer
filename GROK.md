# Grok entrypoint

`AGENTS.md` is the canonical instruction file for this repository.

Before editing code, read:

1. `AGENTS.md`
2. `project_spec.md`
3. The active task under `.crules/tasks/wip/` if one exists
4. `.crules/modes/CODER.md` or `MANAGER.md` depending on the work
5. `CHANGELOG.md` / `README.md` when changing user-facing CLI behavior

Always-on Grok project rules live in `.grok/rules/`.

Optional agent profiles (spawn or select via `/config-agents`):

| Agent | File | Use when |
|-------|------|----------|
| `swarm` | `.grok/agents/swarm.md` | Default orchestrator; pick Manager vs Coder |
| `manager` | `.grok/agents/manager.md` | Planning, tasks, commits, releases |
| `coder` | `.grok/agents/coder.md` | Implementation and tests |

Do not treat this file as a second rulebook. Shared instructions belong in
`AGENTS.md`; durable project facts belong in `project_spec.md`.
