"""Findings are read through the document's authority and the store's policy
(docs/architecture/provenance.md §5), not a table fixed in code."""
from __future__ import annotations

import json

import pytest

import sldb.api as api
from sldb.api.stores.policy import Policy, Subject
from sldb.api.stores.store_declaration import StoreDeclaration, save_declaration
from sldb.cli import main as cli_main
from sldb.models.provenance_block import attach_block
from sldb.store.io import invalidate_index_cache

from .conftest import PAYLOAD


@pytest.mark.parametrize("code, subject, expected", [
    ("store/missing", Subject(), "error"),
    ("store/link-broken", Subject(), "error"),
    ("store/data-mutation", Subject(), "alert"),
    ("store/data-mutation", Subject(authority="source_raw", declared=True), "error"),
    ("store/data-mutation", Subject(authority="generated", declared=True), "error"),
    ("store/data-mutation", Subject(authority="authored", declared=True), "alert"),
    ("store/structural-noise", Subject(narrative=True), "allow"),
    ("store/structural-noise", Subject(authority="authored", declared=True), "allow"),
    ("store/structural-noise", Subject(), "alert"),
    ("store/contract-moved", Subject(), "alert"),
])
def test_sldbs_defaults_only_break_on_what_is_broken(code, subject, expected):
    assert Policy().response(code, "AnyDoc", subject) == expected


def test_a_declared_policy_wins_by_model_then_by_star_and_reads_codes_either_way():
    policy = Policy({"NoteDoc": {"structural_noise": "allow"}, "*": {"store/data-mutation": "error", "rewrite-loss": "hook: echo"}})
    assert policy.response("store/structural-noise", "NoteDoc") == "allow"
    assert policy.response("store/structural-noise", "Other") == "alert"
    assert policy.response("data_mutation", "Other") == "error"
    assert (policy.level("store/rewrite-loss", "X"), policy.level("store/structural-noise", "NoteDoc")) == ("alert", None)


def _check(api_store, capsys, *extra) -> tuple[int, dict]:
    capsys.readouterr()
    code = cli_main(["stores", "check", "--store", str(api_store.store), "--pythonpath", api_store.pythonpath, "--format", "json", *extra])
    return code, json.loads(capsys.readouterr().out.splitlines()[0])


def test_a_hand_edit_is_an_alert_unless_the_document_declared_an_authority_that_forbids_it(api_store, capsys):
    path = api_store.root / "login.md"
    path.write_text(path.read_text(encoding="utf-8").replace("Broken login", "Edited by hand"), encoding="utf-8")
    code, report = _check(api_store, capsys)
    assert code == 0 and [a["code"] for a in report["alerts"]] == ["store/data-mutation"]
    api.update_store_indexes(api_store.store, api_store.pythonpath)
    path.write_text(attach_block(path.read_text(encoding="utf-8"), {"by": "human:jp", "at": 0, "authority": "source_raw"}), encoding="utf-8")
    api.update_store_indexes(api_store.store, api_store.pythonpath)
    invalidate_index_cache()
    path.write_text(path.read_text(encoding="utf-8").replace("Edited by hand", "Edited again"), encoding="utf-8")
    code, report = _check(api_store, capsys)
    assert code == 1 and [e["code"] for e in report["errors"]] == ["store/data-mutation"], "a raw source does not mutate"
    save_declaration(api_store.store, StoreDeclaration(policy={"TicketDoc": {"data_mutation": "alert"}}))
    code, report = _check(api_store, capsys)
    assert code == 0 and [a["code"] for a in report["alerts"]] == ["store/data-mutation"], "the store's policy wins"


def test_apply_runs_the_hook_with_the_finding_and_reindexes_when_asked(api_store, capsys):
    path = api_store.root / "login.md"
    path.write_text(path.read_text(encoding="utf-8").replace("Broken login", "Edited by hand"), encoding="utf-8")
    save_declaration(api_store.store, StoreDeclaration(policy={"TicketDoc": {"data_mutation": "hook: sh -c 'cat > hook.json'"}}))
    code, report = _check(api_store, capsys, "--apply")
    assert code == 0 and report["alerts"][0]["fix"].startswith("policy: hook:")
    assert json.loads((api_store.root / "hook.json").read_text(encoding="utf-8"))["code"] == "store/data-mutation"
    save_declaration(api_store.store, StoreDeclaration(policy={"TicketDoc": {"data_mutation": "reindex"}}))
    code, report = _check(api_store, capsys, "--apply")
    assert code == 0 and report["alerts"][0]["fix"].startswith("policy: reindex")
    invalidate_index_cache()
    code, report = _check(api_store, capsys)
    assert code == 0 and report["alerts"] == [], "reindexed: nothing moves against the index now"


def test_the_write_time_refusal_of_noise_follows_the_same_policy(api_store):
    noisy = api_store.root / "noisy.md"
    noisy.write_text("# Noisy\n\nStatus: open\n\n## Tags\n\n- a\n\n## Extra\n\nfree text\n", encoding="utf-8")
    with pytest.raises(Exception, match="ruido estructural"):
        api.track_document_file(api_store.store, "TicketDoc", noisy, "noisy", api_store.pythonpath)
    save_declaration(api_store.store, StoreDeclaration(policy={"TicketDoc": {"structural_noise": "allow"}}))
    api.track_document_file(api_store.store, "TicketDoc", noisy, "noisy", api_store.pythonpath)
