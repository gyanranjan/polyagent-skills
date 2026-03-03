# Development Lifecycle Gates

Mandatory gated process that every development task follows by default. Gates ensure that discovery, requirements, and design happen **before** code is written.

**Governing ADR:** `docs/adrs/006-gated-development-lifecycle.md`

## Core Rule

**Do not start coding until Gates 0–2 are passed (or explicitly skipped by the user).**

When you receive any task that involves building something, check the gate status in `agent.todo.md`. Begin at the earliest gate that is `Not Started`. If no gate status section exists, start at Gate 0.

## The Seven Gates

### Gate 0: Discovery

**Purpose:** Validate the problem is worth solving before investing in detailed requirements.

**Entry:** User describes an idea, problem, or request.

**Activities:**
- Summarize the idea and confirm understanding with user
- Identify target audience / stakeholders
- Assess competitive landscape (even lightweight)
- Define success criteria (what does "done" look like at the product level?)

**Primary Skill:** `skills/idea-to-mvp/SKILL.md` (Steps 1–6) or manual MRD

**Exit Criteria:**
- [ ] Problem statement is written and confirmed by user
- [ ] Target audience is identified
- [ ] Competitive landscape is acknowledged (even "no known competitors")
- [ ] Success criteria are defined

**Deliverable:** MRD, idea summary document, or confirmed problem statement in `agent.todo.md`.

---

### Gate 1: Requirements

**Purpose:** Translate the validated problem into structured, traceable requirements.

**Entry:** Gate 0 passed or skipped.

**Activities:**
- Extract functional and non-functional requirements from discovery output
- Assign IDs (REQ-NNN, NFR-NNN), priorities (MoSCoW), and acceptance criteria
- Identify gaps, ambiguities, and open questions
- Produce a requirements document

**Primary Skill:** `skills/requirement-study/SKILL.md`

**Exit Criteria:**
- [ ] All Must Have requirements have IDs, priorities, and acceptance criteria
- [ ] Non-functional requirements are measurable
- [ ] Gaps and open questions are surfaced (not silently resolved)
- [ ] Stakeholder has confirmed scope

**Deliverable:** Requirements document (`requirement-study-<topic>.md`)

---

### Gate 2: Design

**Purpose:** Make architecture and technical decisions, identify risks, plan implementation.

**Entry:** Gate 1 passed or skipped.

**Activities:**
- Choose architecture style, tech stack, data model
- Design components and interfaces at sketch level
- Identify technical risks and complexity hotspots
- Run the design readiness gate checklist
- Create phased task breakdown

**Primary Skills:** `skills/implementation-sketch/SKILL.md` + `common-skills/design-readiness-gate.md`

**Exit Criteria:**
- [ ] Architecture style and rationale documented
- [ ] Tech stack chosen with tradeoffs
- [ ] Component boundaries and interfaces defined
- [ ] Design readiness gate checklist completed (all items decided or deferred with owner)
- [ ] Risk register populated with mitigations
- [ ] Task breakdown exists with dependencies

**Deliverable:** Implementation sketch (`implementation-sketch-<topic>.md`) with design readiness gate table.

---

### Gate 3: POC / Spike (Conditional)

**Purpose:** De-risk technical unknowns identified in Gate 2.

**Entry:** Gate 2 passed AND risk register contains high-risk items needing validation.

**Trigger Rule:** This gate activates only when Gate 2 identifies items marked as high-risk, technically uncertain, or "needs spike". If no such items exist, mark this gate `N/A` and proceed to Gate 4.

**Activities:**
- Build minimal, throwaway code to validate risky assumptions
- Test feasibility of critical integrations
- Benchmark performance-critical paths
- Document findings and go/no-go recommendation

**Primary Skill:** `skills/poc-spike/SKILL.md`

**Exit Criteria:**
- [ ] Each identified risk item has been investigated
- [ ] Findings report documents what was learned
- [ ] Go/no-go recommendation for each risk
- [ ] Design updated based on findings (if needed)

**Deliverable:** POC/spike findings report. Updated risk register.

---

### Gate 4: Implementation

**Purpose:** Build production-quality code based on approved design.

**Entry:** Gates 0–2 passed (Gate 3 if triggered). This gate cannot be skipped.

**Activities:**
- Write code following the implementation sketch and task breakdown
- Write tests (unit, integration as appropriate)
- Follow quality checklist
- Keep agent.todo.md updated as tasks complete

**Primary Skill:** Standard coding practices + `common-skills/quality-checklist.md`

**Exit Criteria:**
- [ ] Code is feature-complete per requirements
- [ ] Tests pass
- [ ] Quality checklist passed
- [ ] No TODO or FIXME items that block delivery

**Deliverable:** Working code with tests.

---

### Gate 5: Review

**Purpose:** Validate code quality and correctness before merge.

