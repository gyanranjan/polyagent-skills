# Role Orchestrator — Routing Decisions

_Record significant routing and workflow decisions with rationale._

## Decision Log

### 2026-03-06 — System Design: Lifecycle Model
**Decision**: Use IDEA → VALIDATE → DESIGN → BUILD → HARDEN → OPERATE → LEARN as the routing lifecycle.
**Rationale**: Maps to the natural progression of a product from concept to production. Each stage has clear entry and exit criteria and maps to specific role capabilities.
**Applied to**: All task routing decisions.

### 2026-03-06 — System Design: Challenge Role Policy
**Decision**: devils-advocate and systems-simplifier are available at any stage; apply proactively before major commitments and after design phases respectively.
**Rationale**: These roles improve quality across all stages; restricting them to specific stages reduces their value.
