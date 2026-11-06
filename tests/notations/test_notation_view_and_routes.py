"""Comprehensive tests for notation views, projection views, sync utilities, CLI and HTTP serve routes."""

from __future__ import annotations

import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

import sldb.api as api
from sldb.api import (
    GlyphDoc,
    LinkDoc,
    NotationDoc,
    PaletteDoc,
    SpecDoc,
    SpecNodeDoc,
    ViewDoc,
    evaluate_projection_view,
    list_projection_views,
    resolve_documents,
    resolve_view,
    save_projection_view,
    sync_notation,
    sync_palette,
)
from sldb.api.notations.notation_view import (
    ViewError,
    flatten,
    fragment_kind,
    fragments_of,
    link_order,
    lookup,
    matches,
    render_keyword,
    render_template,
)
from sldb.cli.dispatcher import CLI
from sldb.cli.serve.http_server import build_handler


# --- Helper fixtures & setup --------------------------------------------------

def _request_json(url: str, method: str = "GET", data: dict | None = None) -> tuple[int, dict]:
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = Request(url, data=body, method=method, headers={"Content-Type": "application/json"})
    try:
        with urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8"))
    except HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


@pytest.fixture
def test_store(tmp_path: Path) -> Path:
    """Creates a temporary store initialized with relation types and default palette + uml-class notation."""
    project_root = tmp_path / "project"
    project_root.mkdir()
    store_dir = project_root / ".sldb"
    api.init_store(project_root)

    # Sync default palette and uml-class notation
    sync_palette(store_dir, "default")
    sync_notation(store_dir, "uml-class")

    return store_dir


# --- 1. Unit Tests for helper functions ---------------------------------------

def test_flatten_and_lookup():
    raw = {"id": "foo", "data": {"status": "active", "nested": {"val": 42}}}
    flat = flatten(raw)
    assert flat["id"] == "foo"
    assert flat["status"] == "active"
    assert flat["nested"] == {"val": 42}

    assert lookup(raw, "data.nested.val") == 42
    assert lookup(raw, "data.unknown") is None
    assert lookup(raw, "nonexistent.part") is None


def test_render_template_and_keyword():
    payload = {"title": "MyClass", "kind": "interface", "data": {"author": "Alice", "meta": {"version": "1.0"}}}
    assert render_template("Class: {title} by {author}", payload) == "Class: MyClass by Alice"
    assert render_template("Nested: {data.meta.version}", payload) == "Nested: 1.0"
    assert render_template("Missing: {nonexistent}", payload) == "Missing:"

    # Keyword formatting
    assert render_keyword("«{kind}»", payload) == "«interface»"
    assert render_keyword("«{missing}»", payload) == ""


def test_where_matches_payload():
    payload = {"title": "OrderService", "data": {"tier": "backend", "critical": True}}
    # sldb where grammar uses = instead of == and double quotes for strings
    assert matches('tier = "backend"', payload) is True
    assert matches('tier = "frontend"', payload) is False
    assert matches("", payload) is True


def test_link_order_and_fragments():
    assert link_order("spec.01-A__uses__B") == 1
    assert link_order("spec.15-A__uses__B") == 15
    assert link_order("invalid_format") == 0

    kind, label = fragment_kind("loop for each item")
    assert kind == "loop"
    assert label == "for each item"

    kind, label = fragment_kind("custom block")
    assert kind == "group"
    assert label == "custom block"

    links = [
        {"order": 1, "data": {"group": "loop outer"}},
        {"order": 2, "data": {"group": "loop outer"}},
        {"order": 3, "data": {}},
        {"order": 4, "data": {"group": "opt maybe"}},
    ]
    frags = fragments_of(links)
    assert len(frags) == 2
    assert frags[0] == {"label": "outer", "kind": "loop", "group": "loop outer", "orders": [1, 2]}
    assert frags[1] == {"label": "maybe", "kind": "opt", "group": "opt maybe", "orders": [4]}


# --- 2. Notation View & Resolve Documents Tests ------------------------------

