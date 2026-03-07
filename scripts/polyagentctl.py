#!/usr/bin/env python3
"""polyagentctl — unified CLI for polyagent-skills. No shell script dependencies."""
from __future__ import annotations

import argparse
import base64
import datetime
import html as html_mod
import json
import os
import pathlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import urllib.request
import urllib.parse
import zipfile
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = SCRIPT_DIR.parent
MANAGED_MARKER_KEY = "polyagent-managed-by"
MANAGED_TAG_GLOBAL = "install-global-all.sh"
MANAGED_TAG_OPENCLAW = "install-openclaw-global.sh"

AGENT_CONFIGS = {
    "claude-code": ("CLAUDE.md", None),
    "codex": ("AGENTS.md", None),
    "kiro": (".kiro/specs/polyagent-skills.md", ".kiro"),
    "gemini": (".gemini/instructions.md", ".gemini"),
    "cursor": (".cursor/rules.md", ".cursor"),
}


# ---------------------------------------------------------------------------
# Low-level helpers
# ---------------------------------------------------------------------------

def run(cmd: list[str], cwd: Path | None = None) -> int:
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    return proc.returncode


def run_capture(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return proc.returncode, proc.stdout.strip()


def which(name: str) -> str | None:
    return shutil.which(name)


# ---------------------------------------------------------------------------
# doctor — prerequisite definitions
# ---------------------------------------------------------------------------

# (tool, label, required, npm_fix_cmd_or_None)
_DOCTOR_TOOLS = [
    ("python3",     "Python 3",                    True,  None),
    ("node",        "Node.js",                     False, None),
    ("npm",         "npm",                         False, None),
    ("npx",         "npx",                         False, None),
    ("mmdc",        "Mermaid CLI (mmdc)",           False, "npm install -g @mermaid-js/mermaid-cli"),
    ("wkhtmltopdf", "wkhtmltopdf (HTML→PDF)",       False, None),
    ("pandoc",      "pandoc (doc converter)",       False, None),
]

# (import_name, label, pip_package)
_DOCTOR_PY_PKGS = [
    ("markdown_it", "markdown-it-py (Markdown→HTML)", "markdown-it-py"),
]

# (require_name, label, npm_package)
_DOCTOR_NPM_PKGS = [
    ("puppeteer", "puppeteer (headless PDF)", "puppeteer"),
]

_INSTALL_HINTS = {
    "node":        "https://nodejs.org  or  nvm install --lts",
    "npm":         "ships with Node.js",
    "npx":         "ships with Node.js",
    "wkhtmltopdf": "apt install wkhtmltopdf  |  brew install wkhtmltopdf",
    "pandoc":      "apt install pandoc       |  brew install pandoc",
}


def _has_py_pkg(import_name: str) -> bool:
    import importlib.util as _ilu
    return _ilu.find_spec(import_name) is not None


def _has_npm_pkg(pkg_name: str) -> bool:
    if not which("node"):
        return False
    code, out = run_capture([
        "node", "-e",
        f"try{{require.resolve('{pkg_name}');console.log('yes')}}catch(e){{console.log('no')}}",
    ])
    return code == 0 and out.strip() == "yes"


def _ask_yes(prompt: str) -> bool:
    sys.stdout.write(prompt + " [y/N] ")
    sys.stdout.flush()
    try:
        return sys.stdin.readline().strip().lower() == "y"
    except (EOFError, KeyboardInterrupt):
        return False


def doctor_cmd(args: argparse.Namespace) -> int:
    fix: bool = getattr(args, "fix", False)
    failures = 0
    warnings = 0

    print("=== polyagentctl doctor ===")
    print()

    # ── Binary tools ──────────────────────────────────────────────────────
    print("System tools:")
    for tool, label, required, npm_fix in _DOCTOR_TOOLS:
        found = which(tool)
        if found:
            print(f"  [OK]  {label}: {found}")
            continue
        status = "[ERR]" if required else "[--] "
        print(f"  {status} {label}: not found")
        hint = _INSTALL_HINTS.get(tool)
        if npm_fix:
            print(f"        install: {npm_fix}")
        elif hint:
            print(f"        install: {hint}")
        if required:
            failures += 1
        else:
            warnings += 1
        if npm_fix and fix and which("npm"):
            if _ask_yes(f"  Run `{npm_fix}` now?"):
                run(npm_fix.split())
                if which(tool):
                    print(f"  [OK]  {label}: installed")

    # ── Python packages ───────────────────────────────────────────────────
    print()
    print("Python packages:")
    for import_name, label, pip_pkg in _DOCTOR_PY_PKGS:
        if _has_py_pkg(import_name):
            print(f"  [OK]  {label}")
        else:
            print(f"  [--]  {label}: not installed")
            print(f"        install: pip install {pip_pkg}")
            warnings += 1
            if fix and _ask_yes(f"  Run `pip install {pip_pkg}` now?"):
                run([sys.executable, "-m", "pip", "install", pip_pkg])
                if _has_py_pkg(import_name):
                    print(f"  [OK]  {label}: installed")

    # ── npm packages ──────────────────────────────────────────────────────
    if which("node"):
        print()
        print("Node.js packages:")
        for pkg_name, label, npm_pkg in _DOCTOR_NPM_PKGS:
            if _has_npm_pkg(pkg_name):
                print(f"  [OK]  {label}")
            else:
                print(f"  [--]  {label}: not installed")
                print(f"        install: npm install -g {npm_pkg}")
                warnings += 1
                if fix and which("npm") and _ask_yes(f"  Run `npm install -g {npm_pkg}` now?"):
                    run(["npm", "install", "-g", npm_pkg])
                    if _has_npm_pkg(pkg_name):
                        print(f"  [OK]  {label}: installed")

    print()
    if failures:
        print(f"Result: {failures} required item(s) missing. Fix before proceeding.")
        return 1
    if warnings:
        print(f"Result: OK  ({warnings} optional item(s) missing — some features limited)")
        print("  Run with --fix to install missing optional items interactively.")
    else:
        print("Result: All checks passed.")
    return 0


# ---------------------------------------------------------------------------
# Install/uninstall shared helpers (lib-common equivalents)
# ---------------------------------------------------------------------------

def _backup_path(path: Path, backup_dir: Path) -> None:
    if path.exists() or path.is_symlink():
        backup_dir.mkdir(parents=True, exist_ok=True)
        safe = str(path).lstrip("/").replace("/", "__")
        target = backup_dir / safe
        shutil.move(str(path), str(target))
        print(f"  Backed up: {path} -> {target}")


def _record_manifest(manifest: Path, path: Path, kind: str, tag: str) -> None:
    with manifest.open("a") as f:
        f.write(f"{path}\t{kind}\t{tag}\n")


def _mark_dir_managed(dir_path: Path, managed_tag: str) -> None:
    marker = dir_path / ".polyagent-managed"
    marker.write_text(
        f"{MANAGED_MARKER_KEY}: {managed_tag}\nsource-repo: {REPO_DIR}\n",
        encoding="utf-8",
    )


def _parse_skill_frontmatter(skill_md: Path) -> tuple[str, str]:
    """Return (name, description) from YAML frontmatter."""
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    name = ""
    description = ""
    if not lines or lines[0].strip() != "---":
        return name, description
    in_fm = False
    in_desc_block = False
    desc_lines: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if not in_fm:
            in_fm = True
        m_name = re.match(r"^name:\s*(.+)$", line)
        if m_name:
            name = m_name.group(1).strip().strip('"\'')
            continue
        if re.match(r"^description:\s*>\s*$", line):
            in_desc_block = True
            continue
        if in_desc_block:
            if re.match(r"^[A-Za-z0-9_-]+:\s*", line):
                in_desc_block = False
            else:
                desc_lines.append(line.strip())
            continue
        m_desc = re.match(r"^description:\s*(.+)$", line)
        if m_desc:
            description = m_desc.group(1).strip().strip('"\'')
    if desc_lines:
        description = " ".join(desc_lines).strip()
    return name, description


def _build_skill_list(skills_dir: Path) -> str:
    """Scan skills_dir and return a bullet list of available skills."""
    entries: list[str] = []
    if skills_dir.is_dir():
        for skill_dir in sorted(skills_dir.iterdir()):
            skill_md = skill_dir / "SKILL.md"
            if skill_md.exists():
                _, description = _parse_skill_frontmatter(skill_md)
                desc = f" — {description}" if description else ""
                entries.append(f"- `{skill_dir.name}`{desc}")
    return "\n".join(entries)


def _skill_body(skill_md: Path) -> str:
    """Return skill markdown body without frontmatter."""
    text = skill_md.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return text
    i = 1
    while i < len(lines):
        if lines[i].strip() == "---":
            return "\n".join(lines[i + 1:])
        i += 1
    return text


def _normalize_skill_markdown(src: Path, dst: Path, fallback_name: str) -> None:
    name, description = _parse_skill_frontmatter(src)
    if not name:
        name = fallback_name
    if not description:
        description = f"Portable polyagent skill: {name}"
    body = _skill_body(src)
    esc_desc = description.replace("\\", "\\\\").replace('"', '\\"')
    dst.write_text(
        f'---\nname: {name}\ndescription: "{esc_desc}"\n---\n\n{body}',
        encoding="utf-8",
    )


def _install_normalized_skills_copy(
    src_skills: Path,
    src_common: Path,
    dst_skills: Path,
    dst_common: Path,
    manifest: Path,
    managed_tag: str,
    backup_dir: Path,
) -> None:
    _backup_path(dst_skills, backup_dir)
    dst_skills.mkdir(parents=True, exist_ok=True)
    _mark_dir_managed(dst_skills, managed_tag)
    _record_manifest(manifest, dst_skills, "dir", managed_tag)

    for src_dir in sorted(src_skills.iterdir()):
        if not src_dir.is_dir():
            continue
        skill_name = src_dir.name
        dst_dir = dst_skills / skill_name
        dst_dir.mkdir(parents=True, exist_ok=True)
        shutil.copytree(str(src_dir), str(dst_dir), dirs_exist_ok=True)
        skill_md = src_dir / "SKILL.md"
        if skill_md.exists():
            _normalize_skill_markdown(skill_md, dst_dir / "SKILL.md", skill_name)
        print(f"  Installed skill: {skill_name} -> {dst_skills}")

    _backup_path(dst_common, backup_dir)
    dst_common.mkdir(parents=True, exist_ok=True)
    shutil.copytree(str(src_common), str(dst_common), dirs_exist_ok=True)
    _mark_dir_managed(dst_common, managed_tag)
    _record_manifest(manifest, dst_common, "dir", managed_tag)
    print(f"  Installed common skills -> {dst_common}")


# ---------------------------------------------------------------------------
# Global agent config writers
# ---------------------------------------------------------------------------

def _write_agent_config(
    path: Path,
    content: str,
    manifest: Path,
    managed_tag: str,
    backup_dir: Path,
    label: str,
) -> None:
    _backup_path(path, backup_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    _record_manifest(manifest, path, "file", managed_tag)
    print(f"  Wrote {label}: {path}")


def _claude_content(global_skills: Path, global_common: Path) -> str:
    return f"""\
<!-- {MANAGED_MARKER_KEY}: {MANAGED_TAG_GLOBAL} -->
# Agent Instructions - polyagent-skills (global)

You have access to a portable skill library in:
- `{global_skills}`
- `{global_common}`

When you receive a task:
1. Check `{global_skills}` for a matching skill by reading each SKILL.md description.
2. Read the full SKILL.md for the matched skill.
3. Follow its Process steps in order.
4. Apply referenced common-skills from `{global_common}`.
5. Deliver in the specified Output Format.

## Tooling (use polyagentctl for all standard operations)

```bash
# Check prerequisites (run once after install, or when tools seem missing)
polyagentctl doctor

# Convert Markdown (with Mermaid diagrams) to PDF or HTML
polyagentctl export-pdf <file.md>          # auto-detect output format
polyagentctl export-pdf <file.md> --html   # force HTML

# Gate and design checks
polyagentctl gate-check [agent.todo.md]
polyagentctl design-check <doc.md>
polyagentctl check --strict --project .
```
"""


def _codex_content(global_skills: Path, global_common: Path, skill_list: str = "") -> str:
    skill_section = f"\n## Available Skills\n\n{skill_list}\n" if skill_list else ""
    return f"""\
<!-- {MANAGED_MARKER_KEY}: {MANAGED_TAG_GLOBAL} -->
# Agent Instructions - polyagent-skills (global)

You have access to a portable skill library in:
- `{global_skills}`
- `{global_common}`

## Development Lifecycle Gates (Mandatory)

Before writing production code, follow `{global_common}/development-lifecycle-gates.md`.

G0 Discovery -> G1 Requirements -> G2 Design -> G3 POC/Spike (if needed) -> G4 Implementation -> G5 Review -> G6 Ship.

Gates are mandatory by default. Check `agent.todo.md` for gate status. Start at the earliest incomplete gate. Skip only if the user explicitly asks.

## Operating Expectations (Mandatory)

1. Act as an expert partner: challenge weak assumptions and propose stronger options.
2. Ask 2-4 high-value, decision-oriented questions at each gate transition.
3. In every substantive response, include:
   - `Stage: Gx <name>`
   - `Next: <immediate next step>`
4. Requirements/design deliverables must include in-block Mermaid diagrams by default.
5. Generate shareable PDF exports for requirements/design docs by default unless the user opts out.
6. Keep `agent.todo.md` workflow snapshot and gate evidence updated continuously.

When you receive a task:
1. Match the task to a skill from the list below.
2. Read the full `{global_skills}/<skill-name>/SKILL.md`.
3. Follow its Process steps in order.
4. Apply referenced common-skills from `{global_common}`.
5. Deliver in the specified Output Format.
{skill_section}
## Tooling (use polyagentctl for all standard operations)

```bash
polyagentctl doctor                        # check/install prerequisites
polyagentctl export-pdf <file.md>          # Markdown+Mermaid → PDF/HTML
polyagentctl gate-check [agent.todo.md]    # verify lifecycle gate status
polyagentctl check --strict --project .   # pre-PR quality gate
```

## Pre-PR Quality Gate (Required)

Before opening or merging any PR, run:

```bash
polyagentctl check --strict --project .
```
"""


def _kiro_content(global_skills: Path, global_common: Path, skill_list: str = "") -> str:
    skill_section = f"\n## Available Skills\n\n{skill_list}\n" if skill_list else ""
    return f"""\
<!-- {MANAGED_MARKER_KEY}: {MANAGED_TAG_GLOBAL} -->
# Skill Library Integration - polyagent-skills (global)

You have access to a portable skill library:
- `{global_skills}`
- `{global_common}`

## Development Lifecycle Gates (Mandatory)

Before writing production code, follow `{global_common}/development-lifecycle-gates.md`.
Check `agent.todo.md` for gate status. Start at the earliest incomplete gate. Skip only if the user explicitly asks.

## Operating Expectations (Mandatory)

1. Behave as an expert partner and challenge weak assumptions.
2. Ask 2-4 high-value, decision-oriented questions at each gate transition.
3. In every substantive response, include:
   - `Stage: Gx <name>`
   - `Next: <immediate next step>`
4. Requirements/design deliverables include in-block Mermaid diagrams by default.
5. Generate shareable PDF exports for requirements/design docs by default unless user opts out.
6. Keep `agent.todo.md` workflow snapshot and gate evidence updated.

## Task Workflow

1. Match the task to a skill from the list below.
2. Read the full `{global_skills}/<skill-name>/SKILL.md`.
3. Follow its Process steps in order.
4. Apply referenced common-skills from `{global_common}`.
5. Deliver in the specified output format.
{skill_section}
## Tooling

```bash
polyagentctl doctor                        # check/install prerequisites
polyagentctl export-pdf <file.md>          # Markdown+Mermaid → PDF/HTML
polyagentctl gate-check [agent.todo.md]
polyagentctl check --strict --project .   # pre-PR quality gate
```

## Pre-PR Quality Gate (Required)

Before opening or merging any PR, run:

```bash
polyagentctl check --strict --project .
```
"""


def _gemini_content(global_skills: Path, global_common: Path, skill_list: str = "") -> str:
    skill_section = f"\n## Available Skills\n\n{skill_list}\n" if skill_list else ""
    return f"""\
<!-- {MANAGED_MARKER_KEY}: polyagentctl install-global -->
# Agent Instructions - polyagent-skills (global)

You have access to a portable skill library:
- `{global_skills}`
- `{global_common}`

## Development Lifecycle Gates (Mandatory)

Before writing production code, follow `{global_common}/development-lifecycle-gates.md`.
Check `agent.todo.md` for gate status. Start at the earliest incomplete gate. Skip only if the user explicitly asks.

## Operating Expectations (Mandatory)

1. Act as an expert partner and challenge weak assumptions.
2. Ask 2-4 high-value, decision-oriented questions at each gate transition.
3. In every substantive response, include:
   - `Stage: Gx <name>`
   - `Next: <immediate next step>`
4. Requirements/design deliverables should include in-block Mermaid diagrams by default.
5. Generate shareable PDF exports for requirements/design docs by default unless user opts out.
6. Keep `agent.todo.md` workflow snapshot and gate evidence up to date.

## Task Workflow

1. Match the task to a skill from the list below.
2. Read the full `{global_skills}/<skill-name>/SKILL.md`.
3. Follow its Process steps in order.
4. Apply referenced common-skills from `{global_common}`.
5. Deliver in the specified output format.
{skill_section}
## Tooling

```bash
polyagentctl doctor                        # check/install prerequisites
polyagentctl export-pdf <file.md>          # Markdown+Mermaid → PDF/HTML
polyagentctl gate-check [agent.todo.md]
polyagentctl check --strict --project .   # pre-PR quality gate
```

## Pre-PR Quality Gate (Required)

Before opening or merging any PR, run:

```bash
polyagentctl check --strict --project .
```
"""


# ---------------------------------------------------------------------------
# install-global command
# ---------------------------------------------------------------------------

def install_global_cmd(args: argparse.Namespace) -> int:
    mode = args.mode
    global_root = Path(os.environ.get("POLYAGENT_HOME", Path.home() / ".polyagent-skills"))
    openclaw_home = Path(os.environ.get("OPENCLAW_HOME", Path.home() / ".openclaw"))

    global_skills = global_root / "skills"
    global_common = global_root / "common-skills"
    openclaw_skills = openclaw_home / "skills"
    openclaw_common = openclaw_home / "common-skills"

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path.home() / ".polyagent-backup" / ts
    manifest = global_root / ".global-install-manifest"

    global_root.mkdir(parents=True, exist_ok=True)
    openclaw_home.mkdir(parents=True, exist_ok=True)
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        "# polyagent global install manifest\n# format: <path>\t<kind>\t<tag>\n",
        encoding="utf-8",
    )

    src_skills = REPO_DIR / "skills"
    src_common = REPO_DIR / "common-skills"

    # Run prerequisite check first (fix=True so user is prompted for missing tools)
    doctor_rc = doctor_cmd(argparse.Namespace(fix=True))
    if doctor_rc != 0:
        print("\nInstallation aborted: required prerequisites missing.", file=sys.stderr)
        return doctor_rc
    print()

    print("=== polyagent global installer ===")
    print(f"Mode: {mode}")
    print(f"Global root: {global_root}")
    print(f"OpenClaw home: {openclaw_home}")
    print()

    if mode == "copy":
        print("Installing shared global library (copy mode)...")
        _install_normalized_skills_copy(
            src_skills, src_common, global_skills, global_common,
            manifest, MANAGED_TAG_GLOBAL, backup_dir,
        )
    else:
        print("Installing shared global library (link mode)...")
        _backup_path(global_skills, backup_dir)
        _backup_path(global_common, backup_dir)
        global_skills.symlink_to(src_skills)
        global_common.symlink_to(src_common)
        _record_manifest(manifest, global_skills, "symlink", MANAGED_TAG_GLOBAL)
        _record_manifest(manifest, global_common, "symlink", MANAGED_TAG_GLOBAL)
        print(f"  Linked: {global_skills} -> {src_skills}")
        print(f"  Linked: {global_common} -> {src_common}")

    print()
    print("Installing OpenClaw global skills (normalized copy)...")
    openclaw_manifest = openclaw_home / ".openclaw-install-manifest"
    openclaw_manifest.write_text(
        "# openclaw install manifest\n# format: <path>\t<kind>\t<tag>\n",
        encoding="utf-8",
    )
    _install_normalized_skills_copy(
        src_skills, src_common, openclaw_skills, openclaw_common,
        openclaw_manifest, MANAGED_TAG_OPENCLAW, backup_dir,
    )

    print()
    print("Writing global agent configs...")
    print("  (Existing config files will be backed up before replacement.)")
    skill_list = _build_skill_list(src_skills)
    _write_agent_config(
        Path.home() / ".claude" / "CLAUDE.md",
        _claude_content(global_skills, global_common),
        manifest, MANAGED_TAG_GLOBAL, backup_dir, "Claude Code global config",
    )
    _write_agent_config(
        Path.home() / ".codex" / "AGENTS.md",
        _codex_content(global_skills, global_common, skill_list),
        manifest, MANAGED_TAG_GLOBAL, backup_dir, "Codex global config",
    )
    _write_agent_config(
        Path.home() / ".kiro" / "specs" / "polyagent-skills.md",
        _kiro_content(global_skills, global_common, skill_list),
        manifest, MANAGED_TAG_GLOBAL, backup_dir, "Kiro global config",
    )
    _write_agent_config(
        Path.home() / ".gemini" / "instructions.md",
        _gemini_content(global_skills, global_common, skill_list),
        manifest, MANAGED_TAG_GLOBAL, backup_dir, "Gemini global config",
    )

    # Register skills with Gemini CLI native skill registry if gemini is available
    gemini_bin = shutil.which("gemini")
    if gemini_bin:
        print()
        print("Registering skills with Gemini CLI (gemini skills link)...")
        linked = 0
        for skill_dir in sorted(src_skills.iterdir()):
            if not (skill_dir / "SKILL.md").exists():
                continue
            result = subprocess.run(
                [gemini_bin, "skills", "link", str(skill_dir), "--consent"],
                capture_output=True, text=True,
            )
            if result.returncode == 0:
                linked += 1
            else:
                print(f"  Warning: could not link {skill_dir.name}: {result.stderr.strip()}")
        print(f"  Linked {linked} skills into Gemini CLI registry")
    else:
        print()
        print("  Gemini CLI not found in PATH — skipping native skill registration.")
        print("  Install it with: npm install -g @google/gemini-cli@latest")
        print("  Then re-run: polyagentctl install-global")

    installed_cli = _self_install_default()

    print()
    print("=== Done ===")
    print(f"Manifest: {manifest}")
    print(f"CLI installed: {installed_cli}")
    print("Per-project installer: polyagentctl install-project <path> [agent]")
    print("Uninstall safely with: polyagentctl uninstall-global --dry-run")
    return 0


# ---------------------------------------------------------------------------
# uninstall-global command
# ---------------------------------------------------------------------------

def uninstall_global_cmd(args: argparse.Namespace) -> int:
    dry_run = args.dry_run
    global_root = Path(os.environ.get("POLYAGENT_HOME", Path.home() / ".polyagent-skills"))
    openclaw_home = Path(os.environ.get("OPENCLAW_HOME", Path.home() / ".openclaw"))

    def remove_path(p: Path) -> None:
        if dry_run:
            print(f"  [dry-run] rm -rf {p}")
        else:
            shutil.rmtree(str(p), ignore_errors=True)
            if p.is_symlink():
                p.unlink(missing_ok=True)
            print(f"  Removed: {p}")

    def process_manifest(manifest: Path) -> None:
        if not manifest.exists():
            print(f"Manifest not found: {manifest}")
            return
        print(f"Processing manifest: {manifest}")
        for line in manifest.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) != 3:
                continue
            path_s, kind, tag = parts
            p = Path(path_s)
            if kind == "file":
                if p.is_file() and MANAGED_MARKER_KEY in p.read_text(encoding="utf-8", errors="replace"):
                    remove_path(p)
                else:
                    print(f"  Skipped (unmanaged/missing file): {p}")
            elif kind == "dir":
                marker = p / ".polyagent-managed"
                if p.is_dir() and marker.exists() and MANAGED_MARKER_KEY in marker.read_text(encoding="utf-8", errors="replace"):
                    remove_path(p)
                else:
                    print(f"  Skipped (unmanaged/missing dir): {p}")
            elif kind == "symlink":
                if p.is_symlink():
                    remove_path(p)
                else:
                    print(f"  Skipped (missing symlink): {p}")
            else:
                print(f"  Skipped (unknown kind '{kind}'): {p}")
        if dry_run:
            print(f"  [dry-run] rm -f {manifest}")
        else:
            manifest.unlink(missing_ok=True)
            print(f"  Removed manifest: {manifest}")

    print("=== polyagent global uninstall ===")
    print(f"Dry run: {dry_run}")
    print()
    process_manifest(global_root / ".global-install-manifest")
    print()
    process_manifest(openclaw_home / ".openclaw-install-manifest")
    print()
    print("Done. Only manifest-managed paths were targeted.")
    return 0


