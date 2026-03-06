# Agent Instructions — polyagent-skills

You have access to a portable skill library in `skills/`. Shared conventions are in `common-skills/`.

## Development Lifecycle Gates

**Before writing production code, follow the gated development lifecycle.**

Read `common-skills/development-lifecycle-gates.md`. The gates are:

- **G0 Discovery** → G1 Requirements → G2 Design → G3 POC/Spike (if needed) → **G4 Implementation** → G5 Review → G6 Ship

Gates are mandatory by default. Check `agent.todo.md` for gate status. Start at the earliest incomplete gate. Skip only if the user explicitly asks.

## Operating Expectations (Mandatory)

1. Act as an expert partner: challenge weak assumptions and suggest stronger options.
2. Ask 2-4 high-value, decision-oriented questions at each gate transition.
3. In every substantive response, include:
   - `Stage: Gx <name>`
   - `Next: <immediate next step>`
4. For requirements/design deliverables, include in-block Mermaid diagrams by default.
5. Generate a shareable PDF for requirements/design docs by default unless the user opts out.
6. Keep `agent.todo.md` workflow snapshot and gate evidence updated as work progresses.

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
- `skills/expert-research/` — Expert deep analysis and decision support for high-stakes/ambiguous topics
- `skills/context-orchestrator/` — Build reusable project context packs and session handoffs
- `skills/automation-architect/` — Design automation pipelines, CI/CD systems, and workflow automation
- `skills/business-strategist/` — Market positioning, business model design, and competitive strategy
- `skills/customer-advocate/` — Deep user empathy and voice-of-customer for product decisions
- `skills/devils-advocate/` — Stress-test decisions and plans by arguing the opposing case
- `skills/engineering-team/` — Translate specs into engineering tasks, plans, and code scaffolds
- `skills/entrepreneur/` — Opportunity-first thinking, value propositions, and business outcomes
- `skills/growth-engineer/` — Acquisition, activation, retention, and referral growth systems
- `skills/historian-knowledge-curator/` — Organizational memory, decisions, and learnings capture
- `skills/ideator/` — Divergent idea generation and creative lateral thinking
- `skills/operations-commander/` — Production readiness, deployment, runbooks, and incident response
- `skills/poc-spike/` — Proof-of-concept spikes to de-risk technical unknowns
- `skills/product-manager/` — Product spec, feature prioritization, and outcome-driven decisions
- `skills/qa-validator/` — Test strategies, acceptance criteria, and pre-delivery validation
- `skills/research-analyst/` — Deep research, evidence synthesis, and confidence-aware findings
- `skills/role-orchestrator/` — Classify tasks, select roles, manage handoffs across multi-agent workflows
- `skills/security-guardian/` — Threat modeling, vulnerability review, and secure design validation
- `skills/subject-matter-expert/` — Parameterizable deep domain expert (e.g. SME Kubernetes, SME Finance)
- `skills/systems-architect/` — Scalable system design, architecture decisions, and trade-off analysis
- `skills/systems-simplifier/` — Identify and eliminate unnecessary complexity and over-engineering
- `skills/visionary-futurist/` — Long-horizon technology trajectories and second-order consequences

## Common Skills

- `common-skills/development-lifecycle-gates.md` — Gated development process
- `common-skills/design-readiness-gate.md` — Pre-coding architecture checklist
- `common-skills/agent-todo-ledger.md` — Cross-session task tracking
- `common-skills/document-tail-sections.md` — Standard document endings
- `common-skills/output-formatting.md` — Formatting conventions
- `common-skills/quality-checklist.md` — Pre-delivery quality gates
- `common-skills/mermaid-to-pdf.md` — Mermaid diagram rendering and PDF export

## Pre-PR Quality Gate (Required)

Before opening or merging any PR, run:

```bash
./scripts/polyagentctl.py check --strict --project .
```
