"""Ship the finished poster as the bounty entry image.

poster.png is drawn once, offline, by gen_poster.py and committed beside this
file.  At run time this program does one thing: copy those bytes to the output
directory as entry.png.  A byte copy needs no network, no Pillow and no clock,
so every run produces an identical entry.

Contract:
  * output directory from $MAKEFUN_OUTPUT_DIR, default /output, created if absent
  * poster.png must exist and be at most 1 MiB, or the run stops with an error
  * the destination, its byte count and its sha256 are printed
  * the poster's sha256 is compared with the value recorded below, so a drifted
    or half-written poster is caught before it reaches the judge

Standard library only.
"""

import hashlib
import os
import shutil
import sys

MAX_BYTES = 1_048_576
BLOCK = 1 << 20
SHIPPED_SHA256 = "164bbbd3ee036bb578317d0c0f7951fd5c14aa3438c079bf588767424f43ca74"

HERE = os.path.dirname(os.path.abspath(__file__))
POSTER = os.path.join(HERE, "poster.png")
OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def stop(message):
    sys.stderr.write("error: " + message + "\n")
    raise SystemExit(1)


def digest(path):
    sha = hashlib.sha256()
    with open(path, "rb") as handle:
        while True:
            block = handle.read(BLOCK)
            if not block:
                break
            sha.update(block)
    return sha.hexdigest()


def main():
    if not os.path.isfile(POSTER):
        stop("poster.png is missing next to main.py; run gen_poster.py first")

    size = os.path.getsize(POSTER)
    if size > MAX_BYTES:
        stop("poster.png is %d bytes; the limit is %d" % (size, MAX_BYTES))

    poster_sha = digest(POSTER)
    if poster_sha != SHIPPED_SHA256:
        stop("poster.png is %s, not the shipped %s" % (poster_sha, SHIPPED_SHA256))

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    target = os.path.join(OUTPUT_DIR, "entry.png")
    shutil.copyfile(POSTER, target)

    written = os.path.getsize(target)
    if written != size:
        stop("short write: %d of %d bytes" % (written, size))

    print("poster.png  %s  %d bytes" % (poster_sha, size))
    print("entry.png   %s  %d bytes" % (digest(target), written))


if __name__ == "__main__":
    main()
