# SVG to TTF Font Creation Guide

This guide explains how to create TTF fonts from SVG glyphs (especially from TikZ/LaTeX drawings).

## Prerequisites

### Required Software
```bash
# Node.js 18+ with npm
nvm use 22.2.0  # or your Node version

# Install npm tools globally
npm install -g svgicons2svgfont svg2ttf

# Inkscape (for stroke-to-path conversion)
# Usually available via: apt install inkscape (Linux) or brew install inkscape (macOS)
```

## Workflow

### Step 1: Create SVG from TikZ

Create a standalone LaTeX document:
```latex
\documentclass[tikz,border=0pt]{standalone}
\usepackage{tikz}
\begin{document}
\begin{tikzpicture}[scale=.3,thick]
    \draw (0.3,0) to (0,0) to ++(-0.4,-1.1) to ++(-0.3,0);
    \draw (-0.6,-0.3) to ++(0.9,0);
\end{tikzpicture}
\end{document}
```

Compile to SVG:
```bash
pdflatex squaref.tex
dvisvgm --pdf squaref.pdf -o squaref.svg
```

### Step 2: Convert SVG to TTF

**Using the automated script:**
```bash
chmod +x svg_to_font.sh
./svg_to_font.sh squaref.svg f YKY-symbols
```

**Manual process:**

1. Convert strokes to filled paths:
```bash
inkscape squaref.svg \
    --actions="select-all;object-stroke-to-path;export-filename:squaref-filled.svg;export-plain-svg;export-do"
```

2. Prepare directory structure:
```bash
mkdir -p temp_font/svgs
cp squaref-filled.svg temp_font/svgs/u0066-squaref.svg
# u0066 = Unicode for 'f'
```

3. Generate SVG font:
```bash
svgicons2svgfont \
    --fontName "YKY-symbols" \
    --height 1000 \
    --normalize \
    --centerHorizontally \
    --output temp_font/YKY-symbols.svg \
    temp_font/svgs/*.svg
```

4. Convert to TTF:
```bash
svg2ttf temp_font/YKY-symbols.svg YKY-symbols.ttf
```

## Adding Multiple Characters

### Option 1: Multiple SVG files → Multiple glyphs in one font

```bash
# Prepare SVGs for different characters
inkscape char1.svg --actions="select-all;object-stroke-to-path;export-filename:char1-filled.svg;export-plain-svg;export-do"
inkscape char2.svg --actions="select-all;object-stroke-to-path;export-filename:char2-filled.svg;export-plain-svg;export-do"

# Create directory with all glyphs (Unicode naming is critical)
mkdir -p my_font/svgs
cp char1-filled.svg my_font/svgs/u0066-char1.svg  # f
cp char2-filled.svg my_font/svgs/u0067-char2.svg  # g

# Generate font with all glyphs
svgicons2svgfont \
    --fontName "YKY-symbols" \
    --height 1000 \
    --normalize \
    --centerHorizontally \
    --output my_font/YKY-symbols.svg \
    my_font/svgs/*.svg

svg2ttf my_font/YKY-symbols.svg YKY-symbols.ttf
```

### Option 2: Use FontForge for more control

```bash
# Install FontForge
apt install fontforge  # or: brew install fontforge

# Use FontForge GUI or Python scripting
fontforge -script merge_glyphs.py
```

## Unicode Character Mapping

Common characters and their hex codes:
- `a-z`: U+0061 to U+007A
- `A-Z`: U+0041 to U+005A
- `0-9`: U+0030 to U+0039
- Private Use Area: U+E000 to U+F8FF (for custom symbols)

File naming convention: `u<UNICODE>-<name>.svg`
- Letter 'f': `u0066-squaref.svg`
- Letter 'g': `u0067-squareg.svg`
- Custom symbol: `uE000-mysymbol.svg`

## Using the Font

### In LaTeX with fontspec
```latex
\usepackage{fontspec}
\newfontfamily\ykysymbols{YKY-symbols}

% Use it
{\ykysymbols f}  % Displays your square-f symbol
```

### Install System-Wide
```bash
# Linux
mkdir -p ~/.local/share/fonts
cp YKY-symbols.ttf ~/.local/share/fonts/
fc-cache -f -v

# macOS
cp YKY-symbols.ttf ~/Library/Fonts/

# Windows
# Right-click font file → Install
```

## Troubleshooting

### Empty glyphs in FontForge
**Problem:** Glyphs appear empty when viewing in FontForge.
**Solution:** Your SVG has strokes but no fills. Use Inkscape to convert strokes to paths:
```bash
inkscape input.svg --actions="select-all;object-stroke-to-path;export-filename:output.svg;export-plain-svg;export-do"
```

### Commands not found
**Problem:** `svgicons2svgfont: command not found`
**Solution:** Ensure correct Node.js version and npm global bin is in PATH:
```bash
nvm use 22  # or your Node version
npm install -g svgicons2svgfont svg2ttf
```

### Wrong coordinate system
**Problem:** Glyph appears upside down or misaligned.
**Solution:** Add `--normalize` and `--centerHorizontally` to svgicons2svgfont, or edit SVG viewBox.

## Files in This Project

- `svg_to_font.sh` - Automated script for single glyph
- `create_font.sh` - Original batch script
- `squaref.svg` - Original TikZ-generated SVG
- `squaref-filled.svg` - SVG with strokes converted to paths
- `YKY-symbols.ttf` - Final font file

## References

- [svgicons2svgfont](https://github.com/nfroidure/svgicons2svgfont)
- [svg2ttf](https://github.com/fontello/svg2ttf)
- [FontForge](https://fontforge.org/)
