---
name: repo-bootstrap
description: >
  Scaffold new repositories with best practices, folder structure, CI/CD, linting,
  and documentation. Use when someone asks to "set up a new repo", "bootstrap a project",
  "scaffold an app", "create a new project from scratch", or needs a production-ready
  starting point for any tech stack.
tags: [repo, scaffold, bootstrap, project-setup, devops]
version: "1.0"
common-skills-used: [output-formatting, quality-checklist]
agents-tested: [claude-code, kiro]
---

# Repo Bootstrap

## Purpose

Create well-structured, production-ready project scaffolds with appropriate tooling, CI/CD, documentation, and conventions for any tech stack.

## When to Use

- User asks to set up a new project or repository
- User wants a scaffold for a specific tech stack
- User needs best-practice project structure

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

### Step 3: Generate Files
Create all scaffold files including: README, LICENSE, .gitignore, CI config, linting config, folder structure, and starter code.

### Step 4: Add Documentation
Include README with setup instructions, CONTRIBUTING guide, and architecture notes.

### Step 5: Validate
Run linters and build tools to ensure the scaffold is immediately usable.

## Output Format

Complete directory structure with all files. Ready to `git init` and push.

## Common Skills Used

- `common-skills/output-formatting.md` — For generated documentation
- `common-skills/quality-checklist.md` — Validate the scaffold
