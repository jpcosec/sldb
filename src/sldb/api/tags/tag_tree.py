"""`sldb.api.tag_tree(store, namespace)`: one namespace's tags as a tree (docs/architecture/tags.md).

    {"namespace": "area",
     "roots": [{"tag": "area:a", "document": "Anchor:a", "children": [{"tag": "area:a.b", ...}]}],
     "orphans": [{"tag": "area:c", "used_by": ["Note:n1"]}],
     "unplaced": [{"tag": "area:a.x", "document": "Anchor:ax"}]}

With `anchored_by`, the tree is the anchors' (an intermediate prefix without its anchor is a
node with `document: null`), `orphans` are the tags local documents use that no anchor
declares and `unplaced` the anchors no document uses, directly or (hierarchical) through a tag
under them; without it, the tree is the used tags' and both lists are empty. A
non-hierarchical namespace has roots only. Alphabetical by tag.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.rules.builtin_tag_rules import anchors_of, payload_of, tag_rules
from sldb.api.rules.rule_graph import RuleGraph, rule_graph
from sldb.api.stores.tag_namespace import TagNamespace
from sldb.core.exceptions import SLDBStoreError
from sldb.store.semantic_tags import namespaced_tags


def tag_tree(store: str | Path | None, namespace: str) -> dict[str, Any]:
    """The tree of `namespace`; an undeclared namespace is `SLDBStoreError`."""
    graph = rule_graph(store)
    declared = tag_rules(graph.store_path).get(namespace)
    if declared is None:
        raise SLDBStoreError(f"tag namespace '{namespace}' is not declared in store.yaml (declared: {sorted(tag_rules(graph.store_path))})")
    used, anchors = used_tags(graph, namespace), anchors_of(graph, declared) if declared.anchored_by else {}
    roots = _nested(declared, set(anchors) if declared.anchored_by else set(used), anchors)
    orphans = [{"tag": tag, "used_by": nodes} for tag, nodes in sorted(used.items()) if tag not in anchors] if declared.anchored_by else []
    covered = {prefix for tag in used for prefix in declared.required(tag)}
    unplaced = [{"tag": tag, "document": node} for tag, node in sorted(anchors.items()) if tag not in covered]
    return {"namespace": namespace, "roots": roots, "orphans": orphans, "unplaced": unplaced}


def used_tags(graph: RuleGraph, namespace: str) -> dict[str, list[str]]:
    """Tag -> the local documents carrying it, for the tags of `namespace`."""
    found: dict[str, list[str]] = {}
    for node in sorted(graph.local):
        for name, tag in namespaced_tags(payload_of(graph, node)):
            if name == namespace:
                found.setdefault(tag, []).append(node)
    return found


def _nested(declared: TagNamespace, tags: set[str], anchors: dict[str, str]) -> list[dict[str, Any]]:
    """The tags nested by prefix (every prefix a node), or flat when not hierarchical."""
    nodes = {tag for value in tags for tag in declared.required(value)}
    children: dict[str | None, list[str]] = {}
    for tag in sorted(nodes):
        children.setdefault(_parent(declared, tag), []).append(tag)
    return [_node(tag, anchors, children) for tag in children.get(None, [])]


def _parent(declared: TagNamespace, tag: str) -> str | None:
    required = declared.required(tag)
    return required[-2] if len(required) > 1 else None


def _node(tag: str, anchors: dict[str, str], children: dict[str | None, list[str]]) -> dict[str, Any]:
    return {"tag": tag, "document": anchors.get(tag), "children": [_node(child, anchors, children) for child in children.get(tag, [])]}