def _create_sample_spec_and_nodes(store_dir: Path):
    open_res = api.open_store(store_dir)
    root = Path(open_res.project_root)

    # Create SpecNodeDocs
    node1_payload = {
        "id": "spec1.User",
        "title": "User",
        "spec": "SpecDoc:spec1",
        "kind": "entity",
        "collection": "classes",
        "element": "User",
        "contains": [],
        "refs": [],
        "atom_refs": [],
        "data": {
            "attributes": ["+id: int", "+name: string"],
            "methods": ["+save(): void"],
        },
        "description": "",
    }
    node2_payload = {
        "id": "spec1.Order",
        "title": "Order",
        "spec": "SpecDoc:spec1",
        "kind": "entity",
        "collection": "classes",
        "element": "Order",
        "contains": [],
        "refs": [],
        "atom_refs": [],
        "data": {
            "attributes": ["+order_id: int"],
        },
        "description": "",
    }
    api.create_document(
        store_dir,
        "SpecNodeDoc",
        root / "sldb" / "specs" / "nodes" / "User.md",
        node1_payload,
        name="spec1.User",
    )
    api.create_document(
        store_dir,
        "SpecNodeDoc",
        root / "sldb" / "specs" / "nodes" / "Order.md",
        node2_payload,
        name="spec1.Order",
    )

    # Create RelationDoc connecting them
    rel_payload = {
        "title": "spec1.01-User__association__Order",
        "source_id": "SpecNodeDoc:spec1.User",
        "target_id": "SpecNodeDoc:spec1.Order",
        "relation_type": "association",
        "condition": "",
        "notes": "places",
        "attributes": {"label": "places"},
    }
    api.create_document(
        store_dir,
        "RelationDoc",
        root / "sldb" / "specs" / "relations" / "rel1.md",
        rel_payload,
        name="spec1.01-User__association__Order",
    )

    spec_payload = {
        "id": "spec1",
        "title": "Shop Spec",
        "diagram_type": "class",
        "version": "1.0",
        "spec_path": "specs/shop.yml",
        "sha256": "abcdef",
        "notation": "NotationDoc:uml-class",
        "nodes": ["SpecNodeDoc:spec1.User", "SpecNodeDoc:spec1.Order"],
        "category": "diagram",
        "nav": "",
        "summary": "Shop model",
        "style": {},
        "description": "",
    }
    api.create_document(
        store_dir,
        "SpecDoc",
        root / "sldb" / "specs" / "spec1.md",
        spec_payload,
        name="spec1",
    )

    api.rebuild_edges(store_dir)


def test_resolve_documents_and_view(test_store: Path):
    _create_sample_spec_and_nodes(test_store)

    doc_refs = ["SpecNodeDoc:spec1.User", "SpecNodeDoc:spec1.Order"]
    res = resolve_documents(test_store, "NotationDoc:uml-class", doc_refs)

    assert res["notation"] == "NotationDoc:uml-class"
    assert len(res["nodes"]) == 2
    user_node = next(n for n in res["nodes"] if n["doc"] == "SpecNodeDoc:spec1.User")
    assert user_node["title"] == "User"
    assert user_node["shape"] == "class-box"
    assert len(user_node["compartments"]) == 2
    assert user_node["compartments"][0]["path"] == "data.attributes"
    assert user_node["compartments"][0]["items"] == ["+id: int", "+name: string"]

    assert len(res["links"]) == 1
    link = res["links"][0]
    assert link["source"] == "SpecNodeDoc:spec1.User"
    assert link["target"] == "SpecNodeDoc:spec1.Order"
    assert link["relation"] == "association"
    assert link["label"] == "places"
    assert link["order"] == 1

    assert "legend" in res
    assert len(res["legend"]["glyphs"]) > 0
    assert len(res["legend"]["links"]) > 0

    # Test resolve_view
    view_res = resolve_view(test_store, "SpecDoc:spec1")
    assert view_res["spec"] == "SpecDoc:spec1"
    assert view_res["title"] == "Shop Spec"
    assert view_res["diagram_type"] == "class"
    assert len(view_res["nodes"]) == 2
    assert len(view_res["links"]) == 1


def test_resolve_view_errors(test_store: Path):
    with pytest.raises(ViewError, match="is not in the store"):
        resolve_view(test_store, "SpecDoc:nonexistent")

    # Mismatched diagram_type
    open_res = api.open_store(test_store)
    root = Path(open_res.project_root)
    spec_payload = {
        "id": "bad_spec",
        "title": "Bad Spec",
        "diagram_type": "sequence",  # notation uml-class is class
        "version": "1.0",
        "spec_path": "",
        "sha256": "",
        "notation": "NotationDoc:uml-class",
        "nodes": [],
        "category": "",
        "nav": "",
        "summary": "",
        "style": {},
        "description": "",
    }
    api.create_document(
        test_store,
        "SpecDoc",
        root / "sldb" / "specs" / "bad.md",
        spec_payload,
        name="bad_spec",
    )
    with pytest.raises(ViewError, match="draws `class` specs and SpecDoc:bad_spec is a `sequence` spec"):
        resolve_view(test_store, "SpecDoc:bad_spec")


# --- 3. Projection Views API Tests --------------------------------------------

def test_projection_views_crud_and_evaluate(test_store: Path):
    _create_sample_spec_and_nodes(test_store)

    view_def = {
        "id": "entities_view",
        "name": "entities_view",
        "title": "Entities View",
        "nodes": [{"model": "SpecNodeDoc", "where": 'kind = "entity"'}],
        "relations": ["association"],
        "direction": "both",
        "notation": "NotationDoc:uml-class",
        "layout": {},
        "params": {},
        "sections": [],
        "description": "",
    }

    # Save projection view
    saved = save_projection_view(test_store, "entities_view", view_def)
    assert saved["saved"] is True
    assert saved["ref"] == "ViewDoc:entities_view"

    # List views
    views = list_projection_views(test_store)
    assert any(v["ref"] == "ViewDoc:entities_view" for v in views)

    # Evaluate projection view by ref
    eval_res = evaluate_projection_view(test_store, "ViewDoc:entities_view")
    assert "nodes" in eval_res
    assert "edges" in eval_res
    assert "layout" in eval_res
    assert "notation" in eval_res
    styled_nodes = eval_res["notation"]["nodes"]
    assert any(n["id"] in styled_nodes for n in eval_res["nodes"])

    # Evaluate by raw dict
    eval_raw = evaluate_projection_view(test_store, view_def)
    assert len(eval_raw["nodes"]) == len(eval_res["nodes"])