# ---------------------------------------------------------------------------
# install-project command
# ---------------------------------------------------------------------------

def install_project_cmd(args: argparse.Namespace) -> int:
    project = Path(args.project_path).resolve()
    agent = args.agent if args.agent else "all"

    if not project.is_dir():
        print(f"Error: Project directory '{project}' does not exist.")
        return 1

    # Run prerequisite check first
    doctor_rc = doctor_cmd(argparse.Namespace(fix=True))
    if doctor_rc != 0:
        print("\nInstallation aborted: required prerequisites missing.", file=sys.stderr)
        return doctor_rc
    print()

    print("=== polyagent-skills installer ===")
    print(f"Project: {project}")
    print(f"Agent:   {agent}")
    print()

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = project / ".polyagent-backup" / ts

    def backup(p: Path) -> None:
        if p.exists():
            backup_dir.mkdir(parents=True, exist_ok=True)
            dest = backup_dir / p.name
            shutil.copytree(str(p), str(dest)) if p.is_dir() else shutil.copy2(str(p), str(dest))
            print(f"  Backed up: {p} -> {dest}")

    print("Copying skill library...")
    shutil.copytree(str(REPO_DIR / "skills"), str(project / "skills"), dirs_exist_ok=True)
    shutil.copytree(str(REPO_DIR / "common-skills"), str(project / "common-skills"), dirs_exist_ok=True)
    print("  Skills and common-skills copied")

    def install_adapter(name: str) -> int:
        print(f"Installing adapter: {name}")
        if name == "claude-code":
            backup(project / "CLAUDE.md")
            shutil.copy2(str(REPO_DIR / "adapters/claude-code/CLAUDE.md"), str(project / "CLAUDE.md"))
            print("  CLAUDE.md installed")
        elif name == "codex":
            backup(project / "AGENTS.md")
            shutil.copy2(str(REPO_DIR / "adapters/codex/AGENTS.md"), str(project / "AGENTS.md"))
            print("  AGENTS.md installed")
        elif name == "kiro":
            backup(project / ".kiro")
            (project / ".kiro" / "specs").mkdir(parents=True, exist_ok=True)
            shutil.copy2(
                str(REPO_DIR / "adapters/kiro/.kiro/specs/polyagent-skills.md"),
                str(project / ".kiro/specs/polyagent-skills.md"),
            )
            print("  .kiro/specs/polyagent-skills.md installed")
        elif name == "gemini":
            backup(project / ".gemini")
            (project / ".gemini").mkdir(exist_ok=True)
            shutil.copy2(
                str(REPO_DIR / "adapters/gemini/.gemini/instructions.md"),
                str(project / ".gemini/instructions.md"),
            )
            print("  .gemini/instructions.md installed")
        elif name == "cursor":
            backup(project / ".cursor")
            (project / ".cursor").mkdir(exist_ok=True)
            shutil.copy2(
                str(REPO_DIR / "adapters/cursor/.cursor/rules.md"),
                str(project / ".cursor/rules.md"),
            )
            print("  .cursor/rules.md installed")
        else:
            print(f"  Unknown agent: {name}")
            print("  Supported: claude-code, codex, kiro, gemini, cursor, all")
            return 1
        return 0

    agents = ["claude-code", "codex", "kiro", "gemini", "cursor"] if agent == "all" else [agent]
    for a in agents:
        rc = install_adapter(a)
        if rc != 0:
            return rc

    print()
    print("=== Installation complete ===")
    print(f"Open {project} in your agent — skills are ready to use.")
    return 0


