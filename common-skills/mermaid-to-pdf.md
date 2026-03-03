# Mermaid-to-PDF

Guidelines and process for reliably converting Markdown documents containing Mermaid diagrams to PDF without losing or degrading diagrams.

## The Problem

Standard Markdown-to-PDF converters (pandoc, markdown-pdf, etc.) do not natively render Mermaid codeblocks. This causes diagrams to either:
- Appear as raw code text in the PDF
- Be silently dropped
- Render as low-resolution blurry images

## When to Apply

Apply these guidelines when:
- A skill produces Markdown with Mermaid diagrams and PDF output is needed
- The user asks to export a document to PDF
- Any document with `mermaid` codeblocks needs to become a PDF

## Strategy

The script `scripts/md-to-pdf.sh` auto-selects the best available approach:

### Path A: Pre-Render Then Convert (Best Quality)

When `mmdc` (Mermaid CLI) is installed:

1. **Pre-render** each Mermaid codeblock to a high-resolution PNG via `mmdc`
2. **Replace** the Mermaid codeblock in Markdown with an image reference
3. **Convert** the image-embedded Markdown to PDF via pandoc or wkhtmltopdf

### Path B: HTML with Mermaid JS (No mmdc Needed)

When `mmdc` is NOT installed:

1. **Generate** a self-contained HTML file with Mermaid JS from CDN
2. Mermaid blocks become `<div class="mermaid">` elements rendered by the browser
3. **Convert** to PDF via headless browser (Chromium, puppeteer) or open in any browser and print

This path requires no pre-rendering tools — the browser renders Mermaid natively.

### Fallback: HTML File

When no PDF converter is available:

1. Produce a self-contained HTML file with live Mermaid diagrams
2. Open in any browser to view rendered diagrams
3. Print to PDF from the browser (Ctrl+P / Cmd+P)

## Authoring Guidelines (PDF-Safe Mermaid)

When writing Mermaid diagrams that will be exported to PDF, follow these rules:

### Diagram Complexity Limits

| Rule | Limit | Reason |
|------|-------|--------|
| Nodes per diagram | Max 15 | Larger diagrams become unreadable in PDF |
| Label length | Max 40 characters | Long labels cause overlap and clipping |
| Nesting depth | Max 3 levels | Deep nesting breaks layout in renderers |
| Diagram types | Prefer flowchart, sequence, mindmap, C4Context | These render most reliably across tools |

### Label and Syntax Rules

- **No special characters in labels** — avoid `&`, `<`, `>`, `"`, `|` inside node text; use plain text or HTML entities
- **No markdown inside labels** — no bold, italic, or links inside node text
- **Short IDs** — use short alphanumeric IDs for nodes (e.g., `A`, `B1`, `svc`) not long descriptive IDs
- **Quote labels with spaces** — use `A["My Label"]` not `A[My Label]` when labels contain spaces
- **Avoid subgraph nesting beyond 2 levels** — deeply nested subgraphs break in mmdc

### Layout Tips

- Use `TD` (top-down) or `LR` (left-right) consistently within a diagram
- Split large diagrams into multiple smaller ones with clear titles
- Add a text description above each diagram explaining what it shows

## Conversion Process

### Option A: Automated Script (`scripts/md-to-pdf.sh`) — Recommended

```bash
# Auto-selects best path (A or B) based on available tools
./scripts/md-to-pdf.sh input.md output.pdf

# Force HTML render path (no mmdc needed)
./scripts/md-to-pdf.sh --html input.md output.html

# The script auto-detects:
# - mmdc available?        → Path A (pre-render to images)
# - Chromium/puppeteer?    → Path B (HTML → headless browser → PDF)
# - Nothing available?     → Fallback (HTML with live Mermaid for browser viewing)
```

### Option B: Manual Steps (Path A)

If the script is not available or tools are missing, follow these steps:

#### Step 1: Check Tooling

```bash
# Required: Mermaid CLI
npm install -g @mermaid-js/mermaid-cli

# Required: One of these PDF converters
# Option 1 (recommended): pandoc + a PDF engine
sudo apt-get install pandoc texlive-xetex
# Option 2: wkhtmltopdf
sudo apt-get install wkhtmltopdf
# Option 3: chromium-based (puppeteer, used by mmdc internally)
```

#### Step 2: Extract and Render Mermaid Blocks

