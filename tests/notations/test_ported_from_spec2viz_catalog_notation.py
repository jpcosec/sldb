"""Portado de spec2viz tests/test_catalog_notation.py: `notation` por vista en vistas.yml; el sync de
un spec conserva el catalogo (categoria, nav, resumen), contra `sldb notations sync`.

Equivalencias de CLI: `spec2viz catalog sync --config X` es `sldb notations sync --catalog X`;
`spec2viz catalog validate --config X` es `sldb notations sync --catalog X --check`;
`spec2viz diagram sync S --notation N` es `sldb notations sync --spec S --notation N`;
`spec2viz notation sync N` es `sldb notations sync --notation N`. En sldb los errores tipados
del catalogo salen por stderr (`Invalid: ...: <Error>: ...`) en vez de stdout.

La fixture activity.lanes.yml ya existia identica en tests/fixtures/specs/.

Casos no portados: ninguno.
"""
import shutil
from pathlib import Path

import pytest
import yaml

import sldb.api as sldb_api
from sldb.api.notations import resolve_spec_notation
from sldb.cli import main
from sldb.notations.exceptions import NotationMismatchError, UnknownNotationError

SPEC = Path(__file__).parent.parent / "fixtures" / "specs" / "activity.lanes.yml"
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


def _catalog(config, tmp_path, *extra):
    return main(["notations", "sync", "--catalog", str(config), "--store", str(tmp_path / ".sldb"), *extra])


def test_diagram_sync_with_notation_keeps_the_catalog_metadata(tmp_path):
    config = _project(tmp_path)
    assert _catalog(config, tmp_path) == 0
    assert main(["notations", "sync", "--spec", str(config.parent / "lanes.yml"), "--store", str(tmp_path / ".sldb"),
                 "--notation", str(config.parent / "notations" / "flow-own.yml")]) == 0
    doc = _spec_doc(tmp_path)
    assert (doc["category"], doc["nav"], doc["summary"]) == ("Flujos", "Carriles", "Aprobacion")
    assert doc["notation"] == "NotationDoc:flow-own"


def test_view_notation_path_is_relative_to_the_vistas_yml(tmp_path):
    config = _project(tmp_path, "notations/flow-own.yml")
    assert _catalog(config, tmp_path) == 0
    doc = _spec_doc(tmp_path)
    assert doc["notation"] == "NotationDoc:flow-own" and doc["category"] == "Flujos"


def test_view_notation_name_resolves_against_the_store(tmp_path, capsys):
    config = _project(tmp_path, "flow-own")
    # sin la notacion en el store, el nombre no resuelve: error tipado y nada se escribe
    assert _catalog(config, tmp_path) == 1
    assert "UnknownNotationError" in capsys.readouterr().err
    assert not any(str(d.model_name) == "SpecDoc" for d in sldb_api.load_runtime_documents(tmp_path / ".sldb", None, include_linked=False))
    # una vez en el store, resuelve por nombre
    assert main(["notations", "sync", "--notation", str(config.parent / "notations" / "flow-own.yml"), "--store", str(tmp_path / ".sldb")]) == 0
    assert _catalog(config, tmp_path) == 0
    assert _spec_doc(tmp_path)["notation"] == "NotationDoc:flow-own"


def test_view_notation_builtin_name_and_absent_field(tmp_path):
    config = _project(tmp_path, "activity")
    assert _catalog(config, tmp_path) == 0
    assert _spec_doc(tmp_path)["notation"] == "NotationDoc:activity"


@pytest.mark.parametrize("value, error", [
    ("notations/missing.yml", "UnknownNotationError"),
    ("no-such-notation", "UnknownNotationError"),
    ("deployment", "NotationMismatchError"),
])
def test_catalog_validate_and_sync_give_typed_errors(tmp_path, capsys, value, error):
    config = _project(tmp_path, value)
    for extra in (["--check"], []):
        assert _catalog(config, tmp_path, *extra) == 1, extra
        captured = capsys.readouterr()
        assert error in captured.err, (extra, captured.out, captured.err)


def test_catalog_validate_passes_and_resolver_raises_typed_errors(tmp_path, capsys):
    config = _project(tmp_path, "notations/flow-own.yml")
    assert _catalog(config, tmp_path, "--check") == 0
    assert "Valid: lanes" in capsys.readouterr().out
    with pytest.raises(NotationMismatchError):
        resolve_spec_notation("statechart", "activity", "activity.x")
    with pytest.raises(UnknownNotationError):
        resolve_spec_notation("nope", "activity", "activity.x", tmp_path / ".sldb")
