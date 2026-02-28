# PR Review: `feat: add global install and safe uninstall flows`

**Branch:** `feat/global-install-uninstall-managed-cleanup`
**Commit:** `965d71d`
**Changes:** 7 files, +688 / -9 lines
**Reviewer:** Claude
**Date:** 2026-02-28

## Summary

This PR adds three new shell scripts for global (machine-wide) installation of polyagent-skills to agent config directories (`~/.codex`, `~/.kiro`, `~/.gemini`, `~/.openclaw`), plus a safe uninstaller. It also introduces OpenClaw as a newly supported agent and updates docs accordingly.

---

## Positive Aspects

1. **Manifest-based uninstall** — The install scripts write a manifest file, and the uninstaller only removes paths listed in the manifest with ownership marker verification. This is a safe, well-thought-out pattern that avoids accidentally deleting user files.

2. **Backup-before-overwrite** — Consistent with the existing `install-to-project.sh` pattern. Backups go to timestamped directories.

3. **`--dry-run` on uninstall** — Good UX; lets users preview what would be removed.

4. **`copy` vs `link` modes** — Useful for both production users and developers actively editing skills.

5. **SKILL.md frontmatter normalization** — Solves a real parser compatibility issue (KI-007) where multi-line YAML `description: >` blocks cause problems for OpenClaw.

6. **Docs updated holistically** — README, CONTRIBUTING, KNOWN_ISSUES, and adapter-contract-spec all updated together.

---

## Issues and Suggestions

### High Priority

#### 1. Massive code duplication between `install-global-all.sh` and `install-openclaw-global.sh`

The following functions are duplicated verbatim across both scripts (~100 lines each):
- `extract_skill_name()`
- `extract_skill_description()`
- `extract_skill_body()`
- `normalize_skill_markdown()`
- `backup_if_exists()`
- `record_manifest()`
- `mark_dir_managed()`

**Suggestion:** Extract shared functions into a `scripts/lib-common.sh` and `source` it from both scripts. This aligns with the project's own "shared patterns" philosophy (Layer 1: Common Foundation).

#### 2. `install-global-all.sh` link mode still copies to OpenClaw (inconsistency)

In `link` mode (line 256-266), the shared library is symlinked, but then `install_normalized_skills_copy` is called for OpenClaw anyway (line 270). The comment says "normalized copy required" but this means `link` mode is really "hybrid" mode. This is documented but could confuse users.

**Suggestion:** Make the output messaging clearer — e.g., `"Link mode: OpenClaw still receives a copy (parser requires normalized frontmatter)"`.

#### 3. `install-openclaw-global.sh` link mode doesn't normalize and silently breaks OpenClaw

In `install-openclaw-global.sh`, link mode (line 187-198) symlinks directly without normalization and prints a note: `! Note: link mode does not normalize SKILL.md frontmatter.` But this is the exact problem documented in KI-007 — OpenClaw's parser can't handle multi-line frontmatter. So running `./scripts/install-openclaw-global.sh link` will install broken skills.

**Suggestion:** Either (a) disallow link mode for the OpenClaw-specific script, (b) always copy+normalize for OpenClaw (like `install-global-all.sh` does), or (c) add a much more prominent warning that link mode is incompatible with the current OpenClaw parser.

#### 4. Gemini/Codex/Kiro global config overwrites without merge

`write_gemini_global_instructions()` backs up then overwrites `~/.gemini/instructions.md`. If a user already has Gemini global instructions for other purposes, the backup-and-replace approach loses their existing config. The same applies to Codex and Kiro configs.

**Suggestion:** Consider an append/merge strategy, or at minimum add prominent documentation that these files will be fully replaced.

### Medium Priority

#### 5. No OpenClaw adapter in `adapters/` directory

The PR adds OpenClaw to the README support table and creates global install scripts, but there's no `adapters/openclaw/` directory. The existing pattern has per-agent adapters. Is OpenClaw intentionally different (global-only, no per-project adapter)?

**Suggestion:** Either add an OpenClaw adapter directory or document why the adapter pattern doesn't apply to OpenClaw (perhaps via an ADR note).

#### 6. `install-to-project.sh` not updated for OpenClaw

The project-level installer still only supports `claude-code, codex, kiro, gemini, cursor`. OpenClaw is a new supported agent but has no project-level install path.

**Suggestion:** If OpenClaw is global-only by design, document this explicitly. Otherwise, add OpenClaw support to `install-to-project.sh`.

#### 7. Manifest file is overwritten on re-install

Both scripts start with `printf ... > "$MANIFEST_FILE"` which truncates the manifest. If a user runs the installer twice, only the second run's paths are tracked. Paths from the first run that were replaced become orphaned from the manifest.

**Suggestion:** This is mostly fine because the installer replaces those same paths anyway, but worth noting. Consider appending (`>>`) or documenting that re-installs are safe because they replace the same paths.

#### 8. Hardcoded `rg` in verification commands

The output suggests users verify with `rg` (ripgrep):
```
openclaw skills list | rg -i 'requirement-study|repo-bootstrap|remote-ops'
```
Not all users will have `rg` installed. Consider using `grep -i` instead.

### Low Priority

#### 9. Whitespace-only changes in README diagram

Lines 19-30 of the README diff are pure trailing-whitespace alignment changes to the ASCII architecture diagram. These add noise to the diff.

#### 10. No linting evidence for new scripts

The new scripts are substantial bash (~600 lines total). No evidence of `shellcheck` or `shfmt` linting. The complex awk scripts would benefit from validation.

#### 11. No tests for the normalization logic

The `normalize_skill_markdown` function has complex awk-based YAML frontmatter parsing. There are no tests to verify edge cases (empty description, special characters, missing frontmatter, etc.).

**Suggestion:** Consider adding a `tests/` directory with test cases for the normalization pipeline.

---

## Verdict

The PR adds genuinely useful functionality — global install is a natural next step for this project. The manifest-based safe uninstall is well-designed. However, the significant code duplication between the two install scripts and the OpenClaw link-mode footgun (silently installing broken skills) should be addressed before merging.

**Recommendation: Request changes** — address items 1, 3, and 5 before merging.
