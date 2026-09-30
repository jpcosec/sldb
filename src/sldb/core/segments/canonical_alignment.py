"""Map canonical-text offsets onto the raw markdown they were extracted from.

Extraction is lossy in surface but not in data: the payload extracted from raw
markdown re-renders to a *canonical* text that may differ in whitespace, YAML
quoting or line folding. Field spans are exact over the canonical text, so they
are transported to the raw text through a character-level diff.

A span whose both borders land inside ``equal`` runs is ``exact``; otherwise the
border is clamped to the run's edge and the span is ``approximate``. Nothing is
guessed: ``approximate`` says "this is where it went, roughly".
"""

from __future__ import annotations

from difflib import SequenceMatcher

Opcode = tuple[str, int, int, int, int]


def align(canonical: str, raw: str) -> list[Opcode]:
    """The character-level opcodes taking ``canonical`` to ``raw``.

    Args:
        canonical: The re-rendered text the spans address.
        raw: The markdown the payload was extracted from.

    Returns:
        ``SequenceMatcher`` opcodes, computed without autojunk so long texts
        are not silently treated as junk-heavy and mis-aligned.
    """
    return SequenceMatcher(None, canonical, raw, autojunk=False).get_opcodes()


def map_offset(opcodes: list[Opcode], position: int, is_end: bool = False) -> tuple[int, bool]:
    """Carry one canonical offset over to the raw text.

    Args:
        opcodes: The alignment from :func:`align`.
        position: The canonical offset to map.
        is_end: Whether the offset is an exclusive end, which makes it belong to
            the run ending at it rather than the one starting there.

    Returns:
        The raw offset and whether it landed inside an ``equal`` run.
    """
    for tag, i1, i2, j1, j2 in opcodes:
        if _covers(i1, i2, position, is_end):
            return (j1 + (position - i1), True) if tag == "equal" else (j2 if is_end else j1, False)
    return (opcodes[-1][4] if opcodes else 0), False


def _covers(i1: int, i2: int, position: int, is_end: bool) -> bool:
    """Whether an opcode's canonical range contains ``position``.

    Args:
        i1: Inclusive start of the opcode's canonical range.
        i2: Exclusive end of the opcode's canonical range.
        position: The canonical offset being placed.
        is_end: Whether the offset is an exclusive end.

    Returns:
        True when the offset belongs to this run.
    """
    return i1 < position <= i2 if is_end else i1 <= position < i2
