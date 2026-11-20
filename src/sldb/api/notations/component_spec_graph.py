"""Compile an sldb graph `(nodes, edges)` into a component spec (migrated from `spec2viz.graph_import`).

`component_spec_from_graph` filtra por tipo de nodo, modelo y relacion, traduce los ids
`sldb://...` a identificadores seguros y devuelve un dict listo para `yaml.dump` que valida
como `ComponentDiagram`. Same signature and behaviour as in spec2viz, split to sldb's size rules.
"""

from __future__ import annotations

from typing import Iterable

from sldb.api.notations.component_spec_build import _Fields, _connected, _live_edges, _spec_data
from sldb.api.notations.component_spec_constants import DEFAULT_EXCLUDED_RELATIONS, DEFAULT_NODE_TYPES, GraphAttrs, GraphEdges, GraphNodes
from sldb.api.notations.component_spec_describe import _describe, _spec
from sldb.api.notations.component_spec_filters import _in_scope, _keeps
from sldb.api.notations.component_spec_ids import _normalize_type


def component_spec_from_graph(
    nodes: GraphNodes,
    edges: GraphEdges,
    *,
    node_types: Iterable[str] | None = None,
    models: Iterable[str] | None = None,
    relations: Iterable[str] | None = None,
    exclude_relations: Iterable[str] | None = None,
    drop_isolated: bool = False,
    spec_id: str = "sldb-graph",
    title: str = "sldb graph",
    source: str = "graph",
    attrs: GraphAttrs | None = None,
    module_prefixes: Iterable[str] | None = None,
    payloads: dict[str, dict] | None = None,
    label_field: str | None = None,
    kind_field: str | None = None,
    group_field: str | None = None,
) -> dict:
    """Compila `(nodes, edges)` en un dict de spec `component` listo para serializar.

    - `node_types`: tipos canonicos a conservar (`document`, `model`, ...); vacio ->
      `DEFAULT_NODE_TYPES`. Se acepta el prefijo `sldb_`.
    - `models`: solo documentos de estos modelos (los nodos no documento no se tocan).
    - `relations`: lista blanca de relaciones; si se da, anula `exclude_relations`.
    - `exclude_relations`: relaciones a omitir; `None` -> `DEFAULT_EXCLUDED_RELATIONS`.
    - `drop_isolated`: descarta nodos sin aristas ni anidamiento tras filtrar.
    - `attrs`: lo que la fuente declara por nodo (`load_node_link_graph`): label, kind y module
      mandan sobre lo que se deduce del id.
    - `module_prefixes`: alcance por modulo Python (`sldb.selfdoc`); un nodo entra si su
      `module` (o su id) es ese modulo o cuelga de el. Toda arista o `contains` con un
      extremo fuera del alcance se descarta, nada queda colgando.
    - `payloads` (id de nodo -> payload del documento) con `label_field`, `kind_field` y
      `group_field` (`campo` o `tag:<namespace>`): el label y el kind del nodo salen de ese
      campo y los documentos con el mismo valor de grupo quedan en un nodo contenedor
      (`contains`); lo que falta cae al id y al modelo. Sin payload no hay nada que leer.
    - La relacion `contains` se vuelve `contains: [...]` en el nodo origen; las demas se
      copian tal cual.
    """
    attrs, wanted_models = attrs or {}, tuple(models or ())
    prefixes = tuple(p.rstrip(".") for p in (module_prefixes or ()) if p)
    wanted_types = tuple(_normalize_type(t) for t in (node_types or ())) or DEFAULT_NODE_TYPES
    include = tuple(relations or ())
    exclude = DEFAULT_EXCLUDED_RELATIONS if exclude_relations is None else tuple(exclude_relations)
    kept = {nid: t for nid, t in nodes.items() if _keeps(nid, t, wanted_types, wanted_models) and _in_scope(nid, attrs, prefixes)}
    live_edges = _live_edges(edges, kept, include, exclude)
    kept = _connected(kept, live_edges) if drop_isolated else kept
    description = _describe(source, wanted_types, wanted_models, include, exclude, drop_isolated, prefixes)
    return _spec(spec_id, title, description, _spec_data(kept, live_edges, attrs, _Fields(payloads or {}, label_field, kind_field, group_field)))
