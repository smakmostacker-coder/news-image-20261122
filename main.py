#!/usr/bin/env python3
"""Entry program for make.fun's news-image-20261122 bounty.

The repository holds entry.png, a one-image summary of the world news of
Sunday 22 November 2026 (drawn by make_image.py). This program copies it to
the output directory the grader provides: /output inside the sandbox, or
$MAKEFUN_OUTPUT_DIR when run locally:

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

Standard library only, no network, deterministic: both grader runs copy
the same committed bytes.
"""

import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHUNK = 64 * 1024


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    # Stream the copy in fixed chunks so the bytes written never depend on
    # anything but the committed entry.png itself.
    with open(HERE / "entry.png", "rb") as src, open(out_dir / "entry.png", "wb") as dst:
        while True:
            block = src.read(CHUNK)
            if not block:
                break
            dst.write(block)


if __name__ == "__main__":
    main()
