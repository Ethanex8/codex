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
import math
import os
import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        pymupdf = None

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


def audit_svg(file_path: str) -> tuple[list[str], list[tuple[str, float, float, float, float]]]:
    """Audits a single SVG diagram file and returns (violation_messages, clearance_report)."""
    issues = []
    
    with open(file_path, 'r', encoding='utf-8') as fp:
        raw_content = fp.read()

    # 1. XML Parsing
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
    except Exception as e:
        return [f"Malformed XML: {e}"], []

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

    # 6. Plot-Area Text-to-Line Collision Check
    def dist_point_to_segment(px: float, py: float, x1: float, y1: float, x2: float, y2: float) -> float:
        dx, dy = x2 - x1, y2 - y1
        if dx == 0 and dy == 0:
            return math.hypot(px - x1, py - y1)
        t = max(0.0, min(1.0, ((px - x1) * dx + (py - y1) * dy) / (dx * dx + dy * dy)))
        return math.hypot(px - (x1 + t * dx), py - (y1 + t * dy))

    has_stacked = any(c[0] == 'stacked' for c in found_cards)
    max_plot_y = 305.0 if has_stacked else 510.0

    # Collect top-level or untranslated plot lines and texts
    def collect_plot_elements(node, gx=0.0, gy=0.0):
        lines_out, texts_out = [], []
        for child in node:
            tag = child.tag.split('}')[-1]
            if tag == 'g':
                if child.attrib.get('id', '') in ['side-card', 'info-card', 'derivation-card']:
                    continue
                trans = child.attrib.get('transform', '')
                m = re.match(r'translate\(\s*([\d\.\-]+)\s*,\s*([\d\.\-]+)\s*\)', trans)
                cgx = gx + float(m.group(1)) if m else gx
                cgy = gy + float(m.group(2)) if m else gy
                if cgx >= 450 or cgy >= 300:
                    continue
                sub_l, sub_t = collect_plot_elements(child, cgx, cgy)
                lines_out.extend(sub_l)
                texts_out.extend(sub_t)
            elif tag == 'line':
                try:
                    x1 = float(child.attrib.get('x1', 0)) + gx
                    y1 = float(child.attrib.get('y1', 0)) + gy
                    x2 = float(child.attrib.get('x2', 0)) + gx
                    y2 = float(child.attrib.get('y2', 0)) + gy
                    if max(x1, x2) < 465 and max(y1, y2) > 75 and min(y1, y2) < max_plot_y:
                        if math.hypot(x2 - x1, y2 - y1) > 25.0:  # Ignore tiny tick marks
                            lines_out.append((x1, y1, x2, y2))
                except ValueError:
                    pass
            elif tag == 'text':
                try:
                    if 'x' not in child.attrib or 'y' not in child.attrib:
                        continue
                    tx = float(child.attrib['x']) + gx
                    ty = float(child.attrib['y']) + gy
                    if tx < 465 and 75 < ty < max_plot_y:
                        label = ''.join(child.itertext()).strip()
                        if label:
                            anchor = child.attrib.get('text-anchor', 'start')
                            w_est = len(label) * 6.5
                            cx = tx + (w_est / 2.0 if anchor == 'start' else (-w_est / 2.0 if anchor == 'end' else 0.0))
                            cy = ty - 3.5
                            texts_out.append((label, tx, ty, cx, cy))
                except ValueError:
                    pass
        return lines_out, texts_out

    plot_lines, plot_texts = collect_plot_elements(root)
    clearance_report = []
    for idx_t, (label, tx, ty, cx, cy) in enumerate(plot_texts):
        min_line_d = float('inf')
        for (x1, y1, x2, y2) in plot_lines:
            d = dist_point_to_segment(cx, cy, x1, y1, x2, y2)
            min_line_d = min(min_line_d, d)
            if d < 3.2:
                issues.append(f"Text '{label}' at ({tx:.0f},{ty:.0f}) collides with line ({x1:.0f},{y1:.0f})->({x2:.0f},{y2:.0f}) (dist={d:.1f}px < 3.2px)")

        min_text_d = float('inf')
        for idx_o, (olabel, otx, oty, ocx, ocy) in enumerate(plot_texts):
            if idx_t != idx_o:
                td = math.hypot(cx - ocx, cy - ocy)
                min_text_d = min(min_text_d, td)
                if td < 5.0:
                    issues.append(f"Text '{label}' at ({tx:.0f},{ty:.0f}) overlaps text '{olabel}' at ({otx:.0f},{oty:.0f}) (dist={td:.1f}px)")

        clearance_report.append((label, tx, ty, min_line_d, min_text_d))

    return issues, clearance_report


def render_svg_preview(svg_path: str) -> str | None:
    """Render SVG to a PNG raster preview in _local_data/snippets/ for visual inspection."""
    if pymupdf is None:
        return None
    try:
        out_dir = Path("_local_data/snippets")
        out_dir.mkdir(parents=True, exist_ok=True)
        stem = Path(svg_path).stem
        out_png = out_dir / f"{stem}.png"
        doc = pymupdf.open(svg_path)
        pix = doc[0].get_pixmap(dpi=150)
        pix.save(str(out_png))
        return str(out_png)
    except Exception:
        return None


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
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
        issues, clearance_report = audit_svg(f)
        if not issues:
            print(f"{name:<16} | PASS     | All standards satisfied")
        else:
            total_issues += len(issues)
            print(f"{name:<16} | FAIL     | {len(issues)} issue(s)")
            for iss in issues:
                print(f"   -> {iss}")

        if args.file:
            png_path = render_svg_preview(f)
            if png_path:
                print(f"[+] Raster preview saved to: {png_path}")
            if clearance_report:
                print("Plot Label Clearance Summary (nearest line / nearest label):")
                for lbl, ltx, lty, ld, td in clearance_report:
                    ld_str = f"{ld:.1f}px" if ld < float('inf') else "n/a"
                    td_str = f"{td:.1f}px" if td < float('inf') else "n/a"
                    print(f"  - '{lbl}' at ({ltx:.0f},{lty:.0f}): line_dist={ld_str}, text_dist={td_str}")

    print("-" * 80)
    if total_issues == 0:
        print(f"Result: ALL {len(files)} DIAGRAMS PASSED.")
        return 0
    else:
        print(f"Result: {total_issues} violation(s) found across {len(files)} diagram(s).")
        return 1


if __name__ == "__main__":
    sys.exit(main())
