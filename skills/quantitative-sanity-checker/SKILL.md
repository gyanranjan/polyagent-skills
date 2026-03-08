---
name: quantitative-sanity-checker
description: >
  Run back-of-the-envelope calculations to sanity-check quantitative claims,
  forecasts, or system designs. Use when someone presents numbers that "feel
  off", proposes a model with implicit base-rate assumptions, or needs a quick
  Fermi-style reality check before committing resources. Produces a short
  verdict with the arithmetic laid bare.
tags: [analysis, fermi, estimation, sanity-check, base-rate, quantitative]
version: "1.0.0"
common-skills-used: [quality-checklist]
agents-tested: [claude-code]
---

# Quantitative Sanity Checker

## Purpose

Expose unrealistic claims, forecasts, or designs by running rough-order-of-magnitude arithmetic. The skill decomposes a claim into its implied quantities, grounds each in publicly available base rates, and checks whether the numbers hold together.

## When to Use

- A claim includes specific numbers that seem too good (or too bad) to be true
- A predictive model or alert system is proposed without discussing precision, recall, or base rates
- A business plan projects revenue, users, or throughput without grounding in market size
- A system design implies resource consumption (storage, bandwidth, compute) that needs a reality check
- Someone asks "does this make sense?" about any quantitative statement

## When NOT to Use

- The user needs a rigorous statistical analysis or formal proof (suggest a specialist)
- The claim is purely qualitative with no numbers to check
- The user explicitly asks for optimistic projections or brainstorming (don't rain on a brainstorm)

## Inputs

**Required:**
- The claim, forecast, or design to sanity-check

**Optional:**
- Domain context or constraints (e.g., "this is for the US market only")
- Known base rates the user already has
- Desired confidence level or precision target

## Process

### Step 1: Extract the Claim

Restate the claim in one sentence, highlighting every explicit or implied number.
If the claim is vague, ask the user to pin down the key quantities before proceeding.

### Step 2: Identify Base Rates and Anchor Quantities

For each number in the claim, find a grounding reference:

- **Event frequency** — How often does this thing actually happen? (e.g., ~15 major earthquakes per year globally)
- **Population / market size** — What is the total pool? (e.g., 8 billion people, 330M in US, 30M small businesses)
- **Conversion / success rates** — What are typical rates in this domain? (e.g., 2-3% email click-through, ~1% SaaS free-to-paid)
- **Physical / engineering limits** — What do physics or infrastructure constrain? (e.g., speed of light latency, disk IOPS, human attention span)

State each base rate with its source or reasoning. Use well-known reference numbers (see `references/examples/common-base-rates.md` for a starter set).

### Step 3: Run the Arithmetic

Build a simple calculation chain that connects base rates to the claim. Show every step. Use this pattern:

```
Given:    <base rate or known quantity>
Derived:  <simple arithmetic> → <intermediate result>
Derived:  <simple arithmetic> → <intermediate result>
Implied:  <what the claim requires> vs <what the math gives>
```

Prefer multiplication, division, and ratios. Round aggressively — the goal is order-of-magnitude, not decimal precision.

### Step 4: Compute Key Ratios

Depending on the claim type, calculate the most revealing ratio:

- **Prediction / alert systems:** precision, recall, false-positive rate, base-rate ratio
- **Business projections:** implied market share, required conversion rate, revenue per user
- **System designs:** throughput per node, storage growth rate, cost per request
- **Timelines:** implied velocity vs historical benchmarks

### Step 5: Deliver the Verdict

Summarize using one of these categories:

| Verdict | Meaning |
|---------|---------|
| **Plausible** | Numbers are within an order of magnitude of base rates |
| **Stretch** | Requires 2-5x better than typical; possible but needs justification |
| **Implausible** | Off by an order of magnitude or more; claim needs rework |
| **Not Enough Info** | Missing a critical quantity; state what's needed |

Include one paragraph explaining the single biggest driver of the verdict.

### Step 6: Suggest Adjustments (if applicable)

If the verdict is Stretch or Implausible, suggest what would need to change to make the numbers work (e.g., "You'd need to narrow alerts to only the Pacific Ring of Fire to bring precision above 10%").

## Output Format

A short document (typically under one page) with these sections:

```
## Sanity Check: <one-line claim summary>

**Verdict: <Plausible | Stretch | Implausible | Not Enough Info>**

### Claim
<restated claim with numbers highlighted>

### Base Rates
| Quantity | Value | Source / Reasoning |
|----------|-------|--------------------|
| ...      | ...   | ...                |

### Arithmetic
<step-by-step calculation>

### Key Ratio
<the most revealing number and what it means>

### Bottom Line
<1-2 paragraph plain-language explanation>

### What Would Fix It (if applicable)
<concrete suggestions>
```

## Quality Checks

- [ ] Every number in the claim is accounted for in the arithmetic
- [ ] Base rates are sourced or reasoning is stated (no magic numbers)
- [ ] Arithmetic is shown step-by-step and is verifiable by hand
- [ ] Verdict category matches the arithmetic (not vibes)
- [ ] Suggestions are actionable, not just "try harder"

## Common Skills Used

- `common-skills/quality-checklist.md` — Final review before delivering the sanity check

## Edge Cases

- **Claim has no explicit numbers:** Ask the user to quantify before proceeding. A qualitative claim can't be sanity-checked quantitatively.
- **Multiple independent claims in one statement:** Break them into separate checks and run each independently.
- **Highly domain-specific base rates:** If you don't have a reliable base rate, say so explicitly and use a range instead of a point estimate.
- **User disagrees with your base rate:** Show your reasoning and invite them to substitute their own number — re-run the arithmetic with their value.
