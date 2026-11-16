"""Merge two parsed versions of a store file: `store_index.yaml` (its lists by name) and
`.sldb/store.yaml` (the `include` rules by model, without repeating a path; links, models and
predicates by name). Everything else is the current branch's. Hashes are not merged here: they
are derived, and `sldb stores rebuild-index` recomputes them from the shards."""

from __future__ import annotations

from typing import Any

from sldb.api.stores.conflict_sides import union_by

INDEX_LISTS = ("stores", "models", "predicates")


def merge_index_data(ours: dict[str, Any], theirs: dict[str, Any]) -> dict[str, Any]:
    """`ours` with the stores, models and predicates only `theirs` registered."""
    merged = dict(ours)
    for key in INDEX_LISTS:
        merged[key] = union_by(ours.get(key) or [], theirs.get(key) or [], "name")
    return merged


def merge_declaration_data(ours: dict[str, Any], theirs: dict[str, Any]) -> dict[str, Any]:
    """`ours` with what only `theirs` declares: links, models, predicates and include rules."""
    merged = dict(ours)
    for key in ("links", "models"):
        merged[key] = union_by(ours.get(key) or [], theirs.get(key) or [], "name")
    merged["predicates"] = {**(theirs.get("predicates") or {}), **(ours.get("predicates") or {})}
    merged["include"] = merge_includes(ours.get("include") or [], theirs.get("include") or [])
    return {k: v for k, v in merged.items() if v or k in ours}


def merge_includes(ours: list[dict], theirs: list[dict]) -> list[dict]:
    """Each rule of `theirs` added to `ours`: a glob ours already has is skipped, paths join the
    model's path rule of ours (only the ones it does not name yet), anything else is appended."""
    rules = [dict(rule, paths=list(rule["paths"])) if "paths" in rule else dict(rule) for rule in ours]
    for rule in theirs:
        _merge_rule(rules, rule)
    return rules


def _merge_rule(rules: list[dict], rule: dict) -> None:
    if "paths" in rule:
        target = next((r for r in rules if r.get("model") == rule.get("model") and "paths" in r), None)
        if target is not None:
            named = {_path_of(p) for p in target["paths"]}
            target["paths"].extend(p for p in rule["paths"] if _path_of(p) not in named)
            return
    if rule not in rules:
        rules.append(dict(rule))


def _path_of(item: Any) -> str:
    return item.get("path") if isinstance(item, dict) else item
