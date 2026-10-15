# Codex Authoring & Collaboration Guidelines

## 1. Problem Lifecycle & Collaborative Protocol
- **Next Problem Auto-Tracking**: Infer the next problem in sequence directly from context (e.g., Problem 1.2 follows 1.1). Only list files if jumping chapters or the sequence is ambiguous.
- **Problem Extraction**: Use the project utility `python scripts/extract_problem.py --chapter X --problem Y` to fetch the problem statement and inspect the rendered snippet from the local PDF.
- **Zero Sibling Reading**: Never read existing or neighboring solution files (`prob_XX_YY-1.md`), diagrams (`fig_XX_YY.svg`), or past commit diffs to look up templates, styling, or formatting. All templates, design tokens, and path conventions are self-contained below.
- **User-Led Strategy First**: Present the clean problem prompt and given parameters. Then wait for the user to provide their physical intuition, coordinate choice, and strategy.
- **Guiding Principle**: Do not lecture or solve ahead of the user. Only interject or nudge if the user's stated approach contains an error, misconception, or sign trap.
- **Strictly Targeted Solutions**: Keep authored solutions strictly focused on what the exercise asks for. Do not include unrequested remarks, checks, or tangent verification sections.
- **Minimal Sufficiency in Derivations**: Prioritize the most direct and elegant path. When closure, symmetry, or coordinate invariance relations are available, link the geometric quantity to a single component or vector product and let algebraic relations establish the remaining equalities, rather than computing redundant geometric projections or auxiliary expressions.
- **Pedagogical Scope Alignment**: Align authored explanations and diagram notes strictly with concepts and techniques introduced up to the active section of the textbook. Never invoke future concepts (e.g., forces, potential energy, harmonic oscillators) before they are formally introduced in the text.
- **Mobile-Friendly Review**: Always format and print the full mathematical solution directly into the chat response so the user can review and verify on mobile without relying on a localhost browser server.
- **Approval Gate & Remote Sync**: Wait for explicit user confirmation before staging and committing. Once committed, push to `origin main` so GitHub Pages deploys the update, then automatically fetch and present the next problem in sequence.
- **Build Verification**: When modifying documentation structure or `mkdocs.yml`, verify site integrity locally using `python -m mkdocs build --strict`.
- **Deployment Architecture**: Deployments to GitHub Pages are handled purely via direct Actions artifacts (`upload-pages-artifact` & `deploy-pages`) from `main`. Never re-introduce the `gh-pages` branch or run `mkdocs gh-deploy`.
- **Personal Scope**: This is a personal repository. Never add "Contributing" guidelines, templates, or pull request prompts.

## 2. Directory Hierarchy & Solution Naming Contract
- **Modular Codex Hierarchy**: All solutions follow the book-agnostic layout:
  `docs/<discipline>/<subfield>/<book_slug>/ch<CC>/prob_<CC>_<PP>.md`
  where `<CC>` and `<PP>` are zero-padded two-digit chapter and problem numbers (e.g., `ch01/prob_01_04.md`).
- **Deterministic Path Derivation**: Maintain the active book and chapter directory in session context. Never search or run directory listings to rediscover the active path.
- **Navigation Invariant**: In `mkdocs.yml`, locate and append the problem under the active chapter:
  `- Problem X.Y: <rel_path_to_prob_XX_YY.md>`
  Do not view large sections of `mkdocs.yml`—only read or edit the immediate chapter nav block.
- **Self-Contained Frontmatter Schema**:
  ```markdown
  # Problem X.Y

  !!! info "Textbook Reference"
      - **Textbook**: *[Book Title]* ([Author])
      - **Chapter**: X — [Chapter Title]
      - **Problem**: X.Y
      - **Topic**: [Topic tags]
  ```
