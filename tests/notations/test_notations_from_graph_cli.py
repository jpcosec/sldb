"""`sldb notations from-graph`: grafo sldb (node-link JSON o edge index) -> spec component.

Ported from spec2viz `tests/test_graph_import.py` (`test_cli_from_graph_*`), rewritten against
`sldb notations from-graph`: `GRAPH_JSON` is `--snapshot`, `--out` is `--output`, the spec2viz
`diagram validate` step is `load_spec` + `validate_spec`, and `diagram render`/`lint` stay in
spec2viz (renderers are out of scope): the nesting the mermaid output showed is asserted on the spec.
"""
import json
from types import SimpleNamespace

import yaml

from sldb.api.notations import load_spec, validate_spec
from sldb.cli import main
from tests.notations.test_component_spec_graph import EDGES, NODES, PY_GRAPH, _node_link, _validated


def test_cli_from_graph_writes_valid_spec(tmp_path, capsys):
    graph = _node_link(tmp_path / "snap.json")
    out = tmp_path / "graph.yml"
    assert main(["notations", "from-graph", "--snapshot", str(graph), "--model", "AtomDoc", "--output", str(out)]) == 0
    output = capsys.readouterr().out
    assert "Generated" in output and "3 nodes" in output

    spec = yaml.safe_load(out.read_text(encoding="utf-8"))
    assert spec["id"] == "snap" and spec["title"] == "snap graph"
    assert "snap.json" in spec["metadata"]["description"]
    _validated(spec)

    validate_spec(load_spec(out))
    nodes = spec["data"]["nodes"]
    assert nodes["document_AtomDoc_atom_x"]["label"] == "atom-x" and nodes["document_AtomDoc_atom_x"]["contains"] == ["document_AtomDoc_atom_y"]
    assert nodes["document_AtomDoc_atom_y"]["label"] == "atom-y"


def test_cli_from_graph_prints_yaml_to_stdout_with_filters(tmp_path, capsys):
    graph = _node_link(tmp_path / "snap.json")
    rc = main(
        ["notations", "from-graph", "--snapshot", str(graph), "--id", "tags", "--title", "Tags", "--node-type", "document",
         "--node-type", "semantic_tag", "--relation", "tagged_as", "--drop-isolated"],
    )
    assert rc == 0
    spec = yaml.safe_load(capsys.readouterr().out)
    assert spec["id"] == "tags" and spec["title"] == "Tags"
    assert set(spec["data"]["nodes"]) == {"document_AtomDoc_atom_x", "semantic_tag_system_spec2viz"}
    assert spec["data"]["edges"][0]["relation"] == "tagged_as"
    _validated(spec)


def test_cli_from_graph_requires_exactly_one_source(tmp_path):
    graph = _node_link(tmp_path / "snap.json")
    assert main(["notations", "from-graph"]) == 2
    assert main(["notations", "from-graph", "--snapshot", str(graph), "--store", str(tmp_path)]) == 2


def test_cli_from_graph_store_goes_through_loader(monkeypatch, tmp_path, capsys):
    import sldb.cli.commands.notations_from_graph as cmd

    fake_index = SimpleNamespace(
        nodes={nid: SimpleNamespace(node_type=ntype) for nid, ntype in NODES.items()},
        edges=[SimpleNamespace(source=s, target=t, relation=r) for s, t, r in EDGES],
    )
    monkeypatch.setattr(cmd, "load_edge_index", lambda store: fake_index)
    assert main(["notations", "from-graph", "--store", str(tmp_path), "--relation", "has_document"]) == 0
    spec = yaml.safe_load(capsys.readouterr().out)
    assert spec["id"] == "sldb-graph"
    assert f"store {tmp_path}" in spec["metadata"]["description"]
    assert spec["data"]["edges"] == [{"from": "model_AtomDoc", "to": "document_AtomDoc_atom_x", "relation": "has_document"}]


def test_cli_from_graph_module_prefix(tmp_path, capsys):
    path = tmp_path / "python-source.graph.json"
    path.write_text(json.dumps(PY_GRAPH), encoding="utf-8")
    out = tmp_path / "selfdoc.yml"
    rc = main(["notations", "from-graph", "--snapshot", str(path), "--node-type", "python_module", "--node-type", "python_symbol", "--module-prefix", "sldb.selfdoc", "--output", str(out)])
    assert rc == 0
    assert "4 nodes, 1 edges" in capsys.readouterr().out
    validate_spec(load_spec(out))


def test_cli_from_graph_reports_dangling_edges_on_stderr(tmp_path, capsys):
    graph = tmp_path / "ghost.json"
    nodes = [{"id": nid, "type": ntype} for nid, ntype in NODES.items()]
    links = [{"source": "sldb://document/AtomDoc:atom-x", "target": "sldb://document/Ghost:g", "relation": "uses"}]
    graph.write_text(json.dumps({"nodes": nodes, "links": links}), encoding="utf-8")
    assert main(["notations", "from-graph", "--snapshot", str(graph)]) == 0
    captured = capsys.readouterr()
    assert "alert: [component-spec/dangling-edge] sldb://document/AtomDoc:atom-x -> sldb://document/Ghost:g" in captured.err
    _validated(yaml.safe_load(captured.out))
