#!/usr/bin/env bash
# md-to-pdf.sh — Convert Markdown with Mermaid diagrams to PDF
#
# Strategy: Pre-render Mermaid blocks to images, replace in Markdown, then
# convert the image-embedded Markdown to PDF.
#
# Usage:
#   ./scripts/md-to-pdf.sh input.md [output.pdf]
#
# If output.pdf is omitted, the output file is input-name.pdf in the same directory.
#
# Requirements:
#   - mmdc (npm install -g @mermaid-js/mermaid-cli)  — for Mermaid rendering
#   - pandoc + xelatex OR wkhtmltopdf                — for PDF conversion
#
# If mmdc is missing, Mermaid blocks are replaced with placeholder text.
# If no PDF engine is found, a processed .md file is produced instead.

set -euo pipefail

INPUT="${1:?Usage: md-to-pdf.sh input.md [output.pdf]}"
OUTPUT="${2:-}"

if [ ! -f "$INPUT" ]; then
  echo "Error: File not found: $INPUT" >&2
  exit 1
fi

# Derive output filename if not provided
if [ -z "$OUTPUT" ]; then
  OUTPUT="${INPUT%.md}.pdf"
fi

WORK_DIR="$(mktemp -d)"
trap 'rm -rf "$WORK_DIR"' EXIT

INPUT_ABS="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
PROCESSED_MD="$WORK_DIR/processed.md"

echo "==> Processing: $INPUT"
echo "==> Output:     $OUTPUT"
echo "==> Work dir:   $WORK_DIR"

# --- Check tooling -----------------------------------------------------------

HAS_MMDC=false
if command -v mmdc >/dev/null 2>&1; then
  HAS_MMDC=true
  echo "==> mmdc: $(mmdc --version 2>&1 | head -1)"
else
  echo "==> mmdc: NOT FOUND (Mermaid blocks will be replaced with placeholders)"
fi

PDF_ENGINE="none"
if command -v pandoc >/dev/null 2>&1; then
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
echo "==> PDF engine: $PDF_ENGINE"

# --- Mermaid config for clean PDF output -------------------------------------

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

# --- Puppeteer config (for sandbox-restricted environments) -------------------

PUPPETEER_CONFIG="$WORK_DIR/puppeteer-config.json"
cat > "$PUPPETEER_CONFIG" <<'PCONF'
{
  "args": ["--no-sandbox", "--disable-setuid-sandbox"]
}
PCONF

# --- Extract and render Mermaid blocks ----------------------------------------

DIAGRAM_COUNT=0
IN_MERMAID=false
MERMAID_CONTENT=""

# Process the markdown line by line
# We'll build the processed markdown and extract mermaid blocks
cp "$INPUT_ABS" "$PROCESSED_MD"

# Use awk to find and replace mermaid blocks
awk -v workdir="$WORK_DIR" -v has_mmdc="$HAS_MMDC" '
BEGIN {
  in_mermaid = 0
  diagram_count = 0
  mermaid_content = ""
}

/^```mermaid/ {
  in_mermaid = 1
  diagram_count++
  mermaid_content = ""
  next
}

in_mermaid && /^```$/ {
  in_mermaid = 0
  # Write mermaid content to file
  mmd_file = workdir "/diagram-" diagram_count ".mmd"
  print mermaid_content > mmd_file
  close(mmd_file)

  # Output image reference
  if (has_mmdc == "true") {
    print "![Diagram " diagram_count "](diagram-" diagram_count ".png)"
  } else {
    print ""
    print "> **[Diagram " diagram_count "]** — Mermaid diagram not rendered (mmdc not installed)."
    print "> Install with: npm install -g @mermaid-js/mermaid-cli"
    print ""
  }
  next
}

in_mermaid {
  if (mermaid_content == "") {
    mermaid_content = $0
  } else {
    mermaid_content = mermaid_content "\n" $0
  }
  next
}

{ print }
' "$INPUT_ABS" > "$PROCESSED_MD"

# Count how many diagrams we extracted
DIAGRAM_COUNT=$(ls "$WORK_DIR"/diagram-*.mmd 2>/dev/null | wc -l || echo 0)
echo "==> Found $DIAGRAM_COUNT Mermaid diagram(s)"