# ---------------------------------------------------------------------------
# gate-check command (gate-status-check.sh)
# ---------------------------------------------------------------------------

def _gate_check(todo_file: Path) -> int:
    if not todo_file.exists():
        print(f"ERROR: {todo_file} not found")
        print("Hint: Run from the repository root or pass the path as an argument.")
        return 2

    text = todo_file.read_text(encoding="utf-8")
    if "## Gate Status" not in text:
        print(f"WARNING: No '## Gate Status' section found in {todo_file}")
        print()
        print("This project has not initialized the development lifecycle gates.")
        print("To start, add the gate status template from:")
        print("  common-skills/development-lifecycle-gates.md")
        return 2

    print("=== Development Lifecycle Gate Status ===")
    print()

    # Extract gate section
    in_section = False
    gate_lines: list[str] = []
    for line in text.splitlines():
        if line.startswith("## Gate Status"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section:
            gate_lines.append(line)

    current_gate = ""
    skipped_gates: list[str] = []
    all_pre_impl_passed = True
    g3_status = ""

    for line in gate_lines:
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 4:
            continue
        gate, name, status = parts[0], parts[1], parts[2]
        if not re.match(r"^G[0-6]$", gate):
            continue
        skip_reason = parts[4].strip() if len(parts) > 4 else ""

        symbols = {"Passed": "✅", "Skipped": "⏭ ", "In Progress": "🔄", "N/A": "➖", "Not Started": "⬜"}
        sym = symbols.get(status, "❓")
        if status == "Skipped":
            print(f"  {gate:<4} {name:<16} {sym} Skipped ({skip_reason})")
            skipped_gates.append(gate)
        else:
            print(f"  {gate:<4} {name:<16} {sym} {status}")

        if not current_gate and status in ("In Progress", "Not Started"):
            current_gate = f"{gate}: {name}"

        if gate in ("G0", "G1", "G2") and status not in ("Passed", "Skipped", "N/A"):
            all_pre_impl_passed = False
        if gate == "G3":
            g3_status = status

    print()
    print(f"Current gate: {current_gate or 'All gates processed'}")
    if skipped_gates:
        print(f"Skipped gates: {' '.join(skipped_gates)}")
    print()

    if g3_status == "In Progress":
        all_pre_impl_passed = False
    if g3_status == "Not Started":
        print("Note: G3 is conditional. If no high-risk spike is needed, mark G3 as N/A.")
        print()

    if all_pre_impl_passed:
        print("✅ READY FOR IMPLEMENTATION — Gates 0–2 (and 3 if applicable) are cleared.")
        return 0
    else:
        print("⛔ NOT READY FOR IMPLEMENTATION — Complete or skip pending gates first.")
        print()
        print("To skip a gate, the user must explicitly say 'skip to [phase]'.")
        print("See: common-skills/development-lifecycle-gates.md")
        return 1


def gate_check_cmd(args: argparse.Namespace) -> int:
    return _gate_check(Path(args.todo_file))


# ---------------------------------------------------------------------------
# design-check command (design-readiness-check.sh)
# ---------------------------------------------------------------------------

DESIGN_CHECKPOINTS = [
    ("architecture pattern", "Architecture pattern"),
    ("language/runtime", "Language/runtime"),
    ("database strategy", "Database strategy"),
    ("logging/observability baseline", "Logging/observability baseline"),
]


def _design_check_file(file: Path, allow_open: bool) -> int:
    if not file.exists():
        print(f"FAIL file_not_found: {file}")
        return 1

    text = file.read_text(encoding="utf-8")
    # Extract Design Readiness section
    section_lines: list[str] = []
    in_section = False
    for line in text.splitlines():
        if re.match(r"^##\s+Design Readiness", line):
            in_section = True
            continue
        if in_section and re.match(r"^##\s+", line):
            break
        if in_section:
            section_lines.append(line)

    if not section_lines:
        print(f"FAIL missing_design_readiness_section: {file}")
        return 1

    statuses: dict[str, str] = {}
    for line in section_lines:
        if not line.startswith("|"):
            continue
        if re.match(r"^\|[-\s|]+\|$", line):
            continue
        parts = [p.strip() for p in line.strip("|").split("|")]
        if len(parts) < 2:
            continue
        col1, col2 = parts[0].lower(), parts[1].lower()
        for key, _ in DESIGN_CHECKPOINTS:
            if key in col1:
                statuses[key] = col2

    failed = 0
    for key, label in DESIGN_CHECKPOINTS:
        if key not in statuses:
            print(f"FAIL missing_checkpoint({label}): {file}")
            failed += 1

    if failed:
        return 1

    if not allow_open:
        open_count = sum(1 for v in statuses.values() if "open" in v)
        if open_count:
            print(f"FAIL open_checkpoints={open_count}: {file}")
            return 1

    print(f"PASS design_readiness: {file}")
    return 0


def design_check_cmd(args: argparse.Namespace) -> int:
    allow_open = args.allow_open
    failures = 0
    for doc in args.docs:
        rc = _design_check_file(Path(doc), allow_open)
        if rc != 0:
            failures += 1
    if failures:
        print(f"design_readiness_check=failed count={failures}")
        return 1
    print("design_readiness_check=passed")
    return 0


# ---------------------------------------------------------------------------
# check command
# ---------------------------------------------------------------------------

def check_cmd(args: argparse.Namespace) -> int:
    tools = ["python3", "node", "npm", "npx", "chromium", "chromium-browser",
             "google-chrome", "pandoc", "wkhtmltopdf", "mmdc"]
    found = {t: p for t in tools if (p := which(t))}

    has_puppeteer = False
    if found.get("node"):
        code, out = run_capture([
            "node", "-e",
            "try{require.resolve('puppeteer');console.log('yes')}catch(e)"
            "{try{require.resolve('puppeteer-core');console.log('yes')}catch(e2){console.log('no')}}",
        ])
        has_puppeteer = code == 0 and out.strip() == "yes"

    agent_paths = {
        "claude": Path.home() / ".claude" / "CLAUDE.md",
        "codex": Path.home() / ".codex" / "AGENTS.md",
        "kiro": Path.home() / ".kiro" / "specs" / "polyagent-skills.md",
        "gemini": Path.home() / ".gemini" / "instructions.md",
        "openclaw_skills": Path.home() / ".openclaw" / "skills",
        "global_skills": Path.home() / ".polyagent-skills" / "skills",
    }
    agents = {k: str(v) for k, v in agent_paths.items() if v.exists()}

    payload: dict = {"tools": found, "has_puppeteer": has_puppeteer, "agents": agents}

    strict_fail = False
    if args.strict:
        project = Path(args.project).resolve() if args.project else Path.cwd()
        strict_results = []

        # Gate check
        todo = project / "agent.todo.md"
        with tempfile.TemporaryDirectory() as _td:
            import io
            from contextlib import redirect_stdout
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = _gate_check(todo)
            strict_results.append({"check": "gate-status", "rc": rc})
            if rc not in (0, 2):  # 2 = no gates section (not an error for strict)
                strict_fail = True

        # Design readiness check
        dr_docs = [
            project / "skills/requirement-study/references/requirement-template.md",
            project / "docs/specs/SPEC_TEMPLATE.md",
        ]
        dr_docs_exist = [str(d) for d in dr_docs if d.exists()]
        if dr_docs_exist:
            import io
            from contextlib import redirect_stdout
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = sum(_design_check_file(Path(d), allow_open=True) for d in dr_docs_exist)
            rc = 0 if rc == 0 else 1
            strict_results.append({"check": "design-readiness", "rc": rc})
            if rc != 0:
                strict_fail = True
        else:
            strict_results.append({"check": "design-readiness", "rc": 0})

        payload["strict_results"] = strict_results

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print("polyagentctl check")
        print()
        print("Tools:")
        for t in tools:
            if t in found:
                print(f"  - {t}: {found[t]}")
        print(f"  - puppeteer: {'yes' if has_puppeteer else 'no'}")
        print()
        print("Agent paths:")
        for k, v in agent_paths.items():
            print(f"  - {k}: {'present' if v.exists() else 'missing'} ({v})")
        if args.strict and "strict_results" in payload:
            print()
            print("Strict checks:")
            for item in payload["strict_results"]:
                status = "PASS" if item["rc"] == 0 else "FAIL"
                print(f"  - {item['check']}: {status} (rc={item['rc']})")

    return 1 if strict_fail else 0


# ---------------------------------------------------------------------------
# sync-todo command (sync-agent-todo.sh)
# ---------------------------------------------------------------------------

def _extract_req_rows(req_file: Path) -> list[str]:
    text = req_file.read_text(encoding="utf-8")
    rows = []
    current_id = ""
    current_title = ""
    for line in text.splitlines():
        m = re.match(r"^\*\*\[REQ-(\d+)\]\*\*", line)
        if m:
            if current_id:
                title = current_title or f"Requirement REQ-{current_id}"
                rows.append(f"| REQ-{current_id} | {title} | (create issue) | Open | [owner] |")
            current_id = m.group(1)
            current_title = ""
            continue
        if current_id and line.startswith("**Title:**"):
            current_title = line.removeprefix("**Title:**").strip()
    if current_id:
        title = current_title or f"Requirement REQ-{current_id}"
        rows.append(f"| REQ-{current_id} | {title} | (create issue) | Open | [owner] |")
    return rows


def _extract_design_rows(spec_file: Path) -> list[str]:
    text = spec_file.read_text(encoding="utf-8")
    rows = []
    in_section = False
    for line in text.splitlines():
        if re.match(r"^##\s+Design Readiness", line):
            in_section = True
            continue
        if in_section and re.match(r"^##\s+", line):
            break
        if in_section and line.startswith("|"):
            if re.match(r"^\|[-\s|]+\|$", line):
                continue
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) >= 2 and parts[0] and parts[0] != "Checkpoint":
                rows.append(f"| {parts[0]} | {parts[1]} | {spec_file} |")
    return rows


