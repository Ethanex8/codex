# Custom Diagrams Guide

All diagrams in **Codex** follow a purposeful **Dual-Track Architecture**: choosing the right tool for the nature of the visualization.

---

## The Dual-Track Standard

| Track | Diagram Type | Recommended Tool | File Artifacts |
| :--- | :--- | :--- | :--- |
| **Track A: Geometric & Conceptual** | Coordinate frames, vector decompositions, right-triangle proofs, free-body diagrams, pulleys, optical rays | **Native SVG** (clean, hand-crafted or template-driven XML with semantic styling) | `figures/fig_XX_YY.svg` directly |
| **Track B: Computational & Analytical** | ODE trajectories, numerical simulations, Fourier series, phase portraits, potential energy wells, vector fields | **Python (Matplotlib / NumPy / SciPy)** | `figures/fig_XX_YY.py` generating `figures/fig_XX_YY.svg` |

---

## Why Dual-Track?

1. **Zero Unnecessary Friction for Conceptual Layouts**: Matplotlib is an analytical plotting library, not an illustration tool. Trying to draw geometric proofs in Matplotlib fights projection quirks and introduces heavy Python dependencies (`matplotlib`, `scipy`) where none are needed.
2. **Web & Theme Independence**: Native SVGs render crisp vector geometry, scale responsively via `viewBox`, and can adapt using CSS variables and `<marker>` definitions.
3. **Preserves Code for Genuine Physics**: Computational and numerical problems retain strict Python script reproducibility (`figures/fig_XX_YY.py`) for diffable, repeatable ODE simulations and curves.

---

## Directory & File Convention

For any problem requiring one or more custom diagrams, place them in a `figures/` subfolder alongside the problem:

```text
ch01-newton/
├── figures/
│   ├── fig_01_03.svg      # Track A: Pure vector SVG asset
│   ├── fig_01_04.py       # Track B: Python script for ODE trajectory simulation
│   └── fig_01_04.svg      # Track B: Exported vector plot
└── prob_01_03.md          # References figures/fig_01_03.svg
```

---

## Authoring Guidelines

### Track A: Native SVGs
- Use standard `<svg>` markup with a clear `viewBox` (e.g. `0 0 700 500`).
- Define arrow heads and markers in `<defs>`.
- Use semantic colors and readable font sizes (minimum 12px).
- Embed in the solution Markdown:
  ```markdown
  ![Figure Description](figures/fig_XX_YY.svg)
  ```

### Track B: Python-Driven SVGs
- Copy the starter template from [`docs/templates/diagram-template.py`](diagram-template.py).
- Save as `figures/fig_XX_YY.py`.
- Run `python figures/fig_XX_YY.py` to generate `figures/fig_XX_YY.svg`.
- Embed in the solution Markdown:
  ```markdown
  ![Plot Description](figures/fig_XX_YY.svg)
  *Figure 1: Trajectory plot. Source: [`figures/fig_XX_YY.py`](figures/fig_XX_YY.py).*
  ```
- Commit **both** the `.py` script and the `.svg` file to Git.
