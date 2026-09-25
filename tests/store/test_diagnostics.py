from pathlib import Path
from pydantic import Field
from sldb import StructuredNLDoc
from sldb.cli import main as cli_main
from sldb.cli.model_utils import resolve_model_ref
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
    cli_main(["stores", "init", "--path", str(tmp_path)])
    cli_main(
        [
            "models",
            "add",
            _MODULE_REF,
            "--store",
            str(tmp_path / ".sldb"),
            "--pythonpath",
            _PYTHONPATH,
        ]
    )
    cli_main(
        [
            "docs",
            "track",
            str(doc),
            "--model",
            CheckDoc.__name__,
            "--store",
            str(tmp_path / ".sldb"),
            "--pythonpath",
            _PYTHONPATH,
        ]
    )
    return tmp_path


def test_clean_store_is_valid(tmp_path):
    _make_store(tmp_path)
    result = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    assert result.is_valid
    assert result.hash_a_ok
    assert result.models[0].documents[0].note == DiagnosisNote.OK


def test_benign_text_mutation(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Hello\n\nextra paragraph\n", encoding="utf-8")
    result = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    assert result.models[0].documents[0].note == DiagnosisNote.BENIGN_MUTATION
    assert result.is_valid


def test_data_mutation_is_invalid(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    result = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    assert result.models[0].documents[0].note == DiagnosisNote.DATA_MUTATION
    assert not result.is_valid


def test_missing_document(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").unlink()
    result = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    assert result.models[0].documents[0].note == DiagnosisNote.MISSING
    assert not result.is_valid


def test_tampered_hash_b(tmp_path):
    _make_store(tmp_path)
    store_index = load_store_index(tmp_path / ".sldb")
    entry = store_index.models[0]
    models_idx = load_models_index(tmp_path / entry.models_index)
    models_idx.hash_b = "tampered"
    save_models_index(tmp_path / entry.models_index, models_idx)
    result = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    assert not result.models[0].hash_b_ok
    assert not result.is_valid


# ── semantic names: what each hash signs ─────────────────────────────────────
#
# The letters say where a hash sits in the chain; the names say what it signs.
# `content` is the markdown TEXT (hash_c), `fields` is the EXTRACTED PAYLOAD under
# the model's contract (hash_d). That distinction is the whole basis of the
# verdict, so the names are asserted against observable behaviour, not just
# aliased: a reformat must move content and hold fields still, and a field edit
# must move both.


def test_reformatting_moves_content_and_holds_fields_still(tmp_path):
    """The defining property of an expected mutation, stated in semantic terms."""
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Hello\n\nextra paragraph\n", encoding="utf-8")
    doc = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH).models[0].documents[0]

    assert not doc.content_ok, "the markdown text changed, so content must not match"
    assert doc.fields_ok, "no field's value changed, so fields must still match"
    assert doc.note == DiagnosisNote.BENIGN_MUTATION
    # the two sides are named for where they were read, not for which is right
    assert doc.content_on_disk != doc.content_in_index
    assert doc.fields_on_disk == doc.fields_in_index


def test_a_field_edit_moves_both_content_and_fields(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    doc = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH).models[0].documents[0]

    assert not doc.content_ok and not doc.fields_ok
    assert doc.note == DiagnosisNote.DATA_MUTATION
    assert doc.fields_on_disk != doc.fields_in_index


def test_letter_names_still_read_the_same_values(tmp_path):
    """hash_c/hash_d are the store's persisted keys; renaming them would invalidate
    every store on disk, so the letter names stay as aliases."""
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Hello\n\nextra\n", encoding="utf-8")
    res = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    doc = res.models[0].documents[0]

    assert doc.hash_c_ok is doc.content_ok
    assert doc.hash_d_ok is doc.fields_ok
    assert doc.hash_c_expected == doc.content_on_disk
    assert doc.hash_c_actual == doc.content_in_index
    assert doc.hash_d_expected == doc.fields_on_disk
    assert doc.hash_d_actual == doc.fields_in_index
    assert res.hash_a_ok is res.root_ok
    assert res.models[0].hash_b_ok is res.models[0].roster_ok


# ── the roster verdict: a failure no document can explain ────────────────────


def test_roster_failure_over_absent_documents_names_no_damaged_document(tmp_path):
    """The case that used to be indistinguishable from corruption.

    A model whose documents are absent (deliberately unversioned: a ledger that is
    gitignored, so a clean clone has none of them) fails the roster hash while every
    document present — none — is clean. Reproduces AgentsKBs MoveDoc: `docs=0,
    notes={}`, yet FAIL.

    The roster entry is removed while `hash_b` keeps signing it: that is exactly a
    clone's state, where the index was written by a tree that had the documents.
    """
    _make_store(tmp_path)
    (tmp_path / "doc.md").unlink()
    # The roster is composed from per-document shards, so a clone missing the
    # documents is missing the shards themselves — emptying the list would not
    # reproduce it. `hash_b` keeps signing the document that is no longer there.
    shard = tmp_path / ".sldb" / "core" / "documents" / "CheckDoc" / "doc.yaml"
    assert shard.exists(), "precondition: the document has a shard to remove"
    shard.unlink()
    # `documents_hash.entries_of` caches the composed roster across operations,
    # keyed on hash_b (which we are deliberately leaving stale), so drop it.
    from sldb.store import documents_hash

    documents_hash.invalidate(tmp_path / ".sldb", "CheckDoc")

    res = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)
    model = next(m for m in res.models if m.name == "CheckDoc")

    assert model.documents == [], "no document is present to carry a verdict"
    assert not model.roster_ok, "the roster hash still signs the document that left"
    assert model.documents_are_clean, "nothing present is damaged"
    assert model.roster_only_failure, "so the failure is roster-only"
    assert res.damaged_documents == [], "and it must not be reported as damage"
    assert model in res.roster_only_models
    assert not res.is_valid, "classifying a failure is not tolerating it"
    assert "0 documents" in model.explain()


def test_damaged_document_is_not_reported_as_roster_only(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    res = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)

    assert len(res.damaged_documents) == 1
    assert res.roster_only_models == [], "a damaged document is damage, not a roster artifact"


def test_reformatted_documents_are_listed_but_keep_the_store_valid(tmp_path):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Hello\n\nextra\n", encoding="utf-8")
    res = diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, pythonpath=_PYTHONPATH)

    assert [d.name for _m, d in res.reformatted_documents] == ["doc"]
    assert res.damaged_documents == []
    assert res.is_valid, "an expected mutation must not fail the store"


