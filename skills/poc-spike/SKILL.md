---
name: poc-spike
description: >
  Conduct a proof-of-concept or technical spike to de-risk unknowns identified during
  design. Use when the implementation sketch flags high-risk items, when a technology
  choice needs validation, when integration feasibility is uncertain, or when someone
  asks to "spike", "prototype", "prove out", or "validate the approach".
tags: [poc, spike, prototype, risk, validation, feasibility]
version: "1.0.0"
common-skills-used: [agent-todo-ledger, quality-checklist]
agents-tested: [claude-code]
---

# POC / Spike

## Purpose

Validate risky technical assumptions before committing to full implementation. Produce throwaway, minimal code that answers specific questions — then document the findings so the team can make informed go/no-go decisions.

A spike is NOT an implementation. It is an experiment with a findings report.

## When to Use

- Gate 2 (Design) identified high-risk or uncertain technical items
- User asks to "spike", "prototype", "prove out", or "POC" something
- A technology/integration choice needs hands-on validation before commitment
- Performance or scalability assumptions need benchmarking
- User asks "will this even work?" or "can we actually do X?"

## When NOT to Use

- Requirements are unclear (use `requirement-study` first)
- No design exists yet (use `implementation-sketch` first)
- User wants production-quality code (that's Gate 4: Implementation)
- The risk is a business/market risk, not a technical one (use `idea-to-mvp` instead)

## Inputs

**Required:**
- Risk items to investigate — specific technical questions to answer (ideally from Gate 2 risk register)

**Optional:**
- Implementation sketch — the design context for the risks
- Constraints — time box, technology restrictions, environment limits
- Success criteria — what constitutes a "validated" risk item

## Process

### Step 1: Define the Spike Scope

For each risk item, write a clear **hypothesis and exit condition**:

```
**Spike Item:** [SPIKE-NNN]
**Risk Source:** [REQ-NNN or risk register item]
**Hypothesis:** "We believe [technology/approach] can [achieve X] within [constraint Y]"
**Validation Method:** [What we'll build/test to prove or disprove]
**Exit Condition:** [Specific, measurable condition that answers the question]
**Time Box:** [Maximum time to spend — stop even if inconclusive]
```

Present the spike scope to the user:

> "Here are the spike items I plan to investigate: [list]. Each has a time box of [N]. Does this scope look right?"

**Do NOT proceed until the user confirms the scope.**

### Step 2: Set Up the Spike Environment

Create a clearly isolated spike workspace:

```bash
# Create spike directory (clearly marked as throwaway)
mkdir -p _spikes/spike-<topic>-<date>
```

**Critical rules for spike code:**
- All spike code lives under `_spikes/` — never in the main source tree
- Add a `README.md` in the spike directory explaining what's being tested
- Spike code is explicitly throwaway — do NOT refactor it, optimize it, or add tests beyond what's needed to answer the question
- Do NOT install permanent dependencies for spike purposes

### Step 3: Execute Each Spike Item

For each spike item, follow this cycle:

1. **Build the minimum code** needed to test the hypothesis
2. **Run the experiment** — execute, benchmark, integrate, or whatever the validation method requires
3. **Record raw results** — logs, timings, error messages, screenshots
4. **Assess against exit condition** — did we prove or disprove the hypothesis?

Keep each spike item focused. If you discover new questions, add them to the backlog rather than expanding the current spike.

### Step 4: Produce the Findings Report

Write a findings document:

```markdown
# Spike Findings: <Topic>

**Date:** YYYY-MM-DD
**Time Spent:** [actual time]
**Gate Source:** Gate 2 — Implementation Sketch for [feature]

## Summary

[2-3 sentences: what was investigated and the overall verdict]

## Spike Items

### SPIKE-001: [Title]

**Hypothesis:** [from Step 1]
**Result:** Validated | Invalidated | Inconclusive
**Evidence:** [what we observed — data, logs, timings]
**Recommendation:** [go/no-go/pivot with rationale]
**Impact on Design:** [what changes in the implementation sketch, if any]

### SPIKE-002: [Title]
[repeat pattern]

## Overall Recommendation

[Go / No-Go / Pivot — with rationale and conditions]

## Design Updates Required

[List specific changes needed in the implementation sketch based on findings]

## Risks Remaining

[Any risks that were NOT fully resolved — what's the plan for those?]
```

Save to `_spikes/spike-<topic>-<date>/findings.md`.

### Step 5: Feed Findings Back to Design

If findings require design changes:

1. List the specific updates needed in the implementation sketch
2. If a risk was invalidated (the approach doesn't work), propose alternatives
3. Update the risk register in the implementation sketch

Do NOT modify the implementation sketch directly during the spike — document what needs to change and let the user/team decide.

### Step 6: Update Cross-Session Ledger

Update `agent.todo.md` using `common-skills/agent-todo-ledger.md`:

- Move spike tasks to Done with findings links
- Update Gate Status: G3 → Passed
- Add any new tasks discovered during the spike
- If findings block implementation, add to Blocked section

### Step 7: Clean Up

After findings are documented and acknowledged:

- Spike code in `_spikes/` can be deleted or archived (user's choice)
- Do NOT carry spike code into production — rewrite based on findings
- Add `_spikes/` to `.gitignore` if not already there (optional — some teams want spike history in version control)

### Step 8: Quality Check

Apply `common-skills/quality-checklist.md` plus:

- [ ] Every spike item has a clear hypothesis and result
- [ ] Results include evidence (not just "it works")
- [ ] Go/no-go recommendation is explicit
- [ ] Design impact is documented (even if "no changes needed")
- [ ] Spike code is isolated in `_spikes/`, not mixed with production code
- [ ] Time box was respected (or deviation explained)

## Output Format

Two artifacts:

1. **Spike code** in `_spikes/spike-<topic>-<date>/` (throwaway)
2. **Findings report** at `_spikes/spike-<topic>-<date>/findings.md`

## Quality Checks

- [ ] Each spike item has hypothesis, result, evidence, and recommendation
- [ ] Findings report has an overall go/no-go recommendation
- [ ] Design updates are documented (not applied silently)
- [ ] Spike code is clearly isolated from production code
- [ ] agent.todo.md is updated with findings and gate status

## Common Skills Used

- `common-skills/agent-todo-ledger.md` — Cross-session task tracking and gate status
- `common-skills/quality-checklist.md` — Pre-delivery quality gate

## Edge Cases

- **Spike proves the approach is infeasible:** Document clearly and recommend alternatives. Update Gate 2 (Design) with the pivot. This is a success — finding out early is the point.
- **Spike is inconclusive within time box:** Document what was learned, what remains uncertain, and recommend either extending the spike or accepting the risk.
- **Multiple risk items with dependencies:** Order spikes so that blocking items are investigated first. If SPIKE-001 fails, reassess whether SPIKE-002 is still relevant.
- **User wants spike code in production:** Strongly recommend rewriting based on findings. Spike code is intentionally quick-and-dirty; carrying it forward accumulates tech debt.
- **No spike needed (Gate 3 is N/A):** Skip this skill entirely. Mark Gate 3 as N/A in agent.todo.md and proceed to Gate 4.
