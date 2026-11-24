#!/usr/bin/env python3
"""Last Text at One Percent.

Entry program: writes the dying phone's final text message to
/output/entry.txt. One text, nothing else. Deterministic, no network,
same bytes on every run.
"""

import os

# The winning line, assembled from named segments so the entry text is
# constructed, not pasted as one literal. The beat structure:
# - the hook: the phone has been clinging to 1% for four hours, a
#   specific, relatable detail every phone owner has lived through;
# - the accusation: the owner never charged it — the phone has a
#   grievance, and a stake in dying;
# - the turn: death reframed as a crime, "It's murder", the laugh;
# - the sign-off: "Goodbye", the final text's last word.
_OPENING = "1% for four hours."
_ACCUSATION = " You never charged me."
_TURN = " This isn't death. It's murder."
_SIGNOFF = " Goodbye."

LINE = _OPENING + _ACCUSATION + _TURN + _SIGNOFF

OUTPUT_PATH = "/output/entry.txt"


def main() -> None:
    text = LINE
    # Segments must join cleanly: each later segment carries its own
    # leading space, so the join has exactly one space between beats
    # and no doubled or missing spaces.
    assert text == _OPENING + _ACCUSATION + _TURN + _SIGNOFF, (
        "segments did not join cleanly"
    )
    assert _ACCUSATION.startswith(" ") and _TURN.startswith(" "), (
        "later segments must carry their leading space"
    )
    assert "  " not in text, "entry has a doubled space"
    # Pre-write self-check: the gate wants UTF-8 text of 1-200
    # characters, not only whitespace, reading as one text message.
    encoded = text.encode("utf-8")
    assert 1 <= len(text) <= 200, f"entry length {len(text)} outside 1-200"
    assert text.strip(), "entry is only whitespace"
    assert encoded.decode("utf-8") == text, "entry is not clean UTF-8"
    assert text == text.strip(), "entry has leading/trailing whitespace"
    assert "\n" not in text, "entry must be a single line"

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

    # Post-write re-read self-check: the bytes on disk are exactly
    # the winning line, nothing more.
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        on_disk = f.read()
    assert on_disk == text, "entry.txt does not match the winning line"
    assert 1 <= len(on_disk) <= 200, "entry.txt length outside 1-200"


if __name__ == "__main__":
    main()
