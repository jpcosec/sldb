import inspect
import json
import pytest
from pathlib import Path
from pydantic import Field
from sldb import StructuredNLDoc
from sldb.cli import main as cli_main
from sldb.store.io import load_store_index, load_models_index, load_documents_index


class SimpleBook(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Book title.")


_PYTHONPATH = str(Path(__file__).parent.parent.parent / "src")
_MODULE_REF = f"{SimpleBook.__module__}:{SimpleBook.__name__}"


def _init(tmp_path):
    cli_main(["store", "init", "--path", str(tmp_path)])


def _add(tmp_path):
    cli_main(["store", "add", _MODULE_REF, "--store", str(tmp_path / ".sldb"), "--pythonpath", _PYTHONPATH])


def _track(tmp_path, doc_path, name=None):
    args = ["store", "track", _MODULE_REF, str(doc_path), "--store", str(tmp_path / ".sldb"), "--pythonpath", _PYTHONPATH]
    if name:
        args += ["--name", name]
    cli_main(args)


# ── init ──────────────────────────────────────────────────────────────────────

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


# ── add ───────────────────────────────────────────────────────────────────────

def test_store_add_registers_model(tmp_path):
    _init(tmp_path)
    assert cli_main(["store", "add", _MODULE_REF, "--store", str(tmp_path / ".sldb"), "--pythonpath", _PYTHONPATH]) == 0
    names = [m.name for m in load_store_index(tmp_path / ".sldb").models]
    assert "SimpleBook" in names


def test_store_add_creates_index_files(tmp_path):
    _init(tmp_path)
    _add(tmp_path)
    store_index = load_store_index(tmp_path / ".sldb")
    entry = next(m for m in store_index.models if m.name == "SimpleBook")
    models_idx = load_models_index(tmp_path / entry.models_index)
    docs_idx = load_documents_index(tmp_path / models_idx.documents_index)
    assert models_idx.name == "SimpleBook"
    assert docs_idx.documents == []


def test_store_add_sets_hash_a(tmp_path):
    _init(tmp_path)
    _add(tmp_path)
    assert load_store_index(tmp_path / ".sldb").hash_a != ""


def test_store_add_fails_if_already_registered(tmp_path):
    _init(tmp_path)
    _add(tmp_path)
    with pytest.raises(SystemExit):
        _add(tmp_path)


# ── track ─────────────────────────────────────────────────────────────────────

def test_store_track_registers_document(tmp_path):
    _init(tmp_path)
    _add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    assert cli_main(["store", "track", _MODULE_REF, str(doc), "--store", str(tmp_path / ".sldb"), "--pythonpath", _PYTHONPATH]) == 0

    entry = next(m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook")
    models_idx = load_models_index(tmp_path / entry.models_index)
    docs_idx = load_documents_index(tmp_path / models_idx.documents_index)
    assert len(docs_idx.documents) == 1
    assert docs_idx.documents[0].name == "book"
    assert docs_idx.documents[0].hash_c != ""
    assert docs_idx.documents[0].hash_d != ""


def test_store_track_custom_name(tmp_path):
    _init(tmp_path)
    _add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _track(tmp_path, doc, name="my-book")
    entry = next(m for m in load_store_index(tmp_path / ".sldb").models if m.name == "SimpleBook")
    models_idx = load_models_index(tmp_path / entry.models_index)
    docs_idx = load_documents_index(tmp_path / models_idx.documents_index)
    assert docs_idx.documents[0].name == "my-book"


def test_store_track_updates_hashes(tmp_path):
    _init(tmp_path)
    _add(tmp_path)
    hash_a_before = load_store_index(tmp_path / ".sldb").hash_a
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _track(tmp_path, doc)
    assert load_store_index(tmp_path / ".sldb").hash_a != hash_a_before


def test_store_track_fails_model_not_registered(tmp_path):
    _init(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    with pytest.raises(SystemExit):
        cli_main(["store", "track", _MODULE_REF, str(doc), "--store", str(tmp_path / ".sldb")])


def test_store_track_fails_duplicate_name(tmp_path):
    _init(tmp_path)
    _add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _track(tmp_path, doc)
    with pytest.raises(SystemExit):
        _track(tmp_path, doc)


# ── check ─────────────────────────────────────────────────────────────────────

def test_store_check_clean_passes(tmp_path, capsys):
    _init(tmp_path)
    _add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _track(tmp_path, doc)
    rc = cli_main(["store", "check", "--store", str(tmp_path / ".sldb"), "--pythonpath", _PYTHONPATH])
    assert rc == 0
    assert "PASS" in capsys.readouterr().out


def test_store_check_data_mutation_fails(tmp_path, capsys):
    _init(tmp_path)
    _add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _track(tmp_path, doc)
    doc.write_text("# Changed Title\n", encoding="utf-8")
    rc = cli_main(["store", "check", "--store", str(tmp_path / ".sldb"), "--pythonpath", _PYTHONPATH])
    assert rc == 1
    assert "FAIL" in capsys.readouterr().out


def test_store_check_json_output(tmp_path, capsys):
    _init(tmp_path)
    _add(tmp_path)
    capsys.readouterr()  # drain init/add output
    cli_main(["store", "check", "--store", str(tmp_path / ".sldb"), "--format", "json", "--pythonpath", _PYTHONPATH])
    data = json.loads(capsys.readouterr().out)
    assert "valid" in data and "models" in data
