# Contributing to polyagent-skills

## How to Contribute

### Adding a New Skill

1. **Write a spec first** — Create `docs/specs/<skill-name>-spec.md` using the [spec template](docs/specs/SPEC_TEMPLATE.md)
2. **Create the skill directory** — `mkdir -p skills/<skill-name>/references`
3. **Write `SKILL.md`** — Follow the [Skill Format Spec](docs/specs/skill-format-spec.md)
4. **Update adapters** — Run `./scripts/sync-adapters.sh`
5. **Test with at least 2 agents** — Verify the skill works with different agents
6. **Submit a PR** with the spec + skill + updated adapters

### Adding a New Adapter

1. **Check the [Adapter Contract Spec](docs/specs/adapter-contract-spec.md)**
2. Create `adapters/<agent-name>/` with the agent's instruction file
3. Update `scripts/install-to-project.sh` with the new agent
4. Write an [ADR](docs/adrs/ADR_TEMPLATE.md) if the agent requires special handling
5. Submit a PR

### Updating Install Flows

If your change affects installation behavior, update all relevant scripts and docs together:

1. Project installer: `scripts/install-to-project.sh`
2. Global installer: `scripts/install-global-all.sh`
3. OpenClaw global installer (if relevant): `scripts/install-openclaw-global.sh`
4. Uninstaller: `scripts/uninstall-global-all.sh`
5. Documentation references in `README.md` and `KNOWN_ISSUES.md`

### Proposing a Significant Change

1. Write an [RFC](docs/rfcs/RFC_TEMPLATE.md)
2. Open a PR with the RFC for discussion
3. Once approved, implement and reference the RFC

### Reporting Issues

Use the GitHub issue templates:
- **Bug Report** — Skill doesn't work with a specific agent
- **Skill Request** — Propose a new skill
- **Agent Support** — Request support for a new agent

## Conventions

- All skill logic lives in `skills/`, never in adapters
- Common patterns go in `common-skills/`
- Architecture decisions get an ADR
- Specs before implementation
- Test with multiple agents before merging

## Commit Messages

Follow conventional commits:
```
feat: add mail-summarizer skill
fix: correct adapter path resolution for Kiro
docs: add ADR for MCP integration decision
chore: update sync-adapters script
```
