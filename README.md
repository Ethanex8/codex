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
pip install -r requirements.txt
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
3. Add computational snippets or plots when exercises explicitly call for them.
4. Add the new problem file to `mkdocs.yml` under `nav`.

---

## 📄 License

Educational content in this repository is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
