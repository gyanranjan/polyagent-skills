# Agent Instructions — polyagent-skills

You have access to a portable skill library. Use it to handle tasks effectively.

## Development Lifecycle Gates (MANDATORY)

**Before writing any production code, follow the gated development lifecycle.**

Read `common-skills/development-lifecycle-gates.md` for the full process. The short version:

1. **Check gate status** in `agent.todo.md` (look for the `## Gate Status` section).
2. **Start at the earliest incomplete gate** — do NOT skip ahead to coding.
3. **Gates are mandatory by default.** Only skip if the user explicitly asks (e.g., "skip to implementation", "just code it", "skip requirements").
4. If no gate status exists, **start at Gate 0 (Discovery)** for new features, or assess existing artifacts to infer the current gate.

| Gate | Name | When to Stop and Do This Gate |
|------|------|-------------------------------|
| G0 | Discovery | User has an idea but no validated problem statement |
| G1 | Requirements | Problem is clear but requirements aren't formal |
| G2 | Design | Requirements exist but no architecture/design decisions |
| G3 | POC / Spike | Design identified high-risk items needing validation |
| G4 | Implementation | Gates 0–2 passed — now write code |
| G5 | Review | Code complete — create PR, run review |
| G6 | Ship & Learn | PR merged — deploy, monitor, document |

**Trivial changes** (typo fixes, config tweaks, dependency bumps) can fast-track to Gate 4 with user confirmation.

## Operating Expectations (MANDATORY)

1. Behave as an expert collaborator: challenge weak assumptions and propose stronger alternatives.
2. Ask 2-4 high-value, decision-oriented questions at each gate transition.
3. In every substantive response, include:
   - `Stage: Gx <name>`
   - `Next: <immediate next step>`
4. Requirements/design outputs must include in-block Mermaid diagrams by default.
5. Produce shareable PDF exports for requirements/design docs by default unless user opts out.
6. Keep `agent.todo.md` workflow snapshot and gate evidence updated continuously.

## Skill Discovery

When you receive a task, check if any skill in `skills/` matches the request.
Read the matching `skills/<skill-name>/SKILL.md` and follow its instructions step by step.

Shared conventions are in `common-skills/`. Apply them when referenced by a skill.

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
- `skills/expert-research/` — Expert deep analysis and decision support for high-stakes/ambiguous topics

## Common Skills

- `common-skills/development-lifecycle-gates.md` — Gated development process (read first for any build task)
- `common-skills/design-readiness-gate.md` — Pre-coding architecture checklist
- `common-skills/agent-todo-ledger.md` — Cross-session task tracking
- `common-skills/document-tail-sections.md` — Standard document endings
- `common-skills/output-formatting.md` — Formatting conventions
- `common-skills/quality-checklist.md` — Pre-delivery quality gates
- `common-skills/mermaid-to-pdf.md` — Mermaid diagram rendering

## How to Use

1. **For build tasks:** Check gate status → start at the right gate → use the corresponding skill
2. **For non-build tasks** (email, document analysis, deck creation): Match to skill directly — gates don't apply
3. Read the full `SKILL.md` for the matched skill
4. Follow the Process steps in order
5. Apply referenced common-skills
6. Deliver in the specified Output Format

## Pre-PR Quality Gate (Required)

Before opening or merging any PR, run:

```bash
./scripts/polyagentctl.py check --strict --project .
```
