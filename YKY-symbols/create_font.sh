#!/bin/bash
# Convert SVG to TTF using svgicons2svgfont and svg2ttf

# Create a temporary directory structure
mkdir -p temp_font/svgs

# Copy and rename SVG with Unicode codepoint (f = U+0066)
cp squaref.svg temp_font/svgs/u0066-squaref.svg

# Create CSS file for metadata
cat > temp_font/svgs/u0066-squaref.css << 'EOF'
.icon-squaref:before {
  content: "\0066";
}
EOF

# Generate SVG font
svgicons2svgfont \
  --fontName "YKY-symbols" \
  --height 1000 \
  --normalize \
  --centerHorizontally \
  --output temp_font/YKY-symbols.svg \
  temp_font/svgs/*.svg

# Convert SVG font to TTF
svg2ttf temp_font/YKY-symbols.svg temp_font/YKY-symbols.ttf

# Copy to current directory
cp temp_font/YKY-symbols.ttf ./YKY-symbols.ttf

# Cleanup
rm -rf temp_font

echo "Font created: YKY-symbols.ttf"
echo "The glyph is mapped to character 'f' (U+0066)"
