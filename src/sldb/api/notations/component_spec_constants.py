"""Constants of the component spec built from a graph (migrated from `spec2viz.graph_import`)."""

from __future__ import annotations

# Nodos del grafo: id -> tipo de nodo tal como lo entrega la fuente.
GraphNodes = dict[str, str]
# Aristas del grafo: (source, target, relation).
GraphEdges = list[tuple[str, str, str]]
# Atributos por nodo que la fuente declara (grafo de fuente Python de sldb): label, kind, module.
GraphAttrs = dict[str, dict[str, str]]

# `ast.node_kind` de un simbolo Python -> kind del nodo cuando no hay `semantics.kind`.
_AST_KINDS = {
    "ClassDef": "class",
    "FunctionDef": "function",
    "AsyncFunctionDef": "function",
    "Assign": "variable",
    "AnnAssign": "variable",
}

SLDB_SCHEME = "sldb://"

# Tipos de nodo que se conservan si el usuario no indica `--node-type`.
DEFAULT_NODE_TYPES: tuple[str, ...] = ("document", "model")

# Relaciones estructurales que solo agregan ruido en un diagrama de componentes.
DEFAULT_EXCLUDED_RELATIONS: tuple[str, ...] = (
    "has_section",
    "tagged_as",
    "has_document",
    "has_field",
    "has_model",
    "names",
    "semantic_parent",
    "semantic_equivalent",
    "applies_to_source",
    "applies_to_target",
)

# Relacion que se vuelve anidamiento (`contains`) en vez de arista.
CONTAINS_RELATION = "contains"

# Palabras que mermaid interpreta como sintaxis si aparecen como id de nodo.
_RESERVED_IDS = frozenset({"end", "graph", "subgraph", "style", "class", "click", "classDef", "linkStyle", "direction"})
