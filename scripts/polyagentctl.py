#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_DIR = SCRIPT_DIR.parent


def run(cmd: list[str], cwd: Path | None = None) -> int:
    proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None)
    return proc.returncode


def run_capture(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return proc.returncode, proc.stdout.strip()


def which(name: str) -> str | None:
    return shutil.which(name)


def check_cmd(args: argparse.Namespace) -> int:
    tools = [
        "python3",
        "node",
        "npm",
        "npx",
        "chromium",
        "chromium-browser",
        "google-chrome",
        "pandoc",
        "wkhtmltopdf",
        "mmdc",
    ]
    found = {}
    for t in tools:
        p = which(t)
        if p:
            found[t] = p

    has_puppeteer = False
    if found.get("node"):
        code, out = run_capture(
            [
                "node",
                "-e",
                "try{require.resolve('puppeteer');console.log('yes')}catch(e){try{require.resolve('puppeteer-core');console.log('yes')}catch(e2){console.log('no')}}",
            ]
        )
        has_puppeteer = code == 0 and out.strip() == "yes"

    agent_paths = {
        "codex": Path.home() / ".codex" / "AGENTS.md",
        "kiro": Path.home() / ".kiro" / "specs" / "polyagent-skills.md",
        "gemini": Path.home() / ".gemini" / "instructions.md",
        "openclaw_skills": Path.home() / ".openclaw" / "skills",
        "global_skills": Path.home() / ".polyagent-skills" / "skills",
    }
    agents = {k: str(v) for k, v in agent_paths.items() if v.exists()}

    payload = {
        "tools": found,
        "has_puppeteer": has_puppeteer,
        "agents": agents,
    }

    strict_fail = False
    if args.strict:
        project = Path(args.project).resolve() if args.project else Path.cwd()
        gate_script = project / "scripts" / "gate-status-check.sh"
        dr_script = project / "scripts" / "design-readiness-check.sh"
        strict_results = []
        if gate_script.exists():
            rc = run([str(gate_script), "agent.todo.md"], cwd=project)
            strict_results.append({"check": "gate-status", "rc": rc})
            if rc != 0:
                strict_fail = True
        if dr_script.exists():
            rc = run(
                [
                    str(dr_script),
                    "--allow-open",
                    "skills/requirement-study/references/requirement-template.md",
                    "docs/specs/SPEC_TEMPLATE.md",
                ],
                cwd=project,
            )
            strict_results.append({"check": "design-readiness", "rc": rc})
            if rc != 0:
                strict_fail = True
        payload["strict_results"] = strict_results

    if args.json:
        print(json.dumps(payload, indent=2))
    else:
        print("polyagentctl check")
        print("")
        print("Tools:")
        for t in tools:
            if t in found:
                print(f"  - {t}: {found[t]}")
        print(f"  - puppeteer: {'yes' if has_puppeteer else 'no'}")
        print("")
        print("Agent paths:")
        for k, v in agent_paths.items():
            print(f"  - {k}: {'present' if v.exists() else 'missing'} ({v})")
        if args.strict and "strict_results" in payload:
            print("")
            print("Strict checks:")
            for item in payload["strict_results"]:
                status = "PASS" if item["rc"] == 0 else "FAIL"
                print(f"  - {item['check']}: {status} (rc={item['rc']})")

    return 1 if strict_fail else 0


def install_global_cmd(args: argparse.Namespace) -> int:
    return run([str(SCRIPT_DIR / "install-global-all.sh"), args.mode], cwd=REPO_DIR)


def uninstall_global_cmd(args: argparse.Namespace) -> int:
    cmd = [str(SCRIPT_DIR / "uninstall-global-all.sh")]
    if args.dry_run:
        cmd.append("--dry-run")
    return run(cmd, cwd=REPO_DIR)


def install_project_cmd(args: argparse.Namespace) -> int:
    agent = args.agent if args.agent else "all"
    return run(
        [str(SCRIPT_DIR / "install-to-project.sh"), args.project_path, agent],
        cwd=REPO_DIR,
    )


def export_pdf_cmd(args: argparse.Namespace) -> int:
    cmd = [str(SCRIPT_DIR / "md-to-pdf.sh")]
    if args.html:
        cmd.append("--html")
    cmd.append(args.input_md)
    if args.output:
        cmd.append(args.output)
    return run(cmd, cwd=Path.cwd())


def self_install_cmd(args: argparse.Namespace) -> int:
    target = Path(args.path).expanduser().resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SCRIPT_DIR / "polyagentctl.py", target)
    target.chmod(target.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    print(f"Installed: {target}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="polyagentctl", description="polyagent unified tooling CLI")
    sub = p.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="check local tooling and agent environment")
    check.add_argument("--json", action="store_true", help="emit JSON output")
    check.add_argument("--strict", action="store_true", help="run strict project checks")
    check.add_argument("--project", help="project path for strict checks (default: cwd)")
    check.set_defaults(func=check_cmd)

    ig = sub.add_parser("install-global", help="run global install")
    ig.add_argument("mode", nargs="?", choices=["copy", "link"], default="copy")
    ig.set_defaults(func=install_global_cmd)

    ip = sub.add_parser("install-project", help="install into a project")
    ip.add_argument("project_path")
    ip.add_argument("agent", nargs="?", default="all")
    ip.set_defaults(func=install_project_cmd)

    ug = sub.add_parser("uninstall-global", help="run global uninstall")
    ug.add_argument("--dry-run", action="store_true")
    ug.set_defaults(func=uninstall_global_cmd)

    pdf = sub.add_parser("export-pdf", help="convert markdown to PDF/HTML")
    pdf.add_argument("input_md")
    pdf.add_argument("output", nargs="?")
    pdf.add_argument("--html", action="store_true")
    pdf.set_defaults(func=export_pdf_cmd)

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
