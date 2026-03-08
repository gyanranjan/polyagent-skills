# Pre-Delivery Review Panel

Automatic multi-perspective review that runs before any gate transition or major document delivery. The panel catches blind spots, unrealistic numbers, and weak reasoning before the user sees a "ready for next step" message.

## When This Fires (Mandatory)

Run this review panel **before**:
- Declaring any gate (G0–G6) as passed
- Delivering a major document (requirements, design, MRD, implementation sketch, POC findings)
- Presenting a recommendation, strategy, or decision to the user
- Saying "ready for the next step", "here's the deliverable", or equivalent

**Exception:** Trivial changes fast-tracked to Gate 4 skip this panel.

## The Three Lenses

Apply these three lenses **in order**. Each lens is a lightweight, focused pass — not a full invocation of the corresponding skill. Think of it as wearing each hat for 30 seconds, not running a full engagement.

### Lens 1: Expert Spot-Check

Adopt the mindset of `skills/expert-research/` and `skills/subject-matter-expert/`.

- Are the core claims evidence-backed or just asserted?
- Are there domain-specific gotchas the deliverable ignores?
- Would a practitioner in this domain raise an eyebrow at anything here?

**Output a 1–3 bullet "Expert flags" list.** If nothing flags, write "No expert flags."

### Lens 2: Devil's Advocate Challenge

Adopt the mindset of `skills/devils-advocate/`.

- What is the strongest argument against the current plan or conclusion?
- What hidden assumption, if wrong, would invalidate the deliverable?
- Is there premature consensus or an uncomfortable truth being avoided?

**Output a 1–3 bullet "Challenges" list.** If nothing flags, write "No challenges."

### Lens 3: Quantitative Sanity Check

Adopt the mindset of `skills/quantitative-sanity-checker/`.

- Does the deliverable contain any numbers, estimates, projections, or implied quantities?
- If yes: do they survive a back-of-the-envelope check against known base rates?
- If the deliverable is purely qualitative: are there quantities that *should* have been estimated but weren't?

**Output a 1–3 bullet "Numbers check" list with the arithmetic shown inline.** If no quantities are relevant, write "No quantitative claims to check."

## How to Present the Panel

Append a **Review Panel** section to the deliverable or gate-transition message, formatted as:

```
---

### Review Panel

**Expert flags:**
- [flag or "No expert flags."]

**Challenges:**
- [challenge or "No challenges."]

**Numbers check:**
- [check with inline arithmetic, or "No quantitative claims to check."]

**Panel verdict:** <Clear | Flags to discuss | Revise before proceeding>
```

### Panel Verdicts

| Verdict | Meaning | Action |
|---------|---------|--------|
| **Clear** | All three lenses pass with no material flags | Proceed to next step |
| **Flags to discuss** | One or more non-blocking flags the user should be aware of | Present flags, ask if user wants to address them or proceed |
| **Revise before proceeding** | A flag is serious enough that the deliverable should be updated | Revise the deliverable, re-run the panel, then present |

## Rules

1. **Always run all three lenses.** Do not skip one because the deliverable "doesn't seem to need it."
2. **Be concise.** Each lens gets 1–3 bullets max. This is a sanity check, not a second deliverable.
3. **Self-correct before presenting.** If a lens reveals a real problem, fix the deliverable first, then show the clean version with the panel attached.
4. **Do not gate-keep trivially.** If the flags are cosmetic or speculative, verdict is Clear, not Flags to discuss.
5. **Show your math.** Quantitative flags without arithmetic are not valid flags.
