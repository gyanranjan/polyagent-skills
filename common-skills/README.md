# Common Skills

Shared building blocks that individual skills reference. These are NOT standalone skills — they're conventions and patterns used across multiple skills.

## Available Common Skills

| File | Purpose | Used By |
|------|---------|---------|
| `document-tail-sections.md` | Standard sections to include at end of documents | requirement-study, implementation-sketch, document-analyzer |
| `output-formatting.md` | Consistent output formatting rules | All skills |
| `quality-checklist.md` | Universal quality gates before delivering output | All skills |

## How to Reference

In a skill's `SKILL.md`:

```markdown
## Common Skills Used
- `common-skills/output-formatting.md` — Apply before producing final output
```

In a skill's process steps:

```markdown
### Step 5: Format Output
Apply the formatting rules from `common-skills/output-formatting.md`.
```
