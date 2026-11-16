"""The frontmatter side of `referrers` (GD22): a mention on a frontmatter line of a document that is
already a `schema` referrer repeats that field, so `find_hits` leaves it out
(docs/architecture/references.md).
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.edges.referrer import Referrer
from sldb.api.stores.indexed_documents import indexed_documents


def document_paths(store_path: Path) -> dict[str, str]:
    """The tracked path (relative to the project) of every tracked document, by export id `Model:name`."""
    return {f"{d['model']}:{d['name']}": d["path"] for d in indexed_documents(store_path)}


def frontmatter_lines(file: Path) -> range:
    """The lines (from 1) of the frontmatter: the first line `---` through the next `---`, both included; empty when there is none."""
    try:
        lines = file.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeDecodeError):
        return range(0)
    if not lines or lines[0].strip() != "---":
        return range(0)
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    return range(1, end + 2) if end is not None else range(0)


def _in_frontmatter(referrer: Referrer, frontmatters: dict[str, range]) -> bool:
    """Whether `referrer` is a mention located on a frontmatter line of its source."""
    lines = frontmatters.get(referrer.source)
    if not lines or referrer.location is None:
        return False
    line = referrer.location.rsplit(":", 1)[-1]
    return line.isdigit() and int(line) in lines
