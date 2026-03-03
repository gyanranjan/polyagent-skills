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
            scripts = proj / "scripts"
            scripts.mkdir(parents=True, exist_ok=True)
            (proj / "agent.todo.md").write_text("## Gate Status\n", encoding="utf-8")
            gate = scripts / "gate-status-check.sh"
            dr = scripts / "design-readiness-check.sh"
            gate.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
            dr.write_text("#!/usr/bin/env bash\nexit 0\n", encoding="utf-8")
            gate.chmod(0o755)
            dr.chmod(0o755)

            args = SimpleNamespace(json=True, strict=True, project=str(proj))
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = self.mod.check_cmd(args)
            self.assertEqual(rc, 0)
            payload = json.loads(buf.getvalue())
            self.assertIn("strict_results", payload)
            self.assertEqual(len(payload["strict_results"]), 2)

    def test_export_pdf_delegates(self):
        args = SimpleNamespace(html=True, input_md="in.md", output="out.html")
        with patch.object(self.mod, "run", return_value=0) as mocked:
            rc = self.mod.export_pdf_cmd(args)
        self.assertEqual(rc, 0)
        cmd = mocked.call_args.args[0]
        self.assertIn("md-to-pdf.sh", cmd[0])
        self.assertIn("--html", cmd)

    def test_install_and_uninstall_delegate(self):
        with patch.object(self.mod, "run", return_value=0) as mocked:
            rc = self.mod.install_global_cmd(SimpleNamespace(mode="copy"))
            self.assertEqual(rc, 0)
            self.assertIn("install-global-all.sh", mocked.call_args.args[0][0])

        with patch.object(self.mod, "run", return_value=0) as mocked:
            rc = self.mod.uninstall_global_cmd(SimpleNamespace(dry_run=True))
            self.assertEqual(rc, 0)
            self.assertIn("uninstall-global-all.sh", mocked.call_args.args[0][0])
            self.assertIn("--dry-run", mocked.call_args.args[0])

    def test_install_project_delegate(self):
        args = SimpleNamespace(project_path="/tmp/project", agent="all")
        with patch.object(self.mod, "run", return_value=0) as mocked:
            rc = self.mod.install_project_cmd(args)
        self.assertEqual(rc, 0)
        cmd = mocked.call_args.args[0]
        self.assertIn("install-to-project.sh", cmd[0])
        self.assertEqual(cmd[-1], "all")

    def test_self_install(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "polyagentctl"
            rc = self.mod.self_install_cmd(SimpleNamespace(path=str(target)))
            self.assertEqual(rc, 0)
            self.assertTrue(target.exists())
            self.assertTrue(os.access(target, os.X_OK))


if __name__ == "__main__":
    unittest.main()
