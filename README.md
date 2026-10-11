# Codex — Textbook Solutions

[![Deploy to GitHub Pages](https://github.com/Ethanex8/codex/actions/workflows/deploy.yml/badge.svg)](https://github.com/Ethanex8/codex/actions/workflows/deploy.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

A personal, curated collection of verified, step-by-step solutions to problems in standard undergraduate and graduate textbooks.

🌐 **Live Website**: [https://Ethanex8.github.io/codex/](https://Ethanex8.github.io/codex/)

---

## 📚 Active Textbooks

- **Physics**:
  - [John R. Taylor — *Classical Mechanics*](docs/physics/classical-mechanics/taylor/index.md)

---

## 🛠️ Local Development & Preview

The site is built with **[MkDocs Material](https://squidfunk.github.io/mkdocs-material/)** and **MathJax 3**.

### 1. Prerequisites
- Python 3.10+
- `pip`

### 2. Setup Virtual Environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
# For site preview only:
pip install -e .

# For authoring diagrams and computational solutions:
pip install -e ".[diagrams]"
```

### 4. Run Development Server
```bash
mkdocs serve
```
Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser to preview changes live as you edit.

### 5. Build Static Site
```bash
mkdocs build --strict
```

---

## ✍️ Authoring New Solutions

Solutions follow the standard schema documented in [`AGENTS.md`](AGENTS.md):
1. **Frontmatter**: Standard reference admonition with textbook, chapter, problem, and topic metadata.
2. **Fair-Use Paraphrasing**: A clean summary of given quantities and targets.
3. **LaTeX Math**: Use display math blocks (`$$...$$`) with mandatory blank-line padding before and after for MathJax compatibility.
4. **Navigation**: Append the new problem under the active chapter block in `mkdocs.yml`.

---

## 🎨 Custom Diagrams Workflow

Codex employs a purposeful **Dual-Track Workflow** for diagrams (detailed in [`AGENTS.md`](AGENTS.md)):

- **Track A (Geometric & Conceptual)**:
  - Vector decompositions, coordinate frames, right-triangle proofs, free-body diagrams.
  - Authored directly as clean, semantic **Native SVGs** (`figures/fig_XX_YY.svg`) using the Catppuccin Mocha theme tokens.
- **Track B (Computational & Analytical)**:
  - ODE trajectories, numerical phase plots, field curves.
  - Authored as Python scripts (`figures/fig_XX_YY.py`) generating vector SVGs (`figures/fig_XX_YY.svg`). Both files are committed to Git.

---

## 📄 License

Educational content in this repository is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
