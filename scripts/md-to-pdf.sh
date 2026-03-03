#!/usr/bin/env bash
# md-to-pdf.sh — Convert Markdown with Mermaid diagrams to PDF
#
# Strategy (auto-selected):
#   Path A: mmdc available → pre-render Mermaid to images → embed in Markdown → PDF via pandoc/wkhtmltopdf
#   Path B: mmdc NOT available → generate HTML with Mermaid JS → PDF via headless browser
#   Fallback: produce self-contained HTML with live Mermaid (viewable in any browser)
#
# Usage:
#   ./scripts/md-to-pdf.sh input.md [output.pdf]
#   ./scripts/md-to-pdf.sh --html input.md [output.html]   # Force HTML render path
#
# If output is omitted, the output file is input-name.pdf (or .html) in the same directory.
#
# Requirements (at least one of):
#   Path A: mmdc + (pandoc+xelatex | wkhtmltopdf)
#   Path B: node (uses inline Mermaid JS; optional: puppeteer for auto PDF)
#   Fallback: none — produces HTML viewable in any browser

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# --- Argument parsing ---------------------------------------------------------

FORCE_HTML=false
if [ "${1:-}" = "--html" ]; then
  FORCE_HTML=true
  shift
fi

INPUT="${1:?Usage: md-to-pdf.sh [--html] input.md [output.pdf|output.html]}"
OUTPUT="${2:-}"

if [ ! -f "$INPUT" ]; then
  echo "Error: File not found: $INPUT" >&2
  exit 1
fi

# Derive output filename if not provided
if [ -z "$OUTPUT" ]; then
  if [ "$FORCE_HTML" = "true" ]; then
    OUTPUT="${INPUT%.md}.html"
  else
    OUTPUT="${INPUT%.md}.pdf"
  fi
fi

# Resolve output to absolute path early so Path A can safely `cd` into WORK_DIR
if [[ "$OUTPUT" = /* ]]; then
  OUTPUT_ABS="$OUTPUT"
else
  OUTPUT_ABS="$(pwd)/$OUTPUT"
fi
mkdir -p "$(dirname "$OUTPUT_ABS")"

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

INPUT_ABS="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
PROCESSED_MD="$WORK_DIR/processed.md"
NORMALIZED_MD="$WORK_DIR/normalized.md"

echo "==> Processing: $INPUT"
echo "==> Output:     $OUTPUT_ABS"
echo "==> Work dir:   $WORK_DIR"

# --- Normalize input quirks ---------------------------------------------------
# Handles:
# 1) Legacy code block markers:
#      [CODE BLOCK START: mermaid] ... [CODE BLOCK END]
#    -> fenced Markdown
# 2) Collapsed heading+list lines:
#      ## Heading- item A- item B
#    -> heading + bullet list lines
awk '
BEGIN {
  sq = sprintf("%c", 39)
  triple = sq sq sq
}
function trim(s) {
  sub(/^[[:space:]]+/, "", s)
  sub(/[[:space:]]+$/, "", s)
  return s
}

{
  line = $0
  # Normalize smart quotes often introduced by copy/paste from docs/editors.
  gsub(/[‘’]/, sq, line)
  gsub(/[“”]/, "\"", line)

  # Fix collapsed heading/list lines (outside fenced code):
  # "## X- A- B" => "## X" + "- A" + "- B"
  if (line ~ /^#{1,6}[[:space:]]+/ && line ~ /-[[:space:]]+/) {
    d = match(line, /-[[:space:]]+/)
    if (d > 0) {
      heading = trim(substr(line, 1, d - 1))
      tail = substr(line, d + RLENGTH)
      if (length(heading) > 0 && length(trim(tail)) > 0) {
        print heading
        n = split(tail, items, /-[[:space:]]+/)
        for (i = 1; i <= n; i++) {
          item = trim(items[i])
          if (length(item) > 0) {
            print "- " item
          }
        }
        next
      }
    }
  }

  if (line ~ /^[[:space:]]*\[CODE BLOCK START:[[:space:]]*mermaid[[:space:]]*\][[:space:]]*$/) {
    print "```mermaid"
    next
  }
  # Accept quote-style fences commonly seen from rich-text copy/paste.
  trimmed = trim(line)
  if (substr(trimmed, 1, 3) == triple) {
    lang = trim(substr(trimmed, 4))
    if (lang == "") {
      print "```"
      next
    }
    if (lang ~ /^[A-Za-z0-9_-]+$/) {
      print "```" lang
      next
    }
  }
  if (line ~ /^[[:space:]]*\[CODE BLOCK START:[[:space:]]*[^]]+[[:space:]]*\][[:space:]]*$/) {
    sub(/^[[:space:]]*\[CODE BLOCK START:[[:space:]]*/, "", line)
    sub(/[[:space:]]*\][[:space:]]*$/, "", line)
    print "```" line
    next
  }
  if (line ~ /^[[:space:]]*\[CODE BLOCK START\][[:space:]]*$/) {
    print "```"
    next
  }
  if (line ~ /^[[:space:]]*\[CODE BLOCK END\][[:space:]]*$/) {
    print "```"
    next
  }
  print line
}
' "$INPUT_ABS" > "$NORMALIZED_MD"

