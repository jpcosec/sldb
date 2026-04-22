from pathlib import Path
from pydantic import Field
from sldb import StructuredNLDoc
from sldb.cli import main as cli_main
from sldb.store.diagnostics import diagnose_store, DiagnosisNote
from sldb.store.io import load_store_index, load_models_index, save_models_index


class CheckDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Document title.")


_PYTHONPATH = str(Path(__file__).parent.parent.parent / "src")
_MODULE_REF = f"{CheckDoc.__module__}:{CheckDoc.__name__}"


def _make_store(tmp_path):
    doc = tmp_path / "doc.md"
    doc.write_text("# Hello\n", encoding="utf-8")
    cli_main(["store", "init", "--path", str(tmp_path)])
    cli_main(["store", "add", _MODULE_REF, "--store", str(tmp_path / ".sldb"), "--pythonpath", _PYTHONPATH])
    cli_main(["store", "track", _MODULE_REF, str(doc), "--store", str(tmp_path / ".sldb"), "--pythonpath", _PYTHONPATH])
    return tmp_path


def test_clean_store_is_valid(tmp_path):
    _make_store(tmp_path)
    result = diagnose_store(tmp_path / ".sldb", tmp_path, pythonpath=_PYTHONPATH)
    assert result.is_valid
    assert result.hash_a_ok
    assert result.models[0].documents[0].note == DiagnosisNote.OK


def test_benign_text_mutation(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Hello\n\nextra paragraph\n", encoding="utf-8")
    result = diagnose_store(tmp_path / ".sldb", tmp_path, pythonpath=_PYTHONPATH)
    assert result.models[0].documents[0].note == DiagnosisNote.BENIGN_MUTATION
    assert result.is_valid


def test_data_mutation_is_invalid(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    result = diagnose_store(tmp_path / ".sldb", tmp_path, pythonpath=_PYTHONPATH)
    assert result.models[0].documents[0].note == DiagnosisNote.DATA_MUTATION
    assert not result.is_valid


def test_missing_document(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").unlink()
    result = diagnose_store(tmp_path / ".sldb", tmp_path, pythonpath=_PYTHONPATH)
    assert result.models[0].documents[0].note == DiagnosisNote.MISSING
    assert not result.is_valid


def test_tampered_hash_b(tmp_path):
    _make_store(tmp_path)
    store_index = load_store_index(tmp_path / ".sldb")
    entry = store_index.models[0]
    models_idx = load_models_index(tmp_path / entry.models_index)
    models_idx.hash_b = "tampered"
    save_models_index(tmp_path / entry.models_index, models_idx)
    result = diagnose_store(tmp_path / ".sldb", tmp_path, pythonpath=_PYTHONPATH)
    assert not result.models[0].hash_b_ok
    assert not result.is_valid
