"""H1 (inbox 3895e9f7): `stores check` over documents their model rejects names each one as
`store/doc-invalid` and diagnoses the rest of the store, instead of leaving with `Unexpected`."""

from __future__ import annotations

import json

from sldb import api
from sldb.cli import main as cli_main

from tests.store.invalid_memo_store import store_with_invalid  # noqa: F401 - the fixture


def test_stores_check_names_each_invalid_document_and_goes_on(store_with_invalid, capsys):
    root, sp, py = store_with_invalid
    rc = cli_main(["stores", "check", "--store", str(sp), "--pythonpath", py, "--format", "json"])
    out = capsys.readouterr()
    assert "Unexpected" not in out.out + out.err
    payload = json.loads(out.out.strip().splitlines()[0])
    assert rc == 1 and payload["valid"] is False
    invalid = [e for e in payload["errors"] if e["code"] == "store/doc-invalid"]
    assert [e["subject"] for e in invalid] == ["Memo:a", "Memo:b"]
    assert invalid[0]["what"].startswith("invalid: Memo rejects a.md: 1 validation error(s); first: status: ")
    assert "errors.pydantic.dev" not in invalid[0]["what"]
    notes = {d["name"]: d["note"] for d in payload["models"][0]["documents"]}
    assert notes == {"a": "doc_invalid", "b": "doc_invalid", "c": "ok"}


def test_an_invalid_document_is_one_finding_not_one_per_subsystem(store_with_invalid):
    root, sp, py = store_with_invalid
    report = api.check_store(sp, root, py)
    about_a = [f for f in report["errors"] + report["alerts"] if f["subject"] == "Memo:a"]
    assert [f["code"] for f in about_a] == ["store/doc-invalid"]
