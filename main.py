#!/usr/bin/env python3
"""Write one Wi-Fi network name to /output/entry.txt.

Bounty: Tell a Whole Story in 32 Characters
(u-xvader-tell-a-whole-story-in-32-characters-f86dd978).

The name is the whole entry: it has to land a joke on the first read
and imply a full story in the few words a stranger sees in a phone's
network list. This one is a confession in the form of a network name:
someone chased free Wi-Fi and it cost them their marriage. The twist
is the price tag -- "free" versus "my marriage" -- and the story fills
itself in: the late nights, the neighbour's signal, the divorce papers.

Stdlib only. No network, no temp files, no deleting /output.
"""

import os
import stat
import sys

MAX_CHARS = 32

# The entry. 30 characters, plain ASCII, no trailing newline: the gate
# counts every character in the file, so the file holds exactly this.
NAME = "Free WiFi, Cost Me My Marriage"


def output_dir():
    """Where the grader wants the artifact (default /output)."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def validate(name):
    """Mirror the sealed gate: UTF-8, 1-32 characters, not only spaces."""
    if not isinstance(name, str):
        raise ValueError("entry must be text")
    if not name.strip():
        raise ValueError("entry must not be only whitespace")
    if len(name) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(name), MAX_CHARS)
        )
    name.encode("utf-8")
    return name


def write_entry(name, out_dir):
    """Write entry.txt directly (open + chmod 0644, never a tempfile)."""
    text = validate(name)
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as handle:
        handle.write(text.encode("utf-8"))
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    return path


def self_check(name):
    """Report how the entry stands against the gate, without writing."""
    text = validate(name)
    data = text.encode("utf-8")
    sys.stdout.write("entry : %r\n" % text)
    sys.stdout.write("chars : %d (limit %d)\n" % (len(text), MAX_CHARS))
    sys.stdout.write("bytes : %d\n" % len(data))
    sys.stdout.write("utf-8 : ok, whitespace-only: no\n")
    return 0


def main(argv):
    if argv[1:] == ["--check"]:
        return self_check(NAME)
    path = write_entry(NAME, output_dir())
    sys.stdout.write("wrote %s (%d chars)\n" % (path, len(NAME)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
