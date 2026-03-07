# Implementation Sketch: <Project Name>

**Date:** YYYY-MM-DD
**Version:** 1.0
**Status:** Draft
**Role:** Engineering Planner

---

## Executive Summary

<2-3 sentence overview of the implementation approach>

---

## Repository Structure

```
<project-name>/
├── src/
│   ├── <module-1>/
│   ├── <module-2>/
│   └── <module-3>/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
├── scripts/
├── config/
├── .github/
│   └── workflows/
├── README.md
├── package.json / pyproject.toml / go.mod
└── Dockerfile
```

**Rationale:** <why this structure>

---

## Module Breakdown

| Module | Purpose | Dependencies | Complexity | Owner |
|--------|---------|-------------|-----------|-------|
| <module> | <what it does> | <what it depends on> | S / M / L | <team/person> |

### Module Details

#### <Module 1>

**Purpose:** <what it does>
**Key Files:** <main files and their responsibilities>
**Dependencies:** <internal and external dependencies>
**Complexity Notes:** <why it's S/M/L, what makes it hard>

#### <Module 2>

<Same structure>

---

## Development Phases

### Phase 0: Spike Experiments

**Duration:** <timeframe>
**Goal:** Validate highest-risk assumptions before committing to implementation

| Spike ID | Description | Success Criteria | Time Box |
|----------|-------------|-----------------|----------|
| SPIKE-001 | <from Feasibility Report> | <criteria> | <time> |

### Phase 1: Foundation

**Duration:** <timeframe>
**Goal:** Infrastructure, auth, data layer, CI/CD pipeline

| Task | Description | Depends On | Estimate |
|------|------------|-----------|----------|
| 1.1 | <task> | — | S / M / L |
| 1.2 | <task> | 1.1 | S / M / L |

**Deliverable:** <what's shippable at the end of this phase>

### Phase 2: Core MVP Features

**Duration:** <timeframe>
**Goal:** Implement Must Have features from PRD

| Task | Description | REQ ID | Depends On | Estimate |
|------|------------|--------|-----------|----------|
| 2.1 | <task> | REQ-001 | Phase 1 | S / M / L |
| 2.2 | <task> | REQ-002 | 2.1 | S / M / L |

**Deliverable:** <what's shippable at the end of this phase>

### Phase 3: Integration and Testing

**Duration:** <timeframe>
**Goal:** End-to-end integration, performance testing, security review

| Task | Description | Depends On | Estimate |
|------|------------|-----------|----------|
| 3.1 | <task> | Phase 2 | S / M / L |
| 3.2 | <task> | 3.1 | S / M / L |

**Deliverable:** <what's shippable at the end of this phase>

### Phase 4: Deployment and Monitoring

**Duration:** <timeframe>
**Goal:** Production deployment, monitoring, observability

| Task | Description | Depends On | Estimate |
|------|------------|-----------|----------|
| 4.1 | <task> | Phase 3 | S / M / L |
| 4.2 | <task> | 4.1 | S / M / L |

**Deliverable:** <what's shippable at the end of this phase>

---

## CI/CD Outline

### Pipeline Stages

| Stage | Trigger | Actions | Gate |
|-------|---------|---------|------|
| Lint | Every push | <linting tools> | Fail on errors |
| Unit Test | Every push | <test framework> | >80% coverage |
| Build | PR merge to main | <build steps> | Clean build |
| Integration Test | PR merge to main | <integration tests> | All pass |
| Deploy Staging | Main branch | <deploy steps> | Health check pass |
| Deploy Production | Manual approval | <deploy steps> | Smoke tests pass |

### Testing Strategy

| Level | Scope | Tools | Target Coverage |
|-------|-------|-------|----------------|
| Unit | Individual functions/classes | <framework> | >80% |
| Integration | Component interactions | <framework> | Key flows |
| E2E | Full user journeys | <framework> | Critical paths |

---

## Spike Experiments

### SPIKE-001: <Title>

**Source:** Feasibility Report — <risk it addresses>
**Hypothesis:** <what we believe>
**Implementation:**

```
<brief code/script outline or steps to execute the spike>
```

**Expected Duration:** <time>
**Go/No-Go Criteria:** <what determines success or failure>
**If Validated:** <what we do next>
**If Invalidated:** <alternative approach>

---

## Technical Debt and Known Shortcuts

| Shortcut | Reason | Remediation Plan | Priority |
|----------|--------|-----------------|----------|
| <shortcut> | <why we're taking it> | <how to fix later> | <when> |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | YYYY-MM-DD | Venture Architect | Initial version |

## Assumptions & Constraints

<List assumptions made during analysis>

## Open Questions

<Unresolved questions with suggested owners>

## References

- Feasibility Report: `docs/Feasibility_Report.md`
- BRD: `docs/BRD.md`
- PRD: `docs/PRD.md`
- SRS: `docs/SRS.md`
