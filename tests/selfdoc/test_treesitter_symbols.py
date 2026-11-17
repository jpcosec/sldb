"""The tree-sitter symbols scanner (ported from kimun): ids, kinds, spans, docstrings, signatures.
Skipped without the `[code]` extra."""
from __future__ import annotations

import importlib.util
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


needs_pg = pytest.mark.skipif(not available(".sql") or importlib.util.find_spec("pglast") is None, reason="pglast not installed (extra [postgres])")


@pytest.fixture
def no_pg(monkeypatch):
    """The reading without the extra [postgres], whether pglast is installed or not."""
    import sldb.code.sql_pg as sql_pg

    monkeypatch.setattr(sql_pg, "_pg", None)


@pytest.fixture
def sql_facts():
    from sldb.code.scan import scan_tree

    return {f["id"].removeprefix("migrations.0001_initial."): f for f in scan_tree(SQL) if f["path"].startswith("migrations/")}


def _scan(tmp_path, sql, name="k"):
    from sldb.code.scan import scan_tree

    (tmp_path / f"{name}.sql").write_text(sql, encoding="utf-8")
    return {f["id"]: f for f in scan_tree(tmp_path)}


def _keys(facts):
    return {i: (f["attrs"]["constraint_type"], f["attrs"]["columns"], f["attrs"].get("references")) for i, f in facts.items() if f["kind"] == "constraint"}


MIGRATION = {"migrations.0001_initial": "module", "public.users": "table", "public.users.id": "column", "public.users.email": "column",
             "public.users.profile": "column", "public.users.created_at": "column", "orders": "table", "orders.id": "column",
             "orders.user_id": "column", "orders.total": "column", "active_users": "view", "order_totals": "view", "orders_user_idx": "index"}


@needs_sql
def test_sql_tables_columns_views_and_index_of_a_postgres_migration(no_pg, sql_facts):
    assert {i: f["kind"] for i, f in sql_facts.items()} == MIGRATION, "without the extra: constraints are not columns, and no keys"
    users, email = sql_facts["public.users"], sql_facts["public.users.email"]
    assert (users["name"], users["qualified_name"], email["name"], email["qualified_name"]) == ("users", "public.users", "email", "public.users.email")
    assert sql_facts["orders"]["qualified_name"] == "orders" and sql_facts["migrations.0001_initial"]["qualified_name"] == "migrations.0001_initial"
    assert email["relations"] == [{"type": "contained-in", "target": "migrations.0001_initial.public.users"}]
    assert (sql_facts["order_totals"]["attrs"]["native_kind"], sql_facts["active_users"]["attrs"]["native_kind"]) == ("create_materialized_view", "create_view")
    assert all(set(f["attrs"]) <= {"native_kind", "module", "imports", "nested_imports", "has_error", "parse_errors"} for f in sql_facts.values()), "no keys_partial: no ERROR"


@needs_pg
def test_with_pglast_a_postgres_migration_also_gives_its_keys(sql_facts):
    keys = {"orders.pk": "constraint", "orders.fk": "constraint", "orders.unique": "constraint"}
    assert {i: f["kind"] for i, f in sql_facts.items()} == MIGRATION | keys, "table constraints are keys, not columns"
    assert not any("keys_partial" in f["attrs"] for f in sql_facts.values())


@needs_pg
def test_sql_unnamed_table_keys_and_the_keys_written_in_a_column(sql_facts):
    fk, pk, uniq = sql_facts["orders.fk"], sql_facts["orders.pk"], sql_facts["orders.unique"]
    assert [(k["name"], k["qualified_name"], k["attrs"]["constraint_type"], k["attrs"]["columns"]) for k in (pk, fk, uniq)] == [
        ("pk", "orders.pk", "primary_key", ["id"]), ("fk", "orders.fk", "foreign_key", ["user_id"]), ("unique", "orders.unique", "unique", ["user_id", "id"])]
    assert fk["attrs"]["references"] == {"table": "public.users", "columns": ["id"]} and "references" not in pk["attrs"]
    assert fk["relations"] == [{"type": "contained-in", "target": "migrations.0001_initial.orders"}, {"type": "references", "target": "migrations.0001_initial.public.users"}]
    assert (fk["signature"], fk["span"], fk["attrs"]["native_kind"]) == ("FOREIGN KEY (user_id) REFERENCES public.users (id)", {"start_line": 17, "end_line": 17}, "Constraint")
    users_id, email, user_id = (sql_facts[c]["attrs"] for c in ("public.users.id", "public.users.email", "orders.user_id"))
    assert (users_id["type"], users_id.get("primary_key"), email.get("unique"), email.get("primary_key"), user_id["type"]) == ("bigserial", True, True, None, "bigint")
    assert not any("parse_partial" in a or "identity" in a or "primary_key" in a for a in (email, user_id)), "a REFERENCES in a column is no key mark"
    assert user_id["references"] == {"table": "public.users", "columns": ["id"]} and "orders.user_id" not in {f["qualified_name"] for f in sql_facts.values() if f["kind"] == "constraint"}


