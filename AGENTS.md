# Codex Authoring & Collaboration Guidelines

## 1. Problem Lifecycle & Collaborative Protocol
- **Next Problem Auto-Tracking**: Infer the next problem in sequence directly from context (e.g., Problem 1.2 follows 1.1). Only list files if jumping chapters or the sequence is ambiguous.
- **Problem Extraction**: Use the project utility `python scripts/extract_problem.py --chapter X --problem Y` to fetch the problem statement and inspect the rendered snippet from the local PDF.
- **Minimal Context Reading**: Do NOT re-read existing solution files, textbook overview pages, or navigation configs for routine formatting style. Reuse established structure and formatting directly without unneeded file inspection.
- **User-Led Strategy First**: Present the clean problem prompt and given parameters. Then wait for the user to provide their physical intuition, coordinate choice, and strategy.
- **Guiding Principle**: Do not lecture or solve ahead of the user. Only interject or nudge if the user's stated approach contains an error, misconception, or sign trap.
- **Strictly Targeted Solutions**: Keep authored solutions strictly focused on what the exercise asks for. Do not include unrequested remarks, checks, or tangent verification sections.
- **Mobile-Friendly Review**: Always format and print the full mathematical solution directly into the chat response so the user can review and verify on mobile without relying on a localhost browser server.
- **Approval Gate & Remote Sync**: Wait for explicit user confirmation before staging and committing. Once committed, push to `origin main` so GitHub Pages deploys the update, then automatically fetch and present the next problem in sequence.
- **Personal Scope**: This is a personal repository. Never add "Contributing" guidelines, templates, or pull request prompts.

## 2. Local Assets & Security
- **Strictly Local**: Textbook PDFs and generated image snippets must reside strictly in `_local_data/` (or external paths) and be excluded by `.gitignore` (`_local_data/`, `*.pdf`). Never stage or commit textbook PDFs or raw copyright scans.
- **Fair Use Problem Paraphrasing**: In the published Markdown solutions, summarize given quantities and target questions clearly in original wording.

## 3. Math & Markdown Formatting Invariants
- **Display Math Padding**: Every display math block (`$$...$$`) must have an empty line before and after it. Failing to pad display math causes `pymdownx.arithmatex` to treat it as inline text inside a `<p>` tag, which breaks MathJax browser rendering.

## 4. Custom Diagrams & Figures Standard
- **Directory Layout**: All problem diagrams reside in a `figures/` subfolder alongside the solution file (e.g., `ch01/figures/fig_01_03.svg`).
- **Dual-Track Workflow**:
  - **Track A (Geometric / Conceptual)**: Author clean, standalone Native SVGs (`fig_XX_YY.svg`) directly without Python scripts.
  - **Track B (Computational / Analytical)**: Author paired Python scripts (`fig_XX_YY.py`) following `docs/templates/diagram-template.py` to generate `fig_XX_YY.svg`. Commit both.
- **In-Chat Preview via Generative UI**: Because raw SVG markup is sanitized in chat markdown, render diagram previews in chat responses using an HTML artifact embedded via `<agent-embed src="...">` so the user can verify it inline on mobile or desktop.
- **Project Permissions**: Project-specific tool permissions belong in `~/.gemini/config/projects/<project-id>.json`, never in global permission configs.

