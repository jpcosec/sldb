"""Edges whose condition holds for a subject: the graph read as a state machine."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from sldb.api.edges.edge_reading import edges_from
from sldb.store.models import EdgeRecord
from sldb.store.query_engine.where_subject import payload_matches


def edges_holding(store: str | Path | None, export_id: str, subject: dict[str, Any], relation: str | None = None, include_linked: bool = True, exclude_tags: Iterable[str] = ()) -> list[EdgeRecord]:
    """The edges leaving `export_id` whose condition holds on `subject`.

    Each edge's condition (its own, else its relation type's) is a `--where` predicate read on
    the subject's fields, `{field}` filled from the subject too; an edge without a condition
    always holds. To test a condition on another document (an edge's target, say) with the
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
    return [e for e in edges if payload_matches(e.metadata.get("condition") or "", subject)]
