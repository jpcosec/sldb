"""`sldb docs create -o <relative>` writes relative to the process cwd, not the project root."""

from __future__ import annotations

import json

from sldb.cli import main as cli_main

from tests.test_cli_v2 import _write_models


def test_docs_create_relative_output_resolves_against_cwd(tmp_path, monkeypatch):
    pythonpath = _write_models(tmp_path)
    root = tmp_path / "repo"
    sub = root / "sub"
    sub.mkdir(parents=True)
    store = root / ".sldb"
    assert cli_main(["stores", "init", "--path", str(root)]) == 0
    assert cli_main(["models", "add", "cli_v2_models:RoadmapDoc", "--store", str(store), "--pythonpath", pythonpath]) == 0
    monkeypatch.chdir(sub)
    payload = json.dumps({"title": "T", "status": "draft", "tasks": ["a"], "semantic_tags": ["project.sldb.database"]})
    assert cli_main(["docs", "create", "--model", "RoadmapDoc", "-o", "sub.md", payload, "--store", str(store), "--pythonpath", pythonpath]) == 0
    assert (sub / "sub.md").is_file()
    assert not (root / "sub.md").exists()
