"""Graph sources of the component spec: a node-link JSON file and a store's edge index.

Migrated from `spec2viz.graph_import`. `load_node_link_graph` reads the raw JSON on purpose:
`snapshot_load` keeps `schema.ast`/`schema.semantics` but builds the edges only from each
node's `schema.edges`, so a node-link file whose edges live only in `links` loses them.
`index_graph` turns what `sldb.api.load_edge_index` returns into the same `(nodes, edges)`.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sldb.api.notations.component_spec_constants import _AST_KINDS, GraphAttrs, GraphEdges, GraphNodes


def _node_identity(node: dict) -> tuple[str | None, str | None]:
    """Extrae (id, tipo) de un nodo node-link; acepta `id`/`type` o `schema.identity`."""
    identity = (node.get("schema") or {}).get("identity") or {}
    node_id = node.get("id") or identity.get("node_id")
    node_type = node.get("type") or identity.get("node_type")
    return node_id, node_type


def _node_attrs(node_id: str, node_type: str, node: dict) -> dict[str, str] | None:
    """Lo que un nodo del grafo de fuente Python de sldb declara sobre si mismo.

    `label` sale del nombre en el codigo (`ast.name`, o `ast.module` para un modulo), `kind`
    de `semantics.kind` cuando esta declarado y si no de la clase AST (module, class,
    function...), y `module` es el modulo Python al que pertenece, para filtrar por alcance.
    None para nodos sin `schema.ast` ni `schema.semantics` (los de un store index).
    """
    schema = node.get("schema") or {}
    ast = schema.get("ast") or {}
    semantics = schema.get("semantics") or {}
    if not ast and not semantics and not node_type.startswith("python_"):
        return None
    tail = node_id[len("python:"):] if node_id.startswith("python:") else node_id
    module = str(ast.get("module") or (tail.split(":", 1)[0] if node_type != "python_external" else ""))
    label, fallback = _label_and_fallback(node_type, tail, ast)
    kind = str(semantics.get("kind") or fallback)
    return {"label": label, "kind": kind, "module": module}


def _label_and_fallback(node_type: str, tail: str, ast: dict) -> tuple[str, str]:
    """Etiqueta del nodo y su `kind` cuando la fuente no declara `semantics.kind`."""
    if node_type == "python_module":
        return str(ast.get("module") or tail), "module"
    if node_type == "python_external":
        return (tail[len("external:"):] if tail.startswith("external:") else tail), "external"
    node_kind_ast = str(ast.get("node_kind") or "")
    return str(ast.get("name") or tail.rsplit(":", 1)[-1]), _AST_KINDS.get(node_kind_ast, node_kind_ast.lower() or "symbol")


def load_node_link_graph(path: str | Path) -> tuple[GraphNodes, GraphEdges, GraphAttrs]:
    """Lee un JSON node-link y ademas los atributos que cada nodo declara (`schema.ast`,
    `schema.semantics`), como los escribe `sldb selfdoc python-sync`."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    nodes: GraphNodes = {}
    attrs: GraphAttrs = {}
    for node in raw.get("nodes") or []:
        _read_node(node, nodes, attrs)
    return nodes, _links(raw), attrs


def _links(raw: dict) -> GraphEdges:
    return [
        (str(link["source"]), str(link["target"]), str(link.get("relation") or ""))
        for link in raw.get("links") or []
        if link.get("source") and link.get("target")
    ]


def _read_node(node: dict, nodes: GraphNodes, attrs: GraphAttrs) -> None:
    node_id, node_type = _node_identity(node)
    if not node_id:
        return
    nodes[str(node_id)] = str(node_type or "")
    found = _node_attrs(str(node_id), str(node_type or ""), node)
    if found:
        attrs[str(node_id)] = found


def load_node_link(path: str | Path) -> tuple[GraphNodes, GraphEdges]:
    """Lee un JSON node-link (`sldb graph snapshot save --output x.json`)."""
    nodes, edges, _ = load_node_link_graph(path)
    return nodes, edges


def index_graph(index: Any) -> tuple[GraphNodes, GraphEdges]:
    """`(nodes, edges)` del edge index que devuelve `sldb.api.load_edge_index(store)`."""
    nodes: GraphNodes = {str(nid): str(rec.node_type or "") for nid, rec in index.nodes.items()}
    edges: GraphEdges = [(str(e.source), str(e.target), str(e.relation or "")) for e in index.edges]
    return nodes, edges
