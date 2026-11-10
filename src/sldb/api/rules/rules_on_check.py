"""`on_check` (GO08, rules.md §9): every `on_check` rule of the store, recomputed only where
something changed, and the document anchors (GO07) beside them; `stores check` reports both.

`recompute` is the one evaluation of a rule on a document that does not come from the cache
(p8): the rest are read from `rule_cache`, unless the document is dirty (`dirty_set`), has no
entry, or its stamp moved. The set is emptied once every rule ran, under the store lock.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.anchors.check_doc_anchors import check_doc_anchors
from sldb.api.rules.builtin_tag_rules import store_findings
from sldb.api.rules.dirty_set import read_dirty, stamps_of, wide, write_dirty
from sldb.api.rules.rule_cache import prune, read_results, rule_hash, write_results
from sldb.api.rules.rule_graph import RuleGraph, rule_graph
from sldb.api.rules.rule_subjects import applies, rules_of
from sldb.api.rules.rules_check import rule_finding
from sldb.api.rules.rules_on_transition import has_rules
from sldb.api.stores.open_store import open_store
from sldb.core.finding import Finding
from sldb.store.io import store_lock


def on_check_findings(store: str | Path | None, pythonpath: str | None = None) -> list[Finding]:
    """The findings `stores check` adds: the `on_check` rules', the built-in tag namespace
    family's (GD27, not cached), then `check_doc_anchors`'."""
    store_path = open_store(store, mode="readonly").store_path
    rules = rules_on_check(store_path) if has_rules(store_path) else []
    return rules + store_findings(store_path) + check_doc_anchors(store_path, pythonpath)


def rules_on_check(store: str | Path | None) -> list[Finding]:
    """The findings of every `on_check` rule over its family, by rule export id then document."""
    graph = rule_graph(store, None)
    rules = [rule for rule in rules_of(graph) if rule.get("moment") == "on_check"]
    with store_lock(graph.store_path, wait=True):
        dirty = read_dirty(graph.store_path)
        found = [finding for rule in rules for finding in _rule_findings(graph, rule, dirty)]
        write_dirty(graph.store_path, set())
        prune(graph.store_path, {rule_hash(graph.store_path, rule) for rule in rules})
    return found


def recompute(graph: RuleGraph, rule: dict[str, Any], node: str) -> dict[str, Any] | None:
    """One recalculation: the finding of `rule` on `node` as a dict, None when it holds or does not apply."""
    if applies(graph, rule, node) is not None:
        return None
    found = rule_finding(graph, rule, node)
    return found.as_dict() if found is not None else None


def _rule_findings(graph: RuleGraph, rule: dict[str, Any], dirty: set[str] | None) -> list[Finding]:
    key = rule_hash(graph.store_path, rule)
    results, stamps = read_results(graph.store_path, key)
    now = stamps_of(graph, rule, sorted(graph.domain(rule["subject"])))
    stale = dirty is None or (bool(dirty) and wide(rule))
    fresh = {n: results[n] if _kept(n, results, stamps, now, stale or n in (dirty or set())) else recompute(graph, rule, n) for n in now}
    write_results(graph.store_path, key, fresh, now)
    return [Finding(**value) for _, value in sorted(fresh.items()) if value]


def _kept(node: str, results: dict, stamps: dict, now: dict, dirty: bool) -> bool:
    return not dirty and node in results and stamps.get(node) == now[node]
