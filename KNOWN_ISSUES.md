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

**Workaround:** After pulling a skill via `polyagentctl pull-skill`, manually review and strip agent-specific syntax. The command flags potential issues but cannot auto-fix all of them.

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

**Problem:** Running `polyagentctl install-project` will overwrite any existing `CLAUDE.md`, `AGENTS.md`, etc. in the target project.

**Workaround:** The command checks for existing files and creates `.polyagent-backup/` before overwriting. Still, review the merged output. Future: support merge mode.

---

## KI-007: OpenClaw SKILL.md parser expects simplified frontmatter

**Status:** Open
**Severity:** Medium
**Agents affected:** OpenClaw

**Problem:** Some portable `SKILL.md` files use multi-line YAML frontmatter (for example `description: >`). OpenClaw skill loading expects single-line frontmatter keys and may skip or misread such skills.

**Workaround:** Use `polyagentctl install-global copy`. This normalizes frontmatter when installing into `~/.openclaw/skills`.

**Tracking:** Re-test with each OpenClaw update to determine if normalization can be removed.

---

## KI-008: Mermaid diagrams lost or degraded when converting Markdown to PDF

**Status:** Resolved
**Severity:** High
**Agents affected:** All

**Problem:** Standard Markdown-to-PDF converters (pandoc, markdown-pdf, etc.) do not natively render Mermaid codeblocks. This causes diagrams to either appear as raw code text in the PDF, be silently dropped, or render as low-resolution blurry images.

**Solution:** `md-to-pdf` auto-selects the best available render path:

- **Markdown render:** via `markdown-it`.
- **Mermaid:** code blocks converted to static `mermaid.ink` image URLs for deterministic exports.
- **PDF:** tries Puppeteer, then Chromium/Chrome CLI, then wkhtmltopdf.
- **Fallback:** HTML output when no PDF backend succeeds. Use `--html` to force this path.

**Requirements:** `markdown-it` is required. For PDF output use at least one backend: Puppeteer, Chromium/Chrome, or `wkhtmltopdf`. Check with `md-to-pdf doctor`.

**Tracking:** See `common-skills/mermaid-to-pdf.md` for full docs.

---

## KI-009: Gemini CLI has a separate native skill registry — instructions.md alone is not enough

**Status:** Resolved
**Severity:** High
**Agents affected:** Gemini CLI (`gemini` command-line tool)

**Problem:** The Gemini CLI (`@google/gemini-cli`) has two distinct configuration layers:

1. `~/.gemini/instructions.md` — system prompt / global instructions (read automatically)
2. A **native skill registry** — populated via `gemini skills link` or `gemini skills install`

Writing skills into `instructions.md` alone causes Gemini CLI to report:

> "I do not currently have a skill named idea-to-mvp in my local library; only skill-creator is available."

Gemini CLI checks its native registry for named skills. If a skill isn't registered there, it falls back to its built-in `skill-creator`. It does NOT discover skills by browsing the filesystem path listed in `instructions.md`.

**Root cause:** The `install-global` command was only writing `~/.gemini/instructions.md` and not registering skills with the native Gemini CLI skill registry.

**Solution:** `polyagentctl install-global` now automatically runs `gemini skills link --consent` for every skill directory after writing config files, if `gemini` is found in PATH. This registers all polyagent skills into the Gemini CLI native registry so they appear as Active Skills.

To manually re-register if needed:

```bash
polyagentctl install-global link   # re-runs everything including skill registration
```

Or register a single skill manually:

```bash
gemini skills link ~/.polyagent-skills/skills/idea-to-mvp --consent
```

Verify registration:

```bash
gemini skills list
```

**Note:** `~/.gemini/instructions.md` (the system prompt) is still written and still provides context. The native registry is an *additional* requirement for Gemini CLI to recognize named skills.

**Tracking:** Re-verify with each `@google/gemini-cli` major release — the registry mechanism or file paths may change.

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
