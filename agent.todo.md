# Agent TODO Ledger

Canonical cross-session task ledger for all agents working in this repository.

## Metadata

- Last Updated: 2026-03-08
- Canonical Source: this file
- Coordination Rule: single writer per artifact

## Workflow Snapshot

- Current Phase: implementation-sketch
- Next Phase: engineering-team
- Current Gate: G4 Implementation
- Next Step: Run strict check, then prepare commit + PR notes for md-to-pdf migration
- Repository: https://github.com/gyanranjan/polyagent-skills
- Default Branch Strategy: trunk (main)
- **Lifecycle Process:** `common-skills/development-lifecycle-gates.md`

## Gate Status

| Gate | Name | Status | Evidence | Skip Reason |
|------|------|--------|----------|-------------|
| G0 | Discovery | Passed | `common-skills/development-lifecycle-gates.md` | — |
| G1 | Requirements | Passed | `README.md`, `common-skills/mermaid-to-pdf.md` updated for standalone `md-to-pdf` workflow | — |
| G2 | Design | Passed | `scripts/md-to-pdf` standalone CLI design finalized (`doctor`, `install-deps`, backend fallbacks) | — |
| G3 | POC / Spike | Not Started | — | — |
| G4 | Implementation | In Progress | `scripts/md-to-pdf`, `package.json`, `scripts/polyagentctl.py`, `tests/test_polyagentctl.py` | — |
| G5 | Review | In Progress | Focused unit tests + strict check run in progress | — |
| G6 | Ship & Learn | Not Started | — | — |

Gate rules: See `common-skills/development-lifecycle-gates.md`. Gates are mandatory by default — skip requires explicit user request.

## Locks

| Artifact | Locked By | Since (UTC) | Purpose | Expected Release |
|----------|-----------|-------------|---------|------------------|
| (none) | — | — | — | — |

Lock policy:
- Acquire lock before major edits to shared artifacts.
- Do not edit a locked artifact owned by another agent.
- Add a handoff note if lock ownership changes.

## Now

- [ ] TASK-103 | Owner: codex | Artifact: md-to-pdf standalone npm packaging + docs alignment | Status: in_progress | DependsOn: -

## Next

- [ ] TASK-104 | Owner: codex | Artifact: final strict gate + PR packaging | Status: todo | DependsOn: TASK-103

## Blocked

- [ ] (none)

## Decision Needed

- [ ] (none)

## Done

- [x] TASK-099 | Owner: codex | Artifact: scripts/gate-status-check.sh | Completed: 2026-03-03 07:44 UTC
- [x] TASK-100 | Owner: codex | Artifact: scripts/install-global-all.sh + adapters/codex/AGENTS.md | Completed: 2026-03-03 07:44 UTC
- [x] TASK-101 | Owner: codex | Artifact: remove `polyagentctl export-pdf`; promote standalone `md-to-pdf` | Completed: 2026-03-08 14:20 UTC
- [x] TASK-102 | Owner: codex | Artifact: add `package.json` for npm-style standalone install | Completed: 2026-03-08 14:20 UTC

## Handoffs

| Time (UTC) | From | To | Task | Context | Next Step |
|------------|------|----|------|---------|-----------|
| 2026-03-03 07:44 | codex | codex | TASK-101 | Medium and high findings fixed; validating PDF + Mermaid rendering on Chromium | Finalize low-severity cleanup and report |

## GitHub Mapping

| Requirement ID | GitHub Issue | Status | Owner |
|----------------|--------------|--------|-------|
| REQ-001 | #123 | Open | [owner] |

## RCA Queue

| Incident/Issue | Severity | RCA Doc | Status | Owner |
|----------------|----------|---------|--------|-------|
| [link/id] | [sev] | [docs/rca/...md] | Open | [owner] |

<!-- BEGIN AUTO-SYNC -->
## Auto-Synced Traceability (Managed)

- Synced At (UTC): 2026-03-01 06:27
- Requirements Source: skills/requirement-study/references/requirement-template.md
- Spec Source: docs/specs/SPEC_TEMPLATE.md

### Requirements Snapshot

| Requirement ID | Title | GitHub Issue | Status | Owner |
|----------------|-------|--------------|--------|-------|
| REQ-001 | Requirement REQ-001 | (create issue) | Open | [owner] |

### Design Readiness Snapshot

| Checkpoint | Status | Source |
|------------|--------|--------|
| Architecture pattern | Open | docs/specs/SPEC_TEMPLATE.md |
| Language/runtime | Open | docs/specs/SPEC_TEMPLATE.md |
| Database strategy | Open | docs/specs/SPEC_TEMPLATE.md |
| Logging/observability baseline | Open | docs/specs/SPEC_TEMPLATE.md |

<!-- END AUTO-SYNC -->