# ── the report: every finding says which document and what to do ─────────────


def _check_output(tmp_path, capsys, *extra):
    """Run `stores check`, returning (rc, stdout) with the setup chatter drained."""
    from sldb.cli import main as _main

    capsys.readouterr()  # drop the init/register/track output of _make_store
    args = ["stores", "check", "--store", str(tmp_path / ".sldb"), "--pythonpath", _PYTHONPATH, *extra]
    try:
        rc = _main(args)
    except SystemExit as exc:  # --format json/yaml exits instead of returning
        rc = exc.code
    return rc, capsys.readouterr().out


def test_report_names_the_damaged_document_and_its_fix(tmp_path, capsys):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    rc, out = _check_output(tmp_path, capsys)

    assert rc == 1
    assert "FAIL: store integrity" in out
    assert "1 damaged" in out
    assert "data_mutation: doc" in out, "the document is named, not just counted"
    assert "doc.md" in out, "and so is its path"
    assert "stores update" in out, "the fix is stated in the message"
    assert "hash_d" in out and "on disk" in out and "in index" in out


def test_report_distinguishes_reformatting_from_damage(tmp_path, capsys):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Hello\n\nextra\n", encoding="utf-8")
    rc, out = _check_output(tmp_path, capsys)

    assert rc == 0, "an expected mutation passes"
    assert "PASS: store integrity" in out
    assert "reformatted (ok)" in out
    assert "damaged" not in out


def test_report_explains_a_roster_only_failure_without_blaming_a_document(tmp_path, capsys):
    _make_store(tmp_path)
    store_index = load_store_index(tmp_path / ".sldb")
    models_idx = load_models_index(tmp_path / store_index.models[0].models_index)
    models_idx.hash_b = "tampered"
    save_models_index(tmp_path / store_index.models[0].models_index, models_idx)
    rc, out = _check_output(tmp_path, capsys)

    assert rc == 1
    assert "roster" in out
    assert "roster-only" in out
    # the legend at the bottom defines every category; the findings above it must
    # not accuse any document
    findings = out.split("what the categories mean:")[0]
    assert "data_mutation" not in findings, "no document is damaged, so none is accused"
    assert "all 1 documents present are clean" in findings


def test_quiet_keeps_the_old_one_line_output(tmp_path, capsys):
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    rc, out = _check_output(tmp_path, capsys, "--quiet")

    assert rc == 1
    assert out.strip() == "FAIL: store integrity", "scripts pinned to the old output keep working"


def test_json_carries_both_letter_and_semantic_keys(tmp_path, capsys):
    import json

    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    _rc, out = _check_output(tmp_path, capsys, "--format", "json")
    payload = json.loads(out)
    doc = payload["models"][0]["documents"][0]

    # deskops reads `note`, `path` and the hash_*_ok keys: that shape must survive
    assert doc["note"] == "data_mutation"
    assert doc["hash_c_ok"] is False and doc["hash_d_ok"] is False
    assert doc["content_ok"] is False and doc["fields_ok"] is False
    assert payload["hash_a_ok"] == payload["root_ok"]
    assert payload["damaged"] == 1
    assert "explain" in doc and "stores update" in doc["explain"]
