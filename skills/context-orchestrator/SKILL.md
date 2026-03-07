---
name: context-orchestrator
description: >
  Build and maintain a reusable context pack for ongoing projects so every session
  starts with the same grounded context. Use when someone asks to "prepare context",
  "create session context", "summarize project state for agents", or wants deterministic
  handoff quality across multiple sessions and agents.
tags: [context, orchestration, handoff, traceability, workflow]
version: "1.0.0"
common-skills-used: [agent-todo-ledger, design-readiness-gate, output-formatting, quality-checklist]
agents-tested: [claude-code, codex]
---

# Context Orchestrator

## Purpose

Create a canonical `context/pack.md` that consolidates requirements, architecture decisions, design readiness, task state, and traceability so agents can resume work reliably with minimal ambiguity.

## When to Use

- User wants context engineering for long-running work
- Multi-agent or multi-session workflows need deterministic handoffs
- Project state is fragmented across requirement/spec/ADR/todo documents
- Team wants a standard "start here" context entry point before coding

## When NOT to Use

- One-off simple tasks that do not require persistent context
- Purely creative tasks with no requirement/design traceability expectations

## Inputs

**Required:**
- At least one source artifact (`requirements.md`, `spec.md`, ADRs, or `agent.todo.md`)

**Optional:**
- GitHub repository/issues links
- RCA documents for recent incidents
- Preference for context size (`short`, `medium`, `full`)

## Process

### Step 1: Collect Source Artifacts

Identify available sources in priority order:

1. Requirements (`REQ-*`, `NFR-*`)
2. Specs/design docs
3. ADRs
4. `agent.todo.md`
5. RCA docs (if any)

If sources are missing, log explicit gaps rather than inferring silently.

### Step 2: Build `context/pack.md`

Use `references/context-pack-template.md` and include:

- Current objective and phase
- Scope, constraints, and non-goals
- Active architecture/runtime/database/logging decisions
- Design readiness status
- Current execution plan and blockers
- Traceability map (`REQ-*` -> spec -> issue/task)

### Step 3: Sync Task and Traceability State

Update `agent.todo.md` using `common-skills/agent-todo-ledger.md` and scripts where available:

- `polyagentctl sync-todo` for requirements/spec snapshots
- `polyagentctl init-issues` for REQ-to-GitHub issue bootstrap

### Step 4: Validate Context Pack Quality

Run deterministic checks:

```bash
polyagentctl verify-context-pack context/pack.md
polyagentctl design-check --allow-open docs/specs/SPEC_TEMPLATE.md
```

If validation fails, keep context pack in draft status and list exact remediation items.

### Step 5: Publish Session Start Protocol

Add a short "Session Start" snippet at top of `context/pack.md`:

1. Read `context/pack.md`
2. Read `agent.todo.md`
3. Confirm locks/ownership
4. Resume top `Now` task

## Output Format

- Primary artifact: `context/pack.md`
- Optional supporting artifact: `context/pack-smoke-test.md` with validation results

## Quality Checks

- [ ] `context/pack.md` has all required sections from template
- [ ] Includes at least one concrete `REQ-*` or explicit "missing requirements" note
- [ ] Design readiness status is visible and current
- [ ] Blockers and decisions are reflected in `agent.todo.md`
- [ ] `polyagentctl verify-context-pack context/pack.md` passes

## Common Skills Used

- `common-skills/agent-todo-ledger.md` — Keep task/lock/handoff state current
- `common-skills/design-readiness-gate.md` — Ensure pre-coding decision readiness visibility
- `common-skills/output-formatting.md` — Consistent document structure
- `common-skills/quality-checklist.md` — Final pre-delivery quality gate

## Edge Cases

- **Sparse project artifacts:** Build minimal pack and clearly list missing inputs
- **Conflicting sources:** Prefer latest accepted ADR/spec and flag conflicts under `Open Questions and Risks`
- **Overlarge context:** Produce short/medium/full variants and mark the canonical default
