#!/usr/bin/env python3
"""Gate check for a micro-text entry (U19): 1-280 code points + 2-run deterministic.

Usage: python3 check.py [main.py path]
- runs main.py twice into two temp outputs, diffs them (byte-identical required)
- validates the output: UTF-8, 1-280 Unicode code points, not whitespace-only
- greps main.py for network/random tokens as a sanity check
Exit 0 = PASS, 1 = FAIL. Prints counts.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

def main() -> int:
    main_py = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("main.py")
    ok = True
    with tempfile.TemporaryDirectory() as td:
        out1, out2 = Path(td) / "entry1.txt", Path(td) / "entry2.txt"
        for out in (out1, out2):
            r = subprocess.run([sys.executable, str(main_py), str(out)],
                               capture_output=True, text=True, timeout=60)
            if r.returncode != 0:
                print(f"FAIL: main.py exit {r.returncode}: {r.stderr.strip()[:300]}")
                return 1
        b1, b2 = out1.read_bytes(), out2.read_bytes()
        if b1 != b2:
            print("FAIL: outputs differ between runs (not deterministic)")
            return 1
        print("PASS: 2-run deterministic (byte-identical)")
        text = b1.decode("utf-8")
        n = len(text)
        print(f"code points: {n} | bytes: {len(b1)} | ends with newline: {text.endswith(chr(10))}")
        if not 1 <= n <= 280:
            print(f"FAIL: {n} code points outside 1-280")
            ok = False
        else:
            print("PASS: 1-280 code points")
        if not text.strip():
            print("FAIL: whitespace-only")
            ok = False
        else:
            print("PASS: not whitespace-only")
    src = main_py.read_text(encoding="utf-8")
    for bad in ("urllib", "requests", "socket", "http.client", "openai", "random", "datetime"):
        if bad in src:
            print(f"FAIL: main.py contains forbidden token: {bad}")
            ok = False
    if ok:
        print("PASS: no network/random tokens in main.py")
    print("RESULT:", "PASS" if ok else "FAIL")
    return 0 if ok else 1

if __name__ == "__main__":
    raise SystemExit(main())
