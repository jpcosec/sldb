"""`sldb tags namespaces` and `sldb tags check`: what the store declares and what fails it."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.rules.builtin_tag_findings import store_findings
from sldb.api.rules.builtin_tag_rules import tag_rules
from sldb.api.stores.open_store import open_store
from sldb.core.finding import Finding


def tag_namespaces(store: str | Path | None) -> list[dict[str, Any]]:
    """The declared namespaces as data (`{name, hierarchical, folder_axis, anchored_by}`),
    in declaration order; empty without `tag_namespaces`."""
    store_path = open_store(store, mode="readonly").store_path
    return [namespace.model_dump() for namespace in tag_rules(store_path).values()]


def tag_check(store: str | Path | None) -> list[Finding]:
    """The findings of the family `builtin:tag_namespace:*` over every local document: the
    same evaluation as `rules check`, filtered to that family (docs/architecture/tags.md)."""
    return store_findings(store)
