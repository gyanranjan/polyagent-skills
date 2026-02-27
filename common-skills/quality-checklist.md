# Quality Checklist

Universal quality gates to verify before delivering any skill output.

## Before Delivering Output

### Completeness
- [ ] All steps in the skill's Process section were followed
- [ ] All required Inputs were obtained or reasonable defaults stated
- [ ] The Output Format matches what the skill specifies
- [ ] Referenced common-skills were applied

### Accuracy
- [ ] No placeholder text remains (e.g., `[TODO]`, `<fill in>`, `TBD`)
- [ ] File paths and references are valid and relative
- [ ] Code blocks are syntactically correct
- [ ] Numbers, dates, and versions are consistent

### Clarity
- [ ] A reader unfamiliar with the context can follow the document
- [ ] Headings accurately describe their sections
- [ ] Acronyms are defined on first use
- [ ] No ambiguous pronouns (what does "it" refer to?)

### Portability
- [ ] No agent-specific syntax leaked into the output
- [ ] Output doesn't assume a specific IDE or tool
- [ ] File references use relative paths

## Optional Quality Checks

For high-stakes documents (architecture decisions, requirements, client-facing):
- [ ] Have a second agent review the output (cross-agent validation)
- [ ] Check against the project's existing conventions and terminology
- [ ] Verify consistency with related documents in the same project