@needs_sql
def test_sql_comments_signatures_spans_and_imports(sql_facts):
    assert sql_facts["public.users"]["doc"] == "Accounts of the app.\nOne row per person.", "contiguous -- lines, not the one after a blank line"
    assert (sql_facts["orders"]["doc"], sql_facts["public.users.email"]["doc"], sql_facts["order_totals"]["doc"]) == (None, None, "Totals per user, refreshed nightly.")
    assert sql_facts["public.users.email"]["signature"] == "email text NOT NULL UNIQUE" and sql_facts["public.users"]["span"] == {"start_line": 5, "end_line": 10}
    assert sql_facts["orders_user_idx"]["signature"] == "CREATE INDEX CONCURRENTLY orders_user_idx ON orders (user_id)"
    assert sql_facts["migrations.0001_initial"]["attrs"]["imports"] == [] and sql_facts["migrations.0001_initial"]["relations"] == []
    assert all(set(f["fingerprints"]) == {"signature", "shape", "docstring", "body"} for f in sql_facts.values())


BAD = ('CREATE TABLE t (a int);\nCREATE TABLE "t" (a int, b int);\n'
       "CREATE TABLE bad (a int GENERATED BY DEFAULT AS IDENTITY, b int, CONSTRAINT k UNIQUE (a));\n"
       'CREATE TABLE (z int);\nCREATE INDEX i ON t (a);\nCREATE INDEX "i" ON t (b);\n')


@needs_sql
def test_sql_repeated_objects_take_a_suffix_and_a_statement_with_errors_keeps_what_reads(no_pg, tmp_path):
    facts = _scan(tmp_path, BAD, "m")
    assert sorted(facts) == ["m", "m.bad", "m.bad.b", "m.i", "m.i~2", "m.t", "m.t.a", "m.t~2", "m.t~2.a", "m.t~2.b"], "no column with an error, nothing of a nameless table"
    assert (facts["m.t~2"]["qualified_name"], facts["m.t~2.b"]["qualified_name"], facts["m.i~2"]["qualified_name"]) == ("t~2", "t~2.b", "i~2"), '"t" is t'
    assert [facts[t]["attrs"].get("keys_partial") for t in ("m.bad", "m.t", "m.t~2")] == [True, None, None], "only the statement with an ERROR"
    modules = {f["id"]: f["attrs"] for f in _scan(tmp_path, "CREATE TABLE (z int);\n", "n").values() if f["kind"] == "module"}
    assert [(modules[m]["has_error"], modules[m]["parse_errors"]) for m in ("m", "n")] == [(False, True), (True, True)], "unparseable only when nothing reads"


@needs_pg
def test_with_pglast_a_column_the_grammar_does_not_parse_is_read_and_its_keys_too(tmp_path):
    facts = _scan(tmp_path, BAD, "m")
    assert sorted(facts) == ["m", "m.bad", "m.bad.a", "m.bad.b", "m.bad.k", "m.i", "m.i~2", "m.t", "m.t.a", "m.t~2", "m.t~2.a", "m.t~2.b"], "nothing of a nameless table"
    assert facts["m.bad.a"]["attrs"] | {"module": None} == {"native_kind": "ColumnDef", "module": None, "type": "int", "identity": True, "parse_partial": True}
    assert (facts["m.bad.a"]["signature"], facts["m.bad.a"]["span"]) == ("a int GENERATED BY DEFAULT AS IDENTITY", {"start_line": 3, "end_line": 3})
    assert _keys(facts) == {"m.bad.k": ("unique", ["a"], None)} and "keys_partial" not in facts["m.bad"]["attrs"], "Postgres parsed it: the keys are whole"


