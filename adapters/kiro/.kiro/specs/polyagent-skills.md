# Skill Library Integration — polyagent-skills

When working on tasks, check the `skills/` directory for a matching skill.
Each skill has a `SKILL.md` with step-by-step instructions to follow.
Shared conventions are in `common-skills/`.

## Development Lifecycle Gates

**Before writing production code, follow the gated development lifecycle.**

Read `common-skills/development-lifecycle-gates.md`. Gates are mandatory by default:

G0 Discovery → G1 Requirements → G2 Design → G3 POC/Spike (if needed) → G4 Implementation → G5 Review → G6 Ship

Check `agent.todo.md` for gate status. Start at the earliest incomplete gate. Skip only when the user explicitly asks.

## Operating Expectations (Mandatory)

1. Behave as an expert partner and challenge weak assumptions.
2. Ask 2-4 high-value, decision-oriented questions at each gate transition.
3. In every substantive response, include:
   - `Stage: Gx <name>`
   - `Next: <immediate next step>`
4. Requirements/design deliverables must include in-block Mermaid diagrams by default.
5. Generate shareable PDF exports for requirements/design docs by default unless user opts out.
6. Keep `agent.todo.md` workflow snapshot and gate evidence updated.

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
- `skills/product-manager/` — Product spec, feature prioritization, and outcome-driven decisions
- `skills/qa-validator/` — Test strategies, acceptance criteria, and pre-delivery validation
- `skills/research-analyst/` — Deep research, evidence synthesis, and confidence-aware findings
- `skills/role-orchestrator/` — Classify tasks, select roles, manage handoffs across multi-agent workflows
- `skills/security-guardian/` — Threat modeling, vulnerability review, and secure design validation
- `skills/subject-matter-expert/` — Parameterizable deep domain expert (e.g. SME Kubernetes, SME Finance)
- `skills/systems-architect/` — Scalable system design, architecture decisions, and trade-off analysis
- `skills/systems-simplifier/` — Identify and eliminate unnecessary complexity and over-engineering
- `skills/visionary-futurist/` — Long-horizon technology trajectories and second-order consequences
- `skills/quantitative-sanity-checker/` — Back-of-the-envelope arithmetic to sanity-check claims and forecasts

## Common Skills

- `common-skills/development-lifecycle-gates.md` — Gated development process
- `common-skills/design-readiness-gate.md` — Pre-coding architecture checklist
- `common-skills/agent-todo-ledger.md` — Cross-session task tracking
- `common-skills/document-tail-sections.md` — Standard document endings
- `common-skills/output-formatting.md` — Formatting conventions
- `common-skills/quality-checklist.md` — Pre-delivery quality gates
- `common-skills/mermaid-to-pdf.md` — Mermaid diagram rendering and PDF export

## Usage

1. For build tasks: Check gate status → start at the right gate → use the corresponding skill
2. For non-build tasks: Match to skill directly
3. Read the skill's SKILL.md fully
4. Follow the Process steps
5. Apply common-skills when referenced
6. Deliver in the specified format

## Pre-PR Quality Gate (Required)

Before opening or merging any PR, run:

```bash
polyagentctl check --strict --project .
```
