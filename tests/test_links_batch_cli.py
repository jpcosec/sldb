from __future__ import annotations

import json
from pathlib import Path

import yaml

from sldb.cli import main as cli_main

MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

⸢rev•body⸥""".strip()
    title: str = Field(description="Document title.")
    body: str = Field(description="Document body.")
'''


def _store(tmp_path: Path) -> list[str]:
    (tmp_path / "link_models.py").write_text(MODELS, "utf-8")
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    base = ["--store", str(tmp_path / ".sldb")]
    assert cli_main(["models", "add", "link_models:NoteDoc", *base, "--pythonpath", str(tmp_path)]) == 0
    return base


def _doc(tmp_path: Path, name: str, body: str = "texto") -> Path:
    path = tmp_path / "docs" / f"{name}.md"
    path.parent.mkdir(exist_ok=True)
    path.write_text(f"# {name}\n\n{body}\n", "utf-8")
    return path


def _track_glob(tmp_path, base):
    args = ["docs", "track", "--glob", str(tmp_path / "docs" / "*.md"), "--model", "NoteDoc", *base, "--pythonpath", str(tmp_path)]
    return cli_main(args)


def _names(tmp_path, base, capsys) -> set[str]:
    capsys.readouterr()
    assert cli_main(["docs", "list", *base, "--format", "json"]) == 0
    return {d["name"] for d in json.loads(capsys.readouterr().out)["documents"]}


def test_track_glob_is_batch_and_skips_tracked(tmp_path, capsys):
    base = _store(tmp_path)
    _doc(tmp_path, "uno"), _doc(tmp_path, "dos")
    assert _track_glob(tmp_path, base) == 0
    assert _names(tmp_path, base, capsys) == {"uno", "dos"}
    _doc(tmp_path, "tres")
    assert _track_glob(tmp_path, base) == 0
    assert "skipped 2 already tracked" in capsys.readouterr().out
    assert _names(tmp_path, base, capsys) == {"uno", "dos", "tres"}


def test_prune_missing_untracks_only_vanished_files(tmp_path, capsys):
    base = _store(tmp_path)
    keep, gone = _doc(tmp_path, "uno"), _doc(tmp_path, "dos")
    assert _track_glob(tmp_path, base) == 0
    gone.unlink()
    assert cli_main(["stores", "update", *base, "--pythonpath", str(tmp_path)]) == 1
    assert cli_main(["stores", "update", *base, "--pythonpath", str(tmp_path), "--prune-missing"]) == 0
    assert "dos" in capsys.readouterr().out
    assert _names(tmp_path, base, capsys) == {"uno"} and keep.exists()


def test_recover_all_and_glob(tmp_path, capsys):
    base = _store(tmp_path)
    _doc(tmp_path, "uno", "ve [[dos.md]] y [rara:: [[dos.md]]]")
    _doc(tmp_path, "dos")
    assert _track_glob(tmp_path, base) == 0
    capsys.readouterr()
    assert cli_main(["docs", "recover", "--all", *base]) == 0
    assert "CUSTOM" in capsys.readouterr().out
    assert cli_main(["docs", "recover", "--all", "--fail-on-custom", *base]) == 1
    _doc(tmp_path, "dos", "roto [[no-existe]]")
    capsys.readouterr()
    assert cli_main(["docs", "recover", "--all", *base, "--format", "json"]) == 1
    kinds = {(p["doc"], p["kind"]) for p in json.loads(capsys.readouterr().out)["problems"]}
    assert ("dos", "unresolved") in kinds
    extra = _doc(tmp_path, "suelto", "[[tampoco]]")
    assert cli_main(["docs", "recover", "--glob", str(extra), *base]) == 1


def test_predicates_export_and_sync_roundtrip(tmp_path, capsys):
    base = _store(tmp_path)
    out = tmp_path / "predicates.yaml"
    assert cli_main(["predicates", "export", "--file", str(out), *base]) == 0
    exported = yaml.safe_load(out.read_text("utf-8"))
    assert exported["implements"]["axis"] == "HOW"
    exported["mio"] = {"axis": "what", "description": "propio"}
    exported["implements"]["description"] = "cambiada"
    out.write_text(yaml.safe_dump(exported), "utf-8")
    capsys.readouterr()
    assert cli_main(["predicates", "sync", "--file", str(out), *base]) == 0
    assert "created: mio" in capsys.readouterr().out
    assert cli_main(["predicates", "sync", "--file", str(out), *base]) == 0
    assert "created: -; updated: -; removed: -" in capsys.readouterr().out
    cli_main(["predicates", "show", "mio", *base, "--format", "json"])
    assert json.loads(capsys.readouterr().out)["axis"] == "WHAT"
    out.write_text(yaml.safe_dump({"mio": exported["mio"]}), "utf-8")
    assert cli_main(["predicates", "sync", "--file", str(out), *base]) == 0
    assert cli_main(["predicates", "show", "implements", *base]) == 0
    assert cli_main(["predicates", "sync", "--file", str(out), "--prune", *base]) == 0
    capsys.readouterr()
    cli_main(["predicates", "list", *base, "--format", "json"])
    assert [p["name"] for p in json.loads(capsys.readouterr().out)["predicates"]] == ["mio"]


def test_compose_render_links(tmp_path, capsys):
    base = _store(tmp_path)
    (tmp_path / "docs").mkdir(exist_ok=True)
    (tmp_path / "docs" / "dest.md").write_text("---\ntitle: El destino\n---\n# Dest\n\n## Parte\n", "utf-8")
    (tmp_path / "docs" / "sin.md").write_text("# Sin título\n", "utf-8")
    view = tmp_path / "docs" / "vista.md"
    view.write_text("[[dest.md]] [[sin.md]] [implements:: [[dest.md#Parte]]] [[roto]]\n", "utf-8")
    out = tmp_path / "out" / "vista.md"
    out.parent.mkdir()
    cli_main(["docs", "compose", str(view), *base, "--render-links", "-o", str(out)])
    text = out.read_text("utf-8")
    assert "[El destino](../docs/dest.md)" in text
    assert "[sin.md](../docs/sin.md)" in text
    assert "*implements*: [El destino](../docs/dest.md#parte)" in text
    assert "[[roto]]" in text
    capsys.readouterr()
    cli_main(["docs", "compose", str(view), *base, "--render-links"])
    assert "[El destino](dest.md)" in capsys.readouterr().out
