---
name: desensitizer
description: >
  Desensitize, anonymize, and mask sensitive data in documents, code, configs, and
  datasets. Use when someone asks to "remove PII", "anonymize data", "mask sensitive
  info", "desensitize a document", or needs to prepare data for sharing, demos,
  or testing without exposing real information.
tags: [privacy, anonymization, pii, masking, data-protection]
version: "1.0.0"
common-skills-used: [quality-checklist]
agents-tested: [claude-code, kiro]
---

# Desensitizer

## Purpose

Remove or mask sensitive information from any content while preserving its structure and usefulness for the intended purpose (sharing, demos, testing, compliance).

## When to Use

- User needs to remove PII from documents or data
- User wants to create anonymized versions of real data
- User needs to prepare content for external sharing
- User asks to mask credentials, API keys, or secrets in configs/code

## When NOT to Use

- User asks for legal/privacy policy interpretation without providing masking work
- User requests irreversible deletion from live systems (this skill handles content transformation)

## Inputs

**Required:**
- Content to desensitize

**Optional:**
- What to mask (specific fields, all PII, secrets only)
- Replacement strategy (fake data, redaction, hashing, placeholders)
- Compliance context (GDPR, HIPAA, etc.)

## Process

### Step 1: Identify Sensitive Data
Scan for: names, emails, phone numbers, addresses, SSNs, credit cards, API keys, passwords, IP addresses, and domain-specific sensitive fields.

### Step 2: Choose Masking Strategy
Based on context: replace with realistic fake data (for demos), redact with [REDACTED] (for compliance), or hash (for data analysis).

### Step 3: Apply Masking
Replace all identified sensitive data consistently — same real name maps to same fake name throughout the document.

### Step 4: Verify
Review the output to ensure no sensitive data leaked through and the document remains usable.

## Output Format

Desensitized version of the input in the same format.

## Quality Checks

- [ ] All obvious direct identifiers (names, emails, phone numbers, IDs) are handled
- [ ] Secret patterns (keys/tokens/passwords) are masked consistently
- [ ] Replacement strategy preserves structure needed for downstream use
- [ ] Same source entity maps to the same replacement value throughout

## Common Skills Used

- `common-skills/quality-checklist.md` — Verify completeness of desensitization

## Edge Cases

- **Partially structured data:** Preserve delimiters/schema while masking cell values
- **High re-identification risk context:** Prefer `[REDACTED]` over realistic fake replacements
- **Binary or encoded payloads:** Flag unsupported formats and request decoded text form first
