---
name: document-analyzer
description: >
  Understand, analyze, and extract insights from documents — PDFs, reports, technical
  docs, contracts, or any text-heavy material. Use when someone asks to "understand
  this document", "analyze this report", "what does this document say", "extract
  key points", "summarize this PDF", or needs to quickly grasp unfamiliar material.
tags: [document, analysis, summary, extraction, understanding]
version: "1.0"
common-skills-used: [document-tail-sections, output-formatting, quality-checklist]
agents-tested: [claude-code]
---

# Document Analyzer

## Purpose

Rapidly understand and extract structured insights from any document — technical docs, reports, contracts, research papers, policies, or any text-heavy material. Produces a clear analysis that helps the user grasp the document's key content without reading it end-to-end.

## When to Use

- User uploads or shares a document and asks to understand it
- User needs key points extracted from a long document
- User asks "what does this say" about a document
- User needs to compare multiple documents
- User wants to quickly get up to speed on unfamiliar material

## When NOT to Use

- User wants to write or create a new document (that's authoring)
- The "document" is actually an email thread (use `mail-summarizer`)
- User wants requirements extracted (use `requirement-study`)

## Inputs

**Required:**
- The document(s) to analyze

**Optional:**
- Specific questions — what the user wants to know
- Context — why they're reading this, what they'll use it for
- Comparison targets — if comparing multiple documents

## Process

### Step 1: Initial Assessment

Quickly determine:
- Document type (technical spec, contract, report, research paper, policy, etc.)
- Length and structure
- Intended audience of the document
- Date and currency of the information

### Step 2: Structural Analysis

Map the document's structure:
- Major sections and their purpose
- Key arguments or themes
- Data, figures, or tables present
- References and dependencies

### Step 3: Content Extraction

Extract based on document type:

**For Technical Documents:**
- Core technology/approach described
- Key decisions and their rationale
- Dependencies and requirements
- Limitations and known issues

**For Reports/Research:**
- Main findings and conclusions
- Methodology (brief)
- Data highlights and key metrics
- Recommendations

**For Contracts/Policies:**
- Key obligations and rights
- Important dates and deadlines
- Conditions and exceptions
- Risks and liabilities

**For General Documents:**
- Main message/thesis
- Supporting arguments
- Action items or implications
- Context and background

### Step 4: Produce Analysis

Deliver as:

```
## Document Analysis: [Title]

**Type:** [document type]
**Date:** [document date]
**Pages/Length:** [size]

### TL;DR
[3-5 sentences capturing the essence]

### Key Points
1. [Most important point]
2. [Second most important]
3. [Continue as needed]

### Detailed Analysis
[Structured breakdown based on document type - see Step 3]

### Implications for You
[Based on context the user provided — what should they do with this info?]

### Questions This Raises
[Things the document doesn't answer that might matter]
```

### Step 5: Quality Check

Apply `common-skills/quality-checklist.md` plus:
- [ ] Analysis is significantly shorter than the original document
- [ ] Key points are ordered by importance, not by document order
- [ ] No opinions are stated as facts from the document

## Output Format

Markdown analysis, inline for short documents, as a file (`analysis-<doc-name>.md`) for long ones.

## Common Skills Used

- `common-skills/output-formatting.md` — Consistent formatting
- `common-skills/quality-checklist.md` — Pre-delivery quality gate
- `common-skills/document-tail-sections.md` — If producing a formal analysis document
