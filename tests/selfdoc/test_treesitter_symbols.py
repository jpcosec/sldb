"""The tree-sitter symbols scanner (ported from kimun): ids, kinds, spans, docstrings, signatures.
Skipped without the `[code]` extra."""
from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from sldb.code.runtime import available

pytestmark = pytest.mark.skipif(not available(), reason="tree-sitter runtime not installed (extra [code])")

SOURCE = '''"""Mod doc."""
import os, sys as s
from . import x
from ..a import b
from __future__ import annotations


@deco
async def top(a, b: int = 1, *rest, c="q"):
    """Top.

        Indented.
    """
    def inner(): pass


class K:
    "k doc"

    def m(self): pass

    class N:
        def d(self):
            # trailing comment
            return 1

# trailing comment after class
if True:
    def hidden(): pass
'''


@pytest.fixture
def facts(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "__init__.py").write_text("", encoding="utf-8")
    (tmp_path / "pkg" / "mod.py").write_text(SOURCE, encoding="utf-8")
    return {f["id"]: f for f in scan_tree(tmp_path)}


def test_ids_kinds_and_spans(facts):
    assert sorted(facts) == ["pkg", "pkg.mod", "pkg.mod.K", "pkg.mod.K.N", "pkg.mod.K.N.d", "pkg.mod.K.m", "pkg.mod.top", "pkg.mod.top.inner"]
    assert [facts[i]["kind"] for i in ("pkg.mod", "pkg.mod.top", "pkg.mod.top.inner", "pkg.mod.K", "pkg.mod.K.m")] == ["module", "function", "function", "class", "method"]
    assert facts["pkg.mod.top"]["span"] == {"start_line": 9, "end_line": 14}, "starts at `async def`, not at the decorator"
    assert facts["pkg.mod.top"]["attrs"]["native_kind"] == "AsyncFunctionDef"
    assert facts["pkg.mod.K.N.d"]["span"] == {"start_line": 23, "end_line": 25}, "a trailing comment is not part of the body"
    assert facts["pkg.mod.K"]["span"] == {"start_line": 17, "end_line": 25} and facts["pkg.mod"]["span"] == {"start_line": 1, "end_line": 29}
    assert "pkg.mod.hidden" not in facts, "a definition under `if` is not a symbol"


def test_docstrings_signatures_and_relations(facts):
    assert (facts["pkg.mod"]["doc"], facts["pkg.mod.top"]["doc"], facts["pkg.mod.K"]["doc"], facts["pkg.mod.K.m"]["doc"]) == ("Mod doc.", "Top.\n\nIndented.", "k doc", None)
    assert facts["pkg.mod.top"]["signature"] == "top(a, b: int=1, *rest, c='q')" and facts["pkg.mod.K"]["signature"] is None
    assert facts["pkg.mod.K.N.d"]["relations"] == [{"type": "contained-in", "target": "pkg.mod.K.N"}]
    assert [r["target"] for r in facts["pkg.mod"]["relations"]] == [".", "..a", "__future__", "os,sys"]
    assert facts["pkg.mod"]["source_hash"].startswith("sha256:") and facts["pkg"]["name"] == "pkg"


def test_nested_imports_are_a_separate_attr(facts, tmp_path):
    from sldb.code.scan import scan_tree

    assert facts["pkg.mod"]["attrs"]["imports"] == [".", "..a", "__future__", "os,sys"] and facts["pkg.mod"]["attrs"]["nested_imports"] == []
    (tmp_path / "lazy.py").write_text("import os\nif TYPE_CHECKING:\n    from a.b import C\ntry:\n    import json, sys as s\nexcept ImportError: pass\n"
                                      "class K:\n    def m(self):\n        from . import x\n        with ctx():\n            import os\n", encoding="utf-8")
    lazy = next(f for f in scan_tree(tmp_path) if f["id"] == "lazy")
    assert lazy["attrs"]["imports"] == ["os"] and [r["target"] for r in lazy["relations"]] == ["os"], "attrs.imports y facts.rels sin cambios"
    assert lazy["attrs"]["nested_imports"] == [".", "a.b", "json,sys", "os"]


def test_docstring_forms_and_duplicate_ids(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "docs.py").write_text('def a():\n    r"""raw \\d"""\ndef b():\n    "x\\ty" \'z\'\ndef c():\n    f"{1}"\ndef d():\n    b"bytes"\ndef e():\n    pass\n    "late"\n', encoding="utf-8")
    (tmp_path / "dup.py").write_text("def f(): pass\ndef f(): pass\n", encoding="utf-8")
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert [facts[f"docs.{n}"]["doc"] for n in "abcde"] == ["raw \\d", "x       yz", None, None, None]
    assert "dup.f" in facts and "dup.f~2" in facts


def test_without_the_runtime_the_error_names_the_extra(monkeypatch):
    import sldb.code.runtime as rt

    monkeypatch.setattr(rt, "_RUNTIME", {})
    monkeypatch.setattr(rt.importlib, "import_module", lambda name: (_ for _ in ()).throw(ImportError(name, name=name)))
    with pytest.raises(rt.TreeSitterUnavailable, match=r"\[code\]"):
        rt.runtime()
    assert not rt.available()