def sync_todo_cmd(args: argparse.Namespace) -> int:
    todo_file = Path(args.todo_file)
    req_file = Path(args.req_file)
    spec_file = Path(args.spec_file) if args.spec_file else None

    for f, name in [(todo_file, "todo"), (req_file, "requirements")]:
        if not f.exists():
            print(f"error={name}_file_not_found path={f}", file=sys.stderr)
            return 1
    if spec_file and not spec_file.exists():
        print(f"error=spec_file_not_found path={spec_file}", file=sys.stderr)
        return 1

    now_utc = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    today = datetime.date.today().isoformat()

    req_rows = _extract_req_rows(req_file)
    req_section = "\n".join(req_rows) if req_rows else "| (none) | | | | |"

    if spec_file:
        dr_rows = _extract_design_rows(spec_file)
        dr_section = "\n".join(dr_rows) if dr_rows else f"| (no design readiness table found) | Open | {spec_file} |"
        spec_line = f"- Spec Source: {spec_file}"
    else:
        dr_section = "| (spec not provided) | Open | - |"
        spec_line = "- Spec Source: (not provided)"

    block = (
        "<!-- BEGIN AUTO-SYNC -->\n"
        "## Auto-Synced Traceability (Managed)\n\n"
        f"- Synced At (UTC): {now_utc}\n"
        f"- Requirements Source: {req_file}\n"
        f"{spec_line}\n\n"
        "### Requirements Snapshot\n\n"
        "| Requirement ID | Title | GitHub Issue | Status | Owner |\n"
        "|----------------|-------|--------------|--------|-------|\n"
        f"{req_section}\n\n"
        "### Design Readiness Snapshot\n\n"
        "| Checkpoint | Status | Source |\n"
        "|------------|--------|--------|\n"
        f"{dr_section}\n\n"
        "<!-- END AUTO-SYNC -->"
    )

    text = todo_file.read_text(encoding="utf-8")
    if "<!-- BEGIN AUTO-SYNC -->" in text:
        text = re.sub(
            r"<!-- BEGIN AUTO-SYNC -->.*?<!-- END AUTO-SYNC -->",
            block,
            text,
            flags=re.DOTALL,
        )
    else:
        text = text.rstrip() + "\n\n" + block + "\n"

    text = re.sub(r"^- Last Updated: .*$", f"- Last Updated: {today}", text, flags=re.MULTILINE)
    todo_file.write_text(text, encoding="utf-8")
    print(f"synced_todo={todo_file}")
    return 0


