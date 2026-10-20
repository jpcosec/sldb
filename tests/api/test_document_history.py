"""`sldb docs history`: the document's past from git, each version with who signed it and what moved."""
from __future__ import annotations

import json
import subprocess

import sldb.api as api
from sldb.api.documents.document_history import document_history
from sldb.cli import main as cli_main

from .conftest import PAYLOAD


def _git(root, *argv):
    subprocess.run(["git", *argv], cwd=root, check=True, capture_output=True)


def _repo(api_store):
    _git(api_store.root, "init", "-q")
    _git(api_store.root, "config", "user.email", "t@t")
    _git(api_store.root, "config", "user.name", "t")
    (api_store.root / ".gitignore").write_text(".sldb/\n", encoding="utf-8")
    _git(api_store.root, "add", "-A")
    _git(api_store.root, "commit", "-qm", "one: tracked by hand, no block")
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "Signed"}, api_store.pythonpath, actor="human:jp")
    _git(api_store.root, "commit", "-qam", "two: saved through the api")


def test_each_version_says_who_signed_it_and_which_fields_moved(api_store):
    _repo(api_store)
    newest, oldest = document_history(api_store.store, "login", api_store.pythonpath)
    assert (newest["by"], newest["authority"], newest["declared"], newest["changed_fields"]) == ("human:jp", "generated", True, ["title"])
    assert (oldest["by"], oldest["declared"], oldest["changed_fields"]) == ("agent", False, [])
    assert newest["source_hash"] != oldest["source_hash"] and len(newest["commit"]) == 40


def test_the_cli_prints_it_and_since_narrows_it(api_store, capsys):
    _repo(api_store)
    args = ["docs", "history", "login", "--store", str(api_store.store), "--pythonpath", api_store.pythonpath]
    assert cli_main([*args, "--format", "json"]) == 0
    entries = json.loads(capsys.readouterr().out)["entries"]
    assert [e["changed_fields"] for e in entries] == [["title"], []]
    assert cli_main(args) == 0
    out = capsys.readouterr().out
    assert "2 version(s)" in out and "human:jp (generated)  fields: title" in out and "[no block]" in out
    assert cli_main([*args, "--since", "2999-01-01", "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["entries"] == []


def test_outside_git_the_history_is_empty_and_says_so(api_store, capsys):
    assert document_history(api_store.store, "login", api_store.pythonpath) == []
    assert cli_main(["docs", "history", "login", "--store", str(api_store.store), "--pythonpath", api_store.pythonpath]) == 0
    assert "no git history" in capsys.readouterr().out
