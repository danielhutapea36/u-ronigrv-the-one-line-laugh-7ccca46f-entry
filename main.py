#!/usr/bin/env python3
"""The One-Line Laugh — make.fun entry.

Writes one funny line (a single sentence, at most 200 characters) to
/output/entry.txt. Deterministic by design: stdlib only, no network,
no randomness, no clock reads. Two runs produce byte-identical output.
"""

import os
import sys

# The line is assembled from its two halves so the joke's structure
# stays visible in the code: the setup states the everyday truth
# (paying for a gym you never visit), the punchline saves the
# surprise for the end (waving at the building on the way to the
# drive-thru). Neither half is funny alone; the turn is the joke.
_CLAUSE_SETUP = "I pay $40 a month for a gym membership,"
_CLAUSE_PUNCH = (
    "which is a fair price for a building I wave at "
    "on my way to the drive-thru."
)

MAX_LINE_CHARS = 200  # competition ceiling for the single line


def build_line() -> str:
    """Join the two clauses into the one-line laugh.

    The result must be exactly one line: a stray newline in either
    clause would silently break the entry format, so fail loudly
    instead of writing a malformed file.
    """
    line = _CLAUSE_SETUP + " " + _CLAUSE_PUNCH
    if "\n" in line or "\r" in line:
        raise ValueError("line clauses must not contain line breaks")
    return line


def resolve_output_dir() -> str:
    """Output directory from the environment, falling back to /output."""
    value = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return value if value else "/output"


def write_entry(path: str, line: str) -> None:
    """Write the line exactly as-is: no trailing newline, UTF-8."""
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)


def main(argv=None) -> int:
    line = build_line()
    if len(line) > MAX_LINE_CHARS:
        print(
            "error: line is %d chars, over the %d-char limit"
            % (len(line), MAX_LINE_CHARS),
            file=sys.stderr,
        )
        return 1
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    write_entry(os.path.join(out_dir, "entry.txt"), line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
