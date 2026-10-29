"""The `include` rules of a store that already declares them: kept as authored, then completed.

A glob is the owner's intent and the enumeration of its matches is derived, so `declare` never
rewrites a glob into a path list: it adds only what no rule covers.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.declared_files import declared_files
from sldb.api.stores.declared_includes import tracked_rows
from sldb.api.stores.store_declaration import StoreDeclaration


def merged_includes(store_path: Path, root: Path, current: list[dict]) -> list[dict]:
    """`current` rules verbatim (copied, never rewritten), plus the tracked documents no rule
    names, appended to the model's path list (created at the end when the model has none)."""
    rules = [dict(rule) for rule in current]
    covered = set(declared_files(root, StoreDeclaration(include=rules)))
    for model, path, name in tracked_rows(store_path, root):
        if (model, path, name) not in covered:
            _path_rule(rules, model)["paths"].append(path if Path(path).stem == name else {"path": path, "name": name})
    return rules


def _path_rule(rules: list[dict], model: str) -> dict:
    """The model's own path list (a glob rule is never appended to)."""
    rule = next((r for r in rules if r.get("model") == model and "paths" in r and "glob" not in r), None)
    if rule is None:
        rules.append(rule := {"model": model, "paths": []})
    return rule