# ---------------------------------------------------------------------------
# init-issues command (init-requirement-issues.sh)
# ---------------------------------------------------------------------------

def init_issues_cmd(args: argparse.Namespace) -> int:
    req_file = Path(args.req_file)
    repo = args.repo
    apply = args.apply

    if not req_file.exists():
        print(f"error=requirements_file_not_found path={req_file}", file=sys.stderr)
        return 1

    if apply and not which("gh"):
        print("error=gh_not_found; install GitHub CLI or run without --apply", file=sys.stderr)
        return 1

    pairs: list[tuple[str, str]] = []
    current_id = ""
    current_title = ""
    text = req_file.read_text(encoding="utf-8")
    for line in text.splitlines():
        m = re.match(r"^\*\*\[REQ-(\d+)\]\*\*", line)
        if m:
            if current_id:
                pairs.append((f"REQ-{current_id}", current_title or f"Requirement REQ-{current_id}"))
            current_id = m.group(1)
            current_title = ""
            continue
        if current_id and line.startswith("**Title:**"):
            current_title = line.removeprefix("**Title:**").strip()
    if current_id:
        pairs.append((f"REQ-{current_id}", current_title or f"Requirement REQ-{current_id}"))

    if not pairs:
        print(f"warning=no_req_ids_found in {req_file}")
        return 0

    for req_id, req_title in pairs:
        issue_title = f"{req_id}: {req_title}"
        issue_body = (
            f"Auto-generated from requirement document.\n\n"
            f"- Requirement ID: {req_id}\n"
            f"- Source file: {req_file}\n\n"
            "Please add acceptance criteria, labels, and milestone."
        )
        if apply:
            run(["gh", "issue", "create", "--repo", repo,
                 "--title", issue_title, "--body", issue_body, "--label", "type:req"])
        else:
            print(f"gh issue create --repo {repo!r} --title {issue_title!r} --label type:req")

    print(f"parsed_requirements={len(pairs)} mode={'apply' if apply else 'dry-run'}")
    return 0


