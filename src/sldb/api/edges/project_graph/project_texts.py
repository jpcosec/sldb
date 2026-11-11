"""The texts of project documents, read once, and whether each is history (a record, or closed)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.edges.project_graph.frontmatter_mapping import frontmatter_mapping, is_record_text
from sldb.api.edges.project_graph.project_graph_config import ProjectGraphConfig
from sldb.store.source_guard import aggregate_text


class ProjectTexts:
    """Read each document at most once and answer the record questions the graph asks.

    A surface's `closed` predicate is evaluated with the rules language on the document's
    payload: the edge index's projection when the store tracks it (nothing is re-extracted),
    its frontmatter otherwise. A surface without `closed` is never closed by it.
    """

    def __init__(self, root: Path, config: ProjectGraphConfig, payloads: dict[str, dict[str, Any]] | None = None) -> None:
        """Keep the root, each kind's `closed` predicate, the deprecated callable and the indexed payloads by path."""
        self.root = root
        self.closed_by_kind = {surface.kind: surface.closed for surface in config.surfaces if surface.closed}
        self.closed_document = config.closed_document
        self.payloads = payloads or {}
        self._texts: dict[str, str] = {}
        self._path_of_text: dict[str, str] = {}

    def text(self, relative_path: str) -> str:
        """The text of a repo-relative file; empty (warned once) when the read guard refuses it."""
        if relative_path not in self._texts:
            self._texts[relative_path] = aggregate_text(self.root, self.root / relative_path, relative_path) or ""
            self._path_of_text.setdefault(self._texts[relative_path], relative_path)
        return self._texts[relative_path]

    def is_history(self, kind: str, text: str) -> bool | None:
        """True when a document is an archived record or closed by its surface's rule; else None."""
        return True if is_record_text(text) or self.is_closed(kind, text) else None

    def is_closed(self, kind: str, text: str) -> bool:
        """Whether the surface's `closed` predicate holds on the document's payload.

        A kind whose surface declares no `closed` falls back to the deprecated callable, if any.
        """
        predicate = self.closed_by_kind.get(kind)
        if predicate is None:
            return self.closed_document is not None and self.closed_document(kind, text)
        from sldb.api.where import where_matches

        return where_matches(predicate, self.payload_of(text))

    def payload_of(self, text: str) -> dict[str, Any]:
        """The indexed payload of the document whose text this is, else its frontmatter mapping."""
        path = self._path_of_text.get(text)
        indexed = self.payloads.get(path) if path is not None else None
        return indexed if indexed is not None else (frontmatter_mapping(text) or {})

    def is_record_path(self, relative_path: str) -> bool | None:
        """True when the file at a path exists and carries `record: true`; else None."""
        is_record = (self.root / relative_path).is_file() and is_record_text(self.text(relative_path))
        return True if is_record else None

    def history_at(self, kind: str, relative_path: str) -> bool | None:
        """`is_history` of the file at a path, None when there is no such file or it is empty."""
        text = self.text(relative_path) if (self.root / relative_path).is_file() else ""
        return self.is_history(kind, text) if text else None


def indexed_payloads(index: Any) -> dict[str, dict[str, Any]]:
    """`{repo-relative path: payload}` of every document node of an edge index."""
    found: dict[str, dict[str, Any]] = {}
    for node in index.nodes.values():
        path = node.semantics.get("path")
        if node.id.startswith("sldb://document/") and isinstance(path, str):
            found[path] = node.payload
    return found
