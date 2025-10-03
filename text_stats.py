#!/usr/bin/env python3
"""
text_stats.py
Quick text analytics from a file or STDIN.

Shows:
- lines, words, characters
- top N most frequent words (case-insensitive, alphanumeric)

Usage:
  python3 text_stats.py README.md
  cat README.md | python3 text_stats.py
  python3 text_stats.py --top 5 notes.txt
"""

import sys
import re
from collections import Counter
from typing import Iterable

WORD_RE = re.compile(r"[A-Za-z0-9]+")

def read_lines(path: str | None) -> Iterable[str]:
    if path:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            yield from f
    else:
        # read from stdin
        for line in sys.stdin:
            yield line

def stats(lines: Iterable[str], top: int = 10) -> str:
    text = "".join(lines)
    line_count = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    char_count = len(text)
    words = [w.lower() for w in WORD_RE.findall(text)]
    word_count = len(words)
    freq = Counter(words).most_common(top)

    out = []
    out.append(f"Lines: {line_count}")
    out.append(f"Words: {word_count}")
    out.append(f"Characters: {char_count}")
    if top > 0 and freq:
        out.append(f"\nTop {min(top, len(freq))} words:")
        for w, c in freq:
            out.append(f"  {w:<15} {c}")
    return "\n".join(out)

def main():
    args = sys.argv[1:]
    top = 10
    path = None

    if args and args[0] == "--top":
        if len(args) < 2 or not args[1].isdigit():
            print("Usage: python3 text_stats.py [--top N] [file]")
            sys.exit(2)
        top = int(args[1])
        args = args[2:]

    if args:
        path = args[0]

    print(stats(read_lines(path), top=top))

if __name__ == "__main__":
    main()
