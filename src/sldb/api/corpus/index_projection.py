"""What a consumer declares about its corpus: which documents it admits and how it reads
the representative text of one. Nothing else about indexing is the consumer's business.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable


def summary_text(payload: dict[str, Any]) -> str:
    """The default representative text: the document's summary."""
    value = payload.get("summary")
    return value.strip() if isinstance(value, str) else ""


def fields_text(*names: str) -> Callable[[dict[str, Any]], str]:
    """The first of those fields with a non-empty string, in order."""

    def pick(payload: dict[str, Any]) -> str:
        for name in names:
            value = payload.get(name)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return ""

    return pick


@dataclass(frozen=True)
class IndexProjection:
    """What a consumer declares about its corpus: which documents it admits and how it
    reads the text of one.

    `models` is the allowed set (None: every model); `exclude_models` drops from it. `text`
    maps a payload to its representative text; a document whose text is empty stays out,
    and `text_id` names the mapping so a change of representation invalidates the index
    the same way a change of embedder does.
    """

    models: frozenset[str] | None = None
    exclude_models: frozenset[str] = frozenset()
    text: Callable[[dict[str, Any]], str] = summary_text
    text_id: str = "summary"
    stores: tuple[str, ...] | None = None

    def admits(self, model: str) -> bool:
        if model in self.exclude_models:
            return False
        if self.models is None:
            return True
        return model in self.models

    @staticmethod
    def of(
        models: Iterable[str] | None = None,
        exclude_models: Iterable[str] = (),
        text: Callable[[dict[str, Any]], str] | None = None,
        text_id: str = "summary",
        stores: Iterable[str] | None = None,
    ) -> "IndexProjection":
        return IndexProjection(
            models=None if models is None else frozenset(models),
            exclude_models=frozenset(exclude_models),
            text=text or summary_text,
            text_id=text_id,
            stores=None if stores is None else tuple(stores),
        )