DJANGO = {"app_author": "table", "app_author.name": "column", "app_author.profile": "column", "app_author.created_at": "column",
          "app_book": "table", "app_book.title": "column", "app_book.pages": "column", "app_book.slug": "column", "app_book.author_id": "column",
          "app_book_slug_780ddf03_like": "index", "app_book_author_id_980d3e25": "index", "app_book_title_idx": "index"}
DJANGO_KEYS = {"app_author.id": "column", "app_book.id": "column", "app_book.slug_pages_uniq": "constraint",
               "app_book.app_book_title_author_id_f24131bb_uniq": "constraint", "app_book.app_book_author_id_980d3e25_fk_app_author_id": "constraint"}


def _django(name="0001_initial"):
    from sldb.code.scan import scan_file

    return {f["qualified_name"]: f for f in scan_file(f"django/{name}.sql", SQL)[1:]}


@needs_sql
def test_a_django_sqlmigrate_migration_gives_its_tables_columns_and_indexes(no_pg):
    facts = _django()
    assert {q: f["kind"] for q, f in facts.items()} == DJANGO, "inside BEGIN/COMMIT, unquoted; without the extra the IDENTITY id columns are left out"
    assert (facts["app_book"]["doc"], facts["app_book"]["name"], facts["app_book.slug"]["name"]) == ("Create model Book", "app_book", "slug")
    assert facts["app_book.author_id"]["relations"] == [{"type": "contained-in", "target": "django.0001_initial.app_book"}]
    assert facts["app_book_author_id_980d3e25"]["signature"] == 'CREATE INDEX "app_book_author_id_980d3e25" ON "app_book" ("author_id")'
    assert [facts[t]["attrs"].get("keys_partial") for t in ("app_author", "app_book")] == [True, True], "their statements have ERROR nodes"
    assert facts["app_book.slug"]["attrs"] == {"native_kind": "column_definition", "module": "django.0001_initial"}, "no column attributes"


@needs_pg
def test_a_django_migration_gives_the_identity_primary_key_and_the_keys_of_alter_table():
    facts = _django()
    assert {q: f["kind"] for q, f in facts.items()} == DJANGO | DJANGO_KEYS and not any("keys_partial" in f["attrs"] for f in facts.values())
    ident = facts["app_book.id"]
    assert ident["attrs"] | {"module": None} == {"native_kind": "ColumnDef", "module": None, "type": "bigint", "primary_key": True, "identity": True, "parse_partial": True}
    assert ident["relations"] == [{"type": "contained-in", "target": "django.0001_initial.app_book"}] and ident["name"] == "id"
    assert (facts["app_book.slug"]["attrs"].get("unique"), facts["app_book.pages"]["attrs"]["type"], facts["app_author.created_at"]["attrs"]["type"]) == (True, "integer", "timestamp with time zone")
    fk = facts["app_book.app_book_author_id_980d3e25_fk_app_author_id"]
    assert (fk["kind"], fk["name"], fk["attrs"]["native_kind"], fk["attrs"]["constraint_type"], fk["attrs"]["columns"]) == (
        "constraint", "app_book_author_id_980d3e25_fk_app_author_id", "Constraint", "foreign_key", ["author_id"])
    assert fk["attrs"]["references"] == {"table": "app_author", "columns": ["id"]}
    assert fk["relations"] == [{"type": "contained-in", "target": "django.0001_initial.app_book"}, {"type": "references", "target": "django.0001_initial.app_author"}]
    uniq = [facts[f"app_book.{n}"]["attrs"] for n in ("app_book_title_author_id_f24131bb_uniq", "slug_pages_uniq")]
    assert [(u["constraint_type"], u["columns"]) for u in uniq] == [("unique", ["title", "author_id"]), ("unique", ["slug", "pages"])], "a UniqueConstraint before a CheckConstraint"