FRONTEND = Path(__file__).parent.parent / "fixtures" / "treesitter" / "frontend"
needs_ts = pytest.mark.skipif(not available(".ts"), reason="tree-sitter-typescript not installed (extra [code])")


@pytest.fixture
def ts_facts():
    from sldb.code.scan import scan_tree

    return {f["id"]: f for f in scan_tree(FRONTEND)}


@needs_ts
def test_ts_kinds_names_and_top_level_only(ts_facts):
    app = {i.removeprefix("src.App."): f["kind"] for i, f in ts_facts.items() if i.startswith("src.App.")}
    assert app == {"App": "component", "Button": "component", "ButtonProps": "type", "Card": "component", "Mode": "type",
                   "NotComponent": "function", "helper": "function", "useCounter": "hook"}, "no reexport, no nested `inner`"
    assert (ts_facts["src.useToggle.useToggle"]["kind"], ts_facts["src.useToggle.Pair"]["kind"]) == ("hook", "type")
    assert (ts_facts["src.util.double"]["kind"], ts_facts["src.Panel.Panel"]["kind"]) == ("function", "component")
    assert ts_facts["src.App"]["kind"] == "module" and ts_facts["src.App"]["qualified_name"] == "src.App" and ts_facts["src.App.Button"]["qualified_name"] == "Button"
    assert ts_facts["src.App.Button"]["relations"] == [{"type": "contained-in", "target": "src.App"}]


@needs_ts
def test_ts_jsdoc_signature_span_and_imports(ts_facts):
    assert ts_facts["src.App.Button"]["doc"] == "A button.\n\n  Indented.", "the last of two JSDoc blocks"
    assert (ts_facts["src.App.ButtonProps"]["doc"], ts_facts["src.App.Card"]["doc"], ts_facts["src.util.double"]["doc"]) == ("Props of a button.", None, "Doubles a number.")
    assert ts_facts["src.App.Button"]["signature"] == "Button({ label }: ButtonProps)" and ts_facts["src.App.helper"]["signature"] == "helper(x)"
    assert ts_facts["src.App.Mode"]["signature"] is None and ts_facts["src.App.Button"]["span"] == {"start_line": 16, "end_line": 21}
    assert ts_facts["src.App"]["attrs"]["imports"] == ["./app.css", "react"] and [r["target"] for r in ts_facts["src.Panel"]["relations"]] == ["./util"]
    assert all(set(f["fingerprints"]) == {"signature", "shape", "docstring", "body"} for f in ts_facts.values())


@needs_ts
def test_ts_types_only_in_ts_and_same_module_names_take_a_suffix(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "a.ts").write_text("export const f = () => 1;\n", encoding="utf-8")
    (tmp_path / "a.js").write_text("type T = number;\nfunction g() {}\n", encoding="utf-8")
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert sorted(facts) == ["a", "a.f", "a.g", "a~2"] and (facts["a"]["path"], facts["a~2"]["path"]) == ("a.js", "a.ts")


def test_without_the_ts_grammar_python_still_scans(monkeypatch, tmp_path):
    import sldb.code.runtime as rt
    from sldb.code.scan import scan_tree

    real = rt.importlib.import_module
    monkeypatch.setattr(rt, "_RUNTIME", {})
    monkeypatch.setattr(rt.importlib, "import_module", lambda name: (_ for _ in ()).throw(ImportError(name, name=name)) if name == "tree_sitter_typescript" else real(name))
    shutil.copytree(FRONTEND, tmp_path / "front")
    (tmp_path / "front" / "m.py").write_text("def f(): pass\n", encoding="utf-8")
    assert not rt.available(".tsx") and sorted(f["id"] for f in scan_tree(tmp_path / "front")) == ["m", "m.f"]


SQL = Path(__file__).parent.parent / "fixtures" / "treesitter" / "sql"
needs_sql = pytest.mark.skipif(not available(".sql"), reason="tree-sitter-sql not installed (extra [code])")


@pytest.fixture
def sql_facts():
    from sldb.code.scan import scan_tree

    return {f["id"].removeprefix("migrations.0001_initial."): f for f in scan_tree(SQL) if f["path"].startswith("migrations/")}


@needs_sql
def test_sql_tables_columns_views_and_index_of_a_postgres_migration(sql_facts):
    kinds = {i: f["kind"] for i, f in sql_facts.items()}
    assert kinds == {"migrations.0001_initial": "module", "public.users": "table", "public.users.id": "column", "public.users.email": "column",
                     "public.users.profile": "column", "public.users.created_at": "column", "orders": "table", "orders.id": "column",
                     "orders.user_id": "column", "orders.total": "column", "active_users": "view", "order_totals": "view", "orders_user_idx": "index"}, "constraints are not columns"
    users, email = sql_facts["public.users"], sql_facts["public.users.email"]
    assert (users["name"], users["qualified_name"], email["name"], email["qualified_name"]) == ("users", "public.users", "email", "public.users.email")
    assert sql_facts["orders"]["qualified_name"] == "orders" and sql_facts["migrations.0001_initial"]["qualified_name"] == "migrations.0001_initial"
    assert email["relations"] == [{"type": "contained-in", "target": "migrations.0001_initial.public.users"}]
    assert (sql_facts["order_totals"]["attrs"]["native_kind"], sql_facts["active_users"]["attrs"]["native_kind"]) == ("create_materialized_view", "create_view")


