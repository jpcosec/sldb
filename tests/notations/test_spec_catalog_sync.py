"""vistas.yml: notation por vista; el sync de un spec conserva el catalogo (categoria, nav, resumen).

Portado de spec2viz `tests/test_catalog_notation.py` con el minimo cambio: la CLI click de
spec2viz pasa a `sldb notations sync` (`catalog sync --config` -> `--catalog`, `catalog validate`
-> `--catalog --check`, `diagram sync SPEC` -> `--spec SPEC`, `notation sync FILE` ->
`--notation FILE`), las excepciones salen de `sldb.notations.exceptions` y el resolvedor de
`sldb.api.notations`.
"""
import shutil
from pathlib import Path

import pytest
import yaml

import sldb.api as sldb_api
from sldb.cli import main
from sldb.notations.exceptions import NotationMismatchError, UnknownNotationError

REPO = Path(__file__).parent.parent.parent
SPEC = REPO / "tests" / "fixtures" / "specs" / "activity.lanes.yml"
OWN_NOTATION = {
    "name": "flow-own", "title": "Own flow", "diagram_type": "activity", "layout": {"kind": "graph"},
    "glyphs": [{"id": "step", "model": "SpecNodeDoc", "shape": "box"}],
    "links": [{"id": "next", "relation": "next"}],
}


def _project(tmp_path, view_notation=None):
    sldb_api.init_store(tmp_path)
    docs = tmp_path / "docs"
    (docs / "notations").mkdir(parents=True)
    shutil.copy(SPEC, docs / "lanes.yml")
    (docs / "notations" / "flow-own.yml").write_text(yaml.safe_dump(OWN_NOTATION), encoding="utf-8")
    vista = {"id": "lanes", "category": "Flujos", "nav": "Carriles", "desc": "Aprobacion", "specs": ["lanes.yml"]}
    if view_notation is not None:
        vista["notation"] = view_notation
    (docs / "vistas.yml").write_text(yaml.safe_dump({"vistas": [vista]}), encoding="utf-8")
    return docs / "vistas.yml"


def _spec_doc(tmp_path):
    return next(d.payload for d in sldb_api.load_runtime_documents(tmp_path / ".sldb", None, include_linked=False)
                if str(d.model_name) == "SpecDoc" and d.name == "activity.lanes")


def _run(capsys, *argv):
    rc = main(["notations", "sync", *argv])
    captured = capsys.readouterr()
    return rc, captured.out + captured.err


def test_diagram_sync_with_notation_keeps_the_catalog_metadata(tmp_path, capsys):
    config = _project(tmp_path)
    assert _run(capsys, "--catalog", str(config), "--store", str(tmp_path / ".sldb"))[0] == 0
    rc, output = _run(capsys, "--spec", str(config.parent / "lanes.yml"), "--store", str(tmp_path / ".sldb"),
                      "--notation", str(config.parent / "notations" / "flow-own.yml"))
    assert rc == 0, output
    doc = _spec_doc(tmp_path)
    assert (doc["category"], doc["nav"], doc["summary"]) == ("Flujos", "Carriles", "Aprobacion")
    assert doc["notation"] == "NotationDoc:flow-own"


def test_view_notation_path_is_relative_to_the_vistas_yml(tmp_path, capsys):
    config = _project(tmp_path, "notations/flow-own.yml")
    rc, output = _run(capsys, "--catalog", str(config), "--store", str(tmp_path / ".sldb"))
    assert rc == 0, output
    doc = _spec_doc(tmp_path)
    assert doc["notation"] == "NotationDoc:flow-own" and doc["category"] == "Flujos"


def test_view_notation_name_resolves_against_the_store(tmp_path, capsys):
    config = _project(tmp_path, "flow-own")
    # sin la notacion en el store, el nombre no resuelve: error tipado y nada se escribe
    rc, output = _run(capsys, "--catalog", str(config), "--store", str(tmp_path / ".sldb"))
    assert rc == 1 and "UnknownNotationError" in output
    assert not any(str(d.model_name) == "SpecDoc" for d in sldb_api.load_runtime_documents(tmp_path / ".sldb", None, include_linked=False))
    # una vez en el store, resuelve por nombre
    assert _run(capsys, "--notation", str(config.parent / "notations" / "flow-own.yml"), "--store", str(tmp_path / ".sldb"))[0] == 0
    rc, output = _run(capsys, "--catalog", str(config), "--store", str(tmp_path / ".sldb"))
    assert rc == 0, output
    assert _spec_doc(tmp_path)["notation"] == "NotationDoc:flow-own"


def test_view_notation_builtin_name_and_absent_field(tmp_path, capsys):
    config = _project(tmp_path, "activity")
    assert _run(capsys, "--catalog", str(config), "--store", str(tmp_path / ".sldb"))[0] == 0
    assert _spec_doc(tmp_path)["notation"] == "NotationDoc:activity"


@pytest.mark.parametrize("value, error", [
    ("notations/missing.yml", "UnknownNotationError"),
    ("no-such-notation", "UnknownNotationError"),
    ("deployment", "NotationMismatchError"),
])
def test_catalog_validate_and_sync_give_typed_errors(tmp_path, capsys, value, error):
    config = _project(tmp_path, value)
    for command in (["--check"], []):
        rc, output = _run(capsys, "--catalog", str(config), *command, "--store", str(tmp_path / ".sldb"))
        assert rc == 1 and error in output, (command, output)


def test_catalog_validate_passes_and_resolver_raises_typed_errors(tmp_path, capsys):
    from sldb.api.notations import resolve_spec_notation

    config = _project(tmp_path, "notations/flow-own.yml")
    rc, output = _run(capsys, "--catalog", str(config), "--check", "--store", str(tmp_path / ".sldb"))
    assert rc == 0 and "Valid: lanes" in output
    with pytest.raises(NotationMismatchError):
        resolve_spec_notation("statechart", "activity", "activity.x")
    with pytest.raises(UnknownNotationError):
        resolve_spec_notation("nope", "activity", "activity.x", tmp_path / ".sldb")
