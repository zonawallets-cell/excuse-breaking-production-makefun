"""Tests for main.py: the excuse line passes the competition gate.

Run: python3 test_main.py
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MAX_CHARS = 180


def run_entry(out_dir):
    env = dict(os.environ, MAKEFUN_OUTPUT_DIR=out_dir)
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "main.py")],
        env=env, capture_output=True, text=True, timeout=30,
    )
    assert proc.returncode == 0, "main.py failed: %s" % proc.stderr
    with open(os.path.join(out_dir, "entry.txt"), "rb") as f:
        return f.read()


def test_gate():
    data = run_entry(tempfile.mkdtemp())
    text = data.decode("utf-8")
    line = text.rstrip("\n")
    assert text.count("\n") == 1, "entry.txt must be exactly one line"
    assert 1 <= len(line) <= MAX_CHARS, "line is %d chars" % len(line)
    assert line.strip(), "line must not be only whitespace"
    assert "\r" not in text, "no carriage returns"
    print("gate: PASS (%d chars, %d bytes)" % (len(line), len(data)))


def test_deterministic():
    first = run_entry(tempfile.mkdtemp())
    second = run_entry(tempfile.mkdtemp())
    assert first == second, "two runs must be byte-identical"
    print("deterministic: PASS (two runs, identical bytes)")


if __name__ == "__main__":
    test_gate()
    test_deterministic()
    print("all tests passed")