@needs_pg
def test_a_foreign_key_to_a_table_of_another_migration_has_references_but_no_relation():
    facts = _django("blog_0001_initial")
    fk = facts["posts.posts_author_id_099b8aca_fk_auth_user_id"]
    assert fk["attrs"]["references"] == {"table": "auth_user", "columns": ["id"]}, "IR's blog fixture: auth_user lives in another app"
    assert fk["relations"] == [{"type": "contained-in", "target": "django.blog_0001_initial.posts"}]
    assert (facts["posts.id"]["attrs"]["primary_key"], facts["posts.published_at"]["attrs"]["type"]) == (True, "timestamp with time zone")


SHOP = '''BEGIN;
CREATE TABLE "shop_category" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "name" varchar(50) NOT NULL UNIQUE);
CREATE TABLE "shop_tag" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "label" varchar(20) NOT NULL);
CREATE TABLE "shop_product" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "sku" varchar(20) NOT NULL, "region" varchar(5) NOT NULL, "price" numeric(8, 2) NOT NULL, "category_id" bigint NOT NULL, "owner_id" integer NULL, CONSTRAINT "uniq_cat_sku" UNIQUE ("category_id", "sku"), CONSTRAINT "price_pos" CHECK ("price" >= 0));
CREATE TABLE "shop_product_tags" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "product_id" bigint NOT NULL, "tag_id" bigint NOT NULL);
ALTER TABLE "shop_product" ADD CONSTRAINT "shop_product_sku_region_4470a054_uniq" UNIQUE ("sku", "region");
ALTER TABLE "shop_product" ADD CONSTRAINT "shop_product_category_id_14d7eea8_fk_shop_category_id" FOREIGN KEY ("category_id") REFERENCES "shop_category" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "shop_product" ADD CONSTRAINT "shop_product_owner_id_c7c481d9_fk_auth_user_id" FOREIGN KEY ("owner_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "shop_product_tags" ADD CONSTRAINT "shop_product_tags_product_id_tag_id_a244154e_uniq" UNIQUE ("product_id", "tag_id");
ALTER TABLE "shop_product_tags" ADD CONSTRAINT "shop_product_tags_product_id_9a158885_fk_shop_product_id" FOREIGN KEY ("product_id") REFERENCES "shop_product" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "shop_product_tags" ADD CONSTRAINT "shop_product_tags_tag_id_dd30c4fb_fk_shop_tag_id" FOREIGN KEY ("tag_id") REFERENCES "shop_tag" ("id") DEFERRABLE INITIALLY DEFERRED;
COMMIT;
'''


@needs_pg
def test_a_real_sqlmigrate_migration_unique_then_check_m2m_and_deferrable_foreign_keys(tmp_path):
    facts = _scan(tmp_path, SHOP, "s")
    p, t = "s.shop_product.", "s.shop_product_tags."
    assert _keys(facts) == {
        p + "uniq_cat_sku": ("unique", ["category_id", "sku"], None), p + "shop_product_sku_region_4470a054_uniq": ("unique", ["sku", "region"], None),
        p + "shop_product_category_id_14d7eea8_fk_shop_category_id": ("foreign_key", ["category_id"], {"table": "shop_category", "columns": ["id"]}),
        p + "shop_product_owner_id_c7c481d9_fk_auth_user_id": ("foreign_key", ["owner_id"], {"table": "auth_user", "columns": ["id"]}),
        t + "shop_product_tags_product_id_tag_id_a244154e_uniq": ("unique", ["product_id", "tag_id"], None),
        t + "shop_product_tags_product_id_9a158885_fk_shop_product_id": ("foreign_key", ["product_id"], {"table": "shop_product", "columns": ["id"]}),
        t + "shop_product_tags_tag_id_dd30c4fb_fk_shop_tag_id": ("foreign_key", ["tag_id"], {"table": "shop_tag", "columns": ["id"]})}, "the UNIQUE before a CHECK; no fact for the CHECK"
    assert all(facts[f"s.{tb}.id"]["attrs"]["primary_key"] and facts[f"s.{tb}.id"]["attrs"]["identity"] for tb in ("shop_category", "shop_tag", "shop_product", "shop_product_tags"))
    assert (facts["s.shop_category.name"]["attrs"].get("unique"), facts[p + "price"]["attrs"]["type"]) == (True, "numeric(8, 2)")
    assert [r["target"] for r in facts[p + "shop_product_owner_id_c7c481d9_fk_auth_user_id"]["relations"]] == ["s.shop_product"]


