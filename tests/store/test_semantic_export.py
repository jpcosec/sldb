from __future__ import annotations

import json
from pathlib import Path

from sldb.cli import main as cli_main
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.export import export_kgdb_semantic_payload


def _write_model(project: Path) -> str:
    package = project / "tmpdocs"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "models.py").write_text(
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        "class TaskDoc(StructuredNLDoc):\n"
        "    __template__ = '# ⸢rev•title⸥\\n\\n⸢rev•body⸥'\n"
        "    __semantics__ = {'domain': ['workflow', 'task'], 'system': 'desk'}\n"
        "    title: str = Field(description='Title')\n"
        "    body: str = Field(description='Body')\n",
        encoding="utf-8",
    )
    return "tmpdocs.models:TaskDoc"


def _build_tracked_store(tmp_path: Path, capsys) -> tuple[Path, Path]:
    model_ref = _write_model(tmp_path)
    store = tmp_path / ".sldb"
    doc = tmp_path / "task.md"
    doc.write_text("# Alpha\n\n## Overview\n\nBody text\n", encoding="utf-8")

    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert (
        cli_main(
            [
                "models",
                "add",
                model_ref,
                "--store",
                str(store),
                "--pythonpath",
                str(tmp_path),
                "--canonical",
            ]
        )
        == 0
    )
    assert (
        cli_main(
            [
                "docs",
                "track",
                str(doc),
                "--model",
                "TaskDoc",
                "--store",
                str(store),
                "--pythonpath",
                str(tmp_path),
            ]
        )
        == 0
    )
    capsys.readouterr()
    return store, tmp_path


def test_stores_semantic_export_kgdb_json_from_tracked_store(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)

    rc = cli_main(
        [
            "stores",
            "semantic-export",
            "--store",
            str(store),
            "--pythonpath",
            str(root),
            "--format",
            "kgdb",
            "--rebuild",
        ]
    )

    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["contract"]["name"] == "sldb_kgdb_semantic_export"
    assert payload["contract"]["version"] == 1
    assert payload["producer"]["name"] == "sldb"
    assert payload["store"]["root"] == str(root)
    assert payload["store"]["store_path"] == str(store)
    assert payload["store"]["hash_a"]
    assert payload["models"] == [
        {
            "name": "TaskDoc",
            "model_ref": "tmpdocs.models:TaskDoc",
            "path": "tmpdocs/models.py",
            "models_index": ".sldb/core/models/TaskDoc.yaml",
            "documents_index": ".sldb/core/documents/TaskDoc.yaml",
            "sections_index": ".sldb/runtime/sections/TaskDoc.yaml",
            "version": 1,
            "canonical": True,
            "family": None,
            "semantics": [
                "domain.workflow.task",
                "representation.markdown",
                "source.document.markdown",
                "system.desk",
            ],
            "base_models": [],
            "hash_b": payload["models"][0]["hash_b"],
        }
    ]
    assert payload["documents"][0]["id"] == "TaskDoc:task"
    assert payload["documents"][0]["semantic_tags"] == [
        "domain.workflow.task",
        "representation.markdown",
        "source.document.markdown",
        "system.desk",
    ]
    assert [section["path"] for section in payload["sections"]] == [
        "alpha",
        "alpha/overview",
    ]
    assert "domain.workflow.task" in {
        node["id"] for node in payload["semantic_dag"]["nodes"]
    }


def test_export_kgdb_semantic_payload_api(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)

    payload = export_kgdb_semantic_payload(
        store,
        root,
        resolve_model_ref,
        str(root),
        rebuild=True,
        command=["test"],
    )

    assert payload["producer"]["command"] == ["test"]
    assert payload["documents"][0]["id"] == "TaskDoc:task"
    assert payload["sections"][0]["id"] == "TaskDoc:task#alpha"
