"""`sldb notations sync --spec/--catalog/--check/--prune/--json`: lo nuevo de la CLI en sldb.

Los tests portados de spec2viz estan en test_spec_sync.py y test_spec_catalog_sync.py; aqui, la
reconciliacion del catalogo (`--prune`), el informe JSON y los avisos en formato de findings.
"""
import json

import yaml

import sldb.api as sldb_api
from sldb.cli import main
from tests.notations.test_spec_sync import ARQ, FLOW


def _catalog(tmp_path, specs):
    if not (tmp_path / ".sldb").exists():
        sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir(exist_ok=True)
    for spec in (ARQ, FLOW):
        (tmp_path / "docs" / f"{spec['id']}.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
    vistas = [{"id": "v", "category": "Cat", "nav": "N", "desc": "D", "specs": [f"{s}.yml" for s in specs]}]
    (tmp_path / "docs" / "vistas.yml").write_text(yaml.safe_dump({"vistas": vistas}), encoding="utf-8")
    return tmp_path / "docs" / "vistas.yml"


def _names(tmp_path, model):
    return sorted(d.name for d in sldb_api.load_runtime_documents(tmp_path / ".sldb", None, include_linked=False) if str(d.model_name) == model)


def test_catalog_orphan_is_a_finding_and_prune_deletes_it(tmp_path, capsys):
    config = _catalog(tmp_path, ["arq", "flow"])
    assert main(["notations", "sync", "--catalog", str(config), "--store", str(tmp_path / ".sldb")]) == 0
    config = _catalog(tmp_path, ["arq"])
    capsys.readouterr()
    assert main(["notations", "sync", "--catalog", str(config), "--store", str(tmp_path / ".sldb")]) == 0
    captured = capsys.readouterr()
    assert "orphan SpecDoc:flow" in captured.out and "[spec-sync/orphan-spec]" in captured.err
    assert _names(tmp_path, "SpecDoc") == ["arq", "flow"]

    assert main(["notations", "sync", "--catalog", str(config), "--store", str(tmp_path / ".sldb"), "--prune", "--json"]) == 0
    reports = json.loads(capsys.readouterr().out)
    pruned = reports[-1]
    assert pruned["spec_id"] == "catalog vistas.yml" and "SpecDoc:flow" in pruned["deleted"]
    assert "SpecNodeDoc:flow.a" in pruned["deleted"] and any(d.startswith("RelationDoc:flow.") for d in pruned["deleted"])
    assert _names(tmp_path, "SpecDoc") == ["arq"] and not any(n.startswith("flow.") for n in _names(tmp_path, "SpecNodeDoc"))


def test_spec_sync_without_catalog_metadata_is_never_an_orphan(tmp_path, capsys):
    config = _catalog(tmp_path, ["arq"])
    assert main(["notations", "sync", "--spec", str(config.parent / "flow.yml"), "--store", str(tmp_path / ".sldb")]) == 0
    assert main(["notations", "sync", "--catalog", str(config), "--store", str(tmp_path / ".sldb"), "--prune"]) == 0
    assert _names(tmp_path, "SpecDoc") == ["arq", "flow"]


def test_unresolved_ref_is_a_finding_and_json_lists_reports(tmp_path, capsys):
    config = _catalog(tmp_path, ["arq"])
    assert main(["notations", "sync", "--spec", str(config.parent / "arq.yml"), "--json"]) == 0
    captured = capsys.readouterr()
    (report,) = json.loads(captured.out)
    assert report["spec_id"] == "arq" and report["problems"] == report["unresolved"] == ["arq.renderers: 'AtomDoc:atom-nope' no existe en el store"]
    assert "[spec-sync/unresolved-ref] arq" in captured.err


def test_check_writes_nothing(tmp_path, capsys):
    config = _catalog(tmp_path, ["arq", "flow"])
    assert main(["notations", "sync", "--catalog", str(config), "--check"]) == 0
    assert "Valid: v: arq.yml" in capsys.readouterr().out and _names(tmp_path, "SpecDoc") == []