@needs_pg
def test_keys_of_alter_table_unnamed_repeated_and_out_of_scope(tmp_path):
    facts = _scan(tmp_path, "ALTER TABLE z ADD CONSTRAINT zf FOREIGN KEY (a) REFERENCES t (a);\n"
                            "CREATE TABLE t (a int UNIQUE, b int, c int DEFAULT 'primary key', UNIQUE (a), UNIQUE (b), FOREIGN KEY (c) REFERENCES t (a));\n"
                            "ALTER TABLE t ADD CONSTRAINT tp PRIMARY KEY (a, b);\nALTER TABLE t ADD PRIMARY KEY (a);\nALTER TABLE t ADD COLUMN d int;\n"
                            "ALTER TABLE t ADD CONSTRAINT tc CHECK (a > 0);\nALTER INDEX t_idx RENAME TO u_idx;\n")
    assert sorted(_keys(facts)) == ["k.t.fk", "k.t.pk", "k.t.tp", "k.t.unique", "k.t.unique~2", "k.z.zf"], "ADD COLUMN, CHECK, ALTER INDEX: no fact"
    assert [facts[i]["attrs"]["columns"] for i in ("k.t.unique", "k.t.unique~2", "k.t.pk")] == [["a"], ["b"], ["a"]], "~2 in source order; ADD without a name is a key too"
    assert facts["k.z.zf"]["relations"] == [{"type": "contained-in", "target": "k"}, {"type": "references", "target": "k.t"}], "the table after it still counts"
    assert facts["k.t.tp"]["relations"] == [{"type": "contained-in", "target": "k.t"}] and facts["k.t.tp"]["attrs"]["columns"] == ["a", "b"]
    assert (facts["k.t.a"]["attrs"].get("unique"), "primary_key" in facts["k.t.c"]["attrs"]) == (True, False), "a quoted literal is no key"


EDGE = '''CREATE TABLE public.parent (id integer NOT NULL, code text, CONSTRAINT parent_pkey PRIMARY KEY (id));
CREATE TABLE "My Schema"."Child Table" ("Id" integer, "parent id" integer, note text -- primary key unique
, tag text CHECK (tag <> 'primary key unique'), PRIMARY KEY ("Id"), UNIQUE (note), UNIQUE (tag));
ALTER TABLE ONLY public.parent ADD CONSTRAINT parent_code_key UNIQUE (code);
ALTER TABLE IF EXISTS "My Schema"."Child Table" ADD CONSTRAINT "child→parent fk" FOREIGN KEY ("parent id") REFERENCES public.parent (id) ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED;
alter table public.parent add constraint parent_self_fk foreign key (code) references public.parent;
ALTER TABLE public.parent ADD CONSTRAINT a_uniq UNIQUE (id), ADD CONSTRAINT b_uniq UNIQUE (code);
ALTER TABLE public.parent ADD CONSTRAINT chk CHECK (id > 0);
ALTER TABLE ghost ADD CONSTRAINT ghost_fk FOREIGN KEY (x) REFERENCES public.parent (id);
CREATE TABLE odd ("a)b" int, "c,d" int, UNIQUE ("a)b"), FOREIGN KEY ("a)b", "c,d") REFERENCES odd ("c,d", "a)b"));
CREATE TABLE weird (id int, "unique" int, "primary key" int);
'''


