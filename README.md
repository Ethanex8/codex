# Codex — Textbook Solutions

[![Deploy to GitHub Pages](https://github.com/Ethanex8/codex/actions/workflows/deploy.yml/badge.svg)](https://github.com/Ethanex8/codex/actions/workflows/deploy.yml)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

An open-source, curated collection of verified, step-by-step solutions to problems in standard undergraduate and graduate textbooks.

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

1. Check the [Solution Template](docs/templates/solution-template.md) for structure and style guidelines.
2. Use LaTeX syntax for mathematical expressions:
   - Inline math: `$E = mc^2$`
   - Display math:
     ```markdown
     $$
     \oint \mathbf{B} \cdot d\mathbf{l} = \mu_0 I_{\text{enc}}
     $$
     ```
3. Add the new problem file to `mkdocs.yml` under `nav`.

---

## 🎨 Custom Diagrams Workflow

All diagrams (free-body diagrams, coordinate frames, geometric setups, plots) are authored with **Python** and exported as **SVG vector graphics**:

1. Use the starter template at [`docs/templates/diagram-template.py`](docs/templates/diagram-template.py).
2. Save it in a `figures/` folder alongside the problem (e.g., `figures/fig_01_01.py`).
3. Run `python figures/fig_01_01.py` to generate `figures/fig_01_01.svg`.
4. Embed the SVG in the solution Markdown:
   ```markdown
   ![Diagram](figures/fig_01_01.svg)
   *Figure: Description. Source: [`figures/fig_01_01.py`](figures/fig_01_01.py).*
   ```
5. Commit **both** the `.py` source and `.svg` asset so diagrams remain 100% version-controlled, diffable, and editable.

See the [Custom Diagrams Guide](docs/templates/diagrams.md) for full styling details.

---

## 📄 License

Educational content in this repository is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
