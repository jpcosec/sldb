from __future__ import annotations

import json
from pathlib import Path

from sldb.cli import main as cli_main
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.export import export_semantic_payload


def _write_model(project: Path) -> str:
    package = project / "tmpdocs"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "models.py").write_text(
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        "class TaskDoc(StructuredNLDoc):\n"
        "    __template__ = '# ⸢rev•title⸥\\n\\n## Overview\\n\\n⸢rev•body⸥'\n"
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


def test_stores_semantic_export_json_from_tracked_store(tmp_path, capsys):
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
            "sldb",
            "--rebuild",
        ]
    )

    assert rc == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["contract"]["name"] == "sldb_semantic_export"
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
            # v1's single key, plus the semantic names and the model node's two children:
            # `hash_b` could not say whether the roster or the contract moved the node.
            "hash_b": payload["models"][0]["hash_b"],
            "model_hash": payload["models"][0]["hash_b"],
            "roster_hash": payload["models"][0]["roster_hash"],
            "contract_hash": payload["models"][0]["contract_hash"],
        }
    ]
    assert payload["models"][0]["contract_hash"], "the contract is part of the exported node"
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


def test_export_semantic_payload_api(tmp_path, capsys):
    store, root = _build_tracked_store(tmp_path, capsys)

    payload = export_semantic_payload(
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


def test_producer_version_matches_pyproject():
    import re
    from pathlib import Path
    from sldb.store.package_version import package_version as _version

    text = (Path(__file__).resolve().parents[2] / "pyproject.toml").read_text(encoding="utf-8")
    assert _version() == re.search(r'^version\s*=\s*"([^"]+)"', text, re.M).group(1)


def test_a_payload_written_under_the_old_contract_name_is_still_read():
    """sldb writes `sldb_semantic_export`; an export written as `sldb_kgdb_semantic_export`
    before kgdb merged into sldb is read, never written."""
    import json
    from pathlib import Path

    import pytest

    from sldb.store.graph.ingest_sldb import sldb_semantic_export_to_snapshot

    payload = json.loads((Path(__file__).resolve().parents[2] / "contracts" / "fixtures" / "sldb_semantic_export.v1.json").read_text(encoding="utf-8"))
    new_nodes = len(sldb_semantic_export_to_snapshot(payload).nodes)
    payload["contract"]["name"] = "sldb_kgdb_semantic_export"
    assert len(sldb_semantic_export_to_snapshot(payload).nodes) == new_nodes
    payload["contract"]["name"] = "something_else"
    with pytest.raises(ValueError, match="sldb_semantic_export"):
        sldb_semantic_export_to_snapshot(payload)
