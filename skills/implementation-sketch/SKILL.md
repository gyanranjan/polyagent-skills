---
name: implementation-sketch
description: >
  Create implementation plans, technical designs, and architecture sketches from
  requirements or feature descriptions. Use when someone asks for an implementation
  plan, technical approach, system design, architecture sketch, or "how would we
  build this". Also triggers on "break this into tasks", "design this system",
  or "create a technical plan".
tags: [implementation, design, architecture, technical-plan, tasks]
version: "1.0"
common-skills-used: [document-tail-sections, output-formatting, quality-checklist]
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

### Step 1: Understand What's Being Built

Read the requirements/description thoroughly. Identify:
- Core functionality (what MUST work)
- Integration points (what connects to what)
- Data flows (what data moves where)
- User interactions (who does what)

Summarize your understanding and confirm with the user.

### Step 2: Identify Technical Decisions

List the key technical decisions that need to be made:
- Architecture style (monolith, microservices, serverless, etc.)
- Data storage (SQL, NoSQL, file-based, etc.)
- Communication patterns (sync/async, REST/gRPC/events, etc.)
- Authentication/authorization approach
- Deployment model

For each decision, provide 2-3 options with tradeoffs and a recommendation.

### Step 3: Design Components

Break the system into components/modules:

```
**Component:** [Name]
**Responsibility:** What it does (single responsibility)
**Inputs:** What it receives
**Outputs:** What it produces
**Dependencies:** Other components it needs
**Key Technical Notes:** Implementation considerations
```

### Step 4: Define Interfaces

For each component boundary, define:
- API contracts (endpoints, payloads)
- Data models (entities, relationships)
- Event contracts (if event-driven)

Keep these at sketch level — enough to align the team, not production-ready specs.

### Step 5: Identify Risks and Unknowns

Flag:
- Technical risks (things that might not work as expected)
- Complexity hotspots (parts that will take disproportionate effort)
- External dependencies (third-party services, APIs, approvals)
- Knowledge gaps (areas where the team needs to spike/research)

### Step 6: Create Task Breakdown

Break implementation into phases and tasks:

```
## Phase 1: Foundation
- [ ] Task 1.1: [Description] — Est: [time] — Depends on: [nothing]
- [ ] Task 1.2: [Description] — Est: [time] — Depends on: [1.1]

## Phase 2: Core Features
- [ ] Task 2.1: [Description] — Est: [time] — Depends on: [Phase 1]
```

### Step 7: Assemble the Sketch Document

Follow `common-skills/output-formatting.md`:

1. Title and metadata
2. Summary (what and why, 3-5 sentences)
3. Technical Decisions (with rationale)
4. Component Design (with diagram description)
5. Interface Definitions
6. Risks and Unknowns
7. Task Breakdown by Phase
8. Tail sections per `common-skills/document-tail-sections.md`

### Step 8: Quality Check

Apply `common-skills/quality-checklist.md` plus:
- [ ] Every component has a clear single responsibility
- [ ] Technical decisions include rationale, not just choices
- [ ] Task estimates are relative (S/M/L) if absolute time isn't known
- [ ] Risks have mitigation strategies or at least next steps

## Output Format

Markdown document: `implementation-sketch-<topic>.md`

## Common Skills Used

- `common-skills/document-tail-sections.md` — Standard document endings
- `common-skills/output-formatting.md` — Consistent formatting
- `common-skills/quality-checklist.md` — Pre-delivery quality gate
