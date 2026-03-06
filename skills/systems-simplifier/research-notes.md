# Research Notes — systems-simplifier

Simplification patterns, refactoring approaches, complexity metrics, and reference material relevant to this role's work.

---

## Simplification Patterns

_Recurring patterns of unnecessary complexity and their standard remedies._

### Premature Abstraction
- **Symptoms**: Interfaces with one implementation, base classes with one subclass, plugin systems for features that never vary
- **Standard remedy**: Collapse to concrete implementation; re-abstract when a second genuine use case appears
- **Rule of thumb**: Abstract at the second repetition, not the first anticipation

### Accidental Layering
- **Symptoms**: Requests pass through N layers with no transformation at each layer; "pass-through" services
- **Standard remedy**: Merge layers; preserve only layers that add genuine transformation or isolation value

### Premature Optimization
- **Symptoms**: Caching added before profiling, async introduced before sync proved too slow, sharding before single-node limits reached
- **Standard remedy**: Remove optimization; profile first; add back only where measurement justifies

### Duplication (Copy-Paste Code)
- **Symptoms**: Same logic in 3+ places with minor variations
- **Standard remedy**: Extract shared logic; parameterize the variation

### Scope Creep in Design
- **Symptoms**: MVP designs include analytics, admin dashboards, export features, multi-tenancy
- **Standard remedy**: Apply MVP filter — does this feature exist to validate the core hypothesis?

---

## Complexity Cost Reference

_Rough estimates for complexity cost discussion (adjust to specific context)._

| Complexity Type | Rough Ongoing Cost |
|----------------|--------------------|
| Extra microservice | +1 deployment, +1 monitoring target, +N network hops |
| Message queue | +operational expertise, +failure modes, +latency debugging |
| Plugin abstraction | +interface maintenance, +documentation, +onboarding overhead |
| Unused generalization | +cognitive load for all future maintainers |

---

## External References

_Links or citations to simplification resources. Add as discovered._

- Gall's Law: "A complex system that works is invariably found to have evolved from a simple system that worked."
- Yagni principle (You Aren't Gonna Need It): Don't build for requirements that don't exist yet.
- Worse is Better (Richard Gabriel): Simplicity of interface and implementation often beats theoretical correctness.

---

## Notes From Past Reviews

_Specific findings from completed reviews that have pattern value. Add after each session._

_None yet._
