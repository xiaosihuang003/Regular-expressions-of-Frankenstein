# regex_for_years.py
# Regular expressions of Frankenstein
# Find occurrences of "for ... years" where "..." is 1..12 words (letters only).
# Outputs: outputs/for_years.csv and outputs/preview.md

from __future__ import annotations
import os
import re
import csv
import textwrap
import requests
from typing import List, Tuple

# ----------------------------
# Config
# ----------------------------
BOOK_URL = "https://www.gutenberg.org/cache/epub/84/pg84.txt"  # Frankenstein
OUT_DIR = "outputs"
CSV_PATH = os.path.join(OUT_DIR, "for_years.csv")
MD_PATH = os.path.join(OUT_DIR, "preview.md")

# How many words we allow between "for" and "years"
MIN_WORDS = 1
MAX_WORDS = 12

# How much context (characters) to show left/right of the match
CONTEXT_CHARS = 80

# Whether to trim Gutenberg header/footer to keep only the main body
TRIM_GUTENBERG = True


# ----------------------------
# Helpers
# ----------------------------
def ensure_out_dir() -> None:
    os.makedirs(OUT_DIR, exist_ok=True)


def download_text(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    # decode to str; requests normally does this, but we normalize newlines
    txt = r.text.replace("\r\n", "\n")
    return txt


def trim_gutenberg_boilerplate(txt: str) -> str:
    """
    Keep the main body between Gutenberg START/END markers.
    If markers are not found, return the original text.
    """
    start = re.search(r"\*\*\* START OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*", txt, re.I)
    end = re.search(r"\*\*\* END OF THIS PROJECT GUTENBERG EBOOK .* \*\*\*", txt, re.I)
    if start and end and start.end() < end.start():
        return txt[start.end(): end.start()]
    return txt


def build_pattern(min_words: int, max_words: int) -> re.Pattern:
    """
    Build a regex that matches:
      for <1..N words of letters (allow spaces/newlines)> years
    Notes:
      - [A-Za-z]+ for a word (letters only)
      - (?:\s+[A-Za-z]+){k} to repeat words with spaces
      - DOTALL makes '.' match newlines if we used it, but here we restrict to letters + whitespace
    """
    if min_words < 1 or max_words < min_words:
        raise ValueError("Invalid MIN/MAX words.")

    # Example for 1..12 words: ([A-Za-z]+(?:\s+[A-Za-z]+){0,11})
    inner = rf"([A-Za-z]+(?:\s+[A-Za-z]+){{0,{max_words-1}}})"
    pat = rf"\bfor\s+{inner}\s+years\b"
    return re.compile(pat, flags=re.IGNORECASE | re.DOTALL)


def normalize_space(s: str) -> str:
    """Collapse any whitespace (including newlines) to single spaces for neat output."""
    return re.sub(r"\s+", " ", s).strip()


# ----------------------------
# Main
# ----------------------------
def main() -> None:
    ensure_out_dir()

    print("[INFO] Downloading Frankenstein from Project Gutenberg ...")
    txt = download_text(BOOK_URL)

    if TRIM_GUTENBERG:
        print("[INFO] Trimming Gutenberg header/footer to keep only the main body ...")
        txt = trim_gutenberg_boilerplate(txt)

    print(f"[INFO] Text length: {len(txt):,} characters")

    print("[INFO] Compiling regex ...")
    pat = build_pattern(MIN_WORDS, MAX_WORDS)

    print("[INFO] Searching matches ...")
    rows: List[Tuple[str, int, int, str, int, str, str]] = []
    for m in pat.finditer(txt):
        start, end = m.span()
        between = normalize_space(m.group(1))
        num_words = len(between.split())

        # Enforce the lower bound (we already enforce the upper bound in the pattern)
        if num_words < MIN_WORDS:
            continue

        left = normalize_space(txt[max(0, start - CONTEXT_CHARS): start])
        right = normalize_space(txt[end: min(len(txt), end + CONTEXT_CHARS)])

        rows.append((m.group(0), start, end, between, num_words, left, right))

    print(f"[INFO] Total matches: {len(rows)}")

    # Write CSV
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["match", "start", "end", "between_words", "num_words", "left_context", "right_context"])
        for r in rows:
            w.writerow(r)

    # Write preview markdown (first up to 20 examples)
    lines = [
        "# Regex: `for … years` in *Frankenstein*",
        "",
        f"Total matches: **{len(rows)}** (MIN_WORDS={MIN_WORDS}, MAX_WORDS={MAX_WORDS})",
        "",
        "### First 20 examples",
        ""
    ]
    for i, (match, start, end, between, num_words, left, right) in enumerate(rows[:20], 1):
        lines.append(f"{i}. `{match}`  — between = `{between}` (words={num_words})")
        ctx = f"...{left} **{match}** {right}..."
        lines.append(f"   - context: {ctx}")
        lines.append("")

    with open(MD_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[INFO] Saved: {CSV_PATH}")
    print(f"[INFO] Saved: {MD_PATH}")
    print("[INFO] Done.")


if __name__ == "__main__":
    main()