@needs_sql
def test_sql_comments_signatures_spans_and_imports(sql_facts):
    assert sql_facts["public.users"]["doc"] == "Accounts of the app.\nOne row per person.", "contiguous -- lines, not the one after a blank line"
    assert (sql_facts["orders"]["doc"], sql_facts["public.users.email"]["doc"], sql_facts["order_totals"]["doc"]) == (None, None, "Totals per user, refreshed nightly.")
    assert sql_facts["public.users.email"]["signature"] == "email text NOT NULL UNIQUE" and sql_facts["public.users"]["span"] == {"start_line": 5, "end_line": 10}
    assert sql_facts["orders_user_idx"]["signature"] == "CREATE INDEX CONCURRENTLY orders_user_idx ON orders (user_id)"
    assert sql_facts["migrations.0001_initial"]["attrs"]["imports"] == [] and sql_facts["migrations.0001_initial"]["relations"] == []
    assert all(set(f["fingerprints"]) == {"signature", "shape", "docstring", "body"} for f in sql_facts.values())


@needs_sql
def test_sql_repeated_objects_take_a_suffix_and_a_statement_with_errors_keeps_what_reads(tmp_path):
    from sldb.code.scan import scan_tree

    (tmp_path / "m.sql").write_text('CREATE TABLE t (a int);\nCREATE TABLE "t" (a int, b int);\n'
                                    "CREATE TABLE bad (a int GENERATED BY DEFAULT AS IDENTITY, b int, CONSTRAINT k UNIQUE (a));\n"
                                    'CREATE TABLE (z int);\nCREATE INDEX i ON t (a);\nCREATE INDEX "i" ON t (b);\n', encoding="utf-8")
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert sorted(facts) == ["m", "m.bad", "m.bad.b", "m.i", "m.i~2", "m.t", "m.t.a", "m.t~2", "m.t~2.a", "m.t~2.b"], "no column with an error, nothing of a nameless table"
    assert (facts["m.t~2"]["qualified_name"], facts["m.t~2.b"]["qualified_name"], facts["m.i~2"]["qualified_name"]) == ("t~2", "t~2.b", "i~2"), '"t" is t'
    (tmp_path / "n.sql").write_text("CREATE TABLE (z int);\n", encoding="utf-8")
    modules = {f["id"]: f["attrs"] for f in scan_tree(tmp_path) if f["kind"] == "module"}
    assert [(modules[m]["has_error"], modules[m]["parse_errors"]) for m in ("m", "n")] == [(False, True), (True, True)], "unparseable only when nothing reads"


DJANGO = {"app_author": "table", "app_author.name": "column", "app_author.profile": "column", "app_author.created_at": "column",
          "app_book": "table", "app_book.title": "column", "app_book.pages": "column", "app_book.slug": "column", "app_book.author_id": "column",
          "app_book_slug_780ddf03_like": "index", "app_book_author_id_980d3e25": "index", "app_book_title_idx": "index"}


@needs_sql
def test_a_django_sqlmigrate_migration_gives_its_tables_columns_and_indexes():
    from sldb.code.scan import scan_file

    facts = {f["qualified_name"]: f for f in scan_file("django/0001_initial.sql", SQL)[1:]}
    assert {q: f["kind"] for q, f in facts.items()} == DJANGO, "inside BEGIN/COMMIT, unquoted; the IDENTITY id columns are left out"
    assert (facts["app_book"]["doc"], facts["app_book"]["name"], facts["app_book.slug"]["name"]) == ("Create model Book", "app_book", "slug")
    assert facts["app_book.author_id"]["relations"] == [{"type": "contained-in", "target": "django.0001_initial.app_book"}]
    assert facts["app_book_author_id_980d3e25"]["signature"] == 'CREATE INDEX "app_book_author_id_980d3e25" ON "app_book" ("author_id")'


def test_without_the_sql_grammar_sql_files_are_not_scanned(monkeypatch, tmp_path):
    import sldb.code.runtime as rt
    from sldb.code.scan import scan_tree

    real = rt.importlib.import_module
    monkeypatch.setattr(rt, "_RUNTIME", {})
    monkeypatch.setattr(rt.importlib, "import_module", lambda name: (_ for _ in ()).throw(ImportError(name, name=name)) if name == "tree_sitter_sql" else real(name))
    shutil.copytree(SQL, tmp_path / "db")
    (tmp_path / "db" / "m.py").write_text("def f(): pass\n", encoding="utf-8")
    assert not rt.available(".sql") and sorted(f["id"] for f in scan_tree(tmp_path / "db")) == ["m", "m.f"]
