import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
POLYAGENTCTL = REPO_ROOT / "scripts" / "polyagentctl.py"


class PolyagentCtlTests(unittest.TestCase):
    def run_cmd(self, cmd, cwd=None):
        return subprocess.run(
            cmd,
            cwd=str(cwd or REPO_ROOT),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )

    def test_check_json(self):
        proc = self.run_cmd([str(POLYAGENTCTL), "check", "--json"])
        self.assertEqual(proc.returncode, 0, msg=proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertIn("tools", payload)
        self.assertIn("agents", payload)
        self.assertIn("has_puppeteer", payload)

    def test_export_pdf_html(self):
        with tempfile.TemporaryDirectory() as td:
            input_md = Path(td) / "sample.md"
            output_html = Path(td) / "sample.html"
            input_md.write_text(
                "# Sample\n\n```mermaid\nflowchart LR\nA[One] --> B[Two]\n```\n",
                encoding="utf-8",
            )
            proc = self.run_cmd(
                [
                    str(POLYAGENTCTL),
                    "export-pdf",
                    "--html",
                    str(input_md),
                    str(output_html),
                ]
            )
            self.assertEqual(proc.returncode, 0, msg=proc.stderr + "\n" + proc.stdout)
            self.assertTrue(output_html.exists())
            html = output_html.read_text(encoding="utf-8")
            self.assertTrue(
                ('<div class="diagram">' in html)
                or ('<div class="mermaid">' in html),
                msg="Expected static diagram or mermaid container in HTML output",
            )

    def test_self_install(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "polyagentctl"
            proc = self.run_cmd([str(POLYAGENTCTL), "self-install", "--path", str(target)])
            self.assertEqual(proc.returncode, 0, msg=proc.stderr)
            self.assertTrue(target.exists())
            self.assertTrue(os.access(target, os.X_OK))


if __name__ == "__main__":
    unittest.main()
