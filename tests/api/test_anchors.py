"""The anchoring rules, executable (docs/architecture/code-anchoring.md §9): one test per rule of
anchoring.md §3, the error-versus-alert split, and no alert ever silent."""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

import pytest

import sldb.api as api
from sldb.api.anchors import check_anchors, record_anchor
from sldb.api.anchors.anchor_docs import write_anchor
from sldb.cli import main as cli_main
from sldb.models.anchor_state import AnchorState
from sldb.code.runtime import available

pytestmark = pytest.mark.skipif(not available(), reason="tree-sitter runtime not installed (extra [code])")

CODE = 'class K:\n    """K doc."""\n\n    def m(self, x: int = 1) -> int:\n        """M doc."""\n        y = x + 1\n        return y\n\n\ndef free(a):\n    """Free doc."""\n    return a\n'
REF = "code:src/x.py::K.m"


@pytest.fixture
def world(tmp_path):
    root = tmp_path / "repo"
    (root / "src").mkdir(parents=True)
    (root / "src" / "x.py").write_text(CODE, encoding="utf-8")
    store = api.init_store(root).store_path
    api.add_model(store, "sldb.models.code_anchor_doc:CodeAnchorDoc")
    write_anchor(store, None, root / "anchors" / "m.md", record_anchor(root, REF), "m adds one")
    yield root, store
    for name in [m for m in sys.modules if m.startswith("tmpdocs")]:
        del sys.modules[name]


def _edit(root: Path, old: str, new: str) -> None:
    path = root / "src" / "x.py"
    path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")


def _state(store) -> tuple[AnchorState, list[str]]:
    [report] = check_anchors(store)
    return report.state, report.changed


def test_rule_1_docstring_and_body_are_distinct_nodes_and_formatting_is_not_a_mutation(world):
    root, store = world
    assert _state(store) == (AnchorState.INTACT, [])
    _edit(root, "M doc.", "Other doc.")
    assert _state(store) == (AnchorState.CHANGED, ["docstring"])
    _edit(root, "return y", "return y + 1")
    assert _state(store) == (AnchorState.CHANGED, ["docstring", "body"])
    _edit(root, "Other doc.", "M doc.")
    assert _state(store) == (AnchorState.CHANGED, ["body"])
    _edit(root, "return y + 1", "return y")
    _edit(root, "y = x + 1\n", "y   =   x+1\n\n")
    assert _state(store) == (AnchorState.INTACT, [])


