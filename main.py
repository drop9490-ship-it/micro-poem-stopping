#!/usr/bin/env python3
"""Micro-text entry (U19): writes one constant text to /output/entry.txt.

The text IS the entry: 1-280 Unicode code points, deterministic.
No network, no model calls. Run: python3 main.py [out_path]
Default output: /output/entry.txt (the grader's path).
"""
import os
import sys

# The entry text. Replaced per competition by the night run from drafts/<name>.txt.
# Must be 1-280 Unicode code points, not whitespace-only, no trailing newline.
TEXT = 'The switch was under my thumb, the work half-done.\nI did not press it. I set the whole thing down.\nThe kettle, the rain, the clock kept their own time.\nStopping is not losing. It is how the hand learns\nthe door was never locked — it only waited\nfor someone willing to stay.'

def main() -> int:
    out = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    d = os.path.dirname(out)
    if d:
        os.makedirs(d, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        f.write(TEXT)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