# --- 4. CLI Subcommand Tests --------------------------------------------------

def test_cli_notations(test_store: Path, capsys: pytest.CaptureFixture):
    _create_sample_spec_and_nodes(test_store)
    cli = CLI()

    # sldb notations list
    class ArgsList:
        notations_command = "list"
        store = str(test_store)
        pythonpath = None
        views = False

    ret = cli.handlers["notations"](ArgsList())
    assert ret == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    assert "uml-class" in data["builtin_notations"]
    assert "default" in data["builtin_palettes"]

    # sldb notations list --views
    ArgsList.views = True
    ret = cli.handlers["notations"](ArgsList())
    assert ret == 0
    out = capsys.readouterr().out
    views = json.loads(out)
    assert isinstance(views, list)

    # sldb notations sync --notation statechart
    class ArgsSync:
        notations_command = "sync"
        store = str(test_store)
        pythonpath = None
        notation = "statechart"
        palette = None

    ret = cli.handlers["notations"](ArgsSync())
    assert ret == 0
    out = capsys.readouterr().out
    rep = json.loads(out)
    assert rep["spec_id"] == "statechart"

    # sldb notations view spec1
    class ArgsView:
        notations_command = "view"
        store = str(test_store)
        pythonpath = None
        spec = "spec1"
        projection = False

    ret = cli.handlers["notations"](ArgsView())
    assert ret == 0
    out = capsys.readouterr().out
    v = json.loads(out)
    assert v["spec"] == "SpecDoc:spec1"
    assert len(v["nodes"]) == 2

    # sldb notations resolve --notation uml-class --docs SpecNodeDoc:spec1.User
    class ArgsResolve:
        notations_command = "resolve"
        store = str(test_store)
        pythonpath = None
        notation = "uml-class"
        docs = ["SpecNodeDoc:spec1.User"]
        relations = []

    ret = cli.handlers["notations"](ArgsResolve())
    assert ret == 0
    out = capsys.readouterr().out
    r = json.loads(out)
    assert r["notation"] == "NotationDoc:uml-class"
    assert len(r["nodes"]) == 1


# --- 5. HTTP Serve Route Tests ------------------------------------------------

def test_serve_notations_and_projection_routes(test_store: Path):
    _create_sample_spec_and_nodes(test_store)

    handler = build_handler(str(test_store), None, cors=False)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_address[1]}"

    try:
        # GET /notations
        status, data = _request_json(f"{base_url}/notations")
        assert status == 200
        assert data["ok"] is True
        assert "uml-class" in data["builtin_notations"]

        # GET /notations/view?spec=spec1
        status, data = _request_json(f"{base_url}/notations/view?spec=spec1")
        assert status == 200
        assert data["ok"] is True
        assert data["spec"] == "SpecDoc:spec1"
        assert len(data["nodes"]) == 2

        # POST /notations/resolve
        status, data = _request_json(
            f"{base_url}/notations/resolve",
            method="POST",
            data={"notation": "uml-class", "docs": ["SpecNodeDoc:spec1.User", "SpecNodeDoc:spec1.Order"]},
        )
        assert status == 200
        assert data["ok"] is True
        assert len(data["nodes"]) == 2

        # GET /views/projection
        status, data = _request_json(f"{base_url}/views/projection")
        assert status == 200
        assert data["ok"] is True
        assert isinstance(data["views"], list)

        # POST /views/projection/evaluate
        view_payload = {
            "nodes": [{"model": "SpecNodeDoc"}],
            "relations": ["association"],
            "direction": "both",
            "notation": "NotationDoc:uml-class",
        }
        status, data = _request_json(
            f"{base_url}/views/projection/evaluate",
            method="POST",
            data=view_payload,
        )
        assert status == 200
        assert data["ok"] is True
        assert len(data["nodes"]) >= 2
        assert "notation" in data

        # POST /views/projection/save
        status, data = _request_json(
            f"{base_url}/views/projection/save",
            method="POST",
            data={"name": "test_saved_view", "view": view_payload},
        )
        assert status == 200
        assert data["ok"] is True
        assert data["ref"] == "ViewDoc:test_saved_view"

        # GET /views/projection/evaluate?view=test_saved_view
        status, data = _request_json(f"{base_url}/views/projection/evaluate?view=test_saved_view")
        assert status == 200
        assert data["ok"] is True
        assert len(data["nodes"]) >= 2

    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2.0)
