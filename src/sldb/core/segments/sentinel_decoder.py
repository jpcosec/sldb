"""Turn a sentinel-marked render into clean text plus character spans.

``SLDBRenderer.render`` strips the joined blocks before returning. Decoding has to
happen **before** that strip: a value sitting at the end of the document with
trailing whitespace would otherwise be shifted, because the sentinels themselves
occupy positions the strip does not account for. ``strip_with_offsets`` therefore
applies the same strip to the decoded text and clamps every span to it.
"""

from __future__ import annotations

from sldb.core.renderer_engine.span_recorder import CLOSE, OPEN, SEP

Span = tuple[int, int, int]


def decode_sentinels(raw: str) -> tuple[str, list[Span]]:
    """Remove sentinels from ``raw`` and report where each span landed.

    Args:
        raw: Rendered text containing ``U+E000 id U+E001 text U+E002`` groups.

    Returns:
        The text without sentinels and a list of ``(span_id, start, end)``
        character offsets over that text.
    """
    out: list[str] = []
    spans: list[Span] = []
    stack: list[tuple[int, int]] = []
    index = 0
    while index < len(raw):
        index = _step(raw, index, out, spans, stack)
    return "".join(out), spans


def _step(raw: str, index: int, out: list[str], spans: list[Span], stack: list[tuple[int, int]]) -> int:
    """Consume one character (or one opening sentinel) and return the next index.

    Args:
        raw: The full sentinel-marked text.
        index: Position to read.
        out: Accumulator of decoded characters, mutated in place.
        spans: Accumulator of closed spans, mutated in place.
        stack: Open ``(span_id, start)`` pairs, mutated in place.

    Returns:
        The index to read next.
    """
    char = raw[index]
    if char == OPEN:
        return _open_span(raw, index, len(out), stack)
    if char == CLOSE:
        span_id, start = stack.pop()
        spans.append((span_id, start, len(out)))
        return index + 1
    out.append(char)
    return index + 1


def _open_span(raw: str, index: int, position: int, stack: list[tuple[int, int]]) -> int:
    """Push the span opening at ``index`` and return the index after its header.

    Args:
        raw: The full sentinel-marked text.
        index: Position of the ``OPEN`` sentinel.
        position: Offset in the decoded text where the span's value starts.
        stack: Open ``(span_id, start)`` pairs, mutated in place.

    Returns:
        The index just past the ``SEP`` that closes the span header.
    """
    sep = raw.index(SEP, index)
    stack.append((int(raw[index + 1 : sep]), position))
    return sep + 1


def strip_with_offsets(text: str, spans: list[Span]) -> tuple[str, list[Span]]:
    """Strip ``text`` the way the renderer does, clamping spans to the result.

    Args:
        text: Decoded text, not yet stripped.
        spans: Spans addressed against ``text``.

    Returns:
        The stripped text and the spans rebased on it.
    """
    lead = len(text) - len(text.lstrip())
    stripped = text.strip()
    return stripped, [(sid, _clamp(start - lead, stripped), _clamp(end - lead, stripped)) for sid, start, end in spans]


def _clamp(position: int, stripped: str) -> int:
    """Keep an offset inside the stripped text.

    Args:
        position: Candidate offset, already rebased by the leading whitespace.
        stripped: The stripped text the offset addresses.

    Returns:
        ``position`` bounded to ``[0, len(stripped)]``.
    """
    return max(0, min(len(stripped), position))
