---
name: expert-research
description: >
  Expert-mode deep analysis for ambiguous or high-stakes topics. Use when the task
  needs rigorous evidence, tradeoff analysis, and recommendation confidence. The
  workflow either performs deep research with available sources/tools or asks the
  user for targeted inputs needed to complete a high-quality analysis.
tags: [expert, deep-research, analysis, strategy, decision-support]
version: "1.0.0"
common-skills-used: [output-formatting, quality-checklist]
agents-tested: [codex, claude-code, kiro]
---

# Expert Research

## Purpose

Act as a domain expert, not a passive summarizer. Build a defensible recommendation by collecting high-quality evidence, testing assumptions, and presenting clear tradeoffs with confidence levels.

## When to Use

- User asks for expert opinion, deep analysis, or strategic recommendation
- Topic is high-impact, ambiguous, or likely to have hidden risks
- Decision quality depends on external facts, benchmarks, or competing options
- User asks for "deep research", "best approach", "what should we do", or similar

## When NOT to Use

- User only wants a quick draft/summary (use a domain-specific lightweight skill)
- Task is purely mechanical with no meaningful decision/tradeoff

## Inputs

**Required:**
- Decision goal — what decision/action this analysis should support

**Optional (but strongly recommended):**
- Scope boundaries — what to include/exclude
- Constraints — timeline, budget, regulatory, technical
- Success criteria — what "good" looks like
- Existing hypotheses/options

## Process

### Step 1: Frame the Decision

Define:
- Decision question
- Decision deadline/urgency
- Constraints and evaluation criteria

If these are incomplete, ask 3-5 focused questions before continuing.

### Step 2: Build an Evidence Plan

List:
- Key unknowns to resolve
- Sources needed (docs, standards, benchmarks, user data, expert input)
- Validation method for each unknown

### Step 3: Deep Research or Input Collection

- If research tools/sources are available: collect and synthesize evidence
- If unavailable or restricted: ask user for targeted inputs (documents, links, data, assumptions)
- Explicitly mark each claim as:
  - Evidence-backed
  - Inference
  - Open question

### Step 4: Challenge Assumptions

For each major assumption:
- Why it may fail
- What would invalidate it
- Mitigation or contingency plan

### Step 5: Compare Options with Tradeoffs

Build a concise options table:
- Option
- Benefits
- Risks
- Cost/effort
- Time-to-value
- Recommendation fit

### Step 6: Recommendation with Confidence

Provide:
- Recommended option and why
- Confidence level (`High`/`Medium`/`Low`)
- Preconditions required for success
- Top 3 execution risks + mitigations

### Step 7: Actionable Next Steps

Produce a sequenced action plan:
1. Immediate next step (today)
2. Short-term validation tasks
3. Decision checkpoints

## Output Format

Markdown with these sections:
1. Decision Framing
2. Evidence Summary
3. Assumptions and Stress Tests
4. Options and Tradeoffs
5. Recommendation and Confidence
6. Open Questions
7. Next Actions

## Quality Checks

- [ ] Recommendation is explicitly tied to evidence
- [ ] Major assumptions are challenged and documented
- [ ] Tradeoffs are concrete (not generic)
- [ ] Confidence level and uncertainty are clearly stated
- [ ] Next steps are executable and ordered

## Edge Cases

- **No research tools available:** ask for specific source inputs and provide an "evidence gap" list
- **Conflicting evidence:** present both interpretations and decision impact
- **High uncertainty + urgent decision:** give a reversible first step and time-boxed validation plan
