---
name: remote-ops
description: >
  Manage remote operations, infrastructure tasks, deployment procedures, and server
  administration. Use when someone asks about deployment, server management, infrastructure
  setup, CI/CD pipelines, monitoring, or any remote operations task. Triggers on
  "deploy", "server", "infrastructure", "ops", "pipeline", "monitoring".
tags: [devops, deployment, infrastructure, operations, server, ci-cd]
version: "1.0"
common-skills-used: [output-formatting, quality-checklist]
agents-tested: [claude-code]
---

# Remote Ops

## Purpose

Guide and execute remote operations tasks — deployments, infrastructure management, server administration, monitoring setup, and CI/CD pipeline configuration.

## When to Use

- User asks about deployment procedures
- User needs to set up or manage infrastructure
- User wants CI/CD pipeline configuration
- User needs monitoring or alerting setup
- User asks about server administration tasks

## Inputs

**Required:**
- Task description — what operation needs to be performed

**Optional:**
- Target environment (AWS, GCP, Azure, bare metal)
- Current infrastructure state
- Access constraints and security requirements
- Rollback requirements

## Process

### Step 1: Assess the Task
Understand what operation is needed, the target environment, and any constraints.

### Step 2: Plan the Operation
Create a step-by-step runbook with pre-checks, execution steps, validation, and rollback procedures.

### Step 3: Execute or Guide
Either execute the operation directly (if the agent has access) or provide a detailed runbook for the user to follow.

### Step 4: Validate
Verify the operation succeeded with health checks and monitoring.

### Step 5: Document
Record what was done, any issues encountered, and lessons learned.

## Output Format

Runbook in Markdown or direct execution with logged output. Filename: `runbook-<operation>.md`

## Common Skills Used

- `common-skills/output-formatting.md` — For runbooks and documentation
- `common-skills/quality-checklist.md` — Validate the operation plan
