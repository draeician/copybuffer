# CopyBuffer — Agents & Communication Guide

This file defines how contributors coordinate work in this repository using 
ChatGPT Codex and GitHub. It standardizes roles, status signals, and message 
formats so work is traceable and parallelizable.

---

## 1) Roles and source docs

Roles map to mode guides in `.codex/modes/`. Read your mode before starting.

* Task Master → `.codex/modes/TASKMASTER.md`
* Coder → `.codex/modes/CODER.md`
* Reviewer → `.codex/modes/REVIEWER.md`
* Auditor → `.codex/modes/AUDITOR.md`
* Blogger → `.codex/modes/BLOGGER.md`
* Brainstorm → `.codex/modes/BRAINSTORM.md`
* Swarm Manager → `.codex/modes/SWAMMANAGER.md`

Tasks live in **`.codex/tasks/`** with random hash prefixes. Each task 
includes role, deliverables, and acceptance checks.

---

## 2) Ownership model

* **Self-selection by role**: Coders pick tasks from `.codex/tasks/` that match their role and skills.
* **Tier gating**: If a tier is active, only pick tasks from that tier. The current tier is noted in `.codex/notes/ACTIVE_TIER.md` when used.
* **One agent per task at a time**: Use `[CLAIM]` to take it. If you stop or hand off, post `[UNCLAIM]`.

---

## 3) Status signals

Use these bracketed signals at the start of any update in Codex task threads, 
PRs, or issue comments.

* `[CLAIM]` I am taking this task
* `[START]` Work has begun
* `[WIP]` Progress update
* `[BLOCKED]` Waiting on something
* `[NEED-INFO]` Ask a question to proceed
* `[REVIEW-REQUEST]` Ready for review
* `[DONE]` Work is complete per acceptance checks
* `[UNCLAIM]` Releasing ownership
* `[ESCALATE]` Needs Task Master decision

Keep updates concise, action oriented, and link evidence.

---

## 4) Where to post

**In ChatGPT Codex UI**

1. Open the task.
2. Use the composer at the bottom: **“Request changes or ask a question”**.
3. Prefix your message with a status signal and submit with **Code**, not Ask.

**In GitHub**

* Use the same status signals in PR descriptions and comments.
* Reference the task file path and hash.

---

## 5) Update templates

**Claim**

```
```

**WIP**

```
```

**Blocked**

```
```

**Review request**

```
```

**Done**

```
```

---

## 6) Definition of Done

A task is done only if:

1. All acceptance checks in the task file pass.
2. Code, tests, and docs are updated together.
3. CI is green on main for the change.
4. Reviewer or Auditor clears it if required by the task.

---

## 7) Commit and PR conventions

Follow the repo guide:

* Commits: `[TYPE] Title` where TYPE is one of `feat, fix, refactor, test, docs, chore, ci, perf, security`.
* PRs mirror the format and include:

  * Linked task path `(.codex/tasks/<hash>-...)`
  * Summary of change and rationale
  * Test evidence and coverage notes
  * Risks and roll back steps

---

## 8) Escalation ladder

1. Ask in the task thread with `[NEED-INFO]`.
2. If no response, post `[ESCALATE]` tagging Task Master with the specific question.
3. If still blocked, create a Reviewer or Auditor follow up per mode guide and link it back.

---

## 9) Quick start for coders

1. Read your mode guide and the Aether spec sections relevant to your task.
2. Pick a task from `.codex/tasks/` that matches your role.
3. Post `[CLAIM]` with the task path and plan.
4. Ship small PRs tied to the task. Keep tests green.
5. Post `[REVIEW-REQUEST]` with evidence. Then `[DONE]` when accepted.