# Render each diagram
if [ "$HAS_MMDC" = "true" ] && [ "$DIAGRAM_COUNT" -gt 0 ]; then
  for mmd_file in "$WORK_DIR"/diagram-*.mmd; do
    base="$(basename "$mmd_file" .mmd)"
    png_file="$WORK_DIR/${base}.png"
    echo "    Rendering: $base"

    if mmdc \
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
      echo "    WARN: mmdc failed for $base, falling back to placeholder" >&2
      # Replace image ref with placeholder in processed markdown
      sed -i "s|!\[Diagram ${base#diagram-}\](${base}.png)|> **[Diagram ${base#diagram-}]** — Rendering failed. See source Markdown for Mermaid code.|" "$PROCESSED_MD"
    fi
  done
fi

# --- Convert to PDF ----------------------------------------------------------

cd "$WORK_DIR"

case "$PDF_ENGINE" in
  pandoc-xelatex)
    echo "==> Converting with pandoc + xelatex"
    pandoc "$PROCESSED_MD" -o "$OUTPUT" \
      --pdf-engine=xelatex \
      -V geometry:margin=1in \
      -V mainfont="DejaVu Sans" \
      -V monofont="DejaVu Sans Mono" \
      --highlight-style=tango \
      --toc \
      -f markdown+implicit_figures
    echo "==> PDF created: $OUTPUT"
    ;;

  pandoc-weasyprint)
    echo "==> Converting with pandoc + weasyprint"
    pandoc "$PROCESSED_MD" -o "$OUTPUT" \
      --pdf-engine=weasyprint \
      --toc \
      -f markdown+implicit_figures
    echo "==> PDF created: $OUTPUT"
    ;;

  pandoc-html-wkhtmltopdf)
    echo "==> Converting via pandoc (HTML) + wkhtmltopdf"
    pandoc "$PROCESSED_MD" -o "$WORK_DIR/temp.html" \
      --standalone \
      --toc \
      -f markdown+implicit_figures
    wkhtmltopdf --enable-local-file-access "$WORK_DIR/temp.html" "$OUTPUT"
    echo "==> PDF created: $OUTPUT"
    ;;

  pandoc-noengine)
    echo "==> pandoc found but no PDF engine; producing HTML instead"
    HTML_OUT="${OUTPUT%.pdf}.html"
    pandoc "$PROCESSED_MD" -o "$HTML_OUT" \
      --standalone \
      --toc \
      -f markdown+implicit_figures
    echo "==> HTML created (no PDF engine): $HTML_OUT"
    echo "    Convert to PDF by opening in a browser and printing, or install xelatex/wkhtmltopdf."
    ;;

  wkhtmltopdf)
    echo "==> Converting with wkhtmltopdf (no pandoc)"
    # Convert MD to HTML manually (basic)
    if command -v pandoc >/dev/null 2>&1; then
      pandoc "$PROCESSED_MD" -o "$WORK_DIR/temp.html" --standalone
    else
      # Minimal HTML wrapper
      {
        echo "<html><head><meta charset='utf-8'><style>body{font-family:sans-serif;margin:2em;} img{max-width:100%;} pre{background:#f5f5f5;padding:1em;overflow-x:auto;} code{font-family:monospace;}</style></head><body>"
        cat "$PROCESSED_MD"
        echo "</body></html>"
      } > "$WORK_DIR/temp.html"
    fi
    wkhtmltopdf --enable-local-file-access "$WORK_DIR/temp.html" "$OUTPUT"
    echo "==> PDF created: $OUTPUT"
    ;;

  none)
    echo "==> No PDF engine found. Saving processed Markdown with image references."
    PROCESSED_OUT="${OUTPUT%.pdf}-processed.md"
    cp "$PROCESSED_MD" "$PROCESSED_OUT"

    if [ "$DIAGRAM_COUNT" -gt 0 ] && [ "$HAS_MMDC" = "true" ]; then
      # Also copy rendered images next to the processed markdown
      IMG_DIR="$(dirname "$PROCESSED_OUT")/diagrams"
      mkdir -p "$IMG_DIR"
      cp "$WORK_DIR"/diagram-*.png "$IMG_DIR/" 2>/dev/null || true
      echo "==> Images saved to: $IMG_DIR/"
    fi

    echo "==> Processed Markdown: $PROCESSED_OUT"
    echo "    Install pandoc + xelatex or wkhtmltopdf to generate PDF."
    ;;
esac

echo "==> Done."
