"""Which rules a store declares, which documents a rule applies to, and how a reference names one.

A rule is a local RuleDoc (or a document of a submodel of it), read from the edge index's
projection. It applies to a document when the document is in the family of its `subject` and
its `where` (if any) holds `true` on it; `false` or `incomplete` means it does not apply.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.documents.document_payload import runtime_document
from sldb.api.rules.rule_graph import RuleGraph, reading, rule_graph
from sldb.api.rules.rule_reach import qualified
from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.store.layout import project_root

RULE_MODEL = "RuleDoc"


def rules_of(graph: RuleGraph) -> list[dict[str, Any]]:
    """Every local rule: its payload plus `id` (`RuleDoc:name`), `name` and `path`."""
    return [_rule(graph, node) for node in sorted(graph.domain(f"model <= {RULE_MODEL}"))]


def applies(graph: RuleGraph, rule: dict[str, Any], node: str) -> tuple[str, str] | None:
    """None when `rule` applies to `node`; else `(reason, detail)`: `subject` and the rule's
    subject, or `where` and the clause of the where that decided it."""
    if graph.holds(rule["subject"], node)["holds"] != "true":
        return "subject", rule["subject"]
    found = graph.holds(rule["where"], node) if rule.get("where") else None
    return ("where", found["clause"]) if found is not None and found["holds"] != "true" else None


def resolve_subject(graph: RuleGraph, ref: str, pythonpath: str | None = None) -> str:
    """The export id of the document `ref` names: an export id (`Model:name`, `store:Model:name`)
    of the index, else a name, `Model/name` or path, local or behind `alias:`. An unknown
    reference is sldb's `SLDBDocumentTargetError`."""
    if not ref.startswith("sldb://") and graph.semantics(ref):
        return ref
    doc = runtime_document(graph.store_path, pythonpath, _relative(graph.store_path, ref))
    prefix = "" if doc.store_name in ("local", "", None) else f"{doc.store_name}:"
    return f"{prefix}{doc.model_name}:{doc.name}"


def subject_in(graph: RuleGraph, ref: str, pythonpath: str | None = None) -> tuple[RuleGraph, str]:
    """`(graph, export id)` of the document `ref` names, as `resolve_subject`; the graph is the
    composed one when the document is not local (`rule_graph.reading`), and is composed before
    resolving an export id `alias:Model:name`, which only the composed index names."""
    if not graph.linked and qualified(ref):
        graph = rule_graph(graph.store_path, True)
    node = resolve_subject(graph, ref, pythonpath)
    return reading(graph, node), node


def resolve_rule(graph: RuleGraph, ref: str) -> dict[str, Any]:
    """The local rule `ref` names: `RuleDoc:name`, `name` or its path; else the unknown
    document error (`SLDBDocumentTargetError`)."""
    relative = _relative(graph.store_path, ref)
    for rule in rules_of(graph):
        if ref in (rule["id"], rule["name"]) or relative == rule["path"]:
            return rule
    raise SLDBDocumentTargetError(f"Unknown document target: {ref}")


def _rule(graph: RuleGraph, node: str) -> dict[str, Any]:
    known = graph.semantics(node)
    return {**graph.payload(node), "id": node, "name": known.get("name") or node.rsplit(":", 1)[-1], "path": known.get("path", "")}


def _relative(store_path: Path, ref: str) -> str:
    path = Path(ref)
    if not path.is_absolute():
        return ref
    try:
        return path.resolve().relative_to(project_root(store_path).resolve()).as_posix()
    except ValueError:
        return ref
