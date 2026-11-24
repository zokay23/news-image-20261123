#!/usr/bin/env python3
"""news-image-20261123 entry (v2): write the 23 November 2026 world-news
poster to /output/entry.png, byte-for-byte the committed entry.png.

No network, no randomness: the poster is pre-rendered by build_poster.py
(run it to regenerate entry.png deterministically) and copied here.
The copy is verified with SHA-256 so the output is exactly the entry.
"""

import hashlib
import os
import shutil

ENTRY = "entry.png"
OUT_DIR = "/output"


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, ENTRY)
    os.makedirs(OUT_DIR, exist_ok=True)
    dst = os.path.join(OUT_DIR, ENTRY)
    shutil.copyfile(src, dst)
    src_hash = sha256_file(src)
    dst_hash = sha256_file(dst)
    print("wrote", dst, os.path.getsize(dst), "bytes", "sha256", dst_hash)
    assert src_hash == dst_hash, "copy is not byte-for-byte"


if __name__ == "__main__":
    main()