SOURCE_MD="$NORMALIZED_MD"
MERMAID_BLOCK_COUNT=$(grep -c '^```mermaid' "$SOURCE_MD" || true)

# --- Check tooling -----------------------------------------------------------

HAS_MMDC=false
MMDC_TIMEOUT_SECONDS="${MMDC_TIMEOUT_SECONDS:-90}"
if command -v mmdc >/dev/null 2>&1; then
  HAS_MMDC=true
  MMDC_CMD="mmdc"
  echo "==> mmdc: $(mmdc --version 2>&1 | head -1)"
elif command -v npx >/dev/null 2>&1; then
  # Allow ephemeral Mermaid CLI when globally installed mmdc is unavailable.
  HAS_MMDC=true
  MMDC_CMD="npx -y @mermaid-js/mermaid-cli"
  echo "==> mmdc: via npx (@mermaid-js/mermaid-cli)"
else
  MMDC_CMD=""
  echo "==> mmdc: NOT FOUND"
fi

HAS_NODE=false
if command -v node >/dev/null 2>&1; then
  HAS_NODE=true
  echo "==> node: $(node --version 2>&1)"
fi

HAS_PANDOC=false
if command -v pandoc >/dev/null 2>&1; then
  HAS_PANDOC=true
fi

HAS_PY_MARKDOWNIT=false
if command -v python3 >/dev/null 2>&1; then
  if python3 - <<'PY' >/dev/null 2>&1
import importlib.util
import sys
sys.exit(0 if importlib.util.find_spec("markdown_it") else 1)
PY
  then
    HAS_PY_MARKDOWNIT=true
  fi
fi

