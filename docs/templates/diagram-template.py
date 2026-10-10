"""
Codex Diagram Template
======================
Standard template for authoring reproducible, version-controlled diagrams
and plots using Matplotlib and exporting them as vector SVGs.

Usage:
    python fig_XX_YY.py
Output:
    fig_XX_YY.svg (committed to Git alongside this script)
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# --- Plot & Typography Styling ---
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.size": 12,
    "mathtext.fontset": "cm",        # Computer Modern math font
    "figure.autolayout": True,
    "svg.fonttype": "path",          # Convert glyphs to paths so math renders identical on all systems
})

def generate_diagram(output_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(6, 4), dpi=150)

    # --- Draw Geometry / Axes / Vectors ---
    # Example: Draw coordinate axes
    ax.annotate("", xy=(3, 0), xytext=(-0.5, 0),
                arrowprops=dict(arrowstyle="->", color="#333333", lw=1.5))
    ax.annotate("", xy=(0, 2.5), xytext=(0, -0.5),
                arrowprops=dict(arrowstyle="->", color="#333333", lw=1.5))
    ax.text(3.1, 0, "$x$", va="center", fontsize=13)
    ax.text(0, 2.6, "$y$", ha="center", fontsize=13)

    # Example: Draw a force vector
    ax.annotate("", xy=(2, 1.5), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color="#d32f2f", lw=2))
    ax.text(1.0, 1.0, r"$\mathbf{F}$", color="#d32f2f", fontsize=14, weight="bold")

    # Example: Angle arc
    arc = patches.Arc((0, 0), 1.0, 1.0, angle=0, theta1=0, theta2=36.87,
                      color="#1976d2", lw=1.5)
    ax.add_patch(arc)
    ax.text(0.6, 0.15, r"$\theta$", color="#1976d2", fontsize=12)

    # --- Formatting & Limits ---
    ax.set_xlim(-1, 3.5)
    ax.set_ylim(-1, 3.0)
    ax.set_aspect("equal")
    ax.axis("off")  # Turn off box border for clean free-body/geometric diagrams

    # Save as SVG with transparent background and tight bounding box
    fig.savefig(output_path, format="svg", transparent=True, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved diagram to: {output_path}")

if __name__ == "__main__":
    script_dir = Path(__file__).resolve().parent
    # Outputs an SVG with the same stem name as the script
    output_svg = script_dir / f"{Path(__file__).stem}.svg"
    generate_diagram(output_svg)
