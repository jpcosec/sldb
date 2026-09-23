import json
import pytest
from pathlib import Path
from pydantic import Field
from sldb import StructuredNLDoc
from sldb.cli import main as cli_main
from sldb.store.io import load_semantic_index, load_store_index, load_models_index, load_documents_index
from sldb.store.layout import (
    semantic_dag_path,
    store_index_path,
)

_SRC = str(Path(__file__).parent.parent.parent / "src")


class SimpleBook(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Book title.")


_REF = f"{SimpleBook.__module__}:{SimpleBook.__name__}"


def _STORE_ARGS(tmp):
    return ["--store", str(tmp / ".sldb")]


_PY_ARGS = ["--pythonpath", _SRC]


def _init(tmp):
    cli_main(["stores", "init", "--path", str(tmp)])


def _model_add(tmp):
    cli_main(["models", "add", _REF] + _STORE_ARGS(tmp) + _PY_ARGS)


def _doc_track(tmp, doc, name=None):
    args = (
        ["docs", "track", str(doc), "--model", "SimpleBook"]
        + _STORE_ARGS(tmp)
        + _PY_ARGS
    )
    if name:
        args += ["--name", name]
    cli_main(args)


# ── store init ────────────────────────────────────────────────────────────────


def test_store_init_creates_index(tmp_path):
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    index = load_store_index(tmp_path / ".sldb")
    assert index.stores == [] and index.models == []
    assert store_index_path(tmp_path / ".sldb").exists()
    # PLAN 15 capa 5: the semantic index is per-document shards, none yet for an empty store —
    # not one store-wide file — so it composes empty rather than existing on disk.
    assert load_semantic_index(tmp_path / ".sldb").documents == {}
    assert semantic_dag_path(tmp_path / ".sldb").exists()


def test_store_init_fails_if_exists(tmp_path):
    _init(tmp_path)
    # Idempotent: second init exits 0 with info message
    rc = cli_main(["stores", "init", "--path", str(tmp_path)])
    assert rc == 0


def test_store_init_registers_project_in_global_catalog(tmp_path, monkeypatch):
    home = tmp_path / "home"
    project = home / "project"
    project.mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    assert cli_main(["stores", "init", "--path", str(project)]) == 0
    global_index = load_store_index(home / ".sldb")
    assert [(entry.name, entry.path) for entry in global_index.stores] == [
        ("project", str(project / ".sldb")),
    ]


def test_store_init_force_overwrites(tmp_path):
    _init(tmp_path)
    assert cli_main(["stores", "init", "--path", str(tmp_path), "--force"]) == 0


# ── store add (federation) ────────────────────────────────────────────────────


def test_store_add_links_other_store(tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    _init(tmp_path)
    _init(other)
    rc = cli_main(["stores", "add", str(other / ".sldb")] + _STORE_ARGS(tmp_path))
    assert rc == 0
    index = load_store_index(tmp_path / ".sldb")
    assert any(s.path for s in index.stores)


def test_store_add_fails_on_invalid_path(tmp_path):
    _init(tmp_path)
    with pytest.raises(SystemExit):
        cli_main(
            ["stores", "add", str(tmp_path / "nonexistent")] + _STORE_ARGS(tmp_path)
        )


def test_store_add_fails_if_already_linked(tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    _init(tmp_path)
    _init(other)
    cli_main(
        ["stores", "add", str(other / ".sldb"), "--name", "other"]
        + _STORE_ARGS(tmp_path)
    )
    with pytest.raises(SystemExit):
        cli_main(
            ["stores", "add", str(other / ".sldb"), "--name", "other"]
            + _STORE_ARGS(tmp_path)
        )


# ── store check ───────────────────────────────────────────────────────────────


def test_store_check_clean_passes(tmp_path, capsys):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    capsys.readouterr()
    rc = cli_main(["stores", "check"] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    assert rc == 0
    assert "PASS" in capsys.readouterr().out


def test_store_check_data_mutation_fails(tmp_path, capsys):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    doc.write_text("# Changed Title\n", encoding="utf-8")
    capsys.readouterr()
    rc = cli_main(["stores", "check"] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    assert rc == 1
    assert "FAIL" in capsys.readouterr().out


def test_store_check_json_format(tmp_path, capsys):
    """Deliberately produces an invalid store (data mutation after tracking,
    the same pattern as test_store_check_data_mutation_fails) rather than
    relying on a fresh _model_add() with zero documents to be invalid --
    that used to be true only because of a hash_b registration bug, now
    fixed; a freshly registered model with no documents is a valid store."""
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    doc.write_text("# Changed Title\n", encoding="utf-8")
    capsys.readouterr()
    with pytest.raises(SystemExit) as exc:
        cli_main(
            ["stores", "check", "--format", "json"] + _STORE_ARGS(tmp_path) + _PY_ARGS
        )
    assert exc.value.code == 1
    data = json.loads(capsys.readouterr().out)
    assert "valid" in data and "models" in data
    assert data["valid"] is False


# ── store update ──────────────────────────────────────────────────────────────


def test_store_update_recomputes_hashes(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    # Tamper file directly
    doc.write_text("# Changed Title\n", encoding="utf-8")
    # Update should recompute, making check pass again
    cli_main(["stores", "update"] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    from sldb.store.diagnostics import diagnose_store
    from sldb.cli.model_utils import resolve_model_ref

    result = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_SRC)
    assert result.is_valid


# ── model add ────────────────────────────────────────────────────────────────


def test_model_add_registers_model(tmp_path, capsys):
    _init(tmp_path)
    assert cli_main(["models", "add", _REF] + _STORE_ARGS(tmp_path) + _PY_ARGS) == 0
    assert "Registered" in capsys.readouterr().out
    names = [m.name for m in load_store_index(tmp_path / ".sldb").models]
    assert "SimpleBook" in names


def test_model_add_creates_index_files(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    store_index = load_store_index(tmp_path / ".sldb")
    entry = next(m for m in store_index.models if m.name == "SimpleBook")
    assert entry.models_index == ".sldb/core/models/SimpleBook.yaml"
    models_idx = load_models_index(tmp_path / entry.models_index)
    docs_idx = load_documents_index(tmp_path / models_idx.documents_index)
    assert models_idx.name == "SimpleBook"
    assert models_idx.documents_index == ".sldb/core/documents/SimpleBook.yaml"
    assert docs_idx.documents == []


def test_get_store_context_fails_when_no_local_and_no_global(tmp_path, monkeypatch):
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))

    with pytest.raises(SystemExit) as exc:
        cli_main(["models", "list"])
    assert "init --path" in str(exc.value)


def test_get_store_context_readonly_falls_back_to_global(tmp_path, monkeypatch):
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.chdir(project)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))

    global_store = Path.home() / ".sldb"
    from sldb.store.io import save_store_index
    from sldb.store.models import StoreIndex

    save_store_index(global_store, StoreIndex())

    result = cli_main(["models", "list"])
    assert result == 0


def test_store_alias_is_resolved_from_an_ancestor_registry(tmp_path, monkeypatch):
    from sldb.cli.store_context import get_store_context

    parent = tmp_path / "parent"
    child = parent / "child"
    remote = tmp_path / "remote"
    child.mkdir(parents=True)
    remote.mkdir()
    _init(parent)
    _init(child)
    _init(remote)
    cli_main(["stores", "add", str(remote / ".sldb"), "--name", "remote"] + _STORE_ARGS(parent))
    source = child / "src"
    source.mkdir()
    monkeypatch.chdir(source)
    store, _root = get_store_context("remote", mode="readonly")
    assert store == remote / ".sldb"


def test_model_add_sets_hash_a(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    assert load_store_index(tmp_path / ".sldb").hash_a != ""


def test_model_add_invalid_ref_reports_not_found_and_lists_available(tmp_path, capsys):
    _init(tmp_path)
    _model_add(tmp_path)
    capsys.readouterr()
    rc = cli_main(["models", "add", "sldb.models.structured_doc:FooBar"] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    captured = capsys.readouterr()
    assert rc != 0
    assert "Model 'FooBar' not found" in captured.err
    assert "Available models" in captured.err
    assert "SimpleBook" in captured.err


def test_model_add_missing_store_reports_tried_path(tmp_path, capsys):
    missing = tmp_path / "no-such-store" / ".sldb"
    rc = cli_main(["models", "add", _REF, "--store", str(missing)] + _PY_ARGS)
    captured = capsys.readouterr()
    assert rc >= 2
    assert str(missing) in captured.err


def test_model_add_already_registered_is_noop(tmp_path, capsys):
    _init(tmp_path)
    _model_add(tmp_path)
    capsys.readouterr()
    rc = cli_main(["models", "add", _REF] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    captured = capsys.readouterr()
    assert rc == 0
    assert "already registered" in captured.out
    assert len(load_store_index(tmp_path / ".sldb").models) == 1


def test_model_add_sets_correct_hash_b_for_zero_documents(tmp_path):
    """Regression: a freshly registered model with no documents yet must not
    need a follow-up `models update` just to pass `stores check`.

    hash_b used to be hardcoded to "" at registration time, which does not
    match hash_documents_index() of the empty DocumentsIndex it was
    registered with -- stores check then reported a false hash_b_ok=False
    for a store that was never actually mutated.
    """
    from sldb.store.hashing import hash_documents_index
    from sldb.store.models import DocumentsIndex

    _init(tmp_path)
    _model_add(tmp_path)

    store_index = load_store_index(tmp_path / ".sldb")
    entry = next(m for m in store_index.models if m.name == "SimpleBook")
    models_idx = load_models_index(tmp_path / entry.models_index)

    assert models_idx.hash_b == hash_documents_index(DocumentsIndex())
    assert models_idx.hash_b != ""


def test_model_add_passes_stores_check_immediately_with_no_documents(tmp_path):
    """The end-to-end shape of the regression: `stores check` must PASS
    right after `models add`, with no `models update` in between."""
    from sldb.cli.model_utils import resolve_model_ref
    from sldb.store.diagnostics import diagnose_store

    _init(tmp_path)
    _model_add(tmp_path)

    result = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_SRC)

    assert result.hash_a_ok
    book_diagnosis = next(m for m in result.models if m.name == "SimpleBook")
    assert book_diagnosis.hash_b_ok


# ── model update ──────────────────────────────────────────────────────────────


def test_model_update_reindexes_docs(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    hash_a_before = load_store_index(tmp_path / ".sldb").hash_a
    doc.write_text("# Changed Title\n", encoding="utf-8")
    cli_main(["models", "update", "SimpleBook"] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    assert load_store_index(tmp_path / ".sldb").hash_a != hash_a_before


# ── doc track ─────────────────────────────────────────────────────────────────


def test_doc_track_registers_document(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    assert (
        cli_main(
            ["docs", "track", str(doc), "--model", "SimpleBook"]
            + _STORE_ARGS(tmp_path)
            + _PY_ARGS
        )
        == 0
    )
    entry = next(
        m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook"
    )
    docs_idx = load_documents_index(
        tmp_path / load_models_index(tmp_path / entry.models_index).documents_index
    )
    assert len(docs_idx.documents) == 1
    assert docs_idx.documents[0].hash_c != ""
    assert docs_idx.documents[0].hash_d != ""


def test_doc_track_custom_name(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc, name="my-book")
    entry = next(
        m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook"
    )
    docs_idx = load_documents_index(
        tmp_path / load_models_index(tmp_path / entry.models_index).documents_index
    )
    assert docs_idx.documents[0].name == "my-book"


def test_doc_track_fails_idempotency(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    # A doc that doesn't roundtrip: template expects "# title", we give extra structure
    doc = tmp_path / "bad.md"
    doc.write_text(
        "not valid markdown for this template at all !!!!\n", encoding="utf-8"
    )
    with pytest.raises(SystemExit):
        cli_main(
            ["docs", "track", str(doc), "--model", "SimpleBook"]
            + _STORE_ARGS(tmp_path)
            + _PY_ARGS
        )


def test_doc_track_force_bypasses_idempotency(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "bad.md"
    doc.write_text(
        "not valid markdown for this template at all !!!!\n", encoding="utf-8"
    )
    rc = cli_main(
        ["docs", "track", str(doc), "--model", "SimpleBook", "--force"]
        + _STORE_ARGS(tmp_path)
        + _PY_ARGS
    )
    assert rc == 0


def test_doc_track_fails_model_not_registered(tmp_path):
    _init(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        cli_main(
            ["docs", "track", str(doc), "--model", "SimpleBook"] + _STORE_ARGS(tmp_path)
        )


def test_doc_track_fails_duplicate(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    with pytest.raises(SystemExit):
        _doc_track(tmp_path, doc)


# ── doc add ───────────────────────────────────────────────────────────────────


def test_doc_add_creates_file_and_tracks(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    out = tmp_path / "output.md"
    rc = cli_main(
        [
            "docs",
            "create",
            "--model",
            "SimpleBook",
            "-o",
            str(out),
            '{"title": "Hello World"}',
        ]
        + _STORE_ARGS(tmp_path)
        + _PY_ARGS
    )
    assert rc == 0
    assert out.exists()
    assert "Hello World" in out.read_text()
    entry = next(
        m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook"
    )
    docs_idx = load_documents_index(
        tmp_path / load_models_index(tmp_path / entry.models_index).documents_index
    )
    assert any(d.name == "output" for d in docs_idx.documents)


def test_doc_add_from_yaml_file(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    data_file = tmp_path / "data.yaml"
    data_file.write_text("title: From File\n", encoding="utf-8")
    out = tmp_path / "output.md"
    rc = cli_main(
        [
            "docs",
            "create",
            "--model",
            "SimpleBook",
            "-o",
            str(out),
            str(data_file),
        ]
        + _STORE_ARGS(tmp_path)
        + _PY_ARGS
    )
    assert rc == 0
    assert "From File" in out.read_text()


# ── doc update ────────────────────────────────────────────────────────────────


def test_doc_update_rewrites_and_reindexes(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)

    entry = next(
        m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook"
    )
    docs_idx_before = load_documents_index(
        tmp_path / load_models_index(tmp_path / entry.models_index).documents_index
    )
    hash_d_before = docs_idx_before.documents[0].hash_d

    cli_main(
        [
            "docs",
            "update",
            "book",
            '{"title": "Updated Title"}',
        ]
        + _STORE_ARGS(tmp_path)
        + _PY_ARGS
    )
    assert "Updated Title" in doc.read_text()
    docs_idx_after = load_documents_index(
        tmp_path / load_models_index(tmp_path / entry.models_index).documents_index
    )
    assert docs_idx_after.documents[0].hash_d != hash_d_before


def test_doc_update_fails_unknown_doc(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    with pytest.raises(SystemExit):
        cli_main(
            [
                "docs",
                "update",
                "nonexistent",
                '{"title": "x"}',
            ]
            + _STORE_ARGS(tmp_path)
            + _PY_ARGS
        )


def test_doc_untrack_removes_document_from_store(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)

    assert cli_main(["docs", "untrack", "book"] + _STORE_ARGS(tmp_path) + _PY_ARGS) == 0

    entry = next(
        m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook"
    )
    docs_idx = load_documents_index(
        tmp_path / load_models_index(tmp_path / entry.models_index).documents_index
    )
    assert docs_idx.documents == []


def test_doc_untrack_keeps_the_markdown_file(tmp_path):
    """The half of the pair that leaves the file: untrack drops the store entry only."""
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)

    assert cli_main(["docs", "untrack", "book"] + _STORE_ARGS(tmp_path) + _PY_ARGS) == 0
    assert doc.exists()


def test_doc_delete_removes_both_the_store_entry_and_the_file(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)

    rc = cli_main(["docs", "delete", "book", "--yes"] + _STORE_ARGS(tmp_path) + _PY_ARGS)

    assert rc == 0
    assert not doc.exists()
    entry = next(
        m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook"
    )
    docs_idx = load_documents_index(
        tmp_path / load_models_index(tmp_path / entry.models_index).documents_index
    )
    assert docs_idx.documents == []


def test_doc_delete_purges_the_extraction_cache_entry(tmp_path):
    """A deleted document must not stay described in `runtime/cache/extracted.json`."""
    from sldb.store import runtime_cache_disk

    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    store_path = tmp_path / ".sldb"
    runtime_cache_disk.clear()
    cli_main(["docs", "list"] + _STORE_ARGS(tmp_path) + _PY_ARGS)

    cli_main(["docs", "delete", "book", "--yes"] + _STORE_ARGS(tmp_path) + _PY_ARGS)

    runtime_cache_disk.clear()
    assert not [k for k in runtime_cache_disk.entries(store_path) if "book.md" in k]


def test_doc_delete_without_yes_aborts_and_touches_nothing(tmp_path, monkeypatch):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    monkeypatch.setattr("builtins.input", lambda _prompt: "n")

    rc = cli_main(["docs", "delete", "book"] + _STORE_ARGS(tmp_path) + _PY_ARGS)

    assert rc == 1
    assert doc.exists()
    entry = next(
        m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook"
    )
    docs_idx = load_documents_index(
        tmp_path / load_models_index(tmp_path / entry.models_index).documents_index
    )
    assert [d.name for d in docs_idx.documents] == ["book"]
