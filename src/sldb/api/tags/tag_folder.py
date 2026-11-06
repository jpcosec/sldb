"""Where a tag places a document: `a.b` -> `a/b`, one segment per part (`folder_axis`)."""

from __future__ import annotations

from sldb.store.semantic_tags import split_namespace


def tag_folder(tag: str) -> str:
    """The relative POSIX path of a tag's value (`area:a.b` or `a.b` -> `a/b`).

    Pure: it never reads a store. The namespace, when present, is discarded. A blank value,
    an empty segment (`a..b`, `.a`, `a.`) or a slash inside a segment is a `ValueError` naming
    the value.
    """
    value = split_namespace(tag)[1]
    segments = value.split(".")
    if not value or any(not segment or "/" in segment for segment in segments):
        raise ValueError(f"tag value {value!r} does not name a folder: one non-empty segment per dot, without slashes")
    return "/".join(segments)
