# Known Issues

Tracking known limitations, agent quirks, and workarounds.

---

## KI-001: Kiro does not follow multi-file reference chains well

**Status:** Open
**Severity:** Medium
**Agents affected:** Kiro

**Problem:** When a `SKILL.md` references a file in `references/` which itself references `common-skills/`, Kiro sometimes loses context after the second hop.

**Workaround:** For Kiro, inline the most critical common-skill content directly in the skill's SKILL.md rather than referencing it. Use the Kiro adapter to add flattened versions of frequently used skills.

**Tracking:** Will re-test with each Kiro update.

---

## KI-002: Codex AGENTS.md size limits

**Status:** Open
**Severity:** Low
**Agents affected:** OpenAI Codex

**Problem:** Codex may truncate or deprioritize instructions if `AGENTS.md` is too long. When pointing to many skills, the adapter can grow.

**Workaround:** Keep the Codex adapter concise — list skill names only, no descriptions. Let Codex discover details by reading `SKILL.md` files on demand.

---

## KI-003: Gemini instruction file discovery is inconsistent

**Status:** Open
**Severity:** Medium
**Agents affected:** Gemini Code Assist

**Problem:** Gemini doesn't always pick up `.gemini/instructions.md` reliably across different IDE integrations.

**Workaround:** Also place a copy of the instructions at the project root as `GEMINI_INSTRUCTIONS.md` and reference it in the first prompt.

---

## KI-004: skills.sh skill format not fully portable

**Status:** Open
**Severity:** Low
**Agents affected:** All (when importing from skills.sh)

**Problem:** Skills pulled from skills.sh may contain Claude-specific syntax (tool references, slash commands, specific XML tags) that other agents don't understand.

**Workaround:** After pulling a skill via `scripts/pull-skill.sh`, manually review and strip agent-specific syntax. The script flags potential issues but cannot auto-fix all of them.

---

## KI-005: MCP server support varies across agents

**Status:** Open
**Severity:** Medium
**Agents affected:** Kiro, Codex, Gemini, Cursor

**Problem:** MCP is natively supported in Claude Code but adoption varies in other agents. Skills that depend on MCP tools may not work everywhere.

**Workaround:** For skills that need tool capabilities, provide both an MCP-based path (for agents that support it) and a fallback manual path (bash scripts, API calls) in the SKILL.md.

---

## KI-006: Adapter install overwrites existing agent config

**Status:** Open
**Severity:** High
**Agents affected:** All

**Problem:** Running `install-to-project.sh` will overwrite any existing `CLAUDE.md`, `AGENTS.md`, etc. in the target project.

**Workaround:** The script now checks for existing files and creates `.polyagent-backup/` before overwriting. Still, review the merged output. Future: support merge mode.

---

## KI-007: OpenClaw SKILL.md parser expects simplified frontmatter

**Status:** Open
**Severity:** Medium
**Agents affected:** OpenClaw

**Problem:** Some portable `SKILL.md` files use multi-line YAML frontmatter (for example `description: >`). OpenClaw skill loading expects single-line frontmatter keys and may skip or misread such skills.

**Workaround:** Use `scripts/install-global-all.sh` or `scripts/install-openclaw-global.sh` in `copy` mode. These normalize frontmatter when installing into `~/.openclaw/skills`.

**Tracking:** Re-test with each OpenClaw update to determine if normalization can be removed.

---

## KI-008: Mermaid diagrams lost or degraded when converting Markdown to PDF

**Status:** In Progress
**Severity:** High
**Agents affected:** All

**Problem:** Standard Markdown-to-PDF converters (pandoc, markdown-pdf, etc.) do not natively render Mermaid codeblocks. This causes diagrams to either appear as raw code text in the PDF, be silently dropped, or render as low-resolution blurry images. This affects any skill that produces documents with architecture diagrams, flow charts, or other Mermaid visuals.

**Workaround:** Use the two-step pipeline documented in `common-skills/mermaid-to-pdf.md`:
1. Pre-render Mermaid blocks to SVG/PNG via `mmdc` (Mermaid CLI)
2. Replace codeblocks with image references before PDF conversion

An automated script `scripts/md-to-pdf.sh` handles this pipeline. Skills that produce Mermaid diagrams should follow the PDF-safe authoring guidelines (short labels, max 15 nodes per diagram, simple node shapes) to ensure clean rendering.

**Requirements:** `npm install -g @mermaid-js/mermaid-cli` and either `pandoc + xelatex` or `wkhtmltopdf`.

**Tracking:** The `common-skills/mermaid-to-pdf.md` guide and `scripts/md-to-pdf.sh` script provide the current solution. Will monitor for native Mermaid support in pandoc or other converters.

---

## Adding a New Known Issue

Use this format:

```markdown
## KI-NNN: Short title

**Status:** Open | In Progress | Resolved
**Severity:** Low | Medium | High
**Agents affected:** <list>

**Problem:** What happens.

**Workaround:** How to deal with it now.

**Tracking:** When/how this might be resolved.
```