# Detect headless browser for HTML→PDF conversion
BROWSER_CMD=""
BROWSER_IS_SNAP=false
for cmd in chromium chromium-browser google-chrome google-chrome-stable; do
  if command -v "$cmd" >/dev/null 2>&1; then
    BROWSER_CMD="$cmd"
    browser_path="$(command -v "$cmd")"
    if [[ "$browser_path" == /snap/* ]]; then
      BROWSER_IS_SNAP=true
    fi
    break
  fi
done

# Detect PDF engine for Path A (mmdc pre-render approach)
PDF_ENGINE="none"
if [ "$HAS_PANDOC" = "true" ]; then
  if command -v xelatex >/dev/null 2>&1; then
    PDF_ENGINE="pandoc-xelatex"
  elif command -v weasyprint >/dev/null 2>&1; then
    PDF_ENGINE="pandoc-weasyprint"
  elif command -v wkhtmltopdf >/dev/null 2>&1; then
    PDF_ENGINE="pandoc-html-wkhtmltopdf"
  else
    PDF_ENGINE="pandoc-noengine"
  fi
elif command -v wkhtmltopdf >/dev/null 2>&1; then
  PDF_ENGINE="wkhtmltopdf"
fi

# --- Decide which path to take -----------------------------------------------

# Path A: mmdc pre-render (best quality; preferred whenever mmdc is available)
# Path B: HTML with Mermaid JS (no mmdc needed, renders in browser)

USE_PATH="B"  # Default to HTML path
if [ "$FORCE_HTML" = "true" ]; then
  USE_PATH="B"
  echo "==> Mode: HTML render (forced via --html)"
elif [ "$HAS_MMDC" = "true" ]; then
  USE_PATH="A"
  echo "==> Mode: Path A — mmdc pre-render (preferred)"
else
  echo "==> Mode: Path B — HTML with Mermaid JS (browser-rendered)"
fi

# ==============================================================================
# PATH A: mmdc pre-render approach (original)
# ==============================================================================

if [ "$USE_PATH" = "A" ]; then

  # --- Mermaid config for clean PDF output ---
  MERMAID_CONFIG="$WORK_DIR/mermaid-config.json"
  cat > "$MERMAID_CONFIG" <<'MCONF'
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
MCONF

  PUPPETEER_CONFIG="$WORK_DIR/puppeteer-config.json"
  cat > "$PUPPETEER_CONFIG" <<'PCONF'
{
  "args": ["--no-sandbox", "--disable-setuid-sandbox"]
}
PCONF

  # --- Extract and render Mermaid blocks ---
  awk -v workdir="$WORK_DIR" '
  BEGIN { in_mermaid = 0; diagram_count = 0; mermaid_content = "" }
  /^```mermaid/ { in_mermaid = 1; diagram_count++; mermaid_content = ""; next }
  in_mermaid && /^```$/ {
    in_mermaid = 0
    mmd_file = workdir "/diagram-" diagram_count ".mmd"
    print mermaid_content > mmd_file
    close(mmd_file)
    print "![Diagram " diagram_count "](diagram-" diagram_count ".png)"
    next
  }
  in_mermaid {
    mermaid_content = (mermaid_content == "") ? $0 : mermaid_content "\n" $0
    next
  }
  { print }
  ' "$SOURCE_MD" > "$PROCESSED_MD"

  DIAGRAM_COUNT=$(find "$WORK_DIR" -name 'diagram-*.mmd' 2>/dev/null | wc -l)
  echo "==> Found $DIAGRAM_COUNT Mermaid diagram(s)"

  # Render each diagram with mmdc
  if [ "$DIAGRAM_COUNT" -gt 0 ]; then
    for mmd_file in "$WORK_DIR"/diagram-*.mmd; do
      base="$(basename "$mmd_file" .mmd)"
      png_file="$WORK_DIR/${base}.png"
      echo "    Rendering: $base"
      if command -v timeout >/dev/null 2>&1; then
        MMDC_RUNNER=(timeout "${MMDC_TIMEOUT_SECONDS}s")
      else
        MMDC_RUNNER=()
      fi
      if "${MMDC_RUNNER[@]}" $MMDC_CMD \
          -i "$mmd_file" \
          -o "$png_file" \
          -c "$MERMAID_CONFIG" \
          -p "$PUPPETEER_CONFIG" \
          -w 1200 \
          -H 800 \
          -s 2 \
          -b white 2>/dev/null; then
        echo "    OK: $png_file"
      else
        echo "    WARN: mmdc failed/timed out for $base, falling back to placeholder" >&2
        sed -i "s|!\[Diagram ${base#diagram-}\](${base}.png)|> **[Diagram ${base#diagram-}]** — Rendering failed. See source Markdown for Mermaid code.|" "$PROCESSED_MD"
      fi
    done
  fi

  # --- Convert to PDF ---
  cd "$WORK_DIR"

  case "$PDF_ENGINE" in
    pandoc-xelatex)
      echo "==> Converting with pandoc + xelatex"
      pandoc "$PROCESSED_MD" -o "$OUTPUT_ABS" \
        --pdf-engine=xelatex \
        -V geometry:margin=1in \
        -V mainfont="DejaVu Sans" \
        -V monofont="DejaVu Sans Mono" \
        --highlight-style=tango \
        --toc \
        -f markdown+implicit_figures
      echo "==> PDF created: $OUTPUT_ABS"
      echo "==> Done."
      exit 0
      ;;
    pandoc-weasyprint)
      echo "==> Converting with pandoc + weasyprint"
      pandoc "$PROCESSED_MD" -o "$OUTPUT_ABS" \
        --pdf-engine=weasyprint \
        --toc \
        -f markdown+implicit_figures
      echo "==> PDF created: $OUTPUT_ABS"
      echo "==> Done."
      exit 0
      ;;
    pandoc-html-wkhtmltopdf)
      echo "==> Converting via pandoc (HTML) + wkhtmltopdf"
      pandoc "$PROCESSED_MD" -o "$WORK_DIR/temp.html" \
        --standalone --toc -f markdown+implicit_figures
      wkhtmltopdf --enable-local-file-access "$WORK_DIR/temp.html" "$OUTPUT_ABS"
      echo "==> PDF created: $OUTPUT_ABS"
      echo "==> Done."
      exit 0
      ;;
    wkhtmltopdf)
      echo "==> Converting with wkhtmltopdf"
      if [ "$HAS_PANDOC" = "true" ]; then
        pandoc "$PROCESSED_MD" -o "$WORK_DIR/temp.html" --standalone
      else
        {
          echo "<html><head><meta charset='utf-8'><style>body{font-family:sans-serif;margin:2em;} img{max-width:100%;} pre{background:#f5f5f5;padding:1em;overflow-x:auto;}</style></head><body>"
          cat "$PROCESSED_MD"
          echo "</body></html>"
        } > "$WORK_DIR/temp.html"
      fi
      wkhtmltopdf --enable-local-file-access "$WORK_DIR/temp.html" "$OUTPUT_ABS"
      echo "==> PDF created: $OUTPUT_ABS"
      echo "==> Done."
      exit 0
      ;;
    *)
      echo "==> No direct PDF engine found after mmdc pre-render."
      echo "==> Falling back to HTML/PDF conversion path with pre-rendered diagrams."
      # Keep pre-rendered Markdown as source for Path B rendering/fallback.
      SOURCE_MD="$PROCESSED_MD"
      MERMAID_BLOCK_COUNT=$(grep -c '^```mermaid' "$SOURCE_MD" || true)
      ;;
  esac
fi

# ==============================================================================
# PATH B: HTML render with Mermaid JS (or pre-rendered image Markdown fallback)
# ==============================================================================

echo "==> Generating self-contained HTML with Mermaid JS..."

MERMAID_STATIC_ELIGIBLE=false
if [ "$MERMAID_BLOCK_COUNT" -gt 0 ]; then
  if awk '
  BEGIN { in_mermaid=0; need_first=0; invalid=0 }
  /^```mermaid/ { in_mermaid=1; need_first=1; next }
  in_mermaid && /^```$/ { in_mermaid=0; need_first=0; next }
  in_mermaid && need_first {
    line=$0
    gsub(/^[[:space:]]+|[[:space:]]+$/, "", line)
    if (line == "") next
    if (line ~ /^(flowchart|erDiagram)([[:space:]].*)?$/) {
      need_first=0
      next
    }
    invalid=1
    exit
  }
  END { exit invalid }
  ' "$SOURCE_MD"; then
    MERMAID_STATIC_ELIGIBLE=true
  fi
fi

USED_PY_STATIC_RENDER=false
HTML_OUTPUT="$WORK_DIR/output.html"

if [ "$HAS_PY_MARKDOWNIT" = "true" ] && [ "$MERMAID_STATIC_ELIGIBLE" = "true" ]; then
  echo "==> Using Python markdown-it static renderer for Mermaid flowchart/erDiagram blocks"
  USED_PY_STATIC_RENDER=true
  python3 "$SCRIPT_DIR/md-to-pdf-renderer.py" "$SOURCE_MD" "$HTML_OUTPUT"
fi

# Convert Markdown to HTML body.
# Mermaid fenced blocks become <div class="mermaid"> for the JS library to render.
HTML_BODY_FILE="$WORK_DIR/body.html"

if [ "$USED_PY_STATIC_RENDER" = "false" ]; then
awk '
BEGIN { in_mermaid = 0; in_code = 0; in_list = 0 }

function close_list_if_open() {
  if (in_list) {
    print "</ul>"
    in_list = 0
  }
}

# Mermaid fenced blocks → <div class="mermaid">
/^```mermaid/ {
  close_list_if_open()
  in_mermaid = 1
  print "<div class=\"mermaid\">"
  next
}
in_mermaid && /^```$/ {
  in_mermaid = 0
  print "</div>"
  next
}
in_mermaid { print; next }

# Other fenced code blocks → <pre><code>
/^```/ && !in_code {
  close_list_if_open()
  in_code = 1
  lang = $0
  sub(/^```/, "", lang)
  if (lang != "") {
    printf "<pre><code class=\"language-%s\">", lang
  } else {
    printf "<pre><code>"
  }
  next
}
/^```$/ && in_code {
  in_code = 0
  print "</code></pre>"
  next
}
in_code {
  # Escape HTML inside code blocks
  gsub(/&/, "\\&amp;")
  gsub(/</, "\\&lt;")
  gsub(/>/, "\\&gt;")
  print
  next
}

# Headings
/^######/ { close_list_if_open(); sub(/^###### */, ""); printf "<h6>%s</h6>\n", $0; next }
/^#####/  { close_list_if_open(); sub(/^##### */,  ""); printf "<h5>%s</h5>\n", $0; next }
/^####/   { close_list_if_open(); sub(/^#### */,   ""); printf "<h4>%s</h4>\n", $0; next }
/^###/    { close_list_if_open(); sub(/^### */,    ""); printf "<h3>%s</h3>\n", $0; next }
/^##/     { close_list_if_open(); sub(/^## */,     ""); printf "<h2>%s</h2>\n", $0; next }
/^#/      { close_list_if_open(); sub(/^# */,      ""); printf "<h1>%s</h1>\n", $0; next }