# ---------------------------------------------------------------------------
# sync-adapters command
# ---------------------------------------------------------------------------

def sync_adapters_cmd(args: argparse.Namespace) -> int:
    skills_dir = REPO_DIR / "skills"
    print("=== Syncing adapters with skill library ===")

    skill_list: list[str] = []
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            print(f"  Warning: No SKILL.md in {skill_dir.name}, skipping")
            continue
        _, description = _parse_skill_frontmatter(skill_md)
        if not description:
            description = "(no description)"
        description = description[:80]
        skill_list.append(f"- `skills/{skill_dir.name}/` — {description}")
        print(f"  Found: {skill_dir.name}")

    print()
    print(f"Skills found: {len(skill_list)}")
    print()
    print("Generated skill list:")
    print("---")
    for line in skill_list:
        print(line)
    print("---")
    print()

    if not args.print_only:
        adapters = [
            REPO_DIR / "adapters/claude-code/CLAUDE.md",
            REPO_DIR / "adapters/codex/AGENTS.md",
            REPO_DIR / "adapters/kiro/.kiro/specs/polyagent-skills.md",
        ]
        skill_block = "\n".join(skill_list)
        updated = 0
        for adapter in adapters:
            if not adapter.exists():
                continue
            text = adapter.read_text(encoding="utf-8")
            # Replace the skills block between the first "- `skills/" line and the next empty line or "## "
            new_text = re.sub(
                r"(- `skills/.*?\n)+",
                skill_block + "\n",
                text,
                count=1,
                flags=re.DOTALL,
            )
            if new_text != text:
                adapter.write_text(new_text, encoding="utf-8")
                print(f"  Updated: {adapter.relative_to(REPO_DIR)}")
                updated += 1
        print(f"Updated {updated} adapter(s).")
    else:
        print("Copy the above into each adapter's 'Available Skills' section.")
    return 0


# ---------------------------------------------------------------------------
# pull-skill command (pull-skill.sh)
# ---------------------------------------------------------------------------

def pull_skill_cmd(args: argparse.Namespace) -> int:
    skill_input = args.skill
    if skill_input.startswith("http"):
        skill_url = skill_input
        skill_name = Path(skill_input).stem
    else:
        skill_name = skill_input
        skill_url = f"https://skills.sh/download/{skill_name}.skill"

    dest = REPO_DIR / "skills" / skill_name
    print("=== Pull skill from skills.sh ===")
    print(f"Skill:       {skill_name}")
    print(f"Destination: {dest}")
    print()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        skill_file = tmp / f"{skill_name}.skill"

        print("Downloading...")
        try:
            urllib.request.urlretrieve(skill_url, str(skill_file))
        except Exception as e:
            print(f"Error: Could not download from {skill_url}: {e}")
            print(f"You may need to download manually and place in {dest}/")
            return 1

        print("Extracting...")
        extracted = tmp / "extracted"
        extracted.mkdir()
        try:
            with zipfile.ZipFile(str(skill_file)) as zf:
                zf.extractall(str(extracted))
        except zipfile.BadZipFile:
            print("Note: File may not be a ZIP. Treating as plain SKILL.md.")
            shutil.copy2(str(skill_file), str(extracted / "SKILL.md"))

        print(f"Installing to {dest}...")
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "references").mkdir(exist_ok=True)
        shutil.copytree(str(extracted), str(dest), dirs_exist_ok=True)

        print()
        print("=== Portability Check ===")
        issues = 0
        skill_md = dest / "SKILL.md"
        if skill_md.exists():
            content = skill_md.read_text(encoding="utf-8")
            if re.search(r"(</?(tool|function|artifact|antml))|(/slash-command)|(@file)", content, re.I):
                print("Warning: Found potential Claude-specific syntax in SKILL.md")
                issues += 1
            if re.search(r"(/mnt/|/home/|/tmp/|C:\\)", content):
                print("Warning: Found absolute paths in SKILL.md")
                issues += 1
            if not content.startswith("---"):
                print("Warning: Missing YAML frontmatter")
                issues += 1
        if issues == 0:
            print("No portability issues detected")
        else:
            print(f"{issues} issue(s) found — review {dest}/SKILL.md before using")

    print()
    print("=== Done ===")
    print(f"Skill installed at: {dest}/")
    print("Run: polyagentctl.py sync-adapters to update adapter files.")
    return 0


# ---------------------------------------------------------------------------
# verify-context-pack command (verify-context-pack.sh)
# ---------------------------------------------------------------------------

REQUIRED_SECTIONS = [
    r"^## Session Start$",
    r"^## Context Snapshot$",
    r"^## Goals and Non-Goals$",
    r"^## Active Decisions$",
    r"^## Architecture and Runtime$",
    r"^## Data and Storage$",
    r"^## Observability Baseline$",
    r"^## Design Readiness$",
    r"^## Current Execution Plan$",
    r"^## Open Questions and Risks$",
    r"^## Traceability$",
]

DESIGN_PACK_CHECKPOINTS = [
    "Architecture pattern",
    "Language/runtime",
    "Database strategy",
    "Logging/observability baseline",
]


def verify_context_pack_cmd(args: argparse.Namespace) -> int:
    pack = Path(args.pack)
    if not pack.exists():
        print(f"FAIL file_not_found: {pack}")
        return 1

    text = pack.read_text(encoding="utf-8")
    failures = 0

    for pattern in REQUIRED_SECTIONS:
        if not re.search(pattern, text, re.MULTILINE):
            print(f"FAIL missing_section pattern={pattern} file={pack}")
            failures += 1

    for checkpoint in DESIGN_PACK_CHECKPOINTS:
        if checkpoint not in text:
            print(f'FAIL missing_design_checkpoint checkpoint="{checkpoint}" file={pack}')
            failures += 1

    if not re.search(r"REQ-\d+|missing requirements", text, re.IGNORECASE):
        print(f"FAIL missing_traceability_signal file={pack}")
        failures += 1

    if failures:
        print(f"context_pack_verification=failed count={failures}")
        return 1

    print(f"context_pack_verification=passed file={pack}")
    return 0


# ---------------------------------------------------------------------------
# export-pdf command
# ---------------------------------------------------------------------------

def _esc(s: str) -> str:
    return html_mod.escape(s, quote=True)


