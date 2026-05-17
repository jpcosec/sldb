import json

from pathlib import Path

from sldb.cli import main as cli_main


def _write_models(base: Path) -> str:
    module = base / "link_models.py"
    module.write_text(
        '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

⸢rev•body⸥""".strip()
    title: str = Field(description="Document title.")
    body: str = Field(description="Document body.")


class RootDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

See [[⸢rev•linked_doc⸥]] for background.

![[⸢rev•transclusion_doc⸥]]""".strip()
    title: str = Field(description="Document title.")
    linked_doc: str = Field(description="Tracked linked document name.")
    transclusion_doc: str = Field(description="Tracked transcluded document name.")
''',
        encoding="utf-8",
    )
    return str(module.parent)


def test_recover_and_compose_links(tmp_path, capsys):
    pythonpath = _write_models(tmp_path)
    store = tmp_path / ".sldb"

    assert cli_main(["store", "init", "--path", str(tmp_path)]) == 0
    assert (
        cli_main(
            [
                "model",
                "add",
                "link_models:NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "model",
                "add",
                "link_models:RootDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    concept = tmp_path / "concept.md"
    concept.write_text("# Concept\n\nBackground info.\n", encoding="utf-8")
    constraints = tmp_path / "constraints.md"
    constraints.write_text(
        "# Constraints\n\nAlways validate first.\n", encoding="utf-8"
    )
    root = tmp_path / "root.md"
    root.write_text(
        "# Root\n\nSee [[concept]] for background.\n\n![[constraints]]\n",
        encoding="utf-8",
    )

    assert (
        cli_main(
            [
                "doc",
                "track",
                str(concept),
                "--model",
                "NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "doc",
                "track",
                str(constraints),
                "--model",
                "NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "doc",
                "track",
                str(root),
                "--model",
                "RootDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    rc = cli_main(
        [
            "recover",
            str(root),
            "--store",
            str(store),
            "--format",
            "json",
            "--include-transclusions",
        ]
    )
    recovered = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert recovered["root"] == "root"
    assert recovered["links"][0]["target"] == "concept"
    assert recovered["links"][0]["kind"] == "link"
    assert recovered["links"][0]["resolved"] is True
    assert recovered["links"][1]["target"] == "constraints"
    assert recovered["links"][1]["kind"] == "transclusion"
    assert recovered["unresolved"] == []

    capsys.readouterr()
    rc = cli_main(["compose", str(root), "--store", str(store)])
    composed = capsys.readouterr().out
    assert rc == 0
    assert "See [[concept]] for background." in composed
    assert "# Constraints" in composed
    assert "Always validate first." in composed


def test_docs_recover_and_compose_accept_tracked_doc_names_and_yaml(tmp_path, capsys):
    pythonpath = _write_models(tmp_path)
    store = tmp_path / ".sldb"

    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert (
        cli_main(
            [
                "models",
                "add",
                "link_models:NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "models",
                "add",
                "link_models:RootDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    concept = tmp_path / "concept.md"
    concept.write_text("# Concept\n\nBackground info.\n", encoding="utf-8")
    constraints = tmp_path / "constraints.md"
    constraints.write_text(
        "# Constraints\n\nAlways validate first.\n", encoding="utf-8"
    )
    root = tmp_path / "root.md"
    root.write_text(
        "# Root\n\nSee [[concept]] for background.\n\n![[constraints]]\n",
        encoding="utf-8",
    )

    assert (
        cli_main(
            [
                "docs",
                "track",
                str(concept),
                "--model",
                "NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "docs",
                "track",
                str(constraints),
                "--model",
                "NoteDoc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "docs",
                "track",
                str(root),
                "--model",
                "RootDoc",
                "--name",
                "root-doc",
                "--store",
                str(store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    capsys.readouterr()
    rc = cli_main(
        [
            "docs",
            "recover",
            "root-doc",
            "--store",
            str(store),
            "--format",
            "json",
            "--include-transclusions",
        ]
    )
    recovered = json.loads(capsys.readouterr().out)
    assert rc == 0
    assert {link["target"] for link in recovered["links"]} == {"concept", "constraints"}

    capsys.readouterr()
    rc = cli_main(
        [
            "docs",
            "compose",
            "root-doc",
            "--store",
            str(store),
            "--format",
            "yaml",
            "-o",
            "-",
        ]
    )
    out = capsys.readouterr().out
    assert rc == 0
    assert out.lstrip().startswith("root: root")
    assert "transclusions:" in out
