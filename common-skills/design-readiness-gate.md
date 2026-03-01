# Design Readiness Gate

Mandatory pre-coding checklist to ensure architecture and operational foundations are explicit before implementation starts.

## When to Apply

Apply before writing production code for any new feature/system and at major scope pivots.

## Gate Rule

- Do not start coding until all required checklist items are either:
  - decided with rationale, or
  - explicitly marked deferred with owner and due date.

## Required Decisions

### 1) Problem and Scope

- Problem statement and goals are clear
- In-scope vs out-of-scope is explicit
- Success metrics are defined

### 2) Requirement Traceability

- Requirements are enumerated with stable IDs (`REQ-###`, `NFR-###`)
- Each design decision maps to one or more requirement IDs
- Open questions are tracked with owners

### 3) Architecture and Design Pattern

- Architecture style selected (e.g., monolith/modular monolith/services)
- Core design pattern choices documented (layered, hexagonal, event-driven, CQRS, etc.)
- Tradeoffs and rejected alternatives are documented

### 4) Language and Runtime

- Primary language/framework chosen with rationale
- Version/runtime constraints are explicit
- Team capability and hiring/maintenance considerations captured

### 5) Data Model and Database

- Data access pattern and consistency needs are defined
- Database choice justified (SQL/NoSQL/search/cache/object store)
- Schema/migration/versioning strategy documented
- Backup/restore and retention expectations defined

### 6) API and Integration Contracts

- External and internal interfaces defined at sketch level
- Error model and idempotency strategy documented
- Dependency inventory and failure behavior identified

### 7) Logging/Observability

- Structured logging baseline defined (fields, levels, correlation ID)
- Metrics baseline defined (SLIs/SLOs, key counters/latencies)
- Tracing strategy and sampling approach decided (if distributed)
- Dashboards/alerts ownership identified

### 8) Security and Compliance

- AuthN/AuthZ model defined
- Secret handling approach defined
- Data classification and regulatory constraints identified
- Threat/risk hotspots explicitly listed

### 9) Delivery and Quality

- Test strategy defined (unit/integration/e2e and ownership)
- Release and rollback strategy defined
- CI quality gates defined (lint/test/build/security where applicable)
- Non-functional acceptance criteria are measurable

## Output Format

Record a `Design Readiness` section in the design/spec document plus task/state updates in `agent.todo.md`.

Recommended status table:

| Checkpoint | Status (Done/Deferred/Open) | Owner | Evidence/Link |
|------------|------------------------------|-------|---------------|
| Architecture pattern | Done | [name] | [doc section] |
| Language/runtime | Done | [name] | [doc section] |
| Database strategy | Done | [name] | [doc section] |
| Logging baseline | Done | [name] | [doc section] |

## Quality Checks

- [ ] No required checkpoint is left implicit
- [ ] Deferred items have owner + due date
- [ ] Requirement-to-design traceability exists
- [ ] Coding tasks are blocked until gate is satisfied
