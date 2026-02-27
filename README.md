# polyagent-skills

**Write AI agent skills once, use everywhere — portable skill library for Claude Code, Kiro, Codex, Gemini, Cursor & more.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## The Problem

Every AI coding agent has its own way of consuming instructions — `CLAUDE.md`, `AGENTS.md`, `.kiro/specs/`, `.cursor/rules.md`. Writing skills for one means rewriting for another. That's unsustainable when you're switching agents across machines, teams, or tasks.

## The Solution

**polyagent-skills** is a spec-driven, agent-agnostic skill library. Skills are written once in portable Markdown and consumed by any agent through thin adapter files.

```
┌──────────────────────────────────────────────────┐
│  Layer 3: Adapters        (thin, per-agent)       │
│  CLAUDE.md / AGENTS.md / .kiro/ / .gemini/        │
├──────────────────────────────────────────────────┤
│  Layer 2: Skill Library   (portable, markdown)    │
│  skills/requirement-study/  skills/deck-creator/  │
├──────────────────────────────────────────────────┤
│  Layer 1: Common Foundation (shared patterns)     │
│  common-skills/  templates/  conventions          │
└──────────────────────────────────────────────────┘
```

## Supported Agents

| Agent | Adapter File | Status |
|-------|-------------|--------|
| Claude Code | `CLAUDE.md` | ✅ Supported |
| OpenAI Codex | `AGENTS.md` | ✅ Supported |
| AWS Kiro | `.kiro/specs/` | ✅ Supported |
| Google Gemini | `.gemini/instructions.md` | ✅ Supported |
| Cursor | `.cursor/rules.md` | ✅ Supported |
| Windsurf | `.windsurfrules` | 🟡 Planned |

## Quick Start

```bash
# Clone the repo
git clone https://github.com/gyanranjan/polyagent-skills.git
cd polyagent-skills

# Install skills + adapters into your project
./scripts/install-to-project.sh /path/to/my-project all

# Or install for a specific agent only
./scripts/install-to-project.sh /path/to/my-project claude-code
```

Now open your project in any supported agent — it finds its adapter and your full skill library is available.

## Available Skills

| Skill | Purpose | Status |
|-------|---------|--------|
| [requirement-study](skills/requirement-study/) | Analyze, write, and validate requirements | ✅ Active |
| [implementation-sketch](skills/implementation-sketch/) | Create implementation plans from specs | ✅ Active |
| [mail-summarizer](skills/mail-summarizer/) | Summarize and draft replies to emails | ✅ Active |
| [document-analyzer](skills/document-analyzer/) | Understand and extract insights from documents | ✅ Active |
| [deck-creator](skills/deck-creator/) | Create presentations from content | ✅ Active |
| [repo-bootstrap](skills/repo-bootstrap/) | Scaffold new repositories with best practices | ✅ Active |
| [agent-writer](skills/agent-writer/) | Write new agent definitions | ✅ Active |
| [desensitizer](skills/desensitizer/) | Data desensitization and anonymization | ✅ Active |
| [remote-ops](skills/remote-ops/) | Remote operations and infra management | ✅ Active |

## Repo Structure

```
polyagent-skills/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── KNOWN_ISSUES.md
│
├── docs/
│   ├── specs/                 # Spec-driven development
│   │   ├── SPEC_TEMPLATE.md
│   │   ├── skill-format-spec.md
│   │   └── adapter-contract-spec.md
│   ├── adrs/                  # Architecture Decision Records
│   │   ├── ADR_TEMPLATE.md
│   │   ├── 001-markdown-as-skill-format.md
│   │   ├── 002-three-layer-architecture.md
│   │   ├── 003-adapter-pattern.md
│   │   └── 004-mcp-for-tool-skills.md
│   └── rfcs/                  # Proposals for significant changes
│       └── RFC_TEMPLATE.md
│
├── common-skills/             # Shared building blocks
│   ├── README.md
│   ├── document-tail-sections.md
│   ├── output-formatting.md
│   └── quality-checklist.md
│
├── skills/                    # Portable skill library
│   ├── requirement-study/
│   ├── implementation-sketch/
│   ├── mail-summarizer/
│   ├── document-analyzer/
│   ├── deck-creator/
│   ├── repo-bootstrap/
│   ├── agent-writer/
│   ├── desensitizer/
│   └── remote-ops/
│
├── adapters/                  # Thin agent-specific wrappers
│   ├── claude-code/
│   ├── codex/
│   ├── kiro/
│   ├── gemini/
│   └── cursor/
│
├── mcp-servers/               # MCP servers for tool-based skills
│
├── scripts/                   # Automation
│   ├── install-to-project.sh
│   ├── sync-adapters.sh
│   └── pull-skill.sh
│
├── agent-notes/               # Cross-cutting agent observations
│
└── .github/
    ├── ISSUE_TEMPLATE/
    └── workflows/
```

## Design Principles

1. **Skills are knowledge, not code** — Written in Markdown, readable by any LLM
2. **Adapters are thin** — Never put skill logic in an adapter; only pointers
3. **Spec-driven** — Every skill follows the [Skill Format Spec](docs/specs/skill-format-spec.md)
4. **Decisions are recorded** — All architecture choices have an [ADR](docs/adrs/)
5. **Common patterns are shared** — DRY via `common-skills/`
6. **MCP for tools** — When skills need capabilities (not just instructions), use MCP

## Documentation

- [Skill Format Spec](docs/specs/skill-format-spec.md) — How to write a portable skill
- [Adapter Contract Spec](docs/specs/adapter-contract-spec.md) — How adapters work
- [Architecture Decision Records](docs/adrs/) — Why we made the choices we did
- [Known Issues](KNOWN_ISSUES.md) — Current limitations and workarounds
- [Contributing Guide](CONTRIBUTING.md) — How to add skills and adapters

## License

MIT — see [LICENSE](LICENSE)