def test_rule_2_changed_is_an_alert_with_exit_0_visible_in_text_json_and_envelope(world, capsys):
    root, store = world
    _edit(root, "return y", "return y + 1")
    assert cli_main(["anchors", "check", "--store", str(store)]) == 0
    out = capsys.readouterr().out
    assert "1 changed" in out and "alert: [anchors/changed] CodeAnchorDoc:m: changed(body)" in out
    assert cli_main(["anchors", "check", "--store", str(store), "--format", "json"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["anchors"][0]["state"] == "changed" and [a["code"] for a in report["alerts"]] == ["anchors/changed"] and report["errors"] == []
    assert cli_main(["--envelope", "anchors", "check", "--store", str(store), "--format", "json"]) == 0
    assert [w["code"] for w in json.loads(capsys.readouterr().out)["warnings"]] == ["anchors/changed"]


def test_rule_3_a_rename_reconnects_and_only_record_writes_it(world):
    root, store = world
    _edit(root, "def m(", "def renamed(")
    [report] = check_anchors(store)
    assert (report.state, report.to) == (AnchorState.RECONNECTED, "code:src/x.py::K.renamed")
    assert (root / "anchors" / "m.md").read_text(encoding="utf-8").count("K.renamed") == 0, "check reads only"
    [report] = check_anchors(store, record=True)
    assert report.state is AnchorState.RECONNECTED
    text = (root / "anchors" / "m.md").read_text(encoding="utf-8")
    assert "ref: code:src/x.py::K.renamed" in text and "event: reconnected" in text and "from: code:src/x.py::K.m" in text
    assert _state(store) == (AnchorState.INTACT, [])


def test_rule_3_deleted_or_ambiguous_is_lost_and_lists_the_candidates(world):
    root, store = world
    _edit(root, "def m(", "def m1(")
    _edit(root, "def free(a):\n    \"\"\"Free doc.\"\"\"\n    return a\n", "def free(a):\n    \"\"\"Free doc.\"\"\"\n    return a\n\n\nclass J:\n    def m2(self, x: int = 1) -> int:\n        \"\"\"M doc.\"\"\"\n        y = x + 1\n        return y\n")
    [report] = check_anchors(store)
    assert report.state is AnchorState.LOST and sorted(report.candidates) == ["code:src/x.py::J.m2", "code:src/x.py::K.m1"]
    (root / "src" / "x.py").write_text("def other():\n    return 0\n", encoding="utf-8")
    [report] = check_anchors(store)
    assert report.state is AnchorState.LOST and report.candidates == []


def test_errors_fail_the_command_and_alerts_do_not(world, capsys):
    root, store = world
    (root / "src" / "x.py").write_text("def broken(:\n", encoding="utf-8")
    assert cli_main(["anchors", "check", "--store", str(store)]) == 1
    assert "error: [anchors/unparseable]" in capsys.readouterr().out
    (root / "src" / "x.py").write_text(CODE, encoding="utf-8")
    api.save_document_payload(store, "CodeAnchorDoc", "m", {**record_anchor(root, REF), "ref": "nonsense", "claim": "x"})
    [report] = check_anchors(store)
    assert report.state is AnchorState.INVALID


def test_record_refuses_what_it_cannot_see(world):
    root, _store = world
    with pytest.raises(ValueError, match="invalid code reference"):
        record_anchor(root, "src/x.py::K")
    with pytest.raises(ValueError, match="no symbol"):
        record_anchor(root, "code:src/x.py::K.nope")
    assert record_anchor(root, "code:src/x.py::")["kind"] == "module"


def test_the_cli_records_and_writes_a_signed_theorem(world, capsys):
    root, store = world
    assert cli_main(["anchors", "record", "code:src/x.py::free", "--write", "anchors/free.md", "--claim", "free returns its argument", "--store", str(store)]) == 0
    text = (root / "anchors" / "free.md").read_text(encoding="utf-8")
    assert "authority: theorem" in text and "ref: code:src/x.py::free" in text and "free returns its argument" in text
    assert cli_main(["anchors", "check", "--store", str(store)]) == 0
    assert "2 checked" in capsys.readouterr().out


TSX = '/** A card. */\nexport function Card({ title }: { title: string }) {\n  return <div>{title}</div>;\n}\n\nexport const helper = (x: number) => x + 1;\n'
needs_ts = pytest.mark.skipif(not available(".tsx"), reason="tree-sitter-typescript not installed (extra [code])")


@pytest.fixture
def front(tmp_path):
    root = tmp_path / "front"
    (root / "src").mkdir(parents=True)
    (root / "src" / "Card.tsx").write_text(TSX, encoding="utf-8")
    (root / "src" / "util.js").write_text("/** Doubles. */\nexport function double(n) {\n  return n * 2;\n}\n", encoding="utf-8")
    store = api.init_store(root).store_path
    api.add_model(store, "sldb.models.code_anchor_doc:CodeAnchorDoc")
    recorded = record_anchor(root, "code:src/Card.tsx::Card")
    write_anchor(store, None, root / "anchors" / "card.md", recorded, "Card renders its title")
    yield root, store, recorded
    for name in [m for m in sys.modules if m.startswith("tmpdocs")]:
        del sys.modules[name]


@needs_ts
def test_a_tsx_component_anchor_is_intact_changed_reconnected_and_lost(front):
    root, store, recorded = front
    assert recorded["kind"] == "component" and recorded["recorded_with"].startswith("treesitter-symbols/1 (tree-sitter-typescript ") and recorded["recorded_with"].endswith(", tsx)")
    assert _state(store) == (AnchorState.INTACT, [])
    card = root / "src" / "Card.tsx"
    card.write_text(TSX.replace("<div>{title}</div>", "<section>{title}</section>"), encoding="utf-8")
    assert _state(store) == (AnchorState.CHANGED, ["body"])
    card.write_text(TSX.replace("function Card(", "function Tile("), encoding="utf-8")
    [report] = check_anchors(store)
    assert (report.state, report.to) == (AnchorState.RECONNECTED, "code:src/Card.tsx::Tile")
    card.write_text("export const helper = (x: number) => x + 1;\n", encoding="utf-8")
    [report] = check_anchors(store)
    assert report.state is AnchorState.LOST and report.candidates == []


@needs_ts
def test_a_js_function_anchor_records_and_stays_intact(front):
    root, store, _ = front
    recorded = record_anchor(root, "code:src/util.js::double")
    assert recorded["kind"] == "function" and recorded["recorded_with"].endswith(", tsx)") and record_anchor(root, "code:src/Card.tsx::")["kind"] == "module"
    write_anchor(store, None, root / "anchors" / "double.md", recorded, "double doubles")
    assert sorted(r.state.value for r in check_anchors(store)) == ["intact", "intact"]


def test_python_anchors_keep_their_recorded_with_and_ts_refs_parse(world):
    from sldb.models.code_ref import parse_code_ref

    root, _store = world
    assert record_anchor(root, REF)["recorded_with"].startswith("treesitter-symbols/1 (tree-sitter-python ") and record_anchor(root, REF)["recorded_with"].endswith(")")
    assert [parse_code_ref(f"code:a/b{ext}::X") for ext in (".ts", ".tsx", ".js", ".jsx", ".sql")] == [(f"a/b{ext}", "X") for ext in (".ts", ".tsx", ".js", ".jsx", ".sql")]
    assert parse_code_ref("code:a/b.css::X") is None


DDL = ("-- Accounts.\nCREATE TABLE IF NOT EXISTS public.users (\n    id bigserial PRIMARY KEY,\n    email text NOT NULL UNIQUE,\n    profile jsonb\n);\n\n"
       "CREATE TABLE orders (id serial, total numeric(10, 2), PRIMARY KEY (id));\n\n"
       "CREATE MATERIALIZED VIEW totals AS SELECT sum(total) AS total FROM orders;\n\nCREATE INDEX CONCURRENTLY orders_total_idx ON orders (total);\n")
needs_sql = pytest.mark.skipif(not available(".sql"), reason="tree-sitter-sql not installed (extra [code])")


@pytest.fixture
def db(tmp_path):
    root = tmp_path / "db"
    (root / "migrations").mkdir(parents=True)
    (root / "migrations" / "0001_initial.sql").write_text(DDL, encoding="utf-8")
    store = api.init_store(root).store_path
    api.add_model(store, "sldb.models.code_anchor_doc:CodeAnchorDoc")
    yield root, store
    for name in [m for m in sys.modules if m.startswith("tmpdocs")]:
        del sys.modules[name]


def _sql_anchor(db, symbol: str) -> dict:
    root, store = db
    recorded = record_anchor(root, f"code:migrations/0001_initial.sql::{symbol}")
    write_anchor(store, None, root / "anchors" / "a.md", recorded, f"{symbol} is in the schema")
    return recorded


def _rewrite(db, old: str, new: str) -> None:
    (db[0] / "migrations" / "0001_initial.sql").write_text(DDL.replace(old, new), encoding="utf-8")


@needs_sql
@pytest.mark.parametrize(("symbol", "kind", "edit", "rename", "to"), [
    ("public.users", "table", ("profile jsonb", "profile json"), ("public.users", "public.people"), "public.people"),
    ("public.users.email", "column", ("NOT NULL UNIQUE", "NOT NULL"), ("email text", "mail text"), "public.users.mail"),
])
def test_a_sql_table_and_column_anchor_are_intact_changed_reconnected_and_lost(db, symbol, kind, edit, rename, to):
    recorded = _sql_anchor(db, symbol)
    assert recorded["kind"] == kind and recorded["recorded_with"].startswith("treesitter-symbols/1 (tree-sitter-sql ") and recorded["recorded_with"].endswith(", sql)")
    assert _state(db[1]) == (AnchorState.INTACT, [])
    _rewrite(db, *edit)
    assert _state(db[1]) == (AnchorState.CHANGED, ["signature", "body"])
    _rewrite(db, *rename)
    [report] = check_anchors(db[1])
    assert (report.state, report.to) == (AnchorState.RECONNECTED, f"code:migrations/0001_initial.sql::{to}")
    _rewrite(db, DDL.split("\n\n")[0], "")
    [report] = check_anchors(db[1])
    assert report.state is AnchorState.LOST and report.candidates == []


@needs_sql
def test_sql_views_indexes_and_the_module_are_anchored_too(db):
    root, store = db
    assert [record_anchor(root, f"code:migrations/0001_initial.sql::{s}")["kind"] for s in ("totals", "orders_total_idx", "orders.total", "")] == ["view", "index", "column", "module"]
    with pytest.raises(ValueError, match="no symbol 'users'"):
        record_anchor(root, "code:migrations/0001_initial.sql::users")
    write_anchor(store, None, root / "anchors" / "v.md", record_anchor(root, "code:migrations/0001_initial.sql::totals"), "totals sums orders")
    assert [r.state.value for r in check_anchors(store)] == ["intact"]


@needs_sql
def test_anchors_on_a_django_sqlmigrate_migration_use_the_unquoted_names(tmp_path):
    root = tmp_path / "dj"
    shutil.copytree(Path(__file__).parent.parent / "fixtures" / "treesitter" / "sql" / "django", root / "m")
    store = api.init_store(root).store_path
    api.add_model(store, "sldb.models.code_anchor_doc:CodeAnchorDoc")
    kinds = [record_anchor(root, f"code:m/0001_initial.sql::{s}")["kind"] for s in ("app_book", "app_book.title", "app_book_author_id_980d3e25")]
    assert kinds == ["table", "column", "index"]
    write_anchor(store, None, root / "anchors" / "b.md", record_anchor(root, "code:m/0001_initial.sql::app_book.title"), "books have a title")
    assert [r.state.value for r in check_anchors(store)] == ["intact"]
    for name in [m for m in sys.modules if m.startswith("tmpdocs")]:
        del sys.modules[name]
