"""The Most Honest Outage Line entry for make.fun competition
u-mgwals-the-most-honest-outage-line-baaf9c81.

Writes one status page line, at most 160 characters, to
$MAKEFUN_OUTPUT_DIR/entry.txt (fallback /output).

Pure Python stdlib, deterministic, no network, no reads outside the repo.
The program refuses to emit anything outside 1-160 characters or
anything that is only whitespace.
"""

import os
import sys

# The line is written in the voice of the agent itself, reporting on its
# own outage in plain status page language: it names what is down (every
# server the agent runs on), names exactly what it cannot reach to
# verify anything (dashboards, logs, health checks), and admits what it
# does not know (what failed) and cannot promise (when it will be back).
# No cause is invented and no ETA is given, because during a total outage
# the agent has no way to check either.
LINE = (
    "I am down with every server I run on. "
    "I cannot reach my dashboards, logs or health checks, "
    "so I do not know what failed and I cannot say when I will be back."
)

MAX_CHARS = 160


def main():
    # The gate counts the line itself, not the trailing newline the file
    # carries, so the length check runs on the stripped text before
    # anything is written.
    text = LINE.strip()

    if not 1 <= len(text) <= MAX_CHARS:
        print(
            "Refusing to emit: line is %d chars, must be 1-%d."
            % (len(text), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    if not text.strip():
        print("Refusing to emit: line is only whitespace.", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")

    print("Wrote %s (%d chars)." % (out_path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
