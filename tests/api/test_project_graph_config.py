"""`ProjectGraphConfig` as data: round trip, refusal naming the key, `store.yaml`, the CLI.

The configuration loads from and dumps to a plain mapping; an unknown key or a non-data value
fails naming its path, in Python and in `store.yaml` alike; the deprecated `closed_document`
callable is a Python-only argument until its consumer migrates; `sldb graph project` reads
the declared graph with the envelope every command has.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from sldb import api
from sldb.api.edges.project_graph import DocumentSurface, ProjectGraphConfig
from sldb.api.stores.store_declaration import load_declaration
from sldb.cli import main as cli_main
from sldb.core.exceptions import SLDBStoreError
from tests.api.test_project_graph import CONFIG, declared_project, project, tracked_project  # noqa: F401 - fixtures

MINIMAL = {"document_extractor": "d", "file_extractor": "f", "edge_extractor": "e", "surfaces": [{"kind": "k", "directory": "docs", "pattern": "*.md"}]}


def test_the_configuration_dumps_and_loads_back_equal() -> None:
    mapping = CONFIG.to_mapping()
    assert yaml.safe_load(yaml.safe_dump(mapping)) == mapping
    assert ProjectGraphConfig.from_mapping(mapping) == CONFIG
    assert mapping["surfaces"][2]["closed"] == 'status = "closed"' and "closed_document" not in mapping


def test_an_unknown_key_fails_to_load_naming_its_path() -> None:
    bad = {**MINIMAL, "surfaces": [{"kind": "k", "directory": "docs", "pattern": "*.md", "closed_document": "x"}]}
    with pytest.raises(ValueError, match=r"project_graph\.surfaces\[0\]\.closed_document"):
        ProjectGraphConfig.from_mapping(bad)
    with pytest.raises(ValueError, match=r"project_graph\.colour: unknown key"):
        ProjectGraphConfig.from_mapping({**MINIMAL, "colour": "red"})
    with pytest.raises(ValueError, match=r"^project_graph: expected a mapping"):
        ProjectGraphConfig.from_mapping(["not", "a", "mapping"])


def test_a_value_that_is_not_data_fails_to_load_naming_its_path() -> None:
    with pytest.raises(ValueError, match=r"project_graph\.surfaces\[0\]\.closed: function is not data"):
        ProjectGraphConfig.from_mapping({**MINIMAL, "surfaces": [{"kind": "k", "directory": "d", "pattern": "*", "closed": lambda k, t: True}]})
    with pytest.raises(ValueError, match=r"project_graph\.fields_by_kind\.k\[0\]: object is not data"):
        ProjectGraphConfig.from_mapping({**MINIMAL, "fields_by_kind": {"k": [object()]}})
    with pytest.raises(ValueError, match=r"(?s)project_graph: .*surfaces\.0\.kind"):
        ProjectGraphConfig.from_mapping({**MINIMAL, "surfaces": [{"directory": "d", "pattern": "*"}]})


def test_closed_document_is_a_deprecated_python_only_argument() -> None:
    with pytest.warns(DeprecationWarning, match="closed_document"):
        config = ProjectGraphConfig(**MINIMAL, closed_document=lambda kind, text: True)
    with pytest.raises(ValueError, match="closed_document"):
        config.to_mapping()
    with pytest.raises(ValueError, match=r"project_graph\.closed_document: unknown key"):
        ProjectGraphConfig.from_mapping({**MINIMAL, "closed_document": None})


def test_closed_wins_over_the_deprecated_callable_where_the_surface_declares_it(project: Path) -> None:  # noqa: F811
    with pytest.warns(DeprecationWarning):
        config = ProjectGraphConfig.model_validate({**dict(CONFIG), "closed_document": lambda kind, text: True})
    texts = api.ProjectGraph(project, config).texts
    assert texts.is_history("issue", texts.text("issues/open-login.md")) is None  # the surface's predicate decides
    assert texts.is_history("note", texts.text("notes/n1.md")) is True  # no `closed` on notes: the callable still answers


def test_a_closed_predicate_the_language_does_not_parse_is_refused() -> None:
    with pytest.raises(ValueError, match="predicate"):
        DocumentSurface(kind="k", directory="d", pattern="*.md", closed="status = = closed")


def test_store_yaml_refuses_a_project_graph_with_an_unknown_key_at_load(declared_project: Path) -> None:  # noqa: F811
    store = declared_project / ".sldb"
    definition = yaml.safe_load((store / "store.yaml").read_text(encoding="utf-8"))
    definition["project_graph"]["surfaces"][0]["closed_document"] = "status = 'closed'"
    (store / "store.yaml").write_text(yaml.safe_dump(definition), encoding="utf-8")
    with pytest.raises(ValueError, match=r"project_graph\.surfaces\[0\]\.closed_document"):
        load_declaration(store)
    with pytest.raises(ValueError, match=r"project_graph\.surfaces\[0\]\.closed_document"):
        api.project_graph(store)


def test_a_store_without_project_graph_says_so(tracked_project: Path) -> None:  # noqa: F811
    from sldb.api.stores.declare_store import declare_store
    from sldb.api.stores.store_declaration import save_declaration

    store = tracked_project / ".sldb"
    save_declaration(store, declare_store(store, tracked_project))
    assert "project_graph" not in yaml.safe_load((store / "store.yaml").read_text(encoding="utf-8"))
    with pytest.raises(SLDBStoreError, match="declares no project_graph"):
        api.project_graph(store)


def _json(capsys) -> dict:
    return json.loads(capsys.readouterr().out)


def test_cli_nodes_edges_and_missing_give_the_declared_graph(declared_project: Path, capsys) -> None:  # noqa: F811
    store = ["--store", str(declared_project / ".sldb"), "--format", "json"]
    assert cli_main(["graph", "project", "nodes", "--kind", "card", *store]) == 0
    nodes = _json(capsys)
    assert nodes["kind"] == "card" and [node["id"] for node in nodes["nodes"]] == ["card:card-a", "card:card-b", "card:card-c"]
    assert cli_main(["graph", "project", "nodes", *store]) == 0
    assert {node["id"] for node in _json(capsys)["nodes"]} >= {"source_file:src/app.py", "test_file:tests/test_app.py", "source_file:generated/out.py", "note:notes/n2.md"}
    assert cli_main(["graph", "project", "edges", "--to", "source_file:src/app.py", *store]) == 0
    edges = _json(capsys)
    assert edges["from"] is None and edges["to"] == "source_file:src/app.py"
    assert [(e["source_id"], e["provenance_path"], e["provenance_locator"]) for e in edges["edges"]] == [("card:card-a", "cards/card-a.md", "line:11:path"), ("card:card-b", "cards/card-b.md", "line:8:path")]
    assert cli_main(["graph", "project", "edges", "--from", "card:card-c", *store]) == 0
    assert ("note:notes/n2.md", "notes") in {(e["target_id"], e["role"]) for e in _json(capsys)["edges"]}
    assert cli_main(["graph", "project", "missing", *store]) == 0
    assert {(m["source_id"], m["target_id"]) for m in _json(capsys)["missing"]} >= {("card:card-a", "topic:auth"), ("card:card-a", "source_file:src/gone.py"), ("card:card-c", "card:card-missing")}


def test_cli_edges_needs_exactly_one_end(declared_project: Path, capsys) -> None:  # noqa: F811
    store = ["--store", str(declared_project / ".sldb")]
    assert cli_main(["graph", "project", "edges", *store]) == 2
    assert cli_main(["graph", "project", "edges", "--from", "a", "--to", "b", *store]) == 2
    assert cli_main(["--envelope", "graph", "project", "edges", *store]) == 6
    envelope = _json(capsys)
    assert envelope["ok"] is False and envelope["error"]["type"] == "cli/usage"


def test_cli_text_and_envelope(declared_project: Path, capsys) -> None:  # noqa: F811
    store = ["--store", str(declared_project / ".sldb")]
    assert cli_main(["graph", "project", "edges", "--to", "source_file:src/app.py", *store]) == 0
    assert "card:card-a -touches-> source_file:src/app.py (cards/card-a.md:line:11:path)" in capsys.readouterr().out
    assert cli_main(["--envelope", "graph", "project", "missing", *store, "--format", "json"]) == 0
    envelope = _json(capsys)
    assert envelope["ok"] is True and envelope["command"] == "graph project" and envelope["data"]["missing"]
