import importlib.util
import io
import json
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


REPO_ROOT = Path(__file__).resolve().parents[1]
POLYAGENTCTL_PATH = REPO_ROOT / "scripts" / "polyagentctl.py"


def load_polyagentctl_module():
    spec = importlib.util.spec_from_file_location("polyagentctl", POLYAGENTCTL_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


class PolyagentCtlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_polyagentctl_module()

    def test_build_parser(self):
        parser = self.mod.build_parser()
        args = parser.parse_args(["check", "--json"])
        self.assertEqual(args.command, "check")
        self.assertTrue(callable(args.func))

    def test_check_json_direct(self):
        args = SimpleNamespace(json=True, strict=False, project=None)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = self.mod.check_cmd(args)
        self.assertEqual(rc, 0)
        payload = json.loads(buf.getvalue())
        self.assertIn("tools", payload)
        self.assertIn("agents", payload)
        self.assertIn("has_puppeteer", payload)

    def test_check_strict_direct(self):
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td)
            (proj / "agent.todo.md").write_text("## Gate Status\n", encoding="utf-8")

            args = SimpleNamespace(json=True, strict=True, project=str(proj))
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = self.mod.check_cmd(args)
            self.assertEqual(rc, 0)
            payload = json.loads(buf.getvalue())
            self.assertIn("strict_results", payload)
            self.assertEqual(len(payload["strict_results"]), 2)




    def test_polyagentctl_is_standalone(self):
        """Script has shebang and __main__ guard — no shell wrapper needed."""
        src = POLYAGENTCTL_PATH.read_text(encoding="utf-8")
        self.assertTrue(src.startswith("#!/usr/bin/env python3"), "Missing shebang")
        self.assertIn('if __name__ == "__main__"', src, "Missing __main__ guard")

    def test_doctor_no_fix(self):
        args = SimpleNamespace(fix=False)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = self.mod.doctor_cmd(args)
        out = buf.getvalue()
        # python3 is always present; result line must appear
        self.assertIn("[OK]  Python 3", out)
        self.assertIn("Result:", out)
        # rc is 0 (python3 required; everything else optional)
        self.assertEqual(rc, 0)

    def test_install_global_native(self):
        with tempfile.TemporaryDirectory() as td:
            env = {
                "POLYAGENT_HOME": str(Path(td) / "polyagent-skills"),
                "OPENCLAW_HOME": str(Path(td) / "openclaw"),
            }
            with patch.dict(os.environ, env):
                # Patch Path.home() used inside install path builders
                with patch("pathlib.Path.home", return_value=Path(td)):
                    # Patch doctor_cmd to skip interactive prereq prompts in CI
                    with patch.object(self.mod, "doctor_cmd", return_value=0):
                        args = SimpleNamespace(mode="copy")
                        buf = io.StringIO()
                        with redirect_stdout(buf):
                            rc = self.mod.install_global_cmd(args)
            self.assertEqual(rc, 0)
            self.assertTrue((Path(td) / ".local/bin/polyagentctl").exists())

    def test_uninstall_global_dry_run(self):
        with tempfile.TemporaryDirectory() as td:
            env = {
                "POLYAGENT_HOME": str(Path(td) / "polyagent-skills"),
                "OPENCLAW_HOME": str(Path(td) / "openclaw"),
            }
            with patch.dict(os.environ, env):
                args = SimpleNamespace(dry_run=True)
                buf = io.StringIO()
                with redirect_stdout(buf):
                    rc = self.mod.uninstall_global_cmd(args)
            self.assertEqual(rc, 0)

    def test_install_project(self):
        with tempfile.TemporaryDirectory() as td:
            proj = Path(td) / "myproject"
            proj.mkdir()
            # Patch doctor_cmd to skip interactive prereq prompts in CI
            with patch.object(self.mod, "doctor_cmd", return_value=0):
                args = SimpleNamespace(project_path=str(proj), agent="claude-code")
                buf = io.StringIO()
                with redirect_stdout(buf):
                    rc = self.mod.install_project_cmd(args)
            self.assertEqual(rc, 0)
            self.assertTrue((proj / "CLAUDE.md").exists())
            self.assertTrue((proj / "skills").is_dir())

    def test_gate_check_no_section(self):
        with tempfile.TemporaryDirectory() as td:
            todo = Path(td) / "agent.todo.md"
            todo.write_text("# No gate section here\n", encoding="utf-8")
            args = SimpleNamespace(todo_file=str(todo))
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = self.mod.gate_check_cmd(args)
            self.assertEqual(rc, 2)

    def test_gate_check_with_gates(self):
        with tempfile.TemporaryDirectory() as td:
            todo = Path(td) / "agent.todo.md"
            todo.write_text(
                "## Gate Status\n\n"
                "| Gate | Name | Status | Evidence | Skip Reason |\n"
                "|------|------|--------|----------|-------------|\n"
                "| G0 | Discovery | Passed | done | |\n"
                "| G1 | Requirements | Passed | done | |\n"
                "| G2 | Design | Passed | done | |\n"
                "| G3 | POC/Spike | N/A | | |\n",
                encoding="utf-8",
            )
            args = SimpleNamespace(todo_file=str(todo))
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = self.mod.gate_check_cmd(args)
            self.assertEqual(rc, 0)

    def test_design_check(self):
        with tempfile.TemporaryDirectory() as td:
            doc = Path(td) / "spec.md"
            doc.write_text(
                "## Design Readiness\n\n"
                "| Checkpoint | Status |\n"
                "|---|---|\n"
                "| Architecture pattern | Decided |\n"
                "| Language/runtime | Python 3.11 |\n"
                "| Database strategy | SQLite |\n"
                "| Logging/observability baseline | structlog |\n",
                encoding="utf-8",
            )
            args = SimpleNamespace(allow_open=False, docs=[str(doc)])
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = self.mod.design_check_cmd(args)
            self.assertEqual(rc, 0)

    def test_verify_context_pack_missing_sections(self):
        with tempfile.TemporaryDirectory() as td:
            pack = Path(td) / "pack.md"
            pack.write_text("# Incomplete pack\n", encoding="utf-8")
            args = SimpleNamespace(pack=str(pack))
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = self.mod.verify_context_pack_cmd(args)
            self.assertNotEqual(rc, 0)

    def test_sync_todo(self):
        with tempfile.TemporaryDirectory() as td:
            todo = Path(td) / "agent.todo.md"
            todo.write_text("- Last Updated: 2026-01-01\n\n# Tasks\n", encoding="utf-8")
            req = Path(td) / "requirements.md"
            req.write_text(
                "**[REQ-001]** Functional\n**Title:** User login\n",
                encoding="utf-8",
            )
            args = SimpleNamespace(todo_file=str(todo), req_file=str(req), spec_file="")
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = self.mod.sync_todo_cmd(args)
            self.assertEqual(rc, 0)
            result = todo.read_text(encoding="utf-8")
            self.assertIn("REQ-001", result)
            self.assertIn("BEGIN AUTO-SYNC", result)

    def test_normalize_skill_markdown(self):
        with tempfile.TemporaryDirectory() as td:
            src = Path(td) / "SKILL.md"
            src.write_text(
                "---\nname: my-skill\ndescription: Does something useful\n---\n\n# Body\n",
                encoding="utf-8",
            )
            dst = Path(td) / "SKILL_out.md"
            self.mod._normalize_skill_markdown(src, dst, "fallback")
            out = dst.read_text(encoding="utf-8")
            self.assertIn("my-skill", out)
            self.assertIn("Does something useful", out)
            self.assertIn("# Body", out)

    def test_self_install(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "polyagentctl"
            rc = self.mod.self_install_cmd(SimpleNamespace(path=str(target)))
            self.assertEqual(rc, 0)
            self.assertTrue(target.exists())
            self.assertTrue(os.access(target, os.X_OK))

    def test_self_install_also_installs_md_to_pdf(self):
        """self-install copies md-to-pdf companion script alongside polyagentctl."""
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "polyagentctl"
            rc = self.mod.self_install_cmd(SimpleNamespace(path=str(target)))
            self.assertEqual(rc, 0)
            md_to_pdf = Path(td) / "md-to-pdf"
            self.assertTrue(md_to_pdf.exists())
            self.assertTrue(os.access(md_to_pdf, os.X_OK))




    def test_check_plain_text(self):
        """check_cmd without --json prints human-readable tool status."""
        args = SimpleNamespace(json=False, strict=False, project=None)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = self.mod.check_cmd(args)
        out = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("python3", out.lower())

    def test_gate_check_failed_gate(self):
        """gate_check_cmd returns 1 when a required gate is Failed."""
        with tempfile.TemporaryDirectory() as td:
            todo = Path(td) / "agent.todo.md"
            todo.write_text(
                "## Gate Status\n\n"
                "| Gate | Name | Status | Evidence | Skip Reason |\n"
                "|------|------|--------|----------|-------------|\n"
                "| G0 | Discovery | Failed | | |\n",
                encoding="utf-8",
            )
            args = SimpleNamespace(todo_file=str(todo))
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = self.mod.gate_check_cmd(args)
            self.assertEqual(rc, 1)

    def test_design_check_open_allow(self):
        """design_check_cmd passes with Open checkpoints when --allow-open set."""
        with tempfile.TemporaryDirectory() as td:
            doc = Path(td) / "spec.md"
            doc.write_text(
                "## Design Readiness\n\n"
                "| Checkpoint | Status |\n"
                "|---|---|\n"
                "| Architecture pattern | Open |\n"
                "| Language/runtime | Open |\n"
                "| Database strategy | Open |\n"
                "| Logging/observability baseline | Open |\n",
                encoding="utf-8",
            )
            args = SimpleNamespace(allow_open=True, docs=[str(doc)])
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = self.mod.design_check_cmd(args)
            self.assertEqual(rc, 0)

    def test_design_check_open_no_allow(self):
        """design_check_cmd fails with Open checkpoints when --allow-open not set."""
        with tempfile.TemporaryDirectory() as td:
            doc = Path(td) / "spec.md"
            doc.write_text(
                "## Design Readiness\n\n"
                "| Checkpoint | Status |\n"
                "|---|---|\n"
                "| Architecture pattern | Open |\n"
                "| Language/runtime | Open |\n"
                "| Database strategy | Open |\n"
                "| Logging/observability baseline | Open |\n",
                encoding="utf-8",
            )
            args = SimpleNamespace(allow_open=False, docs=[str(doc)])
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = self.mod.design_check_cmd(args)
            self.assertEqual(rc, 1)

    def test_sync_adapters_print_only(self):
        """sync_adapters_cmd --print-only lists skills without writing files."""
        args = SimpleNamespace(print_only=True)
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = self.mod.sync_adapters_cmd(args)
        self.assertEqual(rc, 0)
        out = buf.getvalue()
        self.assertIn("Skills found", out)

    def test_verify_context_pack_file_not_found(self):
        """verify_context_pack_cmd returns 1 for a missing file."""
        args = SimpleNamespace(pack="/nonexistent/pack.md")
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = self.mod.verify_context_pack_cmd(args)
        self.assertEqual(rc, 1)

    def test_verify_context_pack_passing(self):
        """verify_context_pack_cmd passes when all required sections are present."""
        with tempfile.TemporaryDirectory() as td:
            pack = Path(td) / "pack.md"
            pack.write_text(
                "## Session Start\n"
                "## Context Snapshot\n"
                "## Goals and Non-Goals\n"
                "## Active Decisions\n"
                "## Architecture and Runtime\n"
                "Architecture pattern: monolith\n"
                "Language/runtime: Python 3.11\n"
                "## Data and Storage\n"
                "Database strategy: SQLite\n"
                "## Observability Baseline\n"
                "Logging/observability baseline: structlog\n"
                "## Design Readiness\n"
                "## Current Execution Plan\n"
                "## Open Questions and Risks\n"
                "## Traceability\n"
                "REQ-001 covered\n",
                encoding="utf-8",
            )
            args = SimpleNamespace(pack=str(pack))
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = self.mod.verify_context_pack_cmd(args)
            self.assertEqual(rc, 0)

    def test_render_flowchart_empty(self):
        """_render_flowchart returns None for non-flowchart input."""
        result = self.mod._render_flowchart("graph TD\nA --> B")
        self.assertIsNone(result)

    def test_render_er_empty(self):
        """_render_er returns None when no relationships are found."""
        result = self.mod._render_er("flowchart TD\nA --> B")
        self.assertIsNone(result)

    def test_render_sequence_empty(self):
        """_render_sequence returns None for non-sequence input."""
        result = self.mod._render_sequence("flowchart TD\nA --> B")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