# Horizontal rules
/^---+$/ || /^\*\*\*+$/ { close_list_if_open(); print "<hr>"; next }

# Tables (pass through — basic rendering)
/^\|/ { close_list_if_open(); print; next }

# Markdown image: ![alt](url)
/^!\[[^]]*\]\([^)]*\)[[:space:]]*$/ {
  close_list_if_open()
  line = $0
  alt = line
  sub(/^!\[/, "", alt)
  sub(/\][[:space:]]*\(.*/, "", alt)
  src = line
  sub(/^!\[[^]]*\][[:space:]]*\(/, "", src)
  sub(/\)[[:space:]]*$/, "", src)
  printf "<p><img alt=\"%s\" src=\"%s\"></p>\n", alt, src
  next
}

# Unordered list
/^-[[:space:]]+/ {
  if (!in_list) {
    print "<ul>"
    in_list = 1
  }
  item = $0
  sub(/^-[[:space:]]+/, "", item)
  printf "<li>%s</li>\n", item
  next
}

# Blank lines
/^$/ { close_list_if_open(); print "<br>"; next }

# Default: wrap in <p>
{
  close_list_if_open()
  printf "<p>%s</p>\n", $0
}

END {
  close_list_if_open()
}
' "$SOURCE_MD" > "$HTML_BODY_FILE"

