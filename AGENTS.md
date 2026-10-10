# Codex Authoring & Collaboration Guidelines

## 1. Problem Lifecycle & Collaborative Protocol
- **Next Problem Auto-Tracking**: Inspect existing solution files in `docs/physics/.../` to determine the next problem in sequence.
- **Problem Extraction**: Use the project utility `python scripts/extract_problem.py --chapter X --problem Y` to fetch the problem statement and inspect the rendered snippet from the local PDF.
- **User-Led Strategy First**: Present the clean problem prompt and given parameters. Then wait for the user to provide their physical intuition, coordinate choice, and strategy.
- **Guiding Principle**: Do not lecture or solve ahead of the user. Only interject or nudge if the user's stated approach contains an error, misconception, or sign trap.
- **Strictly Targeted Solutions**: Keep authored solutions strictly focused on what the exercise asks for. Do not include unrequested remarks, checks, or tangent verification sections.
- **Mobile-Friendly Review**: Always format and print the full mathematical solution directly into the chat response so the user can review and verify on mobile without relying on a localhost browser server.
- **Approval Gate**: Wait for explicit user confirmation before staging and committing. Once committed, automatically fetch and present the next problem in sequence.

## 2. Local Assets & Security
- **Strictly Local**: Textbook PDFs and generated image snippets must reside strictly in `_local_data/` (or external paths) and be excluded by `.gitignore` (`_local_data/`, `*.pdf`). Never stage or commit textbook PDFs or raw copyright scans.
- **Fair Use Problem Paraphrasing**: In the published Markdown solutions, summarize given quantities and target questions clearly in original wording.
