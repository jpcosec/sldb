"""A notation may declare the standard it implements (`standard: {name, version}`)."""
import json
import shutil

import pytest
import yaml

from sldb.cli import main
from sldb.notations import builtin_notations
from sldb.notations.errors.validation_error import ValidationError
from sldb.notations.notation_files import load_notation


def _write(tmp_path, standard="absent", name="mi-notacion"):
    src = builtin_notations()[next(iter(builtin_notations()))]
    raw = yaml.safe_load(src.read_text(encoding="utf-8"))
    raw["name"] = name
    if standard != "absent":
        raw["standard"] = standard
    path = tmp_path / "n.yml"
    path.write_text(yaml.safe_dump(raw), encoding="utf-8")
    shutil.copy(src.parent / "default.yml", tmp_path / "default.yml") if (src.parent / "default.yml").exists() else None
    return path


def test_without_standard_stays_valid(tmp_path, capsys):
    path = _write(tmp_path)
    assert load_notation(path).standard is None
    assert main(["notations", "validate", str(path)]) == 0
    assert "standard" not in capsys.readouterr().out


def test_standard_is_loaded_and_shown(tmp_path, capsys):
    path = _write(tmp_path, {"name": "BPMN", "version": "2.0"})
    assert load_notation(path).standard.label() == "BPMN 2.0"
    assert main(["notations", "validate", str(path)]) == 0
    assert "standard: BPMN 2.0" in capsys.readouterr().out
    assert main(["notations", "validate", str(path), "--json"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["standard"] == {"name": "BPMN", "version": "2.0"} and out["findings"] == []


def test_version_is_optional(tmp_path):
    assert load_notation(_write(tmp_path, {"name": "UML"})).standard.version is None


@pytest.mark.parametrize("bad", [{"version": "2.0"}, {"name": ""}, {"name": "   ", "version": "2"}, {"name": "UML", "version": " "}, "UML"])
def test_invalid_standard_is_rejected_naming_the_notation(tmp_path, bad, capsys):
    path = _write(tmp_path, bad)
    with pytest.raises(ValidationError, match="mi-notacion.*standard"):
        load_notation(path)
    assert main(["notations", "validate", str(path)]) == 1
    assert "standard" in capsys.readouterr().out


def test_store_notation_lists_and_validates_with_its_standard(tmp_path, capsys):
    from sldb import api

    api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    path = _write(tmp_path, {"name": "BPMN", "version": "2.0"}, name="flujo")
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    raw.pop("palette", None)
    path.write_text(yaml.safe_dump(raw), encoding="utf-8")
    assert main(["notations", "sync", "--notation", str(path), "--store", str(store)]) == 0
    capsys.readouterr()
    assert main(["notations", "list", "--store", str(store)]) == 0
    listed = json.loads(capsys.readouterr().out)
    assert listed["standards"] == {"NotationDoc:flujo": {"name": "BPMN", "version": "2.0"}}
    assert main(["notations", "validate", "flujo", "--store", str(store)]) == 0
    assert "standard: BPMN 2.0" in capsys.readouterr().out


def test_list_without_standards_has_no_key(tmp_path):
    from sldb.api.notations.notation_listing import list_notations

    assert "standards" not in list_notations(tmp_path, None)
