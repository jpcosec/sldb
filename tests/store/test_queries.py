import json

from pathlib import Path

from sldb.cli import main as cli_main


def _write_models(base: Path) -> str:
    module = base / "query_models.py"
    module.write_text(
        '''from pydantic import Field
from sldb import StructuredNLDoc


class ReadmeDoc(StructuredNLDoc):
    __family__ = "readme"
    __semantics__ = {"type": ["documentation", "Readme"]}
    __template__ = """# ⸢rev•title⸥

Status: ⸢rev•status⸥

Coverage: ⸢rev•coverage⸥

## Abstract

⸢optrev•abstract⸥

## Semantic Tags

- ⸢rev,list•semantic_tags⸥
""".strip()
    title: str = Field(description="Document title.")
    status: str = Field(description="Document status.")
    coverage: int = Field(description="Coverage percentage.")
    abstract: str | None = Field(default=None, description="Optional abstract.")
    semantic_tags: list = Field(description="Semantic tags.")


class TypeScriptReadmeDoc(ReadmeDoc):
    __semantics__ = {
        "type": ["documentation", "Readme"],
        "ecosystem": ["typescript"],
    }
''',
        encoding="utf-8",
    )
    return str(module.parent)


def _add_doc(store: Path, pythonpath: str, model: str, out: Path, payload: dict) -> int:
    return cli_main(
        [
            "doc",
            "add",
            "--model",
            model,
            "-o",
            str(out),
            json.dumps(payload),
            "--store",
            str(store),
            "--pythonpath",
            pythonpath,
        ]
    )


def test_structural_semantic_and_global_queries(tmp_path, capsys):
    pythonpath = _write_models(tmp_path)
    root = tmp_path / "root"
    child = tmp_path / "child"
    root.mkdir()
    child.mkdir()

    root_store = root / ".sldb"
    child_store = child / ".sldb"

    assert cli_main(["store", "init", "--path", str(root)]) == 0
    assert cli_main(["store", "init", "--path", str(child)]) == 0

    assert (
        cli_main(
            [
                "model",
                "add",
                "query_models:ReadmeDoc",
                "--canonical",
                "--store",
                str(root_store),
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
                "query_models:TypeScriptReadmeDoc",
                "--store",
                str(root_store),
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
                "query_models:TypeScriptReadmeDoc",
                "--store",
                str(child_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )

    assert (
        _add_doc(
            root_store,
            pythonpath,
            "ReadmeDoc",
            root / "readme.md",
            {
                "title": "Project Readme",
                "status": "accepted",
                "coverage": 90,
                "abstract": "Project overview.",
                "semantic_tags": ["project.sldb.database"],
            },
        )
        == 0
    )
    assert (
        _add_doc(
            root_store,
            pythonpath,
            "TypeScriptReadmeDoc",
            root / "local-ts.md",
            {
                "title": "Local TS Readme",
                "status": "draft",
                "coverage": 88,
                "abstract": "Local specialization.",
                "semantic_tags": ["project.sldb.database"],
            },
        )
        == 0
    )
    assert (
        _add_doc(
            child_store,
            pythonpath,
            "TypeScriptReadmeDoc",
            child / "ts-readme.md",
            {
                "title": "TS Readme",
                "status": "accepted",
                "coverage": 95,
                "abstract": "TypeScript project overview.",
                "semantic_tags": ["project.sldb.database"],
            },
        )
        == 0
    )

    assert (
        cli_main(
            [
                "store",
                "add",
                str(child_store),
                "--name",
                "child",
                "--store",
                str(root_store),
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "store",
                "semantic-map",
                "type.documentation.Readme",
                "type.documentation.Readme",
                "--store",
                str(child_store),
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "store",
                "semantic-map",
                "project.sldb.database",
                "project.sldb.database",
                "--store",
                str(child_store),
            ]
        )
        == 0
    )
    assert (
        cli_main(
            ["store", "update", "--store", str(root_store), "--pythonpath", pythonpath]
        )
        == 0
    )
    assert (
        cli_main(
            ["store", "update", "--store", str(child_store), "--pythonpath", pythonpath]
        )
        == 0
    )

    capsys.readouterr()
    assert (
        cli_main(["ls", "st", "--store", str(root_store), "--pythonpath", pythonpath])
        == 0
    )
    assert "st.{ReadmeDoc}" in capsys.readouterr().out.splitlines()

    capsys.readouterr()
    assert (
        cli_main(
            [
                "ls",
                "st.{ReadmeDoc+}",
                "--store",
                str(root_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert capsys.readouterr().out.splitlines() == ["local-ts", "readme"]

    capsys.readouterr()
    assert (
        cli_main(
            [
                "get",
                "st.{ReadmeDoc}.readme.title",
                "--store",
                str(root_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["result"] == "Project Readme"

    capsys.readouterr()
    assert (
        cli_main(
            [
                "glob",
                "st.{ReadmeDoc}.*.title",
                "--store",
                str(root_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert capsys.readouterr().out.splitlines() == ["st.{ReadmeDoc}.readme.title"]

    capsys.readouterr()
    assert (
        cli_main(
            [
                "find",
                "st.{ReadmeDoc}",
                "--where",
                'status = "accepted"',
                "--store",
                str(root_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert capsys.readouterr().out.splitlines() == ["st.{ReadmeDoc}.readme"]

    capsys.readouterr()
    assert (
        cli_main(
            [
                "get",
                "se.type.documentation.Readme",
                "--store",
                str(root_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["result"] == [
        "st.{ReadmeDoc}.readme",
        "st.{TypeScriptReadmeDoc}.local-ts",
    ]

    capsys.readouterr()
    assert (
        cli_main(
            [
                "glob",
                "se.project.**.database",
                "--store",
                str(root_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert capsys.readouterr().out.splitlines() == ["se.project.sldb.database"]

    capsys.readouterr()
    assert (
        cli_main(
            [
                "get",
                "gse.type.documentation.Readme",
                "--store",
                str(root_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert json.loads(capsys.readouterr().out)["result"] == [
        "child:st.{TypeScriptReadmeDoc}.ts-readme",
        "local:st.{ReadmeDoc}.readme",
        "local:st.{TypeScriptReadmeDoc}.local-ts",
    ]

    capsys.readouterr()
    assert (
        cli_main(
            [
                "ls",
                "gse.type.documentation.Readme.se.{child}",
                "--store",
                str(root_store),
                "--pythonpath",
                pythonpath,
            ]
        )
        == 0
    )
    assert capsys.readouterr().out.splitlines() == ["se.type.documentation.Readme"]
