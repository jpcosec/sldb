"""The family `builtin:tag_namespace:*` as data (H6, docs/architecture/tags.md): per local
document and namespace, what `tags check` evaluated, without parsing a finding's text."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.rules.builtin_tag_rules import PREFIX, family_evaluations, findings_of, tag_rules
from sldb.api.rules.rule_graph import rule_graph
from sldb.api.stores.open_store import open_store
from sldb.core.finding import Finding


def tag_evaluations(store: str | Path | None) -> list[dict[str, Any]]:
    """One entry per local document and namespaced tag family it carries, held or not:
    `{document, namespace, rule, holds, clause, tags, missing}`; `missing` is `[]` when the
    namespace is not anchored. Empty without `tag_namespaces`."""
    return tag_report(store)[1]


def tag_report(store: str | Path | None) -> tuple[list[Finding], list[dict[str, Any]]]:
    """The findings of `tag_check` and the evaluations behind them, from one pass."""
    store_path = open_store(store, mode="readonly").store_path
    if not tag_rules(store_path):
        return [], []
    graph = rule_graph(store_path, None)
    evaluations = family_evaluations(graph, None)
    return findings_of(graph, evaluations), [_entry(name, found) for name, found in evaluations]


def _entry(name: str, found: dict[str, Any]) -> dict[str, Any]:
    seen = found["seen"]
    return {"document": found["node"], "namespace": name, "rule": PREFIX + name, "holds": found["holds"] == "true", "clause": found["clause"], "tags": seen["tags"], "missing": seen.get("missing", [])}
