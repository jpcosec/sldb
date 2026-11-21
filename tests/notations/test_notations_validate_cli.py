"""`sldb notations validate <name|path>`: type detection, findings, --json and exit codes."""
import json
import shutil

import yaml

from sldb.cli import main
from sldb.notations import builtin_notations
from sldb.notations.palette_files import builtin_palettes
from tests.notations.test_spec_sync import ARQ


def _first_notation():
    return next(iter(builtin_notations()))


def _bad_palette(tmp_path):
    raw = yaml.safe_load(builtin_palettes()["default"].read_text(encoding="utf-8"))
    raw["ink"] = {"light": "#ffffff", "dark": "#0d1117"}  # unreadable on every fill
    path = tmp_path / "bad-palette.yml"
    path.write_text(yaml.safe_dump(raw), encoding="utf-8")
    return path


def test_builtin_notation_by_name_is_valid(capsys):
    assert main(["notations", "validate", _first_notation()]) == 0
    assert "error" not in capsys.readouterr().out


def test_builtin_palette_by_name_is_valid():
    assert "default" not in builtin_notations()
    assert main(["notations", "validate", "default"]) == 0


def test_valid_files_of_each_type(tmp_path):
    notation = tmp_path / "n.yml"
    shutil.copy(builtin_notations()[_first_notation()], notation)
    palette = tmp_path / "p.yml"
    shutil.copy(builtin_palettes()["default"], palette)
    spec = tmp_path / "s.json"
    spec.write_text(json.dumps(ARQ), encoding="utf-8")
    assert main(["notations", "validate", str(palette)]) == 0
    assert main(["notations", "validate", str(spec)]) == 0
    assert main(["notations", "validate", str(notation)]) == 0


def test_palette_with_low_contrast_is_an_error(tmp_path, capsys):
    path = _bad_palette(tmp_path)
    assert main(["notations", "validate", str(path)]) == 1
    assert "[notations/palette-invalid]" in capsys.readouterr().out


def test_invalid_spec_is_an_error_and_json_lists_it(tmp_path, capsys):
    spec = tmp_path / "bad.yml"
    spec.write_text(yaml.safe_dump({"id": "x", "title": "x", "type": "nope"}), encoding="utf-8")
    assert main(["notations", "validate", str(spec), "--json"]) == 1
    findings = json.loads(capsys.readouterr().out)
    assert findings[0]["level"] == "error" and findings[0]["code"] == "notations/spec-invalid"


def test_invalid_notation_file_is_an_error(tmp_path, capsys):
    path = tmp_path / "n.yml"
    path.write_text("name: x\n", encoding="utf-8")
    assert main(["notations", "validate", str(path)]) == 1
    assert "[notations/notation-invalid]" in capsys.readouterr().out


def test_unknown_name_exits_2(capsys):
    assert main(["notations", "validate", "no-such-thing"]) == 2
    assert "unknown notation, palette or spec: no-such-thing" in capsys.readouterr().err


def test_name_in_two_types_is_validated_as_notation_with_an_alert(monkeypatch, capsys):
    import sldb.cli.commands.notations_validate as mod

    monkeypatch.setattr(mod, "_kinds_of_name", lambda name, store: ["notation", "palette"])
    assert main(["notations", "validate", _first_notation(), "--json"]) == 0
    findings = json.loads(capsys.readouterr().out)
    assert [f["level"] for f in findings] == ["alert"] and findings[0]["code"] == "notations/ambiguous-name"


def _store_with(tmp_path, notation_name, palette_name):
    """A store holding a notation and a palette that exist only there (no builtin has these names)."""
    import sldb.api as api

    api.init_store(tmp_path)
    store = tmp_path / ".sldb"
    palette = yaml.safe_load(builtin_palettes()["default"].read_text(encoding="utf-8"))
    palette["name"] = palette_name
    palette_file = tmp_path / f"{palette_name}.yml"
    palette_file.write_text(yaml.safe_dump(palette), encoding="utf-8")
    notation = yaml.safe_load(builtin_notations()[_first_notation()].read_text(encoding="utf-8"))
    notation["name"] = notation_name
    notation.pop("palette", None)
    notation_file = tmp_path / f"{notation_name}.yml"
    notation_file.write_text(yaml.safe_dump(notation), encoding="utf-8")
    assert main(["notations", "sync", "--palette", str(palette_file), "--store", str(store)]) == 0
    assert main(["notations", "sync", "--notation", str(notation_file), "--store", str(store)]) == 0
    return store


def test_names_that_exist_only_in_the_store_are_valid(tmp_path, capsys):
    store = _store_with(tmp_path, "only-in-store-notation", "only-in-store-palette")
    capsys.readouterr()
    assert main(["notations", "validate", "only-in-store-notation", "--store", str(store)]) == 0
    assert main(["notations", "validate", "only-in-store-palette", "--store", str(store)]) == 0
    assert "error" not in capsys.readouterr().out
    assert main(["notations", "validate", "only-in-store-palette"]) == 2  # without --store it is unknown


def test_invalid_store_palette_is_an_error(tmp_path, capsys):
    store = _store_with(tmp_path, "only-in-store-notation", "only-in-store-palette")
    doc = tmp_path / "sldb" / "palettes" / "only-in-store-palette.md"
    text = doc.read_text(encoding="utf-8")
    head, front, body = text.split("---\n", 2)
    data = yaml.safe_load(front)
    data["ink"] = {"light": "#ffffff", "dark": "#0d1117"}  # unreadable on every fill
    doc.write_text("---\n" + yaml.safe_dump(data) + "---\n" + body, encoding="utf-8")
    capsys.readouterr()
    assert main(["notations", "validate", "only-in-store-palette", "--store", str(store)]) == 1
    assert "[notations/palette-invalid]" in capsys.readouterr().out


def test_invalid_store_notation_is_an_error(tmp_path, capsys):
    store = _store_with(tmp_path, "only-in-store-notation", "only-in-store-palette")
    doc = tmp_path / "sldb" / "notations" / "only-in-store-notation" / "notation.md"
    text = doc.read_text(encoding="utf-8")
    head, front, body = text.split("---\n", 2)
    data = yaml.safe_load(front)
    data["layout"] = "not-a-mapping"
    doc.write_text("---\n" + yaml.safe_dump(data) + "---\n" + body, encoding="utf-8")
    capsys.readouterr()
    assert main(["notations", "validate", "only-in-store-notation", "--store", str(store)]) == 1
    assert "[notations/notation-invalid]" in capsys.readouterr().out
