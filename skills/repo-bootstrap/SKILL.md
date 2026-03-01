---
name: repo-bootstrap
description: >
  Scaffold new repositories with best practices, folder structure, CI/CD, linting,
  and documentation. Use when someone asks to "set up a new repo", "bootstrap a project",
  "scaffold an app", "create a new project from scratch", or needs a production-ready
  starting point for any tech stack.
tags: [repo, scaffold, bootstrap, project-setup, devops]
version: "1.0.0"
common-skills-used: [agent-todo-ledger, design-readiness-gate, output-formatting, quality-checklist]
agents-tested: [claude-code, kiro]
---

# Repo Bootstrap

## Purpose

Create well-structured, production-ready project scaffolds with appropriate tooling, CI/CD, documentation, and conventions for any tech stack.

## When to Use

- User asks to set up a new project or repository
- User wants a scaffold for a specific tech stack
- User needs best-practice project structure

## When NOT to Use

- User needs improvements to an existing repository without scaffolding from scratch
- User only wants one isolated file template and no broader project setup

## Inputs

**Required:**
- Project type — what's being built (API, web app, CLI tool, library, etc.)
- Tech stack — language/framework preferences

**Optional:**
- Team size and conventions
- CI/CD platform preference (GitHub Actions, GitLab CI, etc.)
- Deployment target (AWS, GCP, Vercel, etc.)

## Process

### Step 1: Gather Requirements
Understand the project type, stack, and any organizational conventions.

### Step 2: Design Structure
Plan the directory layout following the stack's conventions and best practices.

### Step 3: Validate Design Readiness (Before Scaffolding)
Apply `common-skills/design-readiness-gate.md` for language, database, architecture pattern, and logging/observability baseline decisions.

If key decisions are open, scaffold only requirement/spec structure and block coding scaffold tasks in `agent.todo.md`.

### Step 4: Generate Files
Create all scaffold files including: README, LICENSE, .gitignore, CI config, linting config, folder structure, and starter code.

### Step 5: Add Documentation
Include README with setup instructions, CONTRIBUTING guide, and architecture notes.

### Step 6: Validate
Run linters and build tools to ensure the scaffold is immediately usable.

## Output Format

Complete directory structure with all files. Ready to `git init` and push.

## Quality Checks

- [ ] Generated structure matches the requested language/framework conventions
- [ ] Setup commands in README are runnable on a clean machine
- [ ] CI, linting, and formatting configs are present and coherent
- [ ] No placeholder values remain in generated docs or configs
- [ ] Pre-coding design readiness decisions are recorded or unresolved items are explicitly blocked

## Common Skills Used

- `common-skills/agent-todo-ledger.md` — Keep visible task state and block unresolved scaffolding work
- `common-skills/design-readiness-gate.md` — Ensure core architecture/runtime/data/logging decisions exist before code-first bootstrap
- `common-skills/output-formatting.md` — For generated documentation
- `common-skills/quality-checklist.md` — Validate the scaffold

## Edge Cases

- **Unknown stack combination:** Default to minimal, well-documented scaffold and flag assumptions
- **Conflicting org conventions:** Prefer explicit user/org standards over generic best practices
- **Monorepo request:** Generate package/workspace boundaries first, then per-package scaffolds
