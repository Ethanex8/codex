"""Textbook problem extractor utility for Codex.

Extracts problem prompts and renders high-resolution problem snippet images
from locally stored textbook PDFs in `_local_data/books/`.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import pymupdf
except ImportError:
    try:
        import fitz as pymupdf
    except ImportError:
        print("Error: PyMuPDF is required. Run: pip install pymupdf", file=sys.stderr)
        sys.exit(1)


DEFAULT_BOOK_PATH = Path("_local_data/books/taylor_classical_mechanics.pdf")
SNIPPETS_DIR = Path("_local_data/snippets")


def find_problem_in_pdf(
    doc: pymupdf.Document, chapter: int, problem: int
) -> tuple[int, pymupdf.Rect | None, str]:
    """Search for the problem text and bounding rect across the document pages."""
    # Pattern to match problem headers in exercises, e.g. "1.2 *", "1.2*", "1.2 **", "1.2 ★"
    prob_pattern = re.compile(
        rf"^\s*{chapter}\.{problem}\s*[\*★]", re.MULTILINE
    )

    # Next problem pattern to delimit boundary
    next_prob_pattern = re.compile(
        rf"^\s*{chapter}\.{problem + 1}\s*[\*★]", re.MULTILINE
    )

    found_page = -1
    found_rect = None
    extracted_text = ""

    # Most problems appear in the end of chapter problem sections
    for page_idx in range(len(doc)):
        page = doc[page_idx]
        text = page.get_text()

        # Check if this page has the problem number
        match = prob_pattern.search(text)
        if match:
            found_page = page_idx
            # Try to locate the text rect
            search_str = text[match.start() : match.end()].strip()
            rects = page.search_for(search_str)
            if not rects:
                rects = page.search_for(f"{chapter}.{problem}")

            if rects:
                found_rect = rects[0]

            # Extract text block from this problem up to the next problem or end of page
            start_pos = match.start()
            next_match = next_prob_pattern.search(text, pos=match.end())
            if next_match:
                extracted_text = text[start_pos : next_match.start()].strip()
            else:
                extracted_text = text[start_pos:].strip()
            break

    return found_page, found_rect, extracted_text


def extract_and_save(
    pdf_path: Path, chapter: int, problem: int, save_image: bool = True
) -> dict:
    if not pdf_path.exists():
        raise FileNotFoundError(f"Textbook PDF not found at {pdf_path}")

    doc = pymupdf.open(str(pdf_path))
    page_idx, rect, text = find_problem_in_pdf(doc, chapter, problem)

    if page_idx == -1:
        return {"found": False, "message": f"Problem {chapter}.{problem} not found"}

    result = {
        "found": True,
        "chapter": chapter,
        "problem": problem,
        "page_index": page_idx,
        "pdf_page_number": page_idx + 1,
        "text": text,
        "image_path": None,
    }

    if save_image and rect:
        SNIPPETS_DIR.mkdir(parents=True, exist_ok=True)
        page = doc[page_idx]
        # Crop around the problem: wider horizontal, extending vertically
        clip_rect = pymupdf.Rect(
            max(0, rect.x0 - 15),
            max(0, rect.y0 - 8),
            page.rect.width - 20,
            min(page.rect.height, rect.y1 + 120),
        )
        pix = page.get_pixmap(clip=clip_rect, dpi=200)
        img_name = f"prob_{chapter:02d}_{problem:02d}.png"
        out_path = SNIPPETS_DIR / img_name
        pix.save(str(out_path))
        result["image_path"] = str(out_path)

    return result


def main():
    parser = argparse.ArgumentParser(description="Extract textbook problems from local PDF")
    parser.add_argument("--chapter", "-c", type=int, required=True, help="Chapter number")
    parser.add_argument("--problem", "-p", type=int, required=True, help="Problem number")
    parser.add_argument(
        "--pdf",
        type=Path,
        default=DEFAULT_BOOK_PATH,
        help="Path to textbook PDF (default: _local_data/books/taylor_classical_mechanics.pdf)",
    )
    parser.add_argument(
        "--no-image",
        action="store_true",
        help="Do not render problem snippet image",
    )

    args = parser.parse_args()

    res = extract_and_save(args.pdf, args.chapter, args.problem, save_image=not args.no_image)
    if not res["found"]:
        print(f"[-] {res['message']}")
        sys.exit(1)

    print(f"[+] Found Problem {args.chapter}.{args.problem} on PDF page {res['pdf_page_number']}")
    if res["image_path"]:
        print(f"[+] Snippet image saved to: {res['image_path']}")
    print("-" * 60)
    print(res["text"])
    print("-" * 60)


if __name__ == "__main__":
    main()
