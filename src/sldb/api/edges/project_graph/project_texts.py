"""The texts of project documents, read once, and whether each is history."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from sldb.api.edges.project_graph.frontmatter_mapping import is_record_text


class ProjectTexts:
    """Read each document at most once and answer the record questions the graph asks."""

    def __init__(self, root: Path, closed_document: Callable[[str, str], bool] | None) -> None:
        """Keep the project root and the project's own test for closed (history) documents."""
        self.root = root
        self.closed_document = closed_document
        self._texts: dict[str, str] = {}

    def text(self, relative_path: str) -> str:
        """The text of a repo-relative file."""
        if relative_path not in self._texts:
            self._texts[relative_path] = (self.root / relative_path).read_text(encoding="utf-8")
        return self._texts[relative_path]

    def is_history(self, kind: str, text: str) -> bool | None:
        """True when a document is an archived record or closed by the project's rule; else None."""
        closed = self.closed_document is not None and self.closed_document(kind, text)
        return True if is_record_text(text) or closed else None

    def is_record_path(self, relative_path: str) -> bool | None:
        """True when the file at a path exists and carries `record: true`; else None."""
        is_record = (self.root / relative_path).is_file() and is_record_text(self.text(relative_path))
        return True if is_record else None

    def history_at(self, kind: str, relative_path: str) -> bool | None:
        """`is_history` of the file at a path, None when there is no such file or it is empty."""
        text = self.text(relative_path) if (self.root / relative_path).is_file() else ""
        return self.is_history(kind, text) if text else None
