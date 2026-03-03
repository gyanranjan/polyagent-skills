#!/usr/bin/env python3
"""
Reusable Markdown->HTML renderer with static Mermaid support for:
- flowchart
- erDiagram
"""

from __future__ import annotations

import html
import pathlib
import re
import sys

from markdown_it import MarkdownIt


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def render_flowchart(code: str) -> str | None:
    lines = [ln.strip() for ln in code.splitlines() if ln.strip()]
    if not lines or not lines[0].startswith("flowchart"):
        return None
    first = lines[0].split()
    direction = first[1] if len(first) > 1 else "TD"

    node_labels: dict[str, str] = {}
    node_order: list[str] = []
    edges: list[tuple[str, str]] = []

    node_re = re.compile(r"^([A-Za-z0-9_]+)\[(.*?)\]$")
    edge_re = re.compile(
        r"^([A-Za-z0-9_]+)(?:\[(.*?)\])?\s*-->\s*([A-Za-z0-9_]+)(?:\[(.*?)\])?$"
    )

    def ensure(nid: str, label: str | None = None) -> None:
        if nid not in node_labels:
            node_labels[nid] = label if label else nid
            node_order.append(nid)
        elif label:
            node_labels[nid] = label

    for ln in lines[1:]:
        m_edge = edge_re.match(ln)
        if m_edge:
            a, al, b, bl = m_edge.groups()
            ensure(a, al)
            ensure(b, bl)
            edges.append((a, b))
            continue
        m_node = node_re.match(ln)
        if m_node:
            nid, label = m_node.groups()
            ensure(nid, label)

    if not node_order:
        return None

    w_box = 220
    h_box = 56
    gap = 44
    horizontal = direction in ("LR", "RL")
    coords: dict[str, tuple[int, int]] = {}

    for i, nid in enumerate(node_order):
        if horizontal:
            x = 50 + i * (w_box + gap)
            y = 60
        else:
            x = 60
            y = 40 + i * (h_box + gap)
        coords[nid] = (x, y)

    if horizontal:
        svg_w = max(420, 100 + len(node_order) * (w_box + gap))
        svg_h = 200
    else:
        svg_w = 420
        svg_h = max(220, 100 + len(node_order) * (h_box + gap))

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">'
    )
    parts.append(
        '<defs><marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto"><polygon points="0 0, 10 3.5, 0 7" fill="#4b5563"/></marker></defs>'
    )
    parts.append('<rect x="0" y="0" width="100%" height="100%" fill="#ffffff"/>')

    for a, b in edges:
        ax, ay = coords[a]
        bx, by = coords[b]
        if horizontal:
            x1, y1 = ax + w_box, ay + h_box // 2
            x2, y2 = bx, by + h_box // 2
        else:
            x1, y1 = ax + w_box // 2, ay + h_box
            x2, y2 = bx + w_box // 2, by
        parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#4b5563" stroke-width="2" marker-end="url(#arr)"/>'
        )

    for nid in node_order:
        x, y = coords[nid]
        label = esc(node_labels[nid])
        parts.append(
            f'<rect x="{x}" y="{y}" rx="8" ry="8" width="{w_box}" height="{h_box}" fill="#f8fafc" stroke="#334155"/>'
        )
        parts.append(
            f'<text x="{x + w_box/2}" y="{y + h_box/2 + 4}" text-anchor="middle" font-size="13" font-family="Arial" fill="#111827">{label}</text>'
        )

    parts.append("</svg>")
    return "".join(parts)


