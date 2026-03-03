# Common Skills

Shared building blocks that individual skills reference. These are NOT standalone skills — they're conventions and patterns used across multiple skills.

## Available Common Skills

| File | Purpose | Used By |
|------|---------|---------|
| `development-lifecycle-gates.md` | **Gated development process — read first for any build task** | All build tasks (orchestrates the skills below) |
| `agent-todo-ledger.md` | Canonical cross-session TODO, locks, and handoff rules | requirement-study, implementation-sketch, poc-spike, repo-bootstrap, remote-ops |
| `design-readiness-gate.md` | Mandatory pre-coding checklist for architecture/language/DB/observability decisions | requirement-study, implementation-sketch, repo-bootstrap |
| `document-tail-sections.md` | Standard sections to include at end of documents | requirement-study, implementation-sketch, document-analyzer |
| `mermaid-to-pdf.md` | Mermaid diagram rendering and PDF conversion | idea-to-mvp, requirement-study, implementation-sketch |
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
