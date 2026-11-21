#!/usr/bin/env python3
"""Local gate for the poem entry: determinism + 1-280 code points.

Runs main.py twice into temp files, requires byte-identical output,
then validates the text (UTF-8, 1-280 code points, not blank) and
scans main.py for network/random tokens. Exit 0 prints RESULT: PASS.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

FORBIDDEN = ("urllib", "requests", "socket", "http.client", "openai", "random", "datetime")


def run_once(script: Path, out: Path) -> None:
    proc = subprocess.run(
        [sys.executable, str(script), str(out)],
        capture_output=True, text=True, timeout=60,
    )
    if proc.returncode != 0:
        print(f"FAIL: main.py exited {proc.returncode}: {proc.stderr.strip()[:300]}")
        raise SystemExit(1)


def main() -> int:
    script = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("main.py")
    passed = True
    with tempfile.TemporaryDirectory() as tmp:
        first = Path(tmp) / "first.txt"
        second = Path(tmp) / "second.txt"
        run_once(script, first)
        run_once(script, second)
        raw_first = first.read_bytes()
        raw_second = second.read_bytes()
        if raw_first != raw_second:
            print("FAIL: the two runs produced different bytes")
            return 1
        print("PASS: two runs byte-identical")
        text = raw_first.decode("utf-8")
        print(f"code points: {len(text)} | bytes: {len(raw_first)} | trailing newline: {text.endswith(chr(10))}")
        if 1 <= len(text) <= 280:
            print("PASS: 1-280 code points")
        else:
            print(f"FAIL: {len(text)} code points, outside 1-280")
            passed = False
        if text.strip():
            print("PASS: not whitespace-only")
        else:
            print("FAIL: whitespace-only output")
            passed = False
    source = script.read_text(encoding="utf-8")
    found = [token for token in FORBIDDEN if token in source]
    if found:
        print(f"FAIL: forbidden tokens in main.py: {', '.join(found)}")
        passed = False
    else:
        print("PASS: no network/random tokens")
    print("RESULT:", "PASS" if passed else "FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
