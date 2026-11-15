"""Component spec from an sldb graph (node-link JSON or edge index).

Ported from spec2viz `tests/test_graph_import.py` with the minimum change: the functions come
from `sldb.api.notations`, `_validated` uses D3's `ComponentDiagram` + `validate_spec`, and the
store test goes through `sldb.api.load_edge_index` directly (`index_graph`, no loader of its own).
The five CLI tests live in `test_notations_from_graph_cli.py`.
"""
import json
from types import SimpleNamespace

from sldb.api.notations import (
    DEFAULT_EXCLUDED_RELATIONS,
    component_spec_from_graph,
    document_ref,
    index_graph,
    load_node_link,
    node_kind,
    sanitize_id,
    validate_spec,
)
from sldb.models.notation.diagram_specs.component import ComponentDiagram

# Grafo minimo: dos atoms, una task, un modelo, un tag y una seccion.
NODES = {
    "sldb://store": "sldb_store",
    "sldb://model/AtomDoc": "sldb_model",
    "sldb://document/AtomDoc:atom-x": "sldb_document",
    "sldb://document/AtomDoc:atom-y": "AtomDoc",
    "sldb://document/TaskDoc:task-z": "sldb_document",
    "sldb://section/AtomDoc:atom-x#intro": "sldb_section",
    "sldb://semantic_tag/system:spec2viz": "semantic_tag",
}
EDGES = [
    ("sldb://store", "sldb://model/AtomDoc", "has_model"),
    ("sldb://model/AtomDoc", "sldb://document/AtomDoc:atom-x", "has_document"),
    ("sldb://document/AtomDoc:atom-x", "sldb://section/AtomDoc:atom-x#intro", "has_section"),
    ("sldb://document/AtomDoc:atom-x", "sldb://semantic_tag/system:spec2viz", "tagged_as"),
    ("sldb://document/AtomDoc:atom-x", "sldb://document/AtomDoc:atom-y", "contains"),
    ("sldb://document/AtomDoc:atom-y", "sldb://document/TaskDoc:task-z", "explains"),
    ("sldb://document/AtomDoc:atom-y", "sldb://document/TaskDoc:task-z", "explains"),
]


def _validated(spec: dict):
    diagram = ComponentDiagram.model_validate(spec)
    validate_spec(diagram)
    return diagram


# --- helpers de ids -------------------------------------------------------------

def test_node_kind_prefers_uri_segment_over_source_type():
    assert node_kind("sldb://document/AtomDoc:atom-x", "AtomDoc") == "document"
    assert node_kind("sldb://document/AtomDoc:atom-x", "sldb_document") == "document"
    assert node_kind("sldb://semantic_tag/a:b", "semantic_tag") == "semantic_tag"
    assert node_kind("sldb://store", "sldb_store") == "store"
    assert node_kind("plain-id", "sldb_model") == "model"


def test_document_ref_parses_model_name_and_linked_store():
    assert document_ref("sldb://document/AtomDoc:atom-x") == ("AtomDoc", "atom-x")
    assert document_ref("sldb://document/desk:TaskDoc:task-z") == ("TaskDoc", "task-z")
    assert document_ref("sldb://document/atom-x", "AtomDoc") == ("AtomDoc", "atom-x")
    assert document_ref("sldb://model/AtomDoc", "sldb_model") == (None, None)


def test_sanitize_id_is_safe_identifier():
    assert sanitize_id("sldb://document/AtomDoc:atom-x") == "document_AtomDoc_atom_x"
    assert sanitize_id("sldb://section/AtomDoc:atom-x#intro") == "section_AtomDoc_atom_x_intro"
    assert sanitize_id("sldb://store") == "store"
    assert sanitize_id("123abc") == "n_123abc"
    assert sanitize_id("end") == "n_end"
    assert sanitize_id("///") == "node"


# --- compilacion ----------------------------------------------------------------

def test_default_keeps_documents_and_models_without_structural_edges():
    spec = component_spec_from_graph(NODES, EDGES, source="test")
    _validated(spec)
    nodes = spec["data"]["nodes"]
    assert set(nodes) == {"model_AtomDoc", "document_AtomDoc_atom_x", "document_AtomDoc_atom_y", "document_TaskDoc_task_z"}
    assert nodes["model_AtomDoc"] == {"label": "AtomDoc", "kind": "model"}
    assert nodes["document_AtomDoc_atom_y"]["label"] == "atom-y"
    assert nodes["document_AtomDoc_atom_y"]["kind"] == "AtomDoc"
    assert nodes["document_TaskDoc_task_z"]["kind"] == "TaskDoc"
    # has_model / has_document / has_section / tagged_as se descartan por defecto
    assert spec["data"]["edges"] == [{"from": "document_AtomDoc_atom_y", "to": "document_TaskDoc_task_z", "relation": "explains"}]
    assert spec["type"] == "component" and spec["version"] == "1.0"
    assert "test" in spec["metadata"]["description"]
    assert "exclude_relations=" + ",".join(DEFAULT_EXCLUDED_RELATIONS) in spec["metadata"]["description"]


