import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
RENDERER_PATH = REPO_ROOT / "scripts" / "md-to-pdf-renderer.py"


def load_renderer_module():
    spec = importlib.util.spec_from_file_location("md_to_pdf_renderer", RENDERER_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


class MdToPdfRendererTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_renderer_module()

    def test_render_flowchart(self):
        code = "flowchart LR\nA[Start] --> B[Done]"
        svg = self.mod.render_flowchart(code)
        self.assertIsNotNone(svg)
        self.assertIn("<svg", svg)
        self.assertIn("Start", svg)

    def test_render_erdiagram(self):
        code = "erDiagram\nUSER ||--o{ ORDER : places"
        svg = self.mod.render_er(code)
        self.assertIsNotNone(svg)
        self.assertIn("<svg", svg)
        self.assertIn("USER", svg)

    def test_replace_mermaid_blocks(self):
        source = "# T\n\n```mermaid\nflowchart LR\nA --> B\n```\n"
        out = self.mod.replace_mermaid_blocks(source)
        self.assertIn('<div class="diagram">', out)
        self.assertNotIn("```mermaid", out)

    def test_main_writes_html(self):
        with tempfile.TemporaryDirectory() as td:
            inp = Path(td) / "in.md"
            outp = Path(td) / "out.html"
            inp.write_text("# T\n\n```mermaid\nflowchart LR\nA --> B\n```\n", encoding="utf-8")
            # Call through CLI-compatible argv for deterministic behavior.
            import sys

            old_argv = sys.argv
            try:
                sys.argv = ["md-to-pdf-renderer.py", str(inp), str(outp)]
                exit_code = self.mod.main()
            finally:
                sys.argv = old_argv
            self.assertEqual(exit_code, 0)
            self.assertTrue(outp.exists())
            html = outp.read_text(encoding="utf-8")
            self.assertIn("<html>", html)
            self.assertIn('<div class="diagram">', html)


if __name__ == "__main__":
    unittest.main()
