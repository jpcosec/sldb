"""What a consumer declares about indexing FIELDS rather than whole documents.

A document's representative text answers "what is this document about"; one field answers
something narrower ("what is this task's scope"), and a query aimed at that question ranks
better against the field than against the document that contains it.

The unit of indexing is the field, so the unit of invalidation is too: the id carries the
field (`Model:doc#field`) and the hash is that field's own, from `DocumentEntry.field_hashes`.
Editing one field of a forty-field document re-embeds one field.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable

# Fields that are identity, bookkeeping or vocabulary rather than prose. Embedding these
# indexes the shape of the store instead of what it says: an id ranks against every query
# that happens to share its slug, and a tag list is already retrievable by tag.
DEFAULT_EXCLUDED_FIELDS: frozenset[str] = frozenset(
    {"id", "name", "slug", "path", "tags", "semantic_tags", "hash", "source_hash", "content_hash"}
)


def field_id(model: str, doc: str, field_path: str, store: str | None = None) -> str:
    """`docs/<Model>/<doc>/<field_path>` — the address `sldb fields` already takes.

    One address space for fields, so an id from a ranked hit can be handed straight to
    `fields update` without translation. A linked store prefixes its name (`<store>/docs/...`),
    the way export ids do, because two stores of a federated world may hold the same
    document name.

    `field_path` is the field's path in payload space (`tags/0`, `steps/2/title`), so the id
    addresses a nested value as precisely as a top-level one.
    """
    address = f"docs/{model}/{doc}/{field_path}"
    return f"{store}/{address}" if store else address


def split_field_id(value: str) -> tuple[str | None, str, str, str] | None:
    """A field id back into (store, model, doc, field_path), or None if it is not one."""
    store, _, rest = value.rpartition("/docs/")
    body = rest if store else value.removeprefix("docs/")
    if not value.startswith("docs/") and not store:
        return None
    parts = body.split("/", 2)
    return (store or None, parts[0], parts[1], parts[2]) if len(parts) == 3 else None


def default_field_text(value: Any) -> str:
    """The indexable text of a field value, or empty when there is nothing to rank.

    Lists of strings are joined: a list field is one semantic unit, and indexing its items
    separately would need ids the store cannot address.
    """
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (list, tuple)):
        return "\n".join(item.strip() for item in value if isinstance(item, str) and item.strip())
    return ""


@dataclass(frozen=True)
class FieldProjection:
    """Which fields of which models a consumer indexes, and how it reads one.

    `include` is the allowed set (None: every field the payload has); `exclude` drops from
    it and defaults to identity and bookkeeping fields. `min_chars` keeps one-word fields
    out, where similarity is noise.

    `text_id` names the mapping for the same reason `IndexProjection.text_id` does: a change
    of representation has to invalidate the index the way a change of embedder does. It is
    part of the derived file's name, so two projections never share one file.
    """

    include: frozenset[str] | None = None
    exclude: frozenset[str] = DEFAULT_EXCLUDED_FIELDS
    text: Callable[[Any], str] = default_field_text
    text_id: str = "field"
    min_chars: int = 12

    def admits(self, field: str) -> bool:
        if field in self.exclude:
            return False
        return self.include is None or field in self.include

    def text_of(self, value: Any) -> str:
        """The field's indexable text, or empty when it is excluded by length."""
        text = self.text(value)
        return text if len(text) >= self.min_chars else ""

    @staticmethod
    def of(
        include: Iterable[str] | None = None,
        exclude: Iterable[str] | None = None,
        text: Callable[[Any], str] | None = None,
        text_id: str = "field",
        min_chars: int = 12,
    ) -> "FieldProjection":
        return FieldProjection(
            include=None if include is None else frozenset(include),
            exclude=DEFAULT_EXCLUDED_FIELDS if exclude is None else frozenset(exclude),
            text=text or default_field_text,
            text_id=text_id,
            min_chars=min_chars,
        )
