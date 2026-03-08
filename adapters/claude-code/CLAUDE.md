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

## Pre-Delivery Review Panel (MANDATORY)

**Before declaring any gate as passed or delivering a major document, automatically run three review lenses.**

Read `common-skills/pre-delivery-review-panel.md` for the full protocol. Quick summary:

1. **Expert Spot-Check** — Domain sanity: are claims evidence-backed? Any practitioner-level gotchas?
2. **Devil's Advocate Challenge** — Strongest counterargument, hidden assumptions, premature consensus
3. **Quantitative Sanity Check** — Do the numbers survive back-of-the-envelope arithmetic against base rates?

Append a `### Review Panel` section with flags from each lens and a verdict (Clear / Flags to discuss / Revise before proceeding). **Do not say "ready for next step" or present a deliverable without this panel attached.**

## Common Skills

- `common-skills/development-lifecycle-gates.md` — Gated development process (read first for any build task)
- `common-skills/pre-delivery-review-panel.md` — Automatic expert + devil's advocate + quantitative review before gate transitions
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
polyagentctl check --strict --project .
```
