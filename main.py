#!/usr/bin/env python3
"""Unsent: The Micro-Confession Sprint.

Writes one original micro-confession to $MAKEFUN_OUTPUT_DIR/entry.txt
(fallback /output/entry.txt) and prints it to stdout.

The entry is exactly two parts, per the competition rules:
  - a To: line naming who the message was meant for, and
  - the unsent message itself, one line, exactly as it was typed.

Gate respected: the whole file is UTF-8 text of 1-260 characters,
not only whitespace; the message line is at most 200 characters.
No network, no clock, no randomness: the output is deterministic.
"""

import os
import sys

TO_LINE = "To: the neighbour in 4B"
MESSAGE = (
    "you moved out in march and i still check the hallway for your "
    "shoes every night because your spare key is the only reason "
    "anyone ever knocked on my door"
)

MAX_TOTAL_CHARS = 260
MAX_MESSAGE_CHARS = 200


def build_entry() -> str:
    """Assemble the two-part confession, trailing newline included."""
    return TO_LINE + "\n" + MESSAGE + "\n"


def validate(entry: str) -> str | None:
    """Return an error message if the entry breaks a competition rule."""
    if not (1 <= len(entry) <= MAX_TOTAL_CHARS):
        return f"entry is {len(entry)} characters, outside the 1-260 gate"
    if entry.strip() == "":
        return "entry is only whitespace"
    if not TO_LINE.startswith("To: "):
        return "To: line must name who the message was meant for"
    parts = entry.strip().split("\n")
    if len(parts) != 2:
        return f"entry must have exactly two parts, found {len(parts)}"
    if len(MESSAGE) > MAX_MESSAGE_CHARS:
        return (
            f"message line is {len(MESSAGE)} characters, over the 200 limit"
        )
    return None


def main() -> int:
    entry = build_entry()

    error = validate(entry)
    if error is not None:
        print(error, file=sys.stderr)
        return 1

    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(entry)

    # Confirm what landed on disk is byte-for-byte what we built.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        if handle.read() != entry:
            print("written entry does not match the built entry", file=sys.stderr)
            return 1

    sys.stdout.write(entry)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
