"""`edges show` with something that names no node: said, with the documents it may have meant.

A document's name (`pill-008-x`) is not a node id; the index answered `[]`, the same as for a
real node with no edges, so a caller could not tell a typo from an isolated document.
"""

from __future__ import annotations

from typing import Any

_DOC = "sldb://document/"


def unknown_node_message(args: Any) -> str | None:
    """None when `args.node` is a node of the index; else the error, naming candidates."""
    from sldb.api import load_edge_index

    index = load_edge_index(args.store, not args.local, args.exclude_tag)
    if index.node(args.node) is not None:
        return None
    named = sorted(n[len(_DOC):] for n in index.nodes if n.startswith(_DOC) and n.split("#", 1)[0].endswith(f":{args.node}"))
    hint = f" Did you mean {', '.join(named)}?" if named else " A document is named by its export id (`Model:name`), any other node by its id (`sldb://<kind>/...`)."
    return f"No node '{args.node}' in the edge index.{hint}"
