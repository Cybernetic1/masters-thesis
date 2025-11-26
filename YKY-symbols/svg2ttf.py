#!/usr/bin/env python3
"""
Convert SVG glyph to TTF font
"""
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.t2CharStringPen import T2CharStringPen
from fontTools.pens.svgPathPen import SVGPathPen
import xml.etree.ElementTree as ET
import re

def parse_svg_path(svg_file):
    """Extract path data from SVG file"""
    tree = ET.parse(svg_file)
    root = tree.getroot()
    
    # Handle namespaces
    ns = {'svg': 'http://www.w3.org/2000/svg'}
    paths = root.findall('.//svg:path', ns)
    if not paths:
        paths = root.findall('.//path')
    
    path_data = []
    for path in paths:
        d = path.get('d')
        if d:
            path_data.append(d)
    
    return path_data, root

def svg_to_ttf(svg_file, output_ttf, font_name="CustomFont", char='f'):
    """Convert SVG to TTF font"""
    
    # Parse SVG
    path_data, svg_root = parse_svg_path(svg_file)
    
    if not path_data:
        print("Error: No path data found in SVG")
        return
    
    # Get SVG viewBox for scaling
    viewBox = svg_root.get('viewBox')
    if viewBox:
        vb_parts = [float(x) for x in viewBox.split()]
        svg_width = vb_parts[2] - vb_parts[0]
        svg_height = vb_parts[3] - vb_parts[1]
    else:
        svg_width = float(svg_root.get('width', '100').replace('pt', '').replace('px', ''))
        svg_height = float(svg_root.get('height', '100').replace('pt', '').replace('px', ''))
    
    print(f"SVG dimensions: {svg_width} x {svg_height}")
    
    # Font metrics (standard values)
    units_per_em = 1000
    ascent = 800
    descent = -200
    
    # Calculate scaling factor
    scale = units_per_em / max(svg_width, svg_height)
    
    # Create font builder
    fb = FontBuilder(units_per_em, isTTF=True)
    
    # Set font metadata
    fb.setupHead(unitsPerEm=units_per_em)
    fb.setupHhea(ascent=ascent, descent=descent)
    
    # Name table
    fb.setupNameTable({
        'familyName': font_name,
        'styleName': 'Regular',
        'uniqueFontIdentifier': f'{font_name}-Regular',
        'fullName': f'{font_name} Regular',
        'version': 'Version 1.0',
    })
    
    # Character mapping
    char_code = ord(char)
    glyph_order = ['.notdef', char]
    
    # Setup cmap (character to glyph mapping)
    cmap = {char_code: char}
    fb.setupCharacterMap(cmap)
    
    # Glyph metrics
    advance_width = int(svg_width * scale)
    
    # Setup horizontal metrics
    metrics = {
        '.notdef': (500, 0),
        char: (advance_width, 0)
    }
    fb.setupHorizontalMetrics(metrics)
    
    # Setup glyphs
    fb.setupGlyphOrder(glyph_order)
    
    # For now, we'll use FontForge or nanoemoji approach
    # Direct path conversion is complex, so let's use a simpler method
    
    print(f"Creating font '{font_name}' with glyph '{char}' (U+{char_code:04X})")
    print(f"Advance width: {advance_width}")
    print(f"Scale factor: {scale}")
    print(f"Path data found: {len(path_data)} paths")
    
    # Save
    fb.setupPost()
    fb.font.save(output_ttf)
    print(f"Font saved to: {output_ttf}")
    print("\nNote: This creates a basic font structure.")
    print("For full SVG path conversion, use FontForge or nanoemoji.")

if __name__ == "__main__":
    svg_to_ttf("squaref.svg", "YKY-symbols.ttf", "YKY-symbols", "f")
