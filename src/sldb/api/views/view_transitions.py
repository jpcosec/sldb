"""The `holding` and `blocked` edges a section's `transitions` add to each row (GD25): what
`edges_holding` and `edges_blocked` answer (GO08/GO09) for the node `from_field` names, read
with the row's projected payload as subject (the payload the index holds, so its
`on_transition` rules evaluate on the index as they are) over the index and rules the whole
view shares."""

from __future__ import annotations

from typing import Any

from sldb.api.edges.edge_effects import effects_of
from sldb.api.views.view_rules import row_findings
from sldb.store.graph.language.predicate_documents import payload_holds


def row_transitions(index: Any, rules: Any, export_id: str, payload: dict[str, Any], spec: dict[str, str]) -> dict[str, list]:
    """`{holding, blocked}` as `edges_holding`/`edges_blocked` dump them; both empty when the
    row has no `from_field` value (nothing to leave from). `rules` is `(shared, on_transition
    rules)`, or None in a store without RuleDoc (then no rule runs and `findings` is absent)."""
    from_id = payload.get(spec["from_field"])
    if not isinstance(from_id, str) or not from_id:
        return {"holding": [], "blocked": []}
    held = holding_edges(index, from_id, payload, spec["relation"])
    if rules is None:
        return {"holding": [e.model_dump() for e in held], "blocked": []}
    findings = row_findings(rules[0], rules[1], export_id)
    dumped = [{**e.model_dump(), "findings": findings} for e in held]
    blocked = any(f["level"] == "error" for f in findings)
    return {"holding": [] if blocked else dumped, "blocked": dumped if blocked else []}


def holding_edges(index: Any, from_id: str, subject: dict[str, Any], relation: str) -> list[Any]:
    """The edges leaving `from_id` whose condition holds on `subject`, each with its `effects`."""
    held = [e for e in index.edges_from(from_id, relation) if payload_holds(e.metadata.get("condition") or "", subject)]
    effects = [effects_of(e.metadata.get("attributes"), subject) for e in held]
    return [e.model_copy(update={"effects": f}) for e, f in zip(held, effects) if f is not None]
