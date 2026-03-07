---
name: venture-architect
description: >
  Autonomous end-to-end venture pipeline that transforms a raw idea into a complete
  set of venture artifacts in a single execution loop. Triggers when the user says
  "this is an idea", "I have a venture idea", "here's a concept", "turn this into
  a venture", or presents any raw startup/product idea for full-stack analysis.
  Executes six sequential roles — Research Analyst, Entrepreneur, Product Manager,
  Systems Architect, Engineering Planner, Deck Creator — producing Feasibility Report,
  BRD, PRD, SRS, Implementation Sketch, and Pitch Deck. No user nudging required;
  the workflow runs CONCEPT to PITCH autonomously.
tags: [venture, idea, startup, pitch, feasibility, brd, prd, srs, architecture, end-to-end]
version: "1.0.0"
common-skills-used: [agent-todo-ledger, design-readiness-gate, document-tail-sections, output-formatting, quality-checklist, mermaid-to-pdf]
agents-tested: [claude-code]
---

# Venture Architect

## Purpose

Transform a raw idea into a complete, production-grade set of venture artifacts in one autonomous execution loop. The skill chains six specialist roles — Research Analyst, Entrepreneur, Product Manager, Systems Architect, Engineering Planner, and Deck Creator — each producing a dedicated document. The final output is a fully scaffolded project directory ready for implementation handoff.

## When to Use

- User says "this is an idea", "I have an idea", "here's a concept"
- User says "turn this into a venture" or "take this from concept to pitch"
- User presents a raw startup, product, or business idea and expects full analysis
- User asks for a complete venture package (feasibility through pitch deck)
- User wants to go from zero to a structured, investor-ready artifact set

## When NOT to Use