- **Diagram Prerequisite**: Purely algebraic or component evaluations do NOT have a diagram or figures section. Only create diagrams (`figures/fig_<CC>_<PP>.svg`) when the problem involves geometric configurations, trajectories, or visual setups. Never inspect previous problem files to check for figure precedent.
- **No Auxiliary Templates**: All frontmatter schemas, diagram standards, and solution layouts are strictly self-contained within `AGENTS.md`. Never create or maintain auxiliary markdown templates in `docs/templates/`.

## 3. Local Assets & Security
- **Strictly Local**: Textbook PDFs and generated image snippets must reside strictly in `_local_data/` (or external paths) and be excluded by `.gitignore` (`_local_data/`, `*.pdf`). Never stage or commit textbook PDFs or raw copyright scans.
- **Fair Use Problem Paraphrasing**: In the published Markdown solutions, summarize given quantities and target questions clearly in original wording.

## 4. Math & Markdown Formatting Invariants
- **Display Math Padding**: Every display math block (`$$...$$`) must have an empty line before and after it. Failing to pad display math causes `pymdownx.arithmatex` to treat it as inline text inside a `<p>` tag, which breaks MathJax browser rendering.
- **No Display Math in Lists**: Never place display math blocks (`$$...$$`) inside ordered (`1.`) or unordered (`-`) list items. Even with blank line padding, markdown list parsers treat nested display blocks as indented paragraph continuations, which frequently breaks mobile MathJax/KaTeX rendering. Use standalone paragraphs or subheadings (`###`, `####`, `#####`) for multi-step derivations instead.

## 5. Custom Diagrams & Figures Standard
- **Directory Layout**: All problem diagrams reside in a `figures/` subfolder alongside the solution file (e.g., `ch01/figures/fig_01_03.svg`).
- **Visual Style Tokens**:
  - **Theme**: Catppuccin Mocha. Background: `#1e1e2e`, Main Text: `#cdd6f4`, Muted / Axes: `#9399b2`, Box Edges: `#6c7086`.
  - **Accent Colors**: Blue (`#89b4fa`), Red (`#f38ba8`), Orange (`#fab387`), Green (`#a6e3a1`).
  - **Canvas**: `viewBox="0 0 720 520"`.
- **Dual-Track Workflow**:
  - **Track A (Geometric / Conceptual)**: Author clean, standalone Native SVGs (`fig_XX_YY.svg`) directly without Python scripts.
  - **Track B (Computational / Analytical)**: Author paired Python scripts (`fig_XX_YY.py`) following `docs/templates/diagram-template.py` to generate `fig_XX_YY.svg`. Commit both.
- **Layout & Collision Invariants**:
  - **Side-by-Side Cards**: When using an info/derivation card on the right ($x \ge 475$), offset coordinate origins leftward ($x \le 180$) and bound horizontal axes/labels to $x \le 440$ to ensure a minimum 35px visual buffer.
  - **Card Vertical Budget**: Size card heights, line spacing, and font sizes so the bottom-most element or highlight box maintains at least a 20px buffer from the card bottom edge, keeping the overall card bottom bound $\le 505\text{px}$ within the 520px canvas.
  - **Vector & Annotation Clearance**: In 2D and 3D projections, select particle evaluation points $P(t)$ that maximize screen angular separation between $\mathbf{v}$, $\mathbf{a}$, and $\mathbf{r}$ ($\ge 45^\circ$). Place dimensional indicators (e.g., pitch, semi-axes, radii) in clear background zones away from vector rays and coordinate axes.
  - **Stacked Layout for Complex Setups**: When vector configurations require wide horizontal spans or lengthy component derivations, use a vertical split: vector geometry in the upper zone ($y \in [40, 290]$) and a full-width derivation card across the bottom ($y \in [320, 500]$).
- **In-Chat Preview**: Render diagram previews in chat responses using an HTML artifact in the conversation artifact directory wrapping the SVG markup inside an `<agent-embed src="file:///<path>/fig_XX_YY_preview.html"></agent-embed>` block. Never re-read external skill docs or templates to construct this.