**Entry:** Gate 4 passed.

**Activities:**
- Create PR with description linking to requirements and design docs
- Code review (peer or self-review against checklist)
- Verify acceptance criteria from requirements
- CI pipeline passes

**Exit Criteria:**
- [ ] PR description references requirement IDs and design doc
- [ ] Code review completed
- [ ] Acceptance criteria verified
- [ ] CI green

**Deliverable:** Approved PR ready to merge.

---

### Gate 6: Ship & Learn

**Purpose:** Release, monitor, and close the feedback loop.

**Entry:** Gate 5 passed.

**Activities:**
- Merge and deploy
- Verify deployment health (monitoring, alerts)
- Write release notes / update changelog
- Update agent.todo.md (move tasks to Done)
- Retrospective: what went well, what to improve

**Primary Skill:** `skills/remote-ops/SKILL.md` (for deployment)

**Exit Criteria:**
- [ ] Code is merged and deployed (or released)
- [ ] Monitoring confirms healthy operation
- [ ] Documentation is updated
- [ ] agent.todo.md reflects completion

**Deliverable:** Release notes. Updated agent.todo.md.

---

## Skip Rules

### When the User Can Skip Gates

A user may skip gates when:
- They have pre-existing artifacts (e.g., an approved PRD skips Gates 0–1)
- The change is trivial (typo fix, config change, documentation update)
- They explicitly say: "skip to implementation", "just code it", "skip requirements", etc.

### How to Handle Skip Requests

1. **Acknowledge** the skip request.
2. **Warn** about what is being bypassed (one sentence, not a lecture).
3. **Record** the skip in the Gate Status table with the reason.
4. **Proceed** to the requested gate.

Example agent response:
> "Understood — skipping Gates 0–1 and starting at Design. Note: without formal requirements, we'll be working from implicit assumptions. I'll document the key assumptions as we go. Shall I proceed?"

### What Cannot Be Skipped

- **Gate 4 (Implementation):** This is the build phase — it is the work itself.
- **Gate 5 (Review):** For production code, review should not be skipped. For throwaway/POC code, the user may skip it.

## Entering a Project Mid-Stream

When joining an existing project:

1. Check `agent.todo.md` for the Gate Status section.
2. If it exists, resume from the current gate.
3. If it doesn't exist, assess what artifacts already exist:
   - Requirements doc exists → Gate 1 likely passed
   - Implementation sketch exists → Gate 2 likely passed
   - Code exists with tests → Gates 4+ likely passed
4. Propose the inferred gate status to the user for confirmation.

## Trivial Change Fast Path

For genuinely trivial changes (typo fixes, dependency bumps, config tweaks):

1. User indicates the change is trivial, or agent assesses it as such.
2. Agent proposes: "This looks like a trivial change — I'll skip to Implementation (Gate 4). OK?"
3. If user confirms, proceed with skip recorded.

The bar for "trivial": the change requires no new requirements, no design decisions, and no risk assessment.

## Gate Status Template for agent.todo.md

Add this section to `agent.todo.md` when starting a new feature/project:

```markdown
## Gate Status

| Gate | Name | Status | Evidence | Skip Reason |
|------|------|--------|----------|-------------|
| G0 | Discovery | Not Started | — | — |
| G1 | Requirements | Not Started | — | — |
| G2 | Design | Not Started | — | — |
| G3 | POC / Spike | Not Started | — | — |
| G4 | Implementation | Not Started | — | — |
| G5 | Review | Not Started | — | — |
| G6 | Ship & Learn | Not Started | — | — |
```

Update status as gates are completed:
- `Not Started` → `In Progress` → `Passed`
- `Skipped` (with reason in Skip Reason column)
- `N/A` (for Gate 3 when no high-risk items exist)

## Integration with Existing Skills

This gate system orchestrates existing skills — it does not replace them:

| Gate | Skill(s) Used | Common Skills Applied |
|------|--------------|----------------------|
| G0 | `idea-to-mvp` | `output-formatting`, `quality-checklist` |
| G1 | `requirement-study` | `design-readiness-gate`, `agent-todo-ledger`, `quality-checklist` |
| G2 | `implementation-sketch` | `design-readiness-gate`, `agent-todo-ledger`, `quality-checklist` |
| G3 | `poc-spike` | `agent-todo-ledger`, `quality-checklist` |
| G4 | (coding) | `quality-checklist` |
| G5 | (review) | `quality-checklist` |
| G6 | `remote-ops` | `agent-todo-ledger` |

## Quality Checks

- [ ] Gate Status section exists in `agent.todo.md` for active features
- [ ] No gate is bypassed without explicit user authorization
- [ ] Skipped gates have documented reasons
- [ ] Each passed gate has a deliverable artifact linked in the Evidence column
- [ ] Agent warns (once, concisely) before honoring a skip request