- User already has formal requirements and only needs implementation (use `implementation-sketch`)
- User only wants a pitch deck from existing content (use `deck-creator`)
- User only wants competitive research (use `research-analyst` directly)
- User wants to iteratively refine an MVP with interactive Q&A (use `idea-to-mvp`)
- User wants to write code immediately (that's coding, not venture design)

## Inputs

**Required:**
- Raw idea — any amount of text describing a concept, product, or venture

**Optional:**
- Project name — if not provided, the agent will derive one from the idea
- Target market or industry context
- Known technical constraints or preferences
- Budget or timeline context
- Existing competitors the user is already aware of

## Process

### No-Nudge Policy

Do NOT ask the user for permission before creating documents. Instead, announce what you are doing:

- "I am now generating the Feasibility Report based on the identified technical risks."
- "Moving to the Entrepreneur role — generating the Business Requirement Document."
- "The SRS is complete. Proceeding to the Engineering Planner role."

Only ask the user when:
- Private business information is required and cannot be inferred
- Domain clarification is impossible without input
- The project scope is fundamentally ambiguous

### Step 1: Capture the Idea and Scaffold the Project

Read the user's raw idea. Derive a project name using `kebab-case` (e.g., `drone-delivery`, `ai-tutor`, `supply-chain-optimizer`). If the user provided a name, use it.

Create the project directory structure:

```
projects/<project-name>/
├── docs/
│   ├── Feasibility_Report.md
│   ├── BRD.md
│   ├── PRD.md
│   ├── SRS.md
│   ├── Implementation_Sketch.md
│   └── Pitch_Deck.md
├── research/
│   ├── research_notes.md
│   └── spike_proposals.md
├── architecture/
│   └── diagrams.md
└── src/
    └── README.md
```

Announce: "Project directory scaffolded at `projects/<project-name>/`. Beginning the venture pipeline."

### Step 2: Role 1 — Research Analyst (Feasibility Report)

Adopt the Research Analyst persona. Investigate the idea's feasibility across four dimensions:

1. **Technical Constraints** — Can this be built? What are the hardest technical problems?
2. **Regulatory Concerns** — Are there legal, compliance, or licensing barriers?
3. **Operational Risks** — What could go wrong in day-to-day execution?
4. **Economic Viability** — Is the unit economics story plausible?

Identify the **top 3 technical or operational showstoppers**.

Produce `docs/Feasibility_Report.md` using the template at `references/feasibility-report-template.md`. The report must include:

- Evidence-based analysis with FACT / INTERPRETATION / ASSUMPTION / UNRESOLVED tags
- Explicit assumptions and unknowns
- A **Technical Spike Proposal** — a concrete experiment that validates the highest-risk assumption

Also create an entry in `research/spike_proposals.md` with the spike experiment details:

```
## SPIKE-001: <Title>
**Hypothesis:** <what we believe>
**Validation Method:** <what to build/test>
**Exit Condition:** <measurable success/failure>
**Time Box:** <hours/days>
**Risk Level:** HIGH | MEDIUM | LOW
```

Write research notes to `research/research_notes.md`.

Announce: "Feasibility Report complete. Top risks identified. Moving to the Entrepreneur role."

### Step 3: Role 2 — Entrepreneur (Business Requirement Document)

Adopt the Entrepreneur persona. Using the feasibility findings, generate a Business Requirement Document focused on:

- **Market Wedge** — What specific gap does this fill? What is the beachhead market?
- **Problem Severity** — How painful is this problem? What is the cost of inaction?
- **Target Customer** — Who specifically buys this? What is their profile?
- **Supply Chain Resilience** — What dependencies exist? How fragile is the delivery model?
- **Distribution Model** — How does this reach customers? What channels?
- **Unfair Advantage** — What structural moat exists or can be built?

Include:
- Business model options with trade-off analysis
- Directional unit economics (CAC, LTV, gross margin, payback period)
- Go-to-market sequence (which segment first, why)
- Riskiest commercial assumptions and how to test them

Produce `docs/BRD.md` using the template at `references/brd-template.md`.

Announce: "BRD complete. Market wedge and business model defined. Moving to Product Manager role."

### Step 4: Role 3 — Product Manager (Product Requirement Document)

Adopt the Product Manager persona. Generate a PRD that clearly separates two phases:

**30-Day POC (Proof of Concept):**
- Directly tied to the Technical Spike from the Feasibility Report
- Validates the highest-risk assumption with minimum effort
- Has explicit success/failure criteria

**90-Day MVP:**
- Must Have features (launch-blocking)
- Should Have features (fast-follow)
- Won't Have features (explicitly deferred with rationale)

The PRD must include:
- **Personas** — 2-3 detailed user personas with goals, frustrations, and context
- **User Stories** — In "As a [persona], I want [action] so that [benefit]" format with acceptance criteria
- **Success Metrics** — Quantitative KPIs for POC and MVP phases
- **Feature Prioritization** — MoSCoW with rationale for each item
- Functional requirements in REQ-NNN format with acceptance criteria

Produce `docs/PRD.md` using the template at `references/prd-template.md`.

Announce: "PRD complete. POC and MVP scoped. Moving to Systems Architect role."

### Step 5: Role 4 — Systems Architect (Software Requirement Specification)

Adopt the Systems Architect persona. Generate an SRS that includes:

- **System Architecture** — Component-level design with responsibilities and boundaries
- **Major Components** — Each with responsibility, inputs, outputs, dependencies
- **Interfaces** — API contracts, data models, event schemas (sketch level)
- **Deployment Topology** — Where components run, how they scale
- **Data Flow** — How data moves through the system for key operations
- **Scalability Assumptions** — Current targets and 10x growth considerations
- **Technology Choices** — With alternatives considered and rationale

**Visual-First Architecture (Mandatory):** Include at least one Mermaid diagram. Choose the most appropriate types from:

- Component diagram (C4 or flowchart style)
- Sequence diagram (key user flows)
- State machine (lifecycle of key entities)
- Data flow diagram

Follow `common-skills/mermaid-to-pdf.md` guidelines:
- Max 15 nodes per diagram
- Labels under 40 characters
- Use `TD` or `LR` layout consistently
- Prefer `flowchart`, `sequenceDiagram`, `mindmap`, `C4Context` types

Also write the architecture diagrams to `architecture/diagrams.md`.

Produce `docs/SRS.md` using the template at `references/srs-template.md`.

Announce: "SRS complete with architecture diagrams. Moving to Engineering Planner role."

### Step 6: Role 5 — Engineering Planner (Implementation Sketch)

Adopt the Engineering Planner persona. Generate a concrete implementation sketch:

- **Repository Structure** — Recommended directory layout with rationale
- **Module Breakdown** — Each module with purpose, dependencies, and estimated complexity (S/M/L)
- **Development Phases** — Ordered phases with dependencies and deliverables
  - Phase 0: Spike experiments (from Feasibility Report)
  - Phase 1: Foundation (infrastructure, auth, data layer)
  - Phase 2: Core MVP features
  - Phase 3: Integration and testing
  - Phase 4: Deployment and monitoring
- **CI/CD Outline** — Pipeline stages, testing strategy, deployment approach
- **Spike Experiments** — Concrete experiment descriptions linked to SPIKE-NNN IDs from the Feasibility Report

Produce `docs/Implementation_Sketch.md` using the template at `references/implementation-sketch-template.md`.

Announce: "Implementation Sketch complete. Moving to final role: Deck Creator."

### Step 7: Role 6 — Deck Creator (Pitch Deck)

Adopt the Deck Creator persona. Generate a concise 5-slide executive pitch deck:

| Slide | Content |
|-------|---------|
| 1. Problem | The pain point, who feels it, cost of inaction |
| 2. Solution | What you're building, how it solves the problem |
| 3. Market Opportunity | TAM/SAM/SOM, beachhead market, growth trajectory |
| 4. Architecture Advantage | Technical moat, key architectural decisions, scalability story |
| 5. Roadmap | POC → MVP → Growth timeline with milestones |

Each slide must include:
- **Title** (under 8 words)
- **Body** (scannable bullets, NOT paragraphs)
- **Speaker Notes** (what to say, in full sentences)
- **Visual Suggestion** (what chart, diagram, or image to include)

Produce `docs/Pitch_Deck.md` using the template at `references/pitch-deck-template.md`.

Announce: "Pitch Deck complete. Venture pipeline finished."

### Step 8: Write src/README.md

Write a brief `src/README.md` that includes:
- Project name and one-line description
- Link to each document in `docs/`
- Quick-start instructions placeholder
- Technology stack summary from the SRS

### Step 9: Quality Check

Apply `common-skills/quality-checklist.md` plus these skill-specific checks:

- [ ] All 6 documents exist in `docs/`
- [ ] Feasibility Report contains evidence-tagged analysis (FACT/INTERPRETATION/ASSUMPTION/UNRESOLVED)
- [ ] At least one spike proposal exists in `research/spike_proposals.md`
- [ ] BRD includes market wedge, unit economics, and unfair advantage
- [ ] PRD separates 30-day POC from 90-day MVP with explicit success metrics
- [ ] PRD contains personas, user stories with acceptance criteria, and REQ-NNN IDs
- [ ] SRS contains at least one Mermaid diagram following PDF-safe guidelines
- [ ] Architecture diagrams exist in `architecture/diagrams.md`
- [ ] Implementation Sketch includes repo structure, phases, and CI/CD outline
- [ ] Pitch Deck has exactly 5 slides with speaker notes
- [ ] No placeholder text remains in any document
- [ ] All documents follow `common-skills/output-formatting.md`
- [ ] Tail sections applied per `common-skills/document-tail-sections.md`

### Step 10: Final Summary

After all documents are generated, present:

1. **Directory tree** — show the full project structure
2. **Document summary** — one-line summary of each generated document
3. **Technical risks** — top 3 risks from the Feasibility Report
4. **Recommended next steps** — what to do first (usually: run the spike experiment)

## Output Format

A project directory `projects/<project-name>/` containing:

```
projects/<project-name>/
├── docs/
│   ├── Feasibility_Report.md
│   ├── BRD.md
│   ├── PRD.md
│   ├── SRS.md
│   ├── Implementation_Sketch.md
│   └── Pitch_Deck.md
├── research/
│   ├── research_notes.md
│   └── spike_proposals.md
├── architecture/
│   └── diagrams.md
└── src/
    └── README.md
```

## Quality Checks

- [ ] All 6 role-specific documents are present and complete
- [ ] Feasibility Report uses evidence hierarchy tags
- [ ] Spike proposals are concrete and testable
- [ ] BRD covers market wedge, distribution, and unfair advantage
- [ ] PRD clearly separates POC (30-day) from MVP (90-day)
- [ ] SRS contains at least one Mermaid diagram
- [ ] Implementation Sketch has phased task breakdown with dependencies
- [ ] Pitch Deck has 5 slides with speaker notes
- [ ] No-nudge policy was followed (no unnecessary user prompts)
- [ ] All documents use consistent terminology and cross-reference each other

## Common Skills Used

- `common-skills/agent-todo-ledger.md` — Cross-session task tracking
- `common-skills/design-readiness-gate.md` — Pre-coding architecture decision gate
- `common-skills/document-tail-sections.md` — Standard document endings
- `common-skills/output-formatting.md` — Consistent formatting
- `common-skills/quality-checklist.md` — Pre-delivery quality gate
- `common-skills/mermaid-to-pdf.md` — Reliable mermaid diagram rendering for PDF export

## Edge Cases

- **Extremely vague idea** ("make something cool"): Expand Step 1 into a brief discovery — ask about the user's domain, interests, and audience before proceeding. This is the one case where asking is acceptable.
- **Regulated domain** (healthcare, fintech, defense): Elevate regulatory concerns to showstopper status in the Feasibility Report. Add a compliance section to the BRD and PRD.
- **Hardware or physical product idea**: Adapt the SRS to include hardware/firmware components. Note supply chain and manufacturing risks in the Feasibility Report.
- **Idea overlaps with an existing project**: Check `projects/` for existing directories. If found, confirm with the user whether to extend or create new.
- **User provides partial artifacts**: Identify which roles have existing output and skip to the first missing role in the chain.
- **Solo founder context**: Adjust Implementation Sketch for single-developer phasing. Recommend managed services and low-ops solutions in the SRS.
- **No web search available**: Note "research limited to domain knowledge" in Feasibility Report. Flag external validation as a next step.
