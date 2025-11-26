#!/bin/bash
# Create TTF font from SVG glyphs
# Usage: ./svg_to_font.sh <svg-file> <character> <font-name>
#
# Example: ./svg_to_font.sh squaref.svg f YKY-symbols

set -e

if [ $# -lt 3 ]; then
    echo "Usage: $0 <svg-file> <character> <font-name>"
    echo "Example: $0 squaref.svg f YKY-symbols"
    exit 1
fi

SVG_FILE="$1"
CHAR="$2"
FONT_NAME="$3"

# Convert character to Unicode hex
UNICODE=$(printf "%04x" "'$CHAR")

echo "Creating font '$FONT_NAME' with character '$CHAR' (U+$UNICODE)"

# Step 1: Convert strokes to paths using Inkscape
echo "Step 1: Converting strokes to filled paths..."
FILLED_SVG="${SVG_FILE%.svg}-filled.svg"
inkscape "$SVG_FILE" \
    --actions="select-all;object-stroke-to-path;export-filename:$FILLED_SVG;export-plain-svg;export-do" \
    2>/dev/null

# Step 2: Prepare directory structure
echo "Step 2: Preparing directory structure..."
TEMP_DIR="temp_font_$$"
mkdir -p "$TEMP_DIR/svgs"
cp "$FILLED_SVG" "$TEMP_DIR/svgs/u${UNICODE}-${CHAR}.svg"

# Step 3: Generate SVG font
echo "Step 3: Generating SVG font..."
svgicons2svgfont \
    --fontName "$FONT_NAME" \
    --height 1000 \
    --normalize \
    --centerHorizontally \
    --output "$TEMP_DIR/$FONT_NAME.svg" \
    "$TEMP_DIR/svgs/"*.svg

# Step 4: Convert to TTF
echo "Step 4: Converting to TTF..."
svg2ttf "$TEMP_DIR/$FONT_NAME.svg" "${FONT_NAME}.ttf"

# Cleanup
rm -rf "$TEMP_DIR"

echo "✓ Font created: ${FONT_NAME}.ttf"
echo "  Character '$CHAR' is mapped to U+$UNICODE"
