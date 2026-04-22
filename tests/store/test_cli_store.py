import inspect
import json
import pytest
from pathlib import Path
from pydantic import Field
from sldb import StructuredNLDoc
from sldb.cli import main as cli_main
from sldb.store.io import load_store_index, load_models_index, load_documents_index

_SRC = str(Path(__file__).parent.parent.parent / "src")


class SimpleBook(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Book title.")


_REF = f"{SimpleBook.__module__}:{SimpleBook.__name__}"
_STORE_ARGS = lambda tmp: ["--store", str(tmp / ".sldb")]
_PY_ARGS = ["--pythonpath", _SRC]


def _init(tmp):
    cli_main(["store", "init", "--path", str(tmp)])

def _model_add(tmp):
    cli_main(["model", "add", _REF] + _STORE_ARGS(tmp) + _PY_ARGS)

def _doc_track(tmp, doc, name=None):
    args = ["doc", "track", str(doc), "--model", "SimpleBook"] + _STORE_ARGS(tmp) + _PY_ARGS
    if name:
        args += ["--name", name]
    cli_main(args)


# ── store init ────────────────────────────────────────────────────────────────

def test_store_init_creates_index(tmp_path):
    assert cli_main(["store", "init", "--path", str(tmp_path)]) == 0
    index = load_store_index(tmp_path / ".sldb")
    assert index.stores == [] and index.models == []


def test_store_init_fails_if_exists(tmp_path):
    _init(tmp_path)
    with pytest.raises(SystemExit):
        cli_main(["store", "init", "--path", str(tmp_path)])


def test_store_init_force_overwrites(tmp_path):
    _init(tmp_path)
    assert cli_main(["store", "init", "--path", str(tmp_path), "--force"]) == 0


# ── store add (federation) ────────────────────────────────────────────────────

def test_store_add_links_other_store(tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    _init(tmp_path)
    _init(other)
    rc = cli_main(["store", "add", str(other / ".sldb")] + _STORE_ARGS(tmp_path))
    assert rc == 0
    index = load_store_index(tmp_path / ".sldb")
    assert any(s.path for s in index.stores)


def test_store_add_fails_on_invalid_path(tmp_path):
    _init(tmp_path)
    with pytest.raises(SystemExit):
        cli_main(["store", "add", str(tmp_path / "nonexistent")] + _STORE_ARGS(tmp_path))


def test_store_add_fails_if_already_linked(tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    _init(tmp_path)
    _init(other)
    cli_main(["store", "add", str(other / ".sldb"), "--name", "other"] + _STORE_ARGS(tmp_path))
    with pytest.raises(SystemExit):
        cli_main(["store", "add", str(other / ".sldb"), "--name", "other"] + _STORE_ARGS(tmp_path))


# ── store check ───────────────────────────────────────────────────────────────

def test_store_check_clean_passes(tmp_path, capsys):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    capsys.readouterr()
    rc = cli_main(["store", "check"] + _STORE_ARGS(tmp_path) + _PY_ARGS)
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
    rc = cli_main(["store", "check"] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    assert rc == 1
    assert "FAIL" in capsys.readouterr().out


def test_store_check_json_format(tmp_path, capsys):
    _init(tmp_path)
    _model_add(tmp_path)
    capsys.readouterr()
    cli_main(["store", "check", "--format", "json"] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    data = json.loads(capsys.readouterr().out)
    assert "valid" in data and "models" in data


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
    cli_main(["store", "update"] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    from sldb.store.diagnostics import diagnose_store
    result = diagnose_store(tmp_path / ".sldb", tmp_path, pythonpath=_SRC)
    assert result.is_valid


# ── model add ────────────────────────────────────────────────────────────────

def test_model_add_registers_model(tmp_path):
    _init(tmp_path)
    assert cli_main(["model", "add", _REF] + _STORE_ARGS(tmp_path) + _PY_ARGS) == 0
    names = [m.name for m in load_store_index(tmp_path / ".sldb").models]
    assert "SimpleBook" in names


def test_model_add_creates_index_files(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    store_index = load_store_index(tmp_path / ".sldb")
    entry = next(m for m in store_index.models if m.name == "SimpleBook")
    models_idx = load_models_index(tmp_path / entry.models_index)
    docs_idx = load_documents_index(tmp_path / models_idx.documents_index)
    assert models_idx.name == "SimpleBook"
    assert docs_idx.documents == []


def test_model_add_sets_hash_a(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    assert load_store_index(tmp_path / ".sldb").hash_a != ""


def test_model_add_fails_if_already_registered(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    with pytest.raises(SystemExit):
        _model_add(tmp_path)


# ── model update ──────────────────────────────────────────────────────────────

def test_model_update_reindexes_docs(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    hash_a_before = load_store_index(tmp_path / ".sldb").hash_a
    doc.write_text("# Changed Title\n", encoding="utf-8")
    cli_main(["model", "update", "SimpleBook"] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    assert load_store_index(tmp_path / ".sldb").hash_a != hash_a_before


# ── doc track ─────────────────────────────────────────────────────────────────

def test_doc_track_registers_document(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    assert cli_main(["doc", "track", str(doc), "--model", "SimpleBook"] + _STORE_ARGS(tmp_path) + _PY_ARGS) == 0
    entry = next(m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook")
    docs_idx = load_documents_index(tmp_path / load_models_index(tmp_path / entry.models_index).documents_index)
    assert len(docs_idx.documents) == 1
    assert docs_idx.documents[0].hash_c != ""
    assert docs_idx.documents[0].hash_d != ""


def test_doc_track_custom_name(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc, name="my-book")
    entry = next(m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook")
    docs_idx = load_documents_index(tmp_path / load_models_index(tmp_path / entry.models_index).documents_index)
    assert docs_idx.documents[0].name == "my-book"


def test_doc_track_fails_idempotency(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    # A doc that doesn't roundtrip: template expects "# title", we give extra structure
    doc = tmp_path / "bad.md"
    doc.write_text("not valid markdown for this template at all !!!!\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        cli_main(["doc", "track", str(doc), "--model", "SimpleBook"] + _STORE_ARGS(tmp_path) + _PY_ARGS)


def test_doc_track_force_bypasses_idempotency(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "bad.md"
    doc.write_text("not valid markdown for this template at all !!!!\n", encoding="utf-8")
    rc = cli_main(["doc", "track", str(doc), "--model", "SimpleBook", "--force"] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    assert rc == 0


def test_doc_track_fails_model_not_registered(tmp_path):
    _init(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        cli_main(["doc", "track", str(doc), "--model", "SimpleBook"] + _STORE_ARGS(tmp_path))


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
    rc = cli_main([
        "doc", "add", "--model", "SimpleBook", "-o", str(out),
        '{"title": "Hello World"}',
    ] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    assert rc == 0
    assert out.exists()
    assert "Hello World" in out.read_text()
    entry = next(m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook")
    docs_idx = load_documents_index(tmp_path / load_models_index(tmp_path / entry.models_index).documents_index)
    assert any(d.name == "output" for d in docs_idx.documents)


def test_doc_add_from_yaml_file(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    data_file = tmp_path / "data.yaml"
    data_file.write_text("title: From File\n", encoding="utf-8")
    out = tmp_path / "output.md"
    rc = cli_main([
        "doc", "add", "--model", "SimpleBook", "-o", str(out), str(data_file),
    ] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    assert rc == 0
    assert "From File" in out.read_text()


# ── doc update ────────────────────────────────────────────────────────────────

def test_doc_update_rewrites_and_reindexes(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)

    entry = next(m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook")
    docs_idx_before = load_documents_index(tmp_path / load_models_index(tmp_path / entry.models_index).documents_index)
    hash_d_before = docs_idx_before.documents[0].hash_d

    rc = cli_main([
        "doc", "update", "book", "--model", "SimpleBook",
        '{"title": "Updated Title"}',
    ] + _STORE_ARGS(tmp_path) + _PY_ARGS)
    assert rc == 0
    assert "Updated Title" in doc.read_text()

    docs_idx_after = load_documents_index(tmp_path / load_models_index(tmp_path / entry.models_index).documents_index)
    assert docs_idx_after.documents[0].hash_d != hash_d_before


def test_doc_update_fails_unknown_doc(tmp_path):
    _init(tmp_path)
    _model_add(tmp_path)
    with pytest.raises(SystemExit):
        cli_main([
            "doc", "update", "nonexistent", "--model", "SimpleBook",
            '{"title": "x"}',
        ] + _STORE_ARGS(tmp_path) + _PY_ARGS)
