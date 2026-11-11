"""Which ViewDoc node a name means, and its file read from the store that tracks it (H9).

A ViewDoc may live in the calling store or in a store it links to (DA4: deskops' views ship
only in its package store). The composed index names a linked one `<link>:ViewDoc:<name>`
and stamps every node with `facets.source.store_path`, the `.sldb` that contributed it: the
file is read from that store's root, through the read guard (`sldb.store.source_read`)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.models.notation.view_doc import ViewDoc
from sldb.runtime.validation import extract_model_data
from sldb.store.layout import project_root
from sldb.store.source_read import read_source_text, unreadable_reason

VIEW_MODEL = "ViewDoc"


def view_node(index: Any, name: str) -> Any:
    """The ViewDoc node `name` means: the local one first, else the only linked one with that
    name; `<link>:<name>` names a linked one directly. Several linked = ambiguous, an error."""
    local = index.node(f"{VIEW_MODEL}:{name}")
    if local is not None and local.node_type == VIEW_MODEL:
        return local
    found = [n for n in index.nodes_of_type(VIEW_MODEL) if n.semantics.get("store") and name in (bare_name(n), qualified_name(n))]
    if len(found) > 1:
        stores = ", ".join(sorted(n.semantics["store"] for n in found))
        raise SLDBDocumentTargetError(f"Ambiguous view: {name} (linked in {stores})")
    if not found:
        raise SLDBDocumentTargetError(f"Unknown view: {name}")
    return found[0]


def bare_name(node: Any) -> str:
    """The view's name, without the link it comes through."""
    return node.semantics["export_id"].split(":", 1)[1]


def qualified_name(node: Any) -> str:
    """`<link>:<name>` for a linked view, `<name>` for a local one."""
    store = node.semantics.get("store")
    return f"{store}:{bare_name(node)}" if store else bare_name(node)


def view_store(node: Any) -> Path:
    """The `.sldb` of the store that tracks the node (the linked one for a linked view)."""
    return Path(node.facets["source"]["store_path"])


def read_view_node(node: Any) -> ViewDoc:
    """The ViewDoc extracted from its file, under the root of the store that tracks it; a path
    that leaves that root or is a symlink is not read (`SLDBDocumentTargetError` naming why)."""
    root = project_root(view_store(node))
    path = root / node.semantics["path"]
    reason = unreadable_reason(root, path)
    if reason is not None:
        raise SLDBDocumentTargetError(f"view {qualified_name(node)!r}: {node.semantics['path']} not read ({reason})")
    text = read_source_text(path)
    return ViewDoc.model_validate(extract_model_data(ViewDoc, text))
