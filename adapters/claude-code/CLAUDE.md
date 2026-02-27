# Agent Instructions — polyagent-skills

You have access to a portable skill library. Use it to handle tasks effectively.

## Skill Discovery

When you receive a task, check if any skill in `skills/` matches the request.
Read the matching `skills/<skill-name>/SKILL.md` and follow its instructions step by step.

Shared conventions are in `common-skills/`. Apply them when referenced by a skill.

## Available Skills

- `skills/requirement-study/` — Analyze, write, and validate requirements
- `skills/implementation-sketch/` — Create implementation plans and technical designs
- `skills/mail-summarizer/` — Summarize emails and draft replies
- `skills/document-analyzer/` — Understand and extract insights from documents
- `skills/deck-creator/` — Create presentations and slide decks
- `skills/repo-bootstrap/` — Scaffold new repositories with best practices
- `skills/agent-writer/` — Write new agent/skill definitions
- `skills/desensitizer/` — Anonymize and mask sensitive data
- `skills/remote-ops/` — Deployment, infrastructure, and operations management

## Common Skills

- `common-skills/document-tail-sections.md` — Standard document endings
- `common-skills/output-formatting.md` — Formatting conventions
- `common-skills/quality-checklist.md` — Pre-delivery quality gates

## How to Use

1. Match the user's request to a skill by reading skill descriptions
2. Read the full `SKILL.md` for the matched skill
3. Follow the Process steps in order
4. Apply referenced common-skills
5. Deliver in the specified Output Format