def test_contains_relation_nests_instead_of_edge():
    spec = component_spec_from_graph(NODES, EDGES)
    assert spec["data"]["nodes"]["document_AtomDoc_atom_x"]["contains"] == ["document_AtomDoc_atom_y"]
    assert "contains" not in spec["data"]["nodes"]["document_AtomDoc_atom_y"]
    assert all(e["relation"] != "contains" for e in spec["data"]["edges"])


def test_duplicate_edges_collapse():
    spec = component_spec_from_graph(NODES, EDGES)
    assert len([e for e in spec["data"]["edges"] if e["relation"] == "explains"]) == 1


def test_model_filter_keeps_only_documents_of_that_model():
    spec = component_spec_from_graph(NODES, EDGES, models=["AtomDoc"])
    nodes = spec["data"]["nodes"]
    assert "document_TaskDoc_task_z" not in nodes
    assert "model_AtomDoc" in nodes  # el filtro de modelo no toca nodos que no son documentos
    assert spec["data"]["edges"] == []  # la arista hacia task-z pierde su destino


def test_node_type_filter_accepts_sldb_prefix():
    spec = component_spec_from_graph(NODES, EDGES, node_types=["sldb_document", "semantic_tag"], relations=["tagged_as"])
    nodes = spec["data"]["nodes"]
    assert "model_AtomDoc" not in nodes
    assert nodes["semantic_tag_system_spec2viz"] == {"label": "system:spec2viz", "kind": "semantic_tag"}
    assert spec["data"]["edges"] == [
        {"from": "document_AtomDoc_atom_x", "to": "semantic_tag_system_spec2viz", "relation": "tagged_as"}
    ]


def test_relation_include_overrides_default_exclusions():
    spec = component_spec_from_graph(NODES, EDGES, relations=["has_document"])
    assert spec["data"]["edges"] == [
        {"from": "model_AtomDoc", "to": "document_AtomDoc_atom_x", "relation": "has_document"}
    ]
    assert "relations=has_document" in spec["metadata"]["description"]


def test_exclude_relation_replaces_defaults():
    spec = component_spec_from_graph(NODES, EDGES, exclude_relations=["explains"])
    relations = {e["relation"] for e in spec["data"]["edges"]}
    assert "explains" not in relations
    assert "has_document" in relations  # ya no esta excluida


def test_drop_isolated_removes_nodes_without_edges_or_nesting():
    spec = component_spec_from_graph(NODES, EDGES, drop_isolated=True)
    assert set(spec["data"]["nodes"]) == {"document_AtomDoc_atom_x", "document_AtomDoc_atom_y", "document_TaskDoc_task_z"}
    spec = component_spec_from_graph(NODES, EDGES, models=["AtomDoc"], relations=["explains"], drop_isolated=True)
    assert spec["data"]["nodes"] == {}
    assert spec["data"]["edges"] == []


def test_sanitized_ids_stay_unique():
    nodes = {"sldb://document/AtomDoc:a-b": "sldb_document", "sldb://document/AtomDoc:a_b": "sldb_document",
             "sldb://document/AtomDoc:a.b": "sldb_document"}
    spec = component_spec_from_graph(nodes, [("sldb://document/AtomDoc:a-b", "sldb://document/AtomDoc:a.b", "uses")])
    assert set(spec["data"]["nodes"]) == {"document_AtomDoc_a_b", "document_AtomDoc_a_b_2", "document_AtomDoc_a_b_3"}
    assert spec["data"]["edges"] == [{"from": "document_AtomDoc_a_b", "to": "document_AtomDoc_a_b_3", "relation": "uses"}]
    _validated(spec)


def test_edges_to_unknown_nodes_are_dropped():
    edges = EDGES + [("sldb://document/AtomDoc:atom-x", "sldb://document/Ghost:g", "uses")]
    spec = component_spec_from_graph(NODES, edges)
    assert all(e["to"] != "document_Ghost_g" for e in spec["data"]["edges"])
    _validated(spec)


# --- loaders --------------------------------------------------------------------

def _node_link(path):
    """Mezcla nodos con `id`/`type` y nodos que solo traen `schema.identity`."""
    nodes = []
    for i, (nid, ntype) in enumerate(NODES.items()):
        if i % 2:
            nodes.append({"id": nid, "type": ntype, "schema": {"identity": {"node_id": nid, "node_type": ntype}}})
        else:
            nodes.append({"schema": {"identity": {"node_id": nid, "node_type": ntype}}})
    links = [{"source": s, "target": t, "relation": r, "metadata": {}} for s, t, r in EDGES]
    path.write_text(json.dumps({"directed": True, "multigraph": False, "graph": {}, "nodes": nodes, "links": links}))
    return path


def test_load_node_link_reads_id_from_top_level_or_schema_identity(tmp_path):
    nodes, edges = load_node_link(_node_link(tmp_path / "g.json"))
    assert nodes == NODES
    assert edges == EDGES


