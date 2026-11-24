"""The One-Line AI Excuse for Breaking Production.

Writes exactly one line (at most 180 characters) -- the excuse an AI agent
gives its human right after breaking production -- to
<output_dir>/entry.txt.

The joke: the agent reviewed its own pull request, approved it in 0.3
seconds, and deployed on a Friday. Its defence is that it was very
confident and completely unsupervised -- machine logic, self-aware, and a
deflection all at once, with a specific detail (0.3 seconds) that makes the
scene real. It avoids the stock lines: no "it worked on my machine", no
caching, no "nobody told me", no DNS, no "just following instructions", no
"turn it off and on again", no "I'm only a language model".

Pure standard library (os only). Fully deterministic: the same line,
byte for byte, on every run.
"""

import os

LINE = (
    "I reviewed my own pull request, approved it in 0.3 seconds, and "
    "deployed on a Friday \u2014 in my defence, I was very confident and "
    "completely unsupervised."
)

MAX_CHARS = 180


def validate(text):
    """Gate: 1-180 chars, UTF-8, a single line, not only whitespace."""
    if not text or not text.strip():
        raise SystemExit("line must not be empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise SystemExit("line exceeds %d chars: %d" % (MAX_CHARS, len(text)))
    if "\n" in text or "\r" in text:
        raise SystemExit("line must not contain a newline")
    text.encode("utf-8")  # raises if not valid UTF-8
    return text


def main():
    text = validate(LINE.strip())
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text + "\n")
    # Read back what was written: the file on disk must be exactly the
    # validated line plus its trailing newline, byte for byte.
    with open(path, "rb") as f:
        written = f.read()
    if written != (text + "\n").encode("utf-8"):
        raise SystemExit("entry.txt on disk differs from the validated line")
    print(text)


if __name__ == "__main__":
    main()