# Extract title from first H1 if present
DOC_TITLE=$(grep -m1 '^# ' "$SOURCE_MD" | sed 's/^# //' || echo "Document")

# Build self-contained HTML with Mermaid JS
cat > "$HTML_OUTPUT" <<HTMLEOF
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${DOC_TITLE}</title>
  <style>
    @media print {
      .mermaid svg { max-width: 100% !important; page-break-inside: avoid; }
      body { font-size: 11pt; }
      h1, h2, h3 { page-break-after: avoid; }
      pre, table { page-break-inside: avoid; }
    }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
      line-height: 1.6;
      max-width: 900px;
      margin: 0 auto;
      padding: 2em;
      color: #24292e;
    }
    h1 { font-size: 2em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
    h2 { font-size: 1.5em; border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }
    h3 { font-size: 1.25em; }
    pre {
      background: #f6f8fa;
      border: 1px solid #e1e4e8;
      border-radius: 6px;
      padding: 16px;
      overflow-x: auto;
      font-size: 0.9em;
    }
    code {
      font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
      font-size: 0.9em;
    }
    table {
      border-collapse: collapse;
      width: 100%;
      margin: 1em 0;
    }
    th, td {
      border: 1px solid #dfe2e5;
      padding: 8px 12px;
      text-align: left;
    }
    th { background: #f6f8fa; font-weight: 600; }
    tr:nth-child(even) { background: #f9f9f9; }
    .mermaid {
      text-align: center;
      margin: 1.5em 0;
      padding: 1em;
      background: #fafbfc;
      border: 1px solid #e1e4e8;
      border-radius: 6px;
    }
    blockquote {
      border-left: 4px solid #dfe2e5;
      padding: 0 1em;
      color: #6a737d;
      margin: 1em 0;
    }
    hr { border: none; border-top: 1px solid #eaecef; margin: 2em 0; }
    img { max-width: 100%; }
  </style>
</head>
<body>
HTMLEOF

cat "$HTML_BODY_FILE" >> "$HTML_OUTPUT"

# Use Mermaid JS from CDN with initialization
cat >> "$HTML_OUTPUT" <<'HTMLEOF'
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
    mermaid.initialize({
      startOnLoad: true,
      theme: 'neutral',
      securityLevel: 'loose',
      fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif',
      flowchart: { useMaxWidth: true, htmlLabels: true },
      sequence: { useMaxWidth: true },
      themeVariables: {
        fontSize: '14px',
        lineColor: '#333333',
        primaryColor: '#e8e8e8',
        primaryTextColor: '#333333',
        primaryBorderColor: '#666666'
      }
    });
    // Signal rendering complete (used by puppeteer PDF path)
    mermaid.run().then(() => {
      document.body.setAttribute('data-mermaid-done', 'true');
    });
  </script>
</body>
</html>
HTMLEOF

echo "==> HTML generated with embedded Mermaid JS"
fi

# --- If pandoc is available, use it for better Markdown→HTML conversion --------
# Rebuild the HTML body using pandoc (better table, list, and inline formatting support)
# but keep our Mermaid JS wrapper intact.

if [ "$HAS_PANDOC" = "true" ] && [ "$USED_PY_STATIC_RENDER" = "false" ]; then
  echo "==> Rebuilding body with pandoc for better formatting..."

  # Convert mermaid blocks to placeholder divs before pandoc
  PANDOC_INPUT="$WORK_DIR/pandoc-input.md"
  awk '
  BEGIN { in_mermaid = 0; count = 0 }
  /^```mermaid/ {
    in_mermaid = 1; count++
    printf "<div class=\"mermaid\" id=\"mermaid-%d\">\n", count
    next
  }
  in_mermaid && /^```$/ {
    in_mermaid = 0
    print "</div>"
    next
  }
  { print }
  ' "$SOURCE_MD" > "$PANDOC_INPUT"

  PANDOC_BODY="$WORK_DIR/pandoc-body.html"
  pandoc "$PANDOC_INPUT" -o "$PANDOC_BODY" \
    -f markdown+pipe_tables+fenced_code_blocks+raw_html \
    --no-highlight 2>/dev/null || true

  if [ -f "$PANDOC_BODY" ] && [ -s "$PANDOC_BODY" ]; then
    # Rebuild the full HTML: header + pandoc body + Mermaid JS footer
    PANDOC_HTML="$WORK_DIR/pandoc-output.html"
    head -n "$(grep -n '^<body>' "$HTML_OUTPUT" | tail -1 | cut -d: -f1)" "$HTML_OUTPUT" > "$PANDOC_HTML"
    cat "$PANDOC_BODY" >> "$PANDOC_HTML"
    # Append everything from </body> onward (the Mermaid JS script)
    sed -n '/^  <script type="module">/,$ p' "$HTML_OUTPUT" >> "$PANDOC_HTML"
    # Close the body and html tags are already in the script block
    HTML_OUTPUT="$PANDOC_HTML"
    echo "==> Pandoc formatting applied"
  fi
fi

# --- Attempt PDF conversion via headless browser or puppeteer -----------------

FINAL_OUTPUT="$OUTPUT_ABS"

# Determine if we should try PDF output
TRY_PDF=true
if [ "$FORCE_HTML" = "true" ]; then
  TRY_PDF=false
fi
if [[ "$OUTPUT" == *.html ]]; then
  TRY_PDF=false
fi

if [ "$TRY_PDF" = "true" ]; then

  PDF_CREATED=false

  if [ "$MERMAID_BLOCK_COUNT" -gt 0 ]; then
    echo "==> Mermaid blocks detected: $MERMAID_BLOCK_COUNT"
  fi

  # Option 1: Node.js + puppeteer (if available) with Mermaid render validation
  if [ "$HAS_NODE" = "true" ] && [ "$PDF_CREATED" = "false" ]; then
    # Check if puppeteer is available
    PUPPETEER_SCRIPT="$WORK_DIR/render-pdf.mjs"
    cat > "$PUPPETEER_SCRIPT" <<'NODESCRIPT'
import { readFileSync } from 'fs';
import { resolve } from 'path';

const htmlPath = process.argv[2];
const pdfPath = process.argv[3];
const expectedMermaidCount = Number(process.argv[4] || 0);

if (!htmlPath || !pdfPath) {
  console.error('Usage: node render-pdf.mjs <input.html> <output.pdf> [expectedMermaidCount]');
  process.exit(1);
}

let puppeteer;
try {
  puppeteer = await import('puppeteer');
} catch {
  try {
    puppeteer = await import('puppeteer-core');
  } catch {
    console.error('Neither puppeteer nor puppeteer-core is available.');
    console.error('Install with: npm install -g puppeteer');
    process.exit(2);
  }
}

const browser = await puppeteer.default.launch({
  headless: 'new',
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});

const page = await browser.newPage();
const fileUrl = 'file://' + resolve(htmlPath);
await page.goto(fileUrl, { waitUntil: 'networkidle0', timeout: 30000 });

// Wait for Mermaid to finish rendering
await page.waitForFunction(
  () => document.body.getAttribute('data-mermaid-done') === 'true',
  { timeout: 15000 }
).catch(() => {
  console.warn('WARN: Mermaid rendering may not have completed; proceeding anyway.');
});

// Small extra delay for SVG layout to settle
await new Promise(r => setTimeout(r, 1000));

if (expectedMermaidCount > 0) {
  const renderedCount = await page.$$eval('.mermaid svg', (els) => els.length);
  if (renderedCount < expectedMermaidCount) {
    console.error(
      `Mermaid render validation failed: expected ${expectedMermaidCount}, rendered ${renderedCount}.`
    );
    await browser.close();
    process.exit(3);
  }
}

await page.pdf({
  path: resolve(pdfPath),
  format: 'A4',
  margin: { top: '1in', right: '1in', bottom: '1in', left: '1in' },
  printBackground: true,
  displayHeaderFooter: false
});

await browser.close();
console.log('PDF created successfully.');
NODESCRIPT

    echo "==> Attempting PDF via Node.js + puppeteer..."
    if node "$PUPPETEER_SCRIPT" "$HTML_OUTPUT" "$FINAL_OUTPUT" "$MERMAID_BLOCK_COUNT" 2>/dev/null; then
      PDF_CREATED=true
      echo "==> PDF created: $FINAL_OUTPUT"
    else
      echo "==> WARN: Puppeteer not available or Mermaid validation failed" >&2
    fi
  fi

  # Option 2: Headless Chromium/Chrome --print-to-pdf
  if [ -n "$BROWSER_CMD" ] && [ "$PDF_CREATED" = "false" ]; then
    if [ "$BROWSER_IS_SNAP" = "true" ]; then
      echo "==> WARN: $BROWSER_CMD is a Snap build; headless PDF may fail in restricted environments." >&2
      echo "    Skipping browser conversion attempt. Prefer puppeteer or manual browser print from HTML." >&2
    else
    echo "==> Converting to PDF via $BROWSER_CMD --headless --print-to-pdf"
    if [ "$MERMAID_BLOCK_COUNT" -gt 0 ]; then
      echo "    WARN: Browser mode cannot validate Mermaid render completeness." >&2
    fi
    if "$BROWSER_CMD" \
      --headless \
      --disable-gpu \
      --no-sandbox \
      --run-all-compositor-stages-before-draw \
      --virtual-time-budget=15000 \
      --allow-file-access-from-files \
      --print-to-pdf="$FINAL_OUTPUT" \
      --print-to-pdf-no-header \
      "file://$HTML_OUTPUT" 2>/dev/null; then
      PDF_CREATED=true
      echo "==> PDF created: $FINAL_OUTPUT"
    else
      echo "==> WARN: Browser PDF conversion failed, trying next option..." >&2
    fi
    fi
  fi

  # Option 3: wkhtmltopdf on the HTML file
  if command -v wkhtmltopdf >/dev/null 2>&1 && [ "$PDF_CREATED" = "false" ]; then
    echo "==> Converting to PDF via wkhtmltopdf"
    # Note: wkhtmltopdf can't execute Mermaid JS, so diagrams may not render.
    # But it's better than nothing for the non-Mermaid content.
    echo "    WARN: wkhtmltopdf cannot execute JavaScript; Mermaid diagrams will appear as text." >&2
    if wkhtmltopdf --enable-local-file-access --enable-javascript --javascript-delay 3000 \
      "$HTML_OUTPUT" "$FINAL_OUTPUT" 2>/dev/null; then
      PDF_CREATED=true
      echo "==> PDF created (diagrams may be text): $FINAL_OUTPUT"
    fi
  fi

  # Fallback: save the HTML file instead
  if [ "$PDF_CREATED" = "false" ]; then
    HTML_FALLBACK="${FINAL_OUTPUT%.pdf}.html"
    cp "$HTML_OUTPUT" "$HTML_FALLBACK"
    echo ""
    echo "==> No PDF renderer available. Saved as HTML instead: $HTML_FALLBACK"
    echo "    The HTML file contains live Mermaid diagrams that render in any browser."
    echo ""
    echo "    To get PDF, either:"
    echo "    1. Open the HTML in a browser and print to PDF (Ctrl+P / Cmd+P)"
    echo "    2. Install puppeteer: npm install -g puppeteer"
    echo "    3. Install a non-Snap Chromium/Chrome build with headless PDF support"
    echo "    Then re-run this script."
  fi

else
  # User requested HTML output
  cp "$HTML_OUTPUT" "$FINAL_OUTPUT"
  echo "==> HTML created: $FINAL_OUTPUT"
  echo "    Open in any browser to view rendered Mermaid diagrams."
fi

echo "==> Done."
