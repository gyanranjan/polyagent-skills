---
name: deck-creator
description: >
  Create presentations and slide decks from content, requirements, or ideas. Use when
  someone asks to "make a presentation", "create slides", "build a deck", or wants
  to present information visually. Supports pitch decks, status updates, technical
  overviews, and training materials.
tags: [presentation, slides, deck, powerpoint, pitch]
version: "1.0"
common-skills-used: [output-formatting]
agents-tested: [claude-code, kiro]
---

# Deck Creator

## Purpose

Transform content into well-structured presentation decks. Handles slide planning, content organization, visual hierarchy suggestions, and speaker notes.

## When to Use

- User asks to create a presentation, deck, or slides
- User has content and wants it formatted for presentation
- User needs a pitch deck, status update deck, or training materials

## When NOT to Use

- User wants a written report (that's document authoring)
- User wants to analyze an existing presentation (use `document-analyzer`)

## Inputs

**Required:**
- Content or topic — what the presentation is about

**Optional:**
- Audience — who will see this
- Slide count target — how many slides
- Style/tone — formal, casual, data-heavy, visual
- Template preference — if the user's org has a standard

## Process

### Step 1: Understand the Presentation Goal
Identify the audience, key message, and desired outcome (inform, persuade, train, update).

### Step 2: Create Slide Outline
Plan the deck structure with a title and purpose for each slide. Follow the rule: one idea per slide.

### Step 3: Write Slide Content
For each slide, produce:
- Title (< 8 words)
- Body content (bullets, key phrases — NOT paragraphs)
- Speaker notes (what to say, in full sentences)
- Visual suggestions (charts, diagrams, images to include)

### Step 4: Review Flow
Check that the deck tells a coherent story from start to finish. Ensure transitions between slides are logical.

### Step 5: Deliver
Output as structured Markdown or generate a `.pptx` file if the agent supports it. Apply `common-skills/output-formatting.md`.

## Output Format

Markdown slide outline or `.pptx` file. Filename: `deck-<topic>.md` or `deck-<topic>.pptx`

## Common Skills Used

- `common-skills/output-formatting.md` — Consistent formatting
