"""Keep sentinels from shielding the trailing newline Jinja drops.

Jinja renders with ``keep_trailing_newline=False``, so a template ending in a
newline loses exactly one. When a marker's value ends the text, the recorder's
CLOSE sentinel is appended *after* that newline, so the newline is no longer
trailing and Jinja keeps it: the instrumented render would gain one character
that the plain render does not have. Moving the newline out from inside the
sentinel group restores the byte-for-byte match.
"""

from __future__ import annotations

from sldb.core.renderer_engine.span_recorder import CLOSE

SHIELDED = "\n" + CLOSE


def unshield_trailing_newline(text: str) -> str:
    """Move a sentinel-shielded trailing newline outside the sentinel group.

    Exactly one newline is moved, which is exactly how many Jinja drops. Moving
    the whole run would delete newlines the plain render keeps.

    Args:
        text: A template line joined for rendering, sentinels included.

    Returns:
        The text with one final shielded newline moved past the closing
        sentinels, letting Jinja drop it as it would without sentinels.
    """
    if not text.endswith(CLOSE) or SHIELDED not in text:
        return text
    body = text.rstrip(CLOSE)
    if not body.endswith("\n"):
        return text
    return body[:-1] + text[len(body):] + "\n"
