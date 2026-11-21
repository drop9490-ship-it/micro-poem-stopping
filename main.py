#!/usr/bin/env python3
"""Write one short poem about stopping to /output/entry.txt.

The poem is the entry: a fixed text, 1-280 Unicode code points.
The program takes no input and makes no network calls,
so both grading runs produce the same bytes.
"""

import os
import sys

LINES = [
    "The switch was under my thumb, the work half-done.",
    "I did not press it. I set the whole thing down.",
    "The kettle, the rain, the clock kept their own time.",
    "Stopping is not losing. It is how the hand learns",
    "the door was never locked — it only waited",
    "for someone willing to stay.",
]

POEM = "\n".join(LINES)  # No trailing newline: the gate counts the text as-is.


def write_entry(path: str) -> None:
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(POEM)


def main(argv) -> int:
    target = argv[1] if len(argv) > 1 else os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    write_entry(target)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