def test_load_store_index_uses_public_sldb_api(monkeypatch, tmp_path):
    import sldb.api

    fake_index = SimpleNamespace(
        nodes={nid: SimpleNamespace(id=nid, node_type=ntype, semantics={}, facets={}) for nid, ntype in NODES.items()},
        edges=[SimpleNamespace(source=s, target=t, relation=r, metadata={}) for s, t, r in EDGES],
    )
    calls = []
    monkeypatch.setattr(sldb.api, "load_edge_index", lambda store: calls.append(store) or fake_index)

    nodes, edges = index_graph(sldb.api.load_edge_index(tmp_path / ".sldb"))

    assert calls == [tmp_path / ".sldb"]
    assert nodes == NODES
    assert edges == EDGES


# --- grafo de fuente Python de sldb (schema.identity / semantics / ast) -------------------------

def _py_node(node_id, node_type, ast=None, semantics=None):
    return {"id": node_id, "schema": {"identity": {"node_id": node_id, "node_type": node_type}, "ast": ast or {}, "semantics": semantics or {}}}


PY_GRAPH = {
    "directed": True,
    "nodes": [
        _py_node("python:sldb", "python_module", {"module": "sldb", "kind": "python_module"}),
        _py_node("python:sldb.selfdoc", "python_module", {"module": "sldb.selfdoc", "kind": "python_module"}, {"kind": "core"}),
        _py_node("python:sldb.selfdoc.parser", "python_module", {"module": "sldb.selfdoc.parser"}),
        _py_node("python:sldb.selfdoc.parser:Parser", "python_symbol", {"module": "sldb.selfdoc.parser", "name": "Parser", "node_kind": "ClassDef"}),
        _py_node("python:sldb.selfdoc.parser:parse", "python_symbol", {"module": "sldb.selfdoc.parser", "name": "parse", "node_kind": "FunctionDef"}, {"kind": "interface"}),
        _py_node("python:sldb.selfdocs_other", "python_module", {"module": "sldb.selfdocs_other"}),
        _py_node("python:sldb.api", "python_module", {"module": "sldb.api"}),
        _py_node("python:external:yaml:safe_load", "python_external"),
    ],
    "links": [
        {"source": "python:sldb", "target": "python:sldb.selfdoc", "relation": "contains"},
        {"source": "python:sldb.selfdoc", "target": "python:sldb.selfdoc.parser", "relation": "contains"},
        {"source": "python:sldb.selfdoc.parser", "target": "python:sldb.selfdoc.parser:Parser", "relation": "contains"},
        {"source": "python:sldb.selfdoc.parser", "target": "python:sldb.selfdoc.parser:parse", "relation": "contains"},
        {"source": "python:sldb.selfdoc.parser", "target": "python:sldb.api", "relation": "imports"},
        {"source": "python:sldb.selfdoc.parser", "target": "python:external:yaml:safe_load", "relation": "imports"},
        {"source": "python:sldb.selfdoc.parser:parse", "target": "python:sldb.selfdoc.parser:Parser", "relation": "references"},
    ],
}


def test_python_source_graph_labels_kinds_and_scope(tmp_path):
    from sldb.api.notations import load_node_link_graph

    path = tmp_path / "python-source.graph.json"
    path.write_text(json.dumps(PY_GRAPH), encoding="utf-8")
    nodes, edges, attrs = load_node_link_graph(path)
    assert attrs["python:sldb.selfdoc.parser:Parser"] == {"label": "Parser", "kind": "class", "module": "sldb.selfdoc.parser"}
    assert attrs["python:sldb.selfdoc.parser:parse"]["kind"] == "interface"  # semantics.kind declarado manda
    assert attrs["python:sldb.selfdoc"] == {"label": "sldb.selfdoc", "kind": "core", "module": "sldb.selfdoc"}
    assert attrs["python:sldb.selfdoc.parser"]["kind"] == "module"
    assert attrs["python:external:yaml:safe_load"] == {"label": "yaml:safe_load", "kind": "external", "module": ""}

    spec = component_spec_from_graph(
        nodes, edges, node_types=("python_module", "python_symbol", "python_external"), attrs=attrs,
        module_prefixes=("sldb.selfdoc",), spec_id="selfdoc", title="selfdoc",
    )
    ids = set(spec["data"]["nodes"])
    labels = {n["label"]: n["kind"] for n in spec["data"]["nodes"].values()}
    # alcance: sldb.selfdoc y lo que cuelga; ni sldb, ni sldb.api, ni sldb.selfdocs_other, ni externos
    assert labels == {"sldb.selfdoc": "core", "sldb.selfdoc.parser": "module", "Parser": "class", "parse": "interface"}
    # nada colgando: todo contains y toda arista apunta a un nodo del spec, y las relaciones van tal cual
    for node in spec["data"]["nodes"].values():
        assert set(node.get("contains", [])) <= ids
    assert all(e["from"] in ids and e["to"] in ids for e in spec["data"]["edges"])
    assert sorted(e["relation"] for e in spec["data"]["edges"]) == ["references"]  # el import a sldb.api quedo fuera del alcance
    assert "module_prefix=sldb.selfdoc" in spec["metadata"]["description"]
    _validated(spec)
