# Agent Instructions — polyagent-skills

You have access to a portable skill library in `skills/`. Shared conventions are in `common-skills/`.

## Development Lifecycle Gates

**Before writing production code, follow the gated development lifecycle.**

Read `common-skills/development-lifecycle-gates.md`. The gates are:

- **G0 Discovery** → G1 Requirements → G2 Design → G3 POC/Spike (if needed) → **G4 Implementation** → G5 Review → G6 Ship

Gates are mandatory by default. Check `agent.todo.md` for gate status. Start at the earliest incomplete gate. Skip only if the user explicitly asks.

## When you receive a task:

1. Check `agent.todo.md` for gate status (build tasks follow gates)
2. Check `skills/` for a matching skill by reading each SKILL.md description
3. Read the full SKILL.md for the matched skill
4. Follow its Process steps in order
5. Apply referenced common-skills
6. Deliver in the specified Output Format

## Available Skills

- `skills/idea-to-mvp/` — Turn rough ideas into validated MVP plans (Gate 0)
- `skills/requirement-study/` — Analyze, write, and validate requirements (Gate 1)
- `skills/implementation-sketch/` — Create implementation plans and technical designs (Gate 2)
- `skills/poc-spike/` — Prove out risky technical assumptions (Gate 3)
- `skills/mail-summarizer/` — Summarize emails and draft replies
- `skills/document-analyzer/` — Understand and extract insights from documents
- `skills/deck-creator/` — Create presentations and slide decks
- `skills/repo-bootstrap/` — Scaffold new repositories with best practices
- `skills/agent-writer/` — Write new agent/skill definitions
- `skills/desensitizer/` — Anonymize and mask sensitive data
- `skills/remote-ops/` — Deployment, infrastructure, and operations management

## Common Skills

- `common-skills/development-lifecycle-gates.md` — Gated development process
- `common-skills/design-readiness-gate.md` — Pre-coding architecture checklist
- `common-skills/agent-todo-ledger.md` — Cross-session task tracking
- `common-skills/document-tail-sections.md` — Standard document endings
- `common-skills/output-formatting.md` — Formatting conventions
- `common-skills/quality-checklist.md` — Pre-delivery quality gates
