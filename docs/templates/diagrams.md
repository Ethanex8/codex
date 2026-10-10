# Custom Diagrams Guide

All diagrams in **Codex** (free-body diagrams, coordinate frames, geometric setups, and trajectory plots) follow a unified, code-driven standard: **Python scripts that export standalone SVG vector graphics**.

---

## Why Code-Driven SVGs?

1. **Version Controlled & Diffable**: Diagrams are written as plain `.py` code. Anyone can inspect, tweak, or fix an angle, label, or force arrow using standard Git diffs.
2. **Crisp Vector Quality**: SVGs are resolution-independent and render sharply at any zoom level on GitHub.com and the documentation site.
3. **No External GUI Dependencies**: No messy proprietary vector files or complex GUI editors required.

---

## Directory & File Convention

For any problem requiring one or more custom diagrams, create a `figures/` subfolder alongside the problem:

```text
ch01-newton/
├── figures/
│   ├── fig_01_01.py       # Source code that generates the diagram
│   └── fig_01_01.svg      # Rendered vector asset (committed to git)
└── prob-01-01.md          # References figures/fig_01_01.svg
```

---

## Authoring a Diagram

0. Ensure diagram dependencies are installed: `pip install -e ".[diagrams]"`
1. Copy the starter template from [`docs/templates/diagram-template.py`](diagram-template.py).
2. Save it as `figures/fig_XX_YY.py` (matching the chapter and problem number).
3. Use `matplotlib.patches`, annotations, and arrows to compose the figure.
4. Run the script:
   ```bash
   python figures/fig_XX_YY.py
   ```
   This generates `figures/fig_XX_YY.svg`.
5. Embed the SVG in the solution Markdown:
   ```markdown
   ![Free Body Diagram](figures/fig_XX_YY.svg)
   *Figure 1: Free-body diagram. Source: [`figures/fig_XX_YY.py`](figures/fig_XX_YY.py).*
   ```
6. Commit **both** the `.py` script and the `.svg` file to Git.

---

## Standard Styling Guidelines

- **Fonts**: Use standard sans-serif text with Computer Modern math (`"mathtext.fontset": "cm"`).
- **Paths**: Set `plt.rcParams["svg.fonttype"] = "path"` so mathematical symbols and Greek letters render identically on all machines without needing local LaTeX installations.
- **Transparency**: Save figures with `transparent=True` so diagrams blend smoothly across both light and dark site themes.
- **Bounding Box**: Use `bbox_inches="tight"` to eliminate unnecessary white margins.
