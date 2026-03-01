# Agent TODO Ledger

Rules for maintaining a single, user-visible, cross-session task ledger at `agent.todo.md`.

## When to Apply

Apply when work spans multiple steps, sessions, or agents, especially for:

- Requirements to implementation handoff
- Parallel work across multiple agents
- Architecture decisions requiring explicit owner/action tracking
- Incident response and RCA follow-up

## Canonical File

- Always use `agent.todo.md` at repository root.
- Treat it as the source of truth for active work tracking.
- Do not create per-agent TODO files unless explicitly requested.

## Update Rules

1. Update `Last Updated` whenever the file changes.
2. Add or update lock entries before editing shared artifacts.
3. Move tasks between `Now`, `Next`, `Blocked`, and `Done` as status changes.
4. Record explicit handoffs in the `Handoffs` table.
5. Keep task IDs stable (`TASK-###`), decision IDs stable (`DEC-###`).
6. Add requirement-to-issue mappings in `GitHub Mapping` as soon as IDs exist.
7. Add unresolved incidents to `RCA Queue` until closed.

## Recommended Task Entry Format

```
- [ ] TASK-014 | Owner: codex | Artifact: docs/specs/auth-flow.md | Status: in_progress | DependsOn: TASK-010
```

## Multi-Agent Coordination

- Single writer per artifact at a time.
- If artifact is locked by another agent, switch to review/comment mode only.
- Use `Decision Needed` for conflicts; do not overwrite silently.

## Quality Checks

- [ ] All active tasks have an owner
- [ ] No duplicate IDs
- [ ] Locks reflect current in-progress edits
- [ ] Blocked tasks include explicit unblock condition
- [ ] GitHub and RCA tables reflect current state
