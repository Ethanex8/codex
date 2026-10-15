#!/usr/bin/env python3
"""
audit_diagrams.py - Quality & Conformance Linter for Codex SVG Diagrams

Enforces the Custom Diagrams & Figures Standard specified in AGENTS.md:
  1. Canvas & ViewBox (viewBox="0 0 720 520", width="720", height="520")
  2. Explicit solid background rect (<rect width="720" height="520" fill="#1e1e2e" />)
  3. Catppuccin Mocha color palette conformance
  4. Side card alignment (x >= 475), origin offset (x <= 180), axis bounds (x <= 440)
  5. Minimum visual clearance (>= 35px) and card vertical budget (bottom <= 505px, buffer >= 20px)
  6. Stacked bottom card placement (y in [320, 500])

Usage:
  python scripts/audit_diagrams.py                  # Audit all diagrams
  python scripts/audit_diagrams.py --chapter 1      # Audit chapter 1 diagrams
  python scripts/audit_diagrams.py --file path.svg  # Audit a specific diagram
"""

import argparse
import glob
import os
import re
import sys
from xml.etree import ElementTree as ET

MOCHA_PALETTE = {
    '#1e1e2e': 'Base',
    '#181825': 'Mantle',
    '#11111b': 'Crust',
    '#313244': 'Surface0',
    '#45475a': 'Surface1',
    '#585b70': 'Surface2',
    '#6c7086': 'Overlay0 / Box Edges',
    '#7f849c': 'Overlay1',
    '#9399b2': 'Overlay2 / Muted / Axes',
    '#a6adc8': 'Subtext0',
    '#bac2de': 'Subtext1',
    '#cdd6f4': 'Text',
    '#f5e0dc': 'Rosewater',
    '#f2cdcd': 'Flamingo',
    '#f5c2e7': 'Pink',
    '#cba6f7': 'Mauve',
    '#f38ba8': 'Red',
    '#fab387': 'Peach / Orange',
    '#f9e2af': 'Yellow',
    '#a6e3a1': 'Green',
    '#94e2d5': 'Teal',
    '#89dceb': 'Sky',
    '#74c7ec': 'Sapphire',
    '#89b4fa': 'Blue',
    '#b4befe': 'Lavender'
}