def render_er(code: str) -> str | None:
    lines = [ln.strip() for ln in code.splitlines() if ln.strip()]
    if not lines or lines[0] != "erDiagram":
        return None

    rel_re = re.compile(r"^([A-Za-z0-9_]+)\s+\S+\s+([A-Za-z0-9_]+)\s*:\s*(.+)$")
    entities: list[str] = []
    rels: list[tuple[str, str, str]] = []

    def add_entity(name: str) -> None:
        if name not in entities:
            entities.append(name)

    for ln in lines[1:]:
        m = rel_re.match(ln)
        if not m:
            continue
        a, b, label = m.groups()
        add_entity(a)
        add_entity(b)
        rels.append((a, b, label))

    if not entities:
        return None

    w_box = 220
    h_box = 54
    col_gap = 120
    row_gap = 50
    cols = 2
    coords: dict[str, tuple[int, int]] = {}
    for i, e in enumerate(entities):
        col = i % cols
        row = i // cols
        x = 60 + col * (w_box + col_gap)
        y = 40 + row * (h_box + row_gap)
        coords[e] = (x, y)

    rows = (len(entities) + cols - 1) // cols
    svg_w = 60 + cols * w_box + (cols - 1) * col_gap + 60
    svg_h = 60 + rows * h_box + (rows - 1) * row_gap + 60

    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_w}" height="{svg_h}" viewBox="0 0 {svg_w} {svg_h}">'
    )
    parts.append('<rect x="0" y="0" width="100%" height="100%" fill="#ffffff"/>')

    for a, b, label in rels:
        ax, ay = coords[a]
        bx, by = coords[b]
        x1, y1 = ax + w_box / 2, ay + h_box / 2
        x2, y2 = bx + w_box / 2, by + h_box / 2
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#4b5563" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{mx}" y="{my - 6}" text-anchor="middle" font-size="12" font-family="Arial" fill="#374151">{esc(label)}</text>'
        )

    for e in entities:
        x, y = coords[e]
        parts.append(
            f'<rect x="{x}" y="{y}" rx="8" ry="8" width="{w_box}" height="{h_box}" fill="#f8fafc" stroke="#334155"/>'
        )
        parts.append(
            f'<text x="{x + w_box/2}" y="{y + h_box/2 + 4}" text-anchor="middle" font-size="13" font-family="Arial" fill="#111827">{esc(e)}</text>'
        )

    parts.append("</svg>")
    return "".join(parts)


def replace_mermaid_blocks(markdown: str) -> str:
    pat = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)

    def repl(m: re.Match[str]) -> str:
        code = m.group(1).strip()
        svg = render_flowchart(code)
        if svg is None:
            svg = render_er(code)
        if svg is None:
            return m.group(0)
        return f'\n<div class="diagram">{svg}</div>\n'

    return pat.sub(repl, markdown)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: md-to-pdf-renderer.py <input.md> <output.html>", file=sys.stderr)
        return 1

    source = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    output = pathlib.Path(sys.argv[2])

    source = replace_mermaid_blocks(source)
    md = MarkdownIt("default", {"html": True, "typographer": True})
    rendered = md.render(source)

    doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>Document Export</title>
<style>
body {{
  font-family: Arial, sans-serif;
  margin: 28px;
  color: #111;
  line-height: 1.5;
}}
h1, h2, h3 {{ margin-top: 1.2em; margin-bottom: 0.5em; }}
h1 {{ border-bottom: 1px solid #ddd; padding-bottom: 0.25em; }}
code {{ background: #f6f8fa; padding: 0.1em 0.3em; border-radius: 4px; }}
pre {{
  background: #f6f8fa;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  padding: 12px;
  font-size: 12px;
  overflow-x: auto;
}}
pre code {{ background: transparent; padding: 0; }}
table {{
  border-collapse: collapse;
  width: 100%;
  margin: 12px 0;
  font-size: 12px;
}}
th, td {{
  border: 1px solid #d0d7de;
  padding: 6px 8px;
  text-align: left;
  vertical-align: top;
}}
th {{ background: #f6f8fa; }}
blockquote {{
  border-left: 4px solid #d0d7de;
  margin: 0;
  padding-left: 12px;
  color: #57606a;
}}
.diagram {{
  margin: 12px 0 20px;
  padding: 10px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #ffffff;
}}
.diagram svg {{
  max-width: 100%;
  height: auto;
}}
</style>
</head>
<body>
{rendered}
</body>
</html>
"""
    output.write_text(doc, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