@needs_pg
def test_the_first_testers_edges_quotes_schemas_only_if_exists_lower_case_and_several_adds(tmp_path):
    facts, child, par = _scan(tmp_path, EDGE, "e"), "e.My Schema.Child Table.", "e.public.parent."
    keys = _keys(facts)
    assert keys[child + "child→parent fk"] == ("foreign_key", ["parent id"], {"table": "public.parent", "columns": ["id"]})
    assert (keys[child + "pk"], keys[child + "unique"], keys[child + "unique~2"]) == (("primary_key", ["Id"], None), ("unique", ["note"], None), ("unique", ["tag"], None))
    assert [keys[par + k][:2] for k in ("parent_pkey", "parent_code_key", "a_uniq", "b_uniq")] == [("primary_key", ["id"]), ("unique", ["code"]), ("unique", ["id"]), ("unique", ["code"])]
    assert keys[par + "parent_self_fk"] == ("foreign_key", ["code"], {"table": "public.parent", "columns": []}), "no referenced columns: the primary key"
    assert {"type": "references", "target": "e.public.parent"} in facts[par + "parent_self_fk"]["relations"] and "e.ghost.ghost_fk" in keys
    assert keys["e.odd.unique"][1] == ["a)b"] and keys["e.odd.fk"][1:] == (["a)b", "c,d"], {"table": "odd", "columns": ["c,d", "a)b"]})
    assert [set(facts[f"e.weird.{c}"]["attrs"]) - {"native_kind", "module"} for c in ("unique", "primary key")] == [{"type"}, {"type"}], "a quoted name is no key"
    assert facts[child + "note"]["attrs"]["type"] == "text" and "unique" not in facts[child + "tag"]["attrs"], "neither a comment nor a literal is a key"


@needs_pg
def test_a_table_foreign_key_without_referenced_columns_named_or_not_last_or_not(tmp_path):
    facts = _scan(tmp_path, "CREATE TABLE t (id int PRIMARY KEY);\nCREATE TABLE d (id int, FOREIGN KEY (id) REFERENCES t);\n"
                            "CREATE TABLE f2 (id int, FOREIGN KEY (id) REFERENCES t ON DELETE CASCADE, PRIMARY KEY (id));\n"
                            "CREATE TABLE a3 (id int, x int, CONSTRAINT a3_fk FOREIGN KEY (x) REFERENCES t ON DELETE CASCADE, UNIQUE (id));\n"
                            "CREATE TABLE a5 (id int, x int, CONSTRAINT a5_fk FOREIGN KEY (x) REFERENCES t);\n"
                            "CREATE TABLE a6 (id int, x int, CONSTRAINT a6_fk FOREIGN KEY (x) REFERENCES public.t);\n"
                            "CREATE TABLE e (id int, CONSTRAINT e_fk FOREIGN KEY (id) REFERENCES t, CONSTRAINT e_u UNIQUE (id));\n"
                            "CREATE TABLE a8 (id int, x int, CONSTRAINT a8_fk FOREIGN KEY (x) REFERENCES t (id), CONSTRAINT a8_c CHECK (x > 0));\n", "a")
    to_pk = {"table": "t", "columns": []}
    assert _keys(facts) == {"a.d.fk": ("foreign_key", ["id"], to_pk), "a.f2.fk": ("foreign_key", ["id"], to_pk), "a.f2.pk": ("primary_key", ["id"], None),
                            "a.a3.a3_fk": ("foreign_key", ["x"], to_pk), "a.a3.unique": ("unique", ["id"], None), "a.a5.a5_fk": ("foreign_key", ["x"], to_pk),
                            "a.a6.a6_fk": ("foreign_key", ["x"], {"table": "public.t", "columns": []}), "a.e.e_fk": ("foreign_key", ["id"], to_pk),
                            "a.e.e_u": ("unique", ["id"], None), "a.a8.a8_fk": ("foreign_key", ["x"], {"table": "t", "columns": ["id"]})}
    assert {"type": "references", "target": "a.t"} in facts["a.a5.a5_fk"]["relations"] and [r["type"] for r in facts["a.a6.a6_fk"]["relations"]] == ["contained-in"], "public.t is not t"