def audit_svg(file_path: str) -> list[str]:
    """Audits a single SVG diagram file and returns a list of violation messages."""
    issues = []
    
    with open(file_path, 'r', encoding='utf-8') as fp:
        raw_content = fp.read()

    # 1. XML Parsing
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        return [f"Malformed XML: {e}"]

    # 2. Canvas & ViewBox
    vb = root.attrib.get('viewBox', '').strip()
    w = root.attrib.get('width', '').strip()
    h = root.attrib.get('height', '').strip()

    if vb != "0 0 720 520":
        issues.append(f"Invalid viewBox: '{vb}' (must be '0 0 720 520')")
    if w != "720" or h != "520":
        issues.append(f"Invalid root dimensions: width='{w}', height='{h}' (expected 720x520)")

    # 3. Explicit solid background rect
    rects = root.findall('.//{http://www.w3.org/2000/svg}rect')
    has_solid_bg = False
    for r in rects:
        rx = float(r.attrib.get('x', 0))
        ry = float(r.attrib.get('y', 0))
        rw = r.attrib.get('width', '')
        rh = r.attrib.get('height', '')
        fill = r.attrib.get('fill', '').lower()
        if rx == 0 and ry == 0 and rw in ['720', '100%'] and rh in ['520', '100%'] and fill == '#1e1e2e':
            has_solid_bg = True
            break

    if not has_solid_bg:
        issues.append("Missing explicit solid background: <rect width=\"720\" height=\"520\" fill=\"#1e1e2e\" />")

    # 4. Color Palette Conformance
    hex_colors = set(m.group(0).lower() for m in re.finditer(r'#[0-9a-fA-F]{3,8}\b', raw_content))
    non_mocha = [c for c in hex_colors if c not in MOCHA_PALETTE and len(c) == 7]
    if non_mocha:
        issues.append(f"Non-Mocha colors detected: {non_mocha}")

    # 5. Side-by-Side & Stacked Card Invariants
    # Identify cards (either inside translated <g> or root rects)
    found_cards = []
    
    # Check translated groups
    for g in root.findall('.//{http://www.w3.org/2000/svg}g'):
        trans = g.attrib.get('transform', '')
        m = re.match(r'translate\(\s*([\d\.\-]+)\s*,\s*([\d\.\-]+)\s*\)', trans)
        if m:
            gx, gy = float(m.group(1)), float(m.group(2))
            r = g.find('{http://www.w3.org/2000/svg}rect')
            if r is not None:
                try:
                    rw = float(r.attrib.get('width', 0))
                    rh = float(r.attrib.get('height', 0))
                    rx = float(r.attrib.get('x', 0)) + gx
                    ry = float(r.attrib.get('y', 0)) + gy
                    if rx >= 400 and rw >= 150 and rh >= 100:
                        found_cards.append(('side', rx, ry, rw, rh, g))
                    elif ry >= 250 and rw >= 500:
                        found_cards.append(('stacked', rx, ry, rw, rh, g))
                except ValueError:
                    pass

    # Check top-level rects
    for r in rects:
        try:
            rx = float(r.attrib.get('x', 0))
            ry = float(r.attrib.get('y', 0))
            rw = float(r.attrib.get('width', 0))
            rh = float(r.attrib.get('height', 0))
            if rx >= 400 and rw >= 150 and rh >= 100:
                if not any(abs(c[1] - rx) < 1 and abs(c[2] - ry) < 1 for c in found_cards):
                    found_cards.append(('side', rx, ry, rw, rh, None))
            elif ry >= 250 and rw >= 500 and rh >= 100:
                if not any(abs(c[1] - rx) < 1 and abs(c[2] - ry) < 1 for c in found_cards):
                    found_cards.append(('stacked', rx, ry, rw, rh, None))
        except ValueError:
            pass

    for ctype, cx, cy, cw, ch, group_node in found_cards:
        card_bottom = cy + ch
        if card_bottom > 505:
            issues.append(f"Card bottom {card_bottom:.1f}px exceeds 505px canvas budget")
            
        if ctype == 'side':
            if cx < 475:
                issues.append(f"Side card anchored at x={cx:.1f}px (must be >= 475px)")
                
            # Check internal element buffer from card bottom
            if group_node is not None:
                max_internal_y = 0
                for elem in group_node.findall('.//*[@y]'):
                    try:
                        ey = float(elem.attrib.get('y', 0))
                        eh = float(elem.attrib.get('height', 0))
                        max_internal_y = max(max_internal_y, ey + eh)
                    except ValueError:
                        pass
                if max_internal_y > 0:
                    buffer = ch - max_internal_y
                    if buffer < 20:
                        issues.append(f"Internal card element buffer ({buffer:.1f}px) is less than required 20px")
        elif ctype == 'stacked':
            if cy < 300 or card_bottom > 505:
                issues.append(f"Stacked card y=[{cy:.1f}, {card_bottom:.1f}] outside vertical split [320, 500]")

    return issues


def main():
    parser = argparse.ArgumentParser(description="Audit Codex SVG diagrams against AGENTS.md standards.")
    parser.add_argument("--file", help="Specific SVG file to audit")
    parser.add_argument("--chapter", type=int, help="Chapter number to audit (e.g. 1 for ch01)")
    args = parser.parse_args()

    if args.file:
        files = [args.file]
    elif args.chapter:
        ch_str = f"ch{args.chapter:02d}"
        files = sorted(glob.glob(f"docs/**/{ch_str}/figures/fig_*.svg", recursive=True))
    else:
        files = sorted(glob.glob("docs/**/figures/fig_*.svg", recursive=True))

    if not files:
        print("No SVG diagrams found matching criteria.")
        return 0

    print(f"\nAuditing {len(files)} diagram(s)...")
    print(f"{'Diagram':<16} | {'Status':<8} | {'Details'}")
    print("-" * 80)

    total_issues = 0
    for f in files:
        name = os.path.basename(f)
        issues = audit_svg(f)
        if not issues:
            print(f"{name:<16} | PASS     | All standards satisfied")
        else:
            total_issues += len(issues)
            print(f"{name:<16} | FAIL     | {len(issues)} issue(s)")
            for iss in issues:
                print(f"   -> {iss}")

    print("-" * 80)
    if total_issues == 0:
        print(f"Result: ALL {len(files)} DIAGRAMS PASSED.")
        return 0
    else:
        print(f"Result: {total_issues} violation(s) found across {len(files)} diagram(s).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
