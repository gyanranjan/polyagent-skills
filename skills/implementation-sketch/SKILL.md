---
name: implementation-sketch
description: >
  Create implementation plans, technical designs, and architecture sketches from
  requirements or feature descriptions. Use when someone asks for an implementation
  plan, technical approach, system design, architecture sketch, or "how would we
  build this". Also triggers on "break this into tasks", "design this system",
  or "create a technical plan".
tags: [implementation, design, architecture, technical-plan, tasks]
version: "1.0.0"
common-skills-used: [agent-todo-ledger, design-readiness-gate, document-tail-sections, output-formatting, quality-checklist]
agents-tested: [claude-code, kiro]
---

# Implementation Sketch

## Purpose

Transform requirements or feature descriptions into actionable implementation plans with technical decisions, component breakdowns, task lists, and risk identification. The output should be sufficient for a development team to start building.

## When to Use

- User has requirements and wants a technical plan
- User asks "how would we build this?"
- User wants to break a feature into development tasks
- User asks for a system design or architecture sketch
- User wants to evaluate technical approaches for a problem

## When NOT to Use

- User needs requirements first (use `requirement-study`)
- User wants actual code written (that's coding, not sketching)
- User wants a presentation of the plan (use `deck-creator` after this)

## Inputs

**Required:**
- Requirements or feature description — what needs to be built

**Optional:**
- Tech stack constraints — languages, frameworks, infrastructure
- Team context — team size, skill sets, timeline
- Existing architecture — current system to extend
- Non-functional requirements — performance, scale, security targets

## Process

### Step 1: Preflight Tooling Check

Run a non-blocking Mermaid check before generating architecture diagrams:

```bash
if command -v mmdc >/dev/null 2>&1; then
  mmdc --version
else
  echo "mmdc not installed; continue with text diagram descriptions and add TODO entry"
fi
```

If `mmdc` is missing, update `agent.todo.md` with a tooling task.

### Step 2: Understand What's Being Built

Read the requirements/description thoroughly. Identify:
- Core functionality (what MUST work)
- Integration points (what connects to what)
- Data flows (what data moves where)
- User interactions (who does what)

Summarize your understanding and confirm with the user.

### Step 3: Identify Technical Decisions

List the key technical decisions that need to be made:
- Architecture style (monolith, microservices, serverless, etc.)
- Data storage (SQL, NoSQL, file-based, etc.)
- Communication patterns (sync/async, REST/gRPC/events, etc.)
- Authentication/authorization approach
- Deployment model

For each decision, provide 2-3 options with tradeoffs and a recommendation.

### Step 4: Design Components

Break the system into components/modules:

```
**Component:** [Name]
**Responsibility:** What it does (single responsibility)
**Inputs:** What it receives
**Outputs:** What it produces
**Dependencies:** Other components it needs
**Key Technical Notes:** Implementation considerations
```

### Step 5: Define Interfaces

For each component boundary, define:
- API contracts (endpoints, payloads)
- Data models (entities, relationships)
- Event contracts (if event-driven)

Keep these at sketch level — enough to align the team, not production-ready specs.

### Step 6: Identify Risks and Unknowns

Flag:
- Technical risks (things that might not work as expected)
- Complexity hotspots (parts that will take disproportionate effort)
- External dependencies (third-party services, APIs, approvals)
- Knowledge gaps (areas where the team needs to spike/research)

### Step 7: Create Task Breakdown

Break implementation into phases and tasks:

```
## Phase 1: Foundation
- [ ] Task 1.1: [Description] — Est: [time] — Depends on: [nothing]
- [ ] Task 1.2: [Description] — Est: [time] — Depends on: [1.1]

## Phase 2: Core Features
- [ ] Task 2.1: [Description] — Est: [time] — Depends on: [Phase 1]
```

### Step 8: Assemble the Sketch Document

Follow `common-skills/output-formatting.md`:

1. Title and metadata
2. Summary (what and why, 3-5 sentences)
3. Technical Decisions (with rationale)
4. Component Design (with diagram description)
5. Interface Definitions
6. Risks and Unknowns
7. Task Breakdown by Phase
8. Tail sections per `common-skills/document-tail-sections.md`

### Step 9: Run Design Readiness Gate (No Coding Before Pass)

Apply `common-skills/design-readiness-gate.md` and explicitly finalize:

- Architecture/design pattern choice and alternatives
- Language/runtime choice and constraints
- Database choice, schema/migration approach, and data risks
- Logging/observability baseline (structured logs, metrics, tracing expectations)

If any required checkpoint remains open, mark coding tasks as blocked in `agent.todo.md`.

### Step 10: Update Cross-Session Ledger

Update `agent.todo.md` using `common-skills/agent-todo-ledger.md`:

- Add architecture/design tasks and owners
- Add locks for active design/spec artifacts
- Add handoffs when moving work between agents
- Link planned implementation tasks to requirement IDs and GitHub issue IDs where known

### Step 11: Quality Check

Apply `common-skills/quality-checklist.md` plus:
- [ ] Every component has a clear single responsibility
- [ ] Technical decisions include rationale, not just choices
- [ ] Task estimates are relative (S/M/L) if absolute time isn't known
- [ ] Risks have mitigation strategies or at least next steps

## Output Format

Markdown document: `implementation-sketch-<topic>.md`

## Quality Checks

- [ ] Each technical decision includes options, tradeoffs, and recommendation
- [ ] Component boundaries and interfaces are explicit and internally consistent
- [ ] Risks include mitigation or concrete next-step actions
- [ ] Task breakdown has dependencies and a buildable phase order
- [ ] Design readiness gate is passed or coding is explicitly blocked in `agent.todo.md`

## Common Skills Used

- `common-skills/agent-todo-ledger.md` — Multi-agent task ownership, locks, and handoffs
- `common-skills/design-readiness-gate.md` — Enforce pre-coding architecture and operational readiness
- `common-skills/document-tail-sections.md` — Standard document endings
- `common-skills/output-formatting.md` — Consistent formatting
- `common-skills/quality-checklist.md` — Pre-delivery quality gate

## Edge Cases

- **Heavy uncertainty in requirements:** Mark assumptions and split discovery spikes from build tasks
- **Hard constraints from legacy systems:** Optimize for compatibility and migration safety over ideal design
- **Extremely tight timeline:** Produce phased scope with explicit deferrals and risk acceptance
