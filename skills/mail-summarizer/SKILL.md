---
name: mail-summarizer
description: >
  Summarize emails, extract action items, and draft replies. Use when someone asks
  to summarize an email, understand a mail thread, extract action items from emails,
  draft a reply, or manage email communication. Triggers on "summarize this email",
  "what does this email say", "draft a reply", "extract action items from mail".
tags: [email, summary, reply, action-items, communication]
version: "1.0"
common-skills-used: [output-formatting]
agents-tested: [claude-code]
---

# Mail Summarizer

## Purpose

Process email content to extract key information, summarize threads, identify action items, and draft contextually appropriate replies.

## When to Use

- User shares an email and wants a summary
- User has a long email thread to understand quickly
- User needs action items extracted from emails
- User wants help drafting a reply
- User asks "what does this email say" or "what do they want"

## When NOT to Use

- User wants to write a new email from scratch (that's general writing)
- User needs formal document analysis (use `document-analyzer`)

## Inputs

**Required:**
- Email content — the email text or thread

**Optional:**
- Context — user's role, relationship with sender, project context
- Reply intent — what the user wants to convey in their reply
- Tone preference — formal, casual, firm, diplomatic, etc.

## Process

### Step 1: Parse the Email

Identify:
- Sender and recipients (and their likely roles)
- Subject and core topic
- Thread order (if multiple emails)
- Tone of the communication (urgent, routine, escalation, etc.)

### Step 2: Summarize

Produce a structured summary:

```
**From:** [sender]
**Subject:** [subject]
**TL;DR:** [1-2 sentence summary of the key point]

**Key Points:**
1. [Point 1]
2. [Point 2]

**Action Items:**
- [ ] [Action] — Owner: [who] — By: [when, if stated]

**Decisions Made:**
- [Decision, if any]

**Tone/Urgency:** [assessment]
```

### Step 3: Draft Reply (if requested)

If the user wants a reply:
1. Ask for reply intent if not provided ("What do you want to say back?")
2. Match the formality level of the original email
3. Address all action items or questions from the original
4. Keep it concise — emails should be scannable
5. Offer 2 variants if the situation is nuanced (e.g., firm vs diplomatic)

### Step 4: Deliver

- For summary only: deliver the structured summary
- For reply: deliver the summary + draft reply
- Apply formatting from `common-skills/output-formatting.md`

## Output Format

Structured summary in Markdown (inline, not a separate file unless the thread is very long). Reply drafts in plain text suitable for email.

## Edge Cases

- **Very long threads:** Summarize the most recent 3-5 emails in detail, and provide a one-line summary of older context
- **Multiple action items for different people:** Group by owner
- **Ambiguous tone:** Flag it — "This could be read as [X] or [Y], depending on context"

## Common Skills Used

- `common-skills/output-formatting.md` — Consistent formatting