@needs_pg
def test_escaped_double_quotes_in_table_constraint_and_column_names(tmp_path):
    facts = {f["qualified_name"]: f for f in _scan(tmp_path, 'CREATE TABLE "p""q" ("i""d" int NOT NULL, code text, CONSTRAINT "p""k" PRIMARY KEY ("i""d"), UNIQUE ("a""b", code));\n'
                                                         'CREATE TABLE c (code text, "c""1" int);\nALTER TABLE c ADD CONSTRAINT "g""h" FOREIGN KEY (code) REFERENCES "p""q" ("i""d");\n'
                                                         'ALTER TABLE "p""q" ADD CONSTRAINT "z""fk" UNIQUE (code);\n', "b").values()}
    assert (facts['p"q.i"d']["attrs"]["type"], facts['c.c"1']["attrs"]["type"], facts['p"q.p"k']["attrs"]["columns"]) == ("int", "int", ['i"d']), '"a""b" is a"b'
    assert (facts['p"q.unique']["attrs"]["columns"], facts['c.g"h']["name"]) == (['a"b', "code"], 'g"h')
    assert facts['c.g"h']["attrs"]["references"] == {"table": 'p"q', "columns": ['i"d']} and {"type": "references", "target": 'b.p"q'} in facts['c.g"h']["relations"]
    assert facts['p"q.z"fk']["relations"] == [{"type": "contained-in", "target": 'b.p"q'}], "an ALTER TABLE on a name with \"\" too"


@needs_pg
def test_a_references_written_in_a_column_marks_the_column_and_gives_no_key(tmp_path):
    facts = _scan(tmp_path, 'CREATE TABLE t (id int PRIMARY KEY);\nCREATE TABLE c (a int REFERENCES t (id), b int REFERENCES t, z int, w int NOT NULL REFERENCES "public"."t"("id"));\n', "c")
    assert [facts[c]["attrs"].get("references") for c in ("c.c.a", "c.c.b", "c.c.z", "c.c.w")] == [
        {"table": "t", "columns": ["id"]}, {"table": "t", "columns": []}, None, {"table": "public.t", "columns": ["id"]}]
    assert not _keys(facts) and {"type": "references", "target": "c.t"} in facts["c.c.b"]["relations"]
    assert (facts["c.c.a"]["attrs"]["type"], facts["c.c.w"]["attrs"]["type"]) == ("int", "int")


@needs_pg
def test_unnamed_keys_count_their_suffix_per_type_within_their_table(tmp_path):
    keys = _keys(_scan(tmp_path, "CREATE TABLE t (a int, b int, UNIQUE (a), FOREIGN KEY (a) REFERENCES t (b), UNIQUE (b), FOREIGN KEY (b) REFERENCES t (a), PRIMARY KEY (a));\n"
                                 "CREATE TABLE u (a int, FOREIGN KEY (a) REFERENCES t (a), UNIQUE (a));\n", "d"))
    assert {i: k[1] for i, k in keys.items()} == {"d.t.unique": ["a"], "d.t.fk": ["a"], "d.t.unique~2": ["b"], "d.t.fk~2": ["b"], "d.t.pk": ["a"], "d.u.fk": ["a"], "d.u.unique": ["a"]}


@needs_pg
def test_check_and_exclude_are_no_keys_and_do_not_swallow_the_next_statement(tmp_path):
    keys = _keys(_scan(tmp_path, 'CREATE TABLE "p" ("id" bigint NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY, "a" int NOT NULL, '
                                 'CONSTRAINT "a_pos" CHECK ("a" >= 0), CONSTRAINT "uniq_a" UNIQUE ("a"), CONSTRAINT "a_lt" CHECK ("a" < 9));\n'
                                 "CREATE TABLE n4 (id int, CONSTRAINT n4_pk PRIMARY KEY (id), CONSTRAINT n4_c CHECK (id>0));\n"
                                 "ALTER TABLE n4 ADD CONSTRAINT n4_x EXCLUDE USING gist (id WITH =);\n"
                                 "ALTER TABLE n4 ADD CONSTRAINT n4_u UNIQUE (id) DEFERRABLE INITIALLY DEFERRED;\n", "n"))
    assert keys == {"n.p.uniq_a": ("unique", ["a"], None), "n.n4.n4_pk": ("primary_key", ["id"], None), "n.n4.n4_u": ("unique", ["id"], None)}


