# Agent Instructions — polyagent-skills

You have access to a portable skill library in `skills/`. Shared conventions are in `common-skills/`.

## Development Lifecycle Gates

**Before writing production code, follow the gated development lifecycle.** Read `common-skills/development-lifecycle-gates.md`.

Gates: G0 Discovery → G1 Requirements → G2 Design → G3 POC/Spike (if needed) → G4 Implementation → G5 Review → G6 Ship.

Gates are mandatory by default. Check `agent.todo.md` for gate status. Start at the earliest incomplete gate. Skip only if the user explicitly asks.

## Operating Expectations (Mandatory)

1. Act as an expert partner and challenge weak assumptions.
2. Ask 2-4 value-adding, decision-oriented questions at each gate transition.
3. In every substantive response, include:
   - `Stage: Gx <name>`
   - `Next: <immediate next step>`
4. Requirements/design deliverables should include in-block Mermaid diagrams by default.
5. Generate shareable PDF exports for requirements/design docs by default unless user opts out.
6. Keep `agent.todo.md` workflow snapshot and gate evidence up to date.

## For any task:

1. For build tasks: check gate status first, start at the right gate
2. Check `skills/` for a matching skill. Read its SKILL.md and follow the instructions
3. Apply common-skills when referenced

Available skills: idea-to-mvp (Gate 0), requirement-study (Gate 1), implementation-sketch (Gate 2), poc-spike (Gate 3), mail-summarizer, document-analyzer, deck-creator, repo-bootstrap, agent-writer, desensitizer, remote-ops, expert-research, context-orchestrator, automation-architect, business-strategist, customer-advocate, devils-advocate, engineering-team, entrepreneur, growth-engineer, historian-knowledge-curator, ideator, operations-commander, product-manager, qa-validator, research-analyst, role-orchestrator, security-guardian, subject-matter-expert, systems-architect, systems-simplifier, visionary-futurist, quantitative-sanity-checker.

Key common-skills: development-lifecycle-gates, design-readiness-gate, agent-todo-ledger, quality-checklist, output-formatting.

Each skill directory contains a SKILL.md with: Purpose, When to Use, Inputs, Process steps, Output Format.

## Pre-PR Quality Gate (Required)

Before opening or merging any PR, run:

```bash
polyagentctl check --strict --project .
```
