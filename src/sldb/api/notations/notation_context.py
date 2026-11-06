"""The notation a view is drawn with: its payload, palette, glyphs and links."""

from __future__ import annotations

from typing import Any

from sldb.api.notations.view_error import ViewError


def _notation(docs: dict[str, dict[str, Any]], notation_ref: str) -> tuple[str, dict[str, Any]]:
    """The normalized `NotationDoc:` ref and its payload, or ViewError."""
    ref = notation_ref if notation_ref.startswith("NotationDoc:") else f"NotationDoc:{notation_ref}"
    notation = docs.get(ref)
    if notation is None:
        raise ViewError(f"{ref} is not in the store")
    return ref, notation["payload"]


def _palette(docs: dict[str, dict[str, Any]], np_: dict[str, Any]) -> dict | None:
    """The payload of the notation's palette, if it is in the store."""
    palette_doc = docs.get(np_.get("palette") or "")
    return palette_doc["payload"] if palette_doc else None


def _members(docs: dict[str, dict[str, Any]], np_: dict[str, Any], key: str) -> list[dict]:
    """`{ref, payload}` of the notation's `glyphs` or `links` that are in the store."""
    return [{"ref": r, "payload": docs[r]["payload"]} for r in np_.get(key) or [] if r in docs]


def notation_context(docs: dict[str, dict[str, Any]], notation_ref: str) -> tuple[str, dict, dict | None, list, list]:
    """`(ref, payload, palette, glyphs, links)` of a notation; ViewError if it has no glyph in the store."""
    ref, np_ = _notation(docs, notation_ref)
    glyphs = _members(docs, np_, "glyphs")
    if not glyphs:
        raise ViewError(f"{ref} lists no glyph that is in the store")
    return ref, np_, _palette(docs, np_), glyphs, _members(docs, np_, "links")