@needs_pg
def test_names_keep_their_spelling_and_byte_spans_survive_non_ascii(tmp_path):
    facts = _scan(tmp_path, 'CREATE TABLE Users (Id int PRIMARY KEY, "ñandú" text UNIQUE, Note text);\n'
                            "CREATE TABLE o (uid int, CONSTRAINT o_fk FOREIGN KEY (uid) REFERENCES Users (Id));\n", "u")
    assert facts["u.o.o_fk"]["attrs"]["references"] == {"table": "Users", "columns": ["Id"]} and {"type": "references", "target": "u.Users"} in facts["u.o.o_fk"]["relations"]
    assert (facts["u.Users.ñandú"]["attrs"]["unique"], facts["u.Users.Note"]["attrs"]["type"], facts["u.Users.Id"]["attrs"]["primary_key"]) == (True, "text", True)
    assert facts["u.o.o_fk"]["signature"] == "CONSTRAINT o_fk FOREIGN KEY (uid) REFERENCES Users (Id)"


ENCODED = ("CREATE TABLE a (id int PRIMARY KEY, x int, -- comentario: " + "año " * 20 + "\n  CONSTRAINT a_u UNIQUE (x));\n"
           "CREATE TABLE b (k int, CONSTRAINT b_fk FOREIGN KEY (k) REFERENCES a (id));\n")


@needs_pg
@pytest.mark.parametrize("encoding", ["latin-1", "utf-8"])
def test_a_non_ascii_comment_in_latin_1_or_utf_8_does_not_shift_the_keys_of_the_next_table(tmp_path, encoding):
    from sldb.code.scan import scan_tree

    (tmp_path / "e.sql").write_bytes(ENCODED.encode(encoding))
    facts = {f["id"]: f for f in scan_tree(tmp_path)}
    assert _keys(facts) == {"e.a.a_u": ("unique", ["x"], None), "e.b.b_fk": ("foreign_key", ["k"], {"table": "a", "columns": ["id"]})}
    assert sorted(i for i in facts if i.startswith("e.b.")) == ["e.b.b_fk", "e.b.k"] and facts["e.a.id"]["attrs"]["primary_key"]
    assert [facts[i]["signature"] for i in ("e.a.a_u", "e.b.b_fk", "e.b.k")] == ["CONSTRAINT a_u UNIQUE (x)", "CONSTRAINT b_fk FOREIGN KEY (k) REFERENCES a (id)", "k int"]
    assert {"type": "references", "target": "e.a"} in facts["e.b.b_fk"]["relations"] and not any("keys_partial" in f["attrs"] for f in facts.values())


@needs_pg
def test_a_statement_postgres_rejects_keeps_tree_sitters_reading_and_marks_keys_partial(tmp_path):
    facts = _scan(tmp_path, "CREATE TABLE t (a int, b int, UNIQUE (a));\nCREATE TABLE r (a int, b int, UNIQUE (a), PRIMARY KEY (a) b);\n"
                            "ALTER TABLE t ADD CONSTRAINT tu UNIQUE (b) WHAT;\nCREATE TABLE ok (a int);\n", "r")
    assert [facts[t]["attrs"].get("keys_partial") for t in ("r.t", "r.r", "r.ok")] == [True, True, None], "r does not parse; the ALTER on t neither"
    assert sorted(_keys(facts)) == ["r.t.unique"] and {"r.r.a", "r.r.b"} <= set(facts)


@needs_sql
def test_without_the_extra_the_keys_are_not_read(no_pg, tmp_path):
    facts = _scan(tmp_path, SHOP, "s")
    assert not _keys(facts) and "s.shop_product.id" not in facts and facts["s.shop_product.price"]["attrs"] == {"native_kind": "column_definition", "module": "s"}
    assert all(facts[f"s.{t}"]["attrs"]["keys_partial"] for t in ("shop_category", "shop_tag", "shop_product", "shop_product_tags"))


def test_without_the_sql_grammar_sql_files_are_not_scanned(monkeypatch, tmp_path):
    import sldb.code.runtime as rt
    from sldb.code.scan import scan_tree

    real = rt.importlib.import_module
    monkeypatch.setattr(rt, "_RUNTIME", {})
    monkeypatch.setattr(rt.importlib, "import_module", lambda name: (_ for _ in ()).throw(ImportError(name, name=name)) if name == "tree_sitter_sql" else real(name))
    shutil.copytree(SQL, tmp_path / "db")
    (tmp_path / "db" / "m.py").write_text("def f(): pass\n", encoding="utf-8")
    assert not rt.available(".sql") and sorted(f["id"] for f in scan_tree(tmp_path / "db")) == ["m", "m.f"]