def _render_flowchart(code: str) -> str | None:
    lines = [ln.strip() for ln in code.splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("flowchart"):
        return None
    first = lines[0].split()
    direction = first[1] if len(first) > 1 else "TD"
    node_labels: dict[str, str] = {}
    node_order: list[str] = []
    edges: list[tuple[str, str]] = []
    node_re = re.compile(r"^([A-Za-z0-9_]+)\[(.*?)\]$")
    edge_re = re.compile(r"^([A-Za-z0-9_]+)(?:\[(.*?)\])?\s*-->\s*([A-Za-z0-9_]+)(?:\[(.*?)\])?$")

    def ensure(nid: str, label: str | None = None) -> None:
        if nid not in node_labels:
            node_labels[nid] = label or nid
            node_order.append(nid)
        elif label:
            node_labels[nid] = label

    for ln in lines[1:]:
        m = edge_re.match(ln)
        if m:
            a, al, b, bl = m.groups()
            ensure(a, al); ensure(b, bl); edges.append((a, b))
            continue
        m = node_re.match(ln)
        if m:
            ensure(m.group(1), m.group(2))
    if not node_order:
        return None
    W, H, G = 220, 56, 44
    horiz = direction in ("LR", "RL")
    coords = {nid: (50 + i * (W + G), 60) if horiz else (60, 40 + i * (H + G)) for i, nid in enumerate(node_order)}
    sw = max(420, 100 + len(node_order) * (W + G)) if horiz else 420
    sh = 200 if horiz else max(220, 100 + len(node_order) * (H + G))
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{sw}" height="{sh}" viewBox="0 0 {sw} {sh}">',
         '<defs><marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#4b5563"/></marker></defs>',
         '<rect x="0" y="0" width="100%" height="100%" fill="#ffffff"/>']
    for a, b in edges:
        ax, ay = coords[a]; bx, by = coords[b]
        x1, y1 = (ax + W, ay + H // 2) if horiz else (ax + W // 2, ay + H)
        x2, y2 = (bx, by + H // 2) if horiz else (bx + W // 2, by)
        p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#4b5563" stroke-width="2" marker-end="url(#arr)"/>')
    for nid in node_order:
        x, y = coords[nid]
        p.append(f'<rect x="{x}" y="{y}" rx="8" ry="8" width="{W}" height="{H}" fill="#f8fafc" stroke="#334155"/>')
        p.append(f'<text x="{x + W/2}" y="{y + H/2 + 4}" text-anchor="middle" font-size="13" font-family="Arial" fill="#111827">{_esc(node_labels[nid])}</text>')
    p.append("</svg>")
    return "".join(p)


def _render_er(code: str) -> str | None:
    lines = [ln.strip() for ln in code.splitlines() if ln.strip()]
    if not lines or lines[0] != "erDiagram":
        return None
    rel_re = re.compile(r"^([A-Za-z0-9_]+)\s+\S+\s+([A-Za-z0-9_]+)\s*:\s*(.+)$")
    entities: list[str] = []
    rels: list[tuple[str, str, str]] = []
    for ln in lines[1:]:
        m = rel_re.match(ln)
        if not m:
            continue
        a, b, label = m.groups()
        for e in (a, b):
            if e not in entities:
                entities.append(e)
        rels.append((a, b, label))
    if not entities:
        return None
    W, H, CG, RG, COLS = 220, 54, 120, 50, 2
    coords = {e: (60 + (i % COLS) * (W + CG), 40 + (i // COLS) * (H + RG)) for i, e in enumerate(entities)}
    rows = (len(entities) + COLS - 1) // COLS
    sw = 60 + COLS * W + (COLS - 1) * CG + 60
    sh = 60 + rows * H + (rows - 1) * RG + 60
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{sw}" height="{sh}" viewBox="0 0 {sw} {sh}">',
         '<rect x="0" y="0" width="100%" height="100%" fill="#ffffff"/>']
    for a, b, label in rels:
        ax, ay = coords[a]; bx, by = coords[b]
        x1, y1, x2, y2 = ax + W/2, ay + H/2, bx + W/2, by + H/2
        mx, my = (x1+x2)/2, (y1+y2)/2
        p.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#4b5563" stroke-width="2"/>')
        p.append(f'<text x="{mx}" y="{my-6}" text-anchor="middle" font-size="12" font-family="Arial" fill="#374151">{_esc(label)}</text>')
    for e in entities:
        x, y = coords[e]
        p.append(f'<rect x="{x}" y="{y}" rx="8" ry="8" width="{W}" height="{H}" fill="#f8fafc" stroke="#334155"/>')
        p.append(f'<text x="{x + W/2}" y="{y + H/2 + 4}" text-anchor="middle" font-size="13" font-family="Arial" fill="#111827">{_esc(e)}</text>')
    p.append("</svg>")
    return "".join(p)


def _render_sequence(code: str) -> str | None:
    lines = [ln.strip() for ln in code.splitlines() if ln.strip()]
    if not lines or lines[0] != "sequenceDiagram":
        return None

    participants: list[str] = []
    messages: list[tuple[str, str, str, bool]] = []

    def ensure(name: str) -> None:
        if name not in participants:
            participants.append(name)

    msg_re = re.compile(r"^(.+?)\s*(-->>|->>|-->|->|-x|--x)\s*(.+?)\s*:\s*(.*)$")
    for ln in lines[1:]:
        low = ln.lower()
        if low.startswith("participant ") or low.startswith("actor "):
            ensure(ln.split(None, 1)[1].strip())
            continue
        m = msg_re.match(ln)
        if m:
            frm, arrow, to, label = m.group(1).strip(), m.group(2), m.group(3).strip(), m.group(4).strip()
            ensure(frm)
            ensure(to)
            messages.append((frm, to, label, arrow.startswith("--")))

    if not participants:
        return None

    BW, BH, GAP = 120, 36, 80
    TOP, MSG_H = 20, 44
    n = len(participants)
    total_w = max(300, 40 + n * (BW + GAP))
    total_h = TOP + BH + max(1, len(messages)) * MSG_H + 40
    cx = {p: 20 + i * (BW + GAP) + BW // 2 for i, p in enumerate(participants)}
    line_y0 = TOP + BH
    line_y1 = total_h - 20

    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="{total_h}" viewBox="0 0 {total_w} {total_h}">',
        '<defs><marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">'
        '<polygon points="0 0, 10 3.5, 0 7" fill="#4b5563"/></marker></defs>',
        '<rect x="0" y="0" width="100%" height="100%" fill="#ffffff"/>',
    ]
    for name in participants:
        x = cx[name] - BW // 2
        svg.append(f'<rect x="{x}" y="{TOP}" rx="4" ry="4" width="{BW}" height="{BH}" fill="#f8fafc" stroke="#334155"/>')
        svg.append(f'<text x="{cx[name]}" y="{TOP + BH // 2 + 5}" text-anchor="middle" font-size="12" font-family="Arial" fill="#111827">{_esc(name)}</text>')
        svg.append(f'<line x1="{cx[name]}" y1="{line_y0}" x2="{cx[name]}" y2="{line_y1}" stroke="#94a3b8" stroke-width="1" stroke-dasharray="4 3"/>')
    for i, (frm, to, label, dashed) in enumerate(messages):
        y = line_y0 + (i + 0.7) * MSG_H
        x1, x2 = cx[frm], cx[to]
        dash = ' stroke-dasharray="6 3"' if dashed else ''
        svg.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="#4b5563" stroke-width="1.5"{dash} marker-end="url(#arr)"/>')
        svg.append(f'<text x="{(x1 + x2) / 2}" y="{y - 5}" text-anchor="middle" font-size="11" font-family="Arial" fill="#374151">{_esc(label)}</text>')
    svg.append("</svg>")
    return "".join(svg)


def _mermaid_ink_img(code: str) -> str:
    """Render Mermaid code via static mermaid.ink image URL (URL-safe base64, no padding)."""
    encoded = base64.urlsafe_b64encode(code.encode("utf-8")).decode("ascii").rstrip("=")
    src = f"https://mermaid.ink/img/{urllib.parse.quote(encoded, safe='-_')}"
    return (
        "\n"
        f'<div class="diagram diagram-image"><img src="{src}" alt="Mermaid diagram" loading="eager"/></div>'
        "\n"
    )


def _replace_mermaid_blocks(markdown: str) -> str:
    def repl(m: re.Match[str]) -> str:
        code = m.group(1).strip()
        svg = _render_flowchart(code) or _render_er(code) or _render_sequence(code)
        if svg:
            return f'\n<div class="diagram">{svg}</div>\n'
        # Unknown diagram type: fall back to static image rendering.
        return _mermaid_ink_img(code)

    result = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL).sub(repl, markdown)
    return result


def _render_to_html(source: str) -> str:
    source = _replace_mermaid_blocks(source)
    try:
        from markdown_it import MarkdownIt
        md = MarkdownIt("default", {"html": True, "typographer": True})
        body = md.render(source)
    except ImportError:
        # Keep embedded HTML (diagrams/images) visible even without markdown-it.
        body = source
    return f"""<!doctype html>
<html>
<head><meta charset="utf-8"/><title>Document Export</title>
<style>
body{{font-family:Arial,sans-serif;margin:28px;color:#111;line-height:1.5}}
h1,h2,h3{{margin-top:1.2em;margin-bottom:.5em}}
h1{{border-bottom:1px solid #ddd;padding-bottom:.25em}}
code{{background:#f6f8fa;padding:.1em .3em;border-radius:4px}}
pre{{background:#f6f8fa;border:1px solid #e5e7eb;border-radius:6px;padding:12px;font-size:12px;overflow-x:auto}}
pre code{{background:transparent;padding:0}}
table{{border-collapse:collapse;width:100%;margin:12px 0;font-size:12px}}
th,td{{border:1px solid #d0d7de;padding:6px 8px;text-align:left;vertical-align:top}}
th{{background:#f6f8fa}}
blockquote{{border-left:4px solid #d0d7de;margin:0;padding-left:12px;color:#57606a}}
.diagram{{margin:12px 0 20px;padding:10px;border:1px solid #e5e7eb;border-radius:8px;background:#fff}}
.diagram svg{{max-width:100%;height:auto}}
.diagram-image img{{max-width:100%;height:auto;display:block;margin:0 auto}}
</style></head>
<body>{body}</body></html>"""


def _write_temp_html(html_content: str) -> tuple[Path, Path]:
    """Write export HTML to a stable absolute temp directory and return (dir, html_path)."""
    tmp_dir = Path(tempfile.mkdtemp(prefix="polyagentctl-export-"))
    tmp_html = tmp_dir / "source.html"
    tmp_html.write_text(html_content, encoding="utf-8")
    return tmp_dir, tmp_html


def export_pdf_cmd(args: argparse.Namespace) -> int:
    input_md = Path(args.input_md)
    if not input_md.exists():
        print(f"Error: File not found: {input_md}", file=sys.stderr)
        return 1

    force_html = args.html
    if args.output:
        output = Path(args.output)
    else:
        output = input_md.with_suffix(".html" if force_html else ".pdf")

    output.parent.mkdir(parents=True, exist_ok=True)
    source = input_md.read_text(encoding="utf-8")
    html_content = _render_to_html(source)

    if force_html:
        output.write_text(html_content, encoding="utf-8")
        print(f"HTML written: {output}")
        return 0

    tmp_dir, tmp_html = _write_temp_html(html_content)
    tmp_url = tmp_html.resolve().as_uri()
    try:
        # Try PDF via wkhtmltopdf
        if which("wkhtmltopdf"):
            rc = run(["wkhtmltopdf", "--quiet", str(tmp_html.resolve()), str(output)])
            if rc == 0:
                print(f"PDF written: {output}")
                return 0

        # Try PDF via headless Chromium
        for browser in ("chromium", "chromium-browser", "google-chrome", "google-chrome-stable"):
            if which(browser):
                rc = run([
                    browser,
                    "--headless",
                    "--disable-gpu",
                    "--no-sandbox",
                    "--allow-file-access-from-files",
                    f"--print-to-pdf={output}",
                    tmp_url,
                ])
                if rc == 0:
                    print(f"PDF written: {output}")
                    return 0
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    # Fallback: write HTML
    html_out = output.with_suffix(".html")
    html_out.write_text(html_content, encoding="utf-8")
    print(f"No PDF tool found (wkhtmltopdf/chromium). HTML written: {html_out}")
    return 0


# ---------------------------------------------------------------------------
# self-install command
# ---------------------------------------------------------------------------

def self_install_cmd(args: argparse.Namespace) -> int:
    target = Path(args.path).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SCRIPT_DIR / "polyagentctl.py", target)
    target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"Installed: {target}")
    return 0


def _self_install_default() -> Path:
    target = (Path.home() / ".local/bin/polyagentctl").resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SCRIPT_DIR / "polyagentctl.py", target)
    target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return target


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="polyagentctl", description="polyagent unified tooling CLI")
    sub = p.add_subparsers(dest="command", required=True)

    # check
    check = sub.add_parser("check", help="check local tooling and agent environment")
    check.add_argument("--json", action="store_true")
    check.add_argument("--strict", action="store_true", help="run gate and design-readiness checks")
    check.add_argument("--project", help="project path for strict checks (default: cwd)")
    check.set_defaults(func=check_cmd)

    # install-global
    ig = sub.add_parser("install-global", help="install skills and agent configs globally")
    ig.add_argument("mode", nargs="?", choices=["copy", "link"], default="copy")
    ig.set_defaults(func=install_global_cmd)

    # uninstall-global
    ug = sub.add_parser("uninstall-global", help="remove manifest-managed global install")
    ug.add_argument("--dry-run", action="store_true")
    ug.set_defaults(func=uninstall_global_cmd)

    # install-project
    ip = sub.add_parser("install-project", help="install into a project directory")
    ip.add_argument("project_path")
    ip.add_argument("agent", nargs="?", default="all")
    ip.set_defaults(func=install_project_cmd)

    # gate-check
    gc = sub.add_parser("gate-check", help="check development lifecycle gate status")
    gc.add_argument("todo_file", nargs="?", default="agent.todo.md")
    gc.set_defaults(func=gate_check_cmd)

    # design-check
    dc = sub.add_parser("design-check", help="validate design readiness sections in docs")
    dc.add_argument("--allow-open", action="store_true", help="pass even if checkpoints are Open")
    dc.add_argument("docs", nargs="+")
    dc.set_defaults(func=design_check_cmd)

    # sync-todo
    st = sub.add_parser("sync-todo", help="sync traceability block in agent.todo.md")
    st.add_argument("todo_file")
    st.add_argument("req_file")
    st.add_argument("spec_file", nargs="?", default="")
    st.set_defaults(func=sync_todo_cmd)

    # init-issues
    ii = sub.add_parser("init-issues", help="create GitHub issues from REQ IDs")
    ii.add_argument("req_file")
    ii.add_argument("repo", help="owner/repo")
    ii.add_argument("--apply", action="store_true", help="actually create issues (default: dry-run)")
    ii.set_defaults(func=init_issues_cmd)

    # sync-adapters
    sa = sub.add_parser("sync-adapters", help="regenerate skill lists in adapter files")
    sa.add_argument("--print-only", action="store_true", help="print list without modifying files")
    sa.set_defaults(func=sync_adapters_cmd)

    # pull-skill
    ps = sub.add_parser("pull-skill", help="download a skill from skills.sh")
    ps.add_argument("skill", help="skill name or URL")
    ps.set_defaults(func=pull_skill_cmd)

    # verify-context-pack
    vc = sub.add_parser("verify-context-pack", help="validate context pack structure")
    vc.add_argument("pack")
    vc.set_defaults(func=verify_context_pack_cmd)

    # export-pdf
    pdf = sub.add_parser("export-pdf", help="convert markdown to PDF or HTML")
    pdf.add_argument("input_md")
    pdf.add_argument("output", nargs="?")
    pdf.add_argument("--html", action="store_true", help="force HTML output")
    pdf.set_defaults(func=export_pdf_cmd)

    # doctor
    dr = sub.add_parser("doctor", help="check prerequisites and optionally install missing tools")
    dr.add_argument("--fix", action="store_true", help="interactively install missing optional tools")
    dr.set_defaults(func=doctor_cmd)

    # self-install
    si = sub.add_parser("self-install", help="install polyagentctl to a reusable path")
    si.add_argument("--path", default="~/.local/bin/polyagentctl")
    si.set_defaults(func=self_install_cmd)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
