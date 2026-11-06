"""Edges whose condition holds for a subject: the graph read as a state machine."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from sldb.api.edges.edge_effects import effects_of
from sldb.api.edges.edge_reading import edges_from
from sldb.store.models import EdgeRecord
from sldb.store.graph.language.predicate_documents import payload_holds


def edges_holding(store: str | Path | None, export_id: str, subject: dict[str, Any], relation: str | None = None, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> list[EdgeRecord]:
    """The edges leaving `export_id` whose condition holds on `subject`.

    Each edge's condition (its own, else its relation type's) is a predicate of the language
    (rules-language.md, the one `--where` reads) evaluated on the subject's fields, `{field}`
    filled from the subject too; an edge without a condition always holds. Each edge returned
    carries `effects` = `{sets, terminal}` from its attributes, `{field}` in `sets` filled from the
    subject (`effects_of`); an edge whose `{field}` cannot be filled does not hold. To test a condition on another document (an edge's target, say) with the
    subject in braces, use `where_matches(condition, that_payload, subject)`.

    Args:
        store: The store (path, alias, or None to discover it).
        export_id: The node the edges leave (`Model:name`), e.g. the state a task is in.
        subject: The payload the conditions read; need not be a tracked document's.
        relation, include_linked, exclude_tags: As in `edges_from`.

    Raises:
        WherePredicateError: An edge's condition does not parse.
    """
    edges = edges_from(store, export_id, relation, include_linked, exclude_tags)
    held = [e for e in edges if payload_holds(e.metadata.get("condition") or "", subject)]
    effects = [effects_of(e.metadata.get("attributes"), subject) for e in held]
    return [e.model_copy(update={"effects": f}) for e, f in zip(held, effects) if f is not None]