For each ` ```mermaid ` block in the document:

```bash
# Save the mermaid content to a temp file
echo '<mermaid content>' > diagram-N.mmd

# Render to SVG (preferred) or PNG
mmdc -i diagram-N.mmd -o diagram-N.svg -t neutral -w 1200 -H 800
# For PNG with high DPI:
mmdc -i diagram-N.mmd -o diagram-N.png -t neutral -w 1200 -H 800 -s 2
```

**Recommended mmdc flags:**
- `-t neutral` — clean, print-friendly theme (no bright colors)
- `-w 1200 -H 800` — adequate resolution for A4/Letter PDF
- `-s 2` — 2x scale for PNG (retina quality)
- `-b transparent` — transparent background for clean embedding

#### Step 3: Replace Codeblocks with Images

In the Markdown, replace each:

````
```mermaid
<diagram code>
```
````

With:

```markdown
![<Diagram Title>](diagram-N.svg)
```

#### Step 4: Convert to PDF

```bash
# With pandoc (recommended)
pandoc input-with-images.md -o output.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=1in \
  -V mainfont="DejaVu Sans" \
  --highlight-style=tango

# With wkhtmltopdf (alternative)
pandoc input-with-images.md -o temp.html
wkhtmltopdf --enable-local-file-access temp.html output.pdf
```

### Option C: HTML Render Path (No mmdc, No PDF Engine)

When mmdc is not available, generate an HTML file with Mermaid JS that renders diagrams in the browser:

```bash
# Generate HTML with live Mermaid diagrams
./scripts/md-to-pdf.sh --html input.md output.html

# Then either:
# 1. Open output.html in a browser → diagrams render automatically
# 2. Print to PDF from the browser (Ctrl+P / Cmd+P)
# 3. Install puppeteer for automated PDF: npm install -g puppeteer
```

The HTML file is self-contained with Mermaid JS loaded from CDN. It includes print-optimized CSS for clean PDF output.

### Option D: No Tooling Available

If no rendering tools are available at all:

1. Keep Mermaid codeblocks as-is in the Markdown document
2. Add a note at the top: "Diagrams are in Mermaid syntax. Render with a Mermaid-compatible viewer (GitHub, VS Code with Mermaid extension, mermaid.live) or install `@mermaid-js/mermaid-cli` for image export."
3. Add a task in `agent.todo.md` for tooling installation
4. Provide the `.md` file — it is the source of truth

## Mermaid Theme Configuration

For PDF output, use a config file for consistent styling:

```json
{
  "theme": "neutral",
  "themeVariables": {
    "fontSize": "14px",
    "fontFamily": "DejaVu Sans, Helvetica, Arial, sans-serif",
    "lineColor": "#333333",
    "primaryColor": "#e8e8e8",
    "primaryTextColor": "#333333",
    "primaryBorderColor": "#666666",
    "secondaryColor": "#f5f5f5",
    "tertiaryColor": "#ffffff"
  }
}
```

Save as `mermaid-pdf-config.json` and use: `mmdc -i input.mmd -o output.svg -c mermaid-pdf-config.json`

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Diagram appears as raw code in PDF | Mermaid block not pre-rendered | Use `md-to-pdf.sh` (auto-selects best path) or use `--html` flag for browser-based rendering |
| Diagram is blurry in PDF | PNG at low resolution | Use SVG instead, or PNG with `-s 2` or higher |
| Diagram labels are clipped/overlapping | Labels too long or too many nodes | Shorten labels to < 40 chars, split diagram |
| mmdc hangs or crashes | Chromium sandbox issue in container/CI | Use `mmdc --puppeteerConfigFile` with `{"args": ["--no-sandbox"]}` |
| Diagram renders but colors are too dark | Dark theme used | Use `-t neutral` or custom config above |
| SVG not rendering in pandoc PDF | xelatex doesn't embed SVG natively | Convert SVG to PNG first: `inkscape -d 300 diagram.svg -o diagram.png`, or use `--pdf-engine=weasyprint` |

## Quality Checks

- [ ] All Mermaid codeblocks in the source document have been accounted for
- [ ] Rendered images are legible at printed A4/Letter size
- [ ] No raw Mermaid code appears in the final PDF
- [ ] Diagram labels are fully visible (not clipped or overlapping)
- [ ] PDF file size is reasonable (SVGs keep it small; large PNGs can bloat)
- [ ] A text description accompanies each diagram for accessibility
