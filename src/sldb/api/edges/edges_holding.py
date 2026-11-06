"""Edges whose condition holds for a subject: the graph read as a state machine."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

from sldb.api.edges.edge_effects import effects_of
from sldb.api.edges.edge_reading import edges_from
from sldb.store.models import EdgeRecord
from sldb.store.graph.language.predicate_documents import payload_holds


def edges_holding(store: str | Path | None, export_id: str, subject: dict[str, Any], relation: str | None = None, include_linked: bool = True, exclude_tags: Iterable[str] = (), document: str | None = None) -> list[EdgeRecord]:
    """The edges leaving `export_id` whose condition holds on `subject`.

    Each edge's condition (its own, else its relation type's) is a predicate of the language
    (rules-language.md, the one `--where` reads) evaluated on the subject's fields, `{field}`
    filled from the subject too; an edge without a condition always holds. Each edge returned
    carries `effects` = `{sets, terminal}` from its attributes, `{field}` in `sets` filled from the
    subject (`effects_of`); an edge whose `{field}` cannot be filled does not hold. To test a condition on another document (an edge's target, say) with the
    subject in braces, use `where_matches(condition, that_payload, subject)`.

    With `document` (the subject's reference: `Model:name`, `store:Model:name` or a path), the
    `on_transition` rules that apply to it are evaluated on `subject` (GO08, rules.md §9): an
    `error` finding blocks every edge (none holds; `edges_blocked` returns them), and each edge
    returned carries `findings`, the alerts. Without it no rule runs and `findings` stays unset.

    Args:
        store: The store (path, alias, or None to discover it).
        export_id: The node the edges leave (`Model:name`), e.g. the state a task is in.
        subject: The payload the conditions read; need not be a tracked document's.
        relation, include_linked, exclude_tags: As in `edges_from`.
        document: The document `subject` is, for its `on_transition` rules.

    Raises:
        WherePredicateError: An edge's condition does not parse.
    """
    held, findings = transition(store, export_id, subject, relation, include_linked, exclude_tags, document)
    if findings is None:
        return held
    blocked = any(f.level == "error" for f in findings)
    return [] if blocked else [e.model_copy(update={"findings": findings}) for e in held]


def transition(store: str | Path | None, export_id: str, subject: dict[str, Any], relation: str | None, include_linked: bool, exclude_tags: Iterable[str], document: str | None) -> tuple[list[EdgeRecord], list[Any] | None]:
    """The edges whose condition holds (with `effects`), and the subject's `on_transition`
    findings (None without `document`)."""
    from sldb.api.rules.rules_on_transition import transition_findings

    edges = edges_from(store, export_id, relation, include_linked, exclude_tags)
    held = [e for e in edges if payload_holds(e.metadata.get("condition") or "", subject)]
    effects = [effects_of(e.metadata.get("attributes"), subject) for e in held]
    found = None if document is None else transition_findings(store, document, subject)
    return [e.model_copy(update={"effects": f}) for e, f in zip(held, effects) if f is not None], found
