"""Inline Markdown links (`[text](dest)`) to a moved path, pointed at its new place."""

from __future__ import annotations

import posixpath
import re
from typing import Any
from urllib.parse import quote, unquote

from sldb.api.documents.move_path_remap import Remap

_LINK = re.compile(r"(\]\()(<[^>\n]*>|[^)\s]+)")
_SCHEME = re.compile(r"^[a-zA-Z][a-zA-Z0-9+.-]*:")


def rewrite_links(text: str, file: str, remap: Remap) -> tuple[str, list[dict[str, Any]]]:
    """`text` of the Markdown file `file` (project-relative, its place before the move) with the
    links to the old path repointed, and each change as `{file, line, old, new}`. Fenced code is left alone."""
    changes: list[dict[str, Any]] = []
    dirs = (posixpath.dirname(file), posixpath.dirname(remap.apply(file) or file))
    out = [line if skip else _relink(line, dirs, remap, (file, number, changes)) for number, line, skip in _lines(text)]
    return "".join(out), changes


def _lines(text: str):
    """`(number, line, skip)`: `skip` is true inside a fenced code block, fences included."""
    fenced = False
    for number, line in enumerate(text.splitlines(keepends=True), 1):
        toggles = line.lstrip(" ").startswith(("```", "~~~"))
        yield number, line, fenced or toggles
        fenced = fenced != toggles


def _relink(line: str, dirs: tuple[str, str], remap: Remap, where: tuple[str, int, list[dict[str, Any]]]) -> str:
    return _LINK.sub(lambda m: m.group(1) + _dest(m.group(2), dirs, remap, where), line)


def _dest(raw: str, dirs: tuple[str, str], remap: Remap, where: tuple[str, int, list[dict[str, Any]]]) -> str:
    inner = raw[1:-1] if raw.startswith("<") else raw
    new = _retarget(inner, dirs, remap)
    if new is None or new == inner:
        return raw
    shown = f"<{new}>" if raw.startswith("<") or " " in new else new
    where[2].append({"file": where[0], "line": where[1], "old": inner, "new": new})
    return shown


def _retarget(inner: str, dirs: tuple[str, str], remap: Remap) -> str | None:
    cut = re.search(r"[#?]", inner)
    path, tail = (inner[:cut.start()], inner[cut.start():]) if cut else (inner, "")
    if not path or path.startswith("/") or _SCHEME.match(path):
        return None
    moved = remap.apply(posixpath.normpath(posixpath.join(dirs[0], unquote(path))))
    return None if moved is None else _spell(path, posixpath.relpath(moved, dirs[1] or ".")) + tail


def _spell(original: str, rel: str) -> str:
    """`rel` written the way `original` was: `./` and trailing `/` kept, percent-encoded when it was."""
    if original.endswith("/") and not rel.endswith("/"):
        rel += "/"
    if original.startswith("./") and not rel.startswith("."):
        rel = "./" + rel
    return quote(rel, safe="/") if "%" in original else rel
