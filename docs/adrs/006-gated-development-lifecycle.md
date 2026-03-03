# ADR-006: Gated Development Lifecycle

**Status:** Accepted
**Date:** 2026-03-03
**Deciders:** repo maintainers
**Canonical TODO Ledger:** `agent.todo.md`

## Context

The polyagent-skills library has strong individual skills for each phase of development (`idea-to-mvp`, `requirement-study`, `implementation-sketch`, `design-readiness-gate`), but no orchestrating process that enforces their use in sequence. An agent receiving a build request can jump straight to coding, bypassing discovery, requirements, and design — exactly the failure mode that industry best practices (stage-gate, SAFe, INVEST, etc.) exist to prevent.

Observed problems:

- Agents start writing code before the problem is validated or understood.
- Requirements are implicit (inferred from conversation) rather than explicit and traceable.
- Architecture decisions are made ad hoc during implementation instead of upfront.
- Technical risks surface late (during coding) instead of being spiked early.
- No consistent handoff between phases; context is lost between sessions.

Industry-standard product development uses stage gates (Cooper, 1990) where each phase must produce explicit deliverables before the next phase begins. This pattern is well-proven in both waterfall and agile contexts (where gates become lightweight but still present).

## Decision

Adopt a mandatory, gated development lifecycle with seven gates (G0–G6). Gates are enforced by default: an agent must not begin a later phase until the preceding gate's exit criteria are met **or** the user explicitly requests a skip.

### The Seven Gates

| Gate | Name | Purpose | Primary Skill |
|------|------|---------|---------------|
| G0 | Discovery | Validate the problem is worth solving | `idea-to-mvp` |
| G1 | Requirements | Structured, traceable requirements | `requirement-study` |
| G2 | Design | Architecture decisions, risk identification | `implementation-sketch` + `design-readiness-gate` |
| G3 | POC / Spike | De-risk technical unknowns (conditional) | `poc-spike` (new) |
| G4 | Implementation | Build production code | Coding + `quality-checklist` |
| G5 | Review | Validate before merge | PR review + QA |
| G6 | Ship & Learn | Release, monitor, retrospect | `remote-ops` + post-ship review |

### Gate Enforcement Rules

1. **Default: gates are mandatory.** An agent receiving a task checks current gate status and begins at the earliest unfinished gate.
2. **Skip requires explicit user intent.** The user must say "skip to [phase]", "skip [gate-name]", or "just code it". The agent acknowledges the skip, warns of risks, and records it.
3. **Gate 3 (POC/Spike) is conditional.** It triggers only when Gate 2 identifies high-risk unknowns. Otherwise it is marked N/A.
4. **Gate 4 (Implementation) cannot be skipped.** It is the build phase itself.
5. **Skips are recorded.** Every skip is logged in `agent.todo.md` with the reason and who authorized it.

### Gate Status Tracking

Gate status is tracked in `agent.todo.md` in a dedicated `## Gate Status` section:

```markdown
## Gate Status

| Gate | Name | Status | Evidence | Skip Reason |
|------|------|--------|----------|-------------|
| G0 | Discovery | Passed | docs/idea-to-mvp-foo.md | — |
| G1 | Requirements | Passed | docs/requirement-study-foo.md | — |
| G2 | Design | In Progress | docs/implementation-sketch-foo.md | — |
| G3 | POC / Spike | N/A | No high-risk items identified | — |
| G4 | Implementation | Not Started | — | — |
| G5 | Review | Not Started | — | — |
| G6 | Ship & Learn | Not Started | — | — |
```

Valid statuses: `Not Started`, `In Progress`, `Passed`, `Skipped`, `N/A`.

## Consequences

### Positive

- Agents follow a repeatable, industry-standard process by default.
- Requirements and design decisions are captured before code is written.
- Technical risks are surfaced early (Gate 2) and validated (Gate 3) before committing to implementation.
- Full traceability from problem → requirements → design → code → release.
- Skip mechanism preserves flexibility for experienced users and trivial changes.
- Existing skills are reused — no reinvention, just orchestration.

### Negative

- Adds ceremony for simple tasks (mitigated by skip rules).
- Agents need to check gate status at task start (small overhead).
- Users unfamiliar with the process may be frustrated by gates (mitigated by clear explanations and easy skip).

### Neutral

- Gate 3 (POC/Spike) is conditional, keeping it lightweight when not needed.
- Gate tracking adds a new section to `agent.todo.md` but follows existing patterns.

## Alternatives Considered

### Alternative 1: Advisory-only gates (recommend but don't enforce)

Each gate would be a suggestion rather than a checkpoint. Rejected because the whole point is to prevent the "jump to code" anti-pattern — advisory gates don't change behavior.

### Alternative 2: Heavyweight stage-gate with formal sign-off documents

Full Cooper-style stage gates with formal review boards and approval signatures. Rejected as too heavyweight for AI-assisted development. The lightweight exit-criteria approach gives structure without bureaucracy.

### Alternative 3: Embed gate logic in each skill individually

Each skill would check whether prerequisites were met. Rejected because it duplicates gate logic across skills and makes the lifecycle hard to see as a whole.

## Related

- [ADR-001: Markdown as Universal Skill Format](001-markdown-as-skill-format.md)
- [ADR-002: Three-Layer Architecture](002-three-layer-architecture.md)
- [ADR-005: Workflow Orchestration and Session TODO](005-workflow-orchestration-and-session-todo.md)
- `common-skills/development-lifecycle-gates.md` — Gate definitions and enforcement rules
- `common-skills/design-readiness-gate.md` — Detailed pre-coding checklist (used in G2)
- `skills/poc-spike/SKILL.md` — New skill for Gate 3
