"""Provenance (docs/architecture/provenance.md): the `sldb` block every write signs, what a
document without one reads as, and what a stamp does and does not move."""
from __future__ import annotations

import json

import pytest

import sldb.api as api
from sldb.api.actor import current_actor, set_actor
from sldb.api.documents.frontmatter_keys import undeclared_frontmatter_keys
from sldb.api.documents.provenance_stamp import provenance_of, stamped
from sldb.cli import main as cli_main
from sldb.models.provenance_block import attach_block, read_block, strip_block
from sldb.runtime.validation import extract_model_data

from .conftest import MODULE, PAYLOAD

BLOCK = {"by": "human:jp", "at": "2026-10-20T10:00:00Z", "authority": "authored"}


@pytest.fixture(autouse=True)
def _no_process_actor():
    set_actor(None)
    yield
    set_actor(None)


def test_the_block_goes_first_in_a_frontmatter_and_makes_one_when_there_is_none():
    plain = "# T\n\nbody\n"
    with_fm = "---\nkind: unclear\n---\n\n# T\n\nbody\n"
    assert attach_block(plain, BLOCK) == "---\nsldb:\n  by: human:jp\n  at: '2026-10-20T10:00:00Z'\n  authority: authored\n---\n\n# T\n\nbody\n"
    assert attach_block(with_fm, BLOCK).startswith("---\nsldb:\n  by: human:jp\n") and "kind: unclear\n---\n\n# T" in attach_block(with_fm, BLOCK)
    for text in (plain, with_fm):
        assert read_block(attach_block(text, BLOCK)) == BLOCK
        assert strip_block(attach_block(text, BLOCK)) == text, "strip is attach's inverse"
    assert read_block(plain) is None and strip_block(plain) == plain


def test_a_document_without_a_block_reads_as_agent_zero_generated():
    found = provenance_of("# T\n\nbody\n")
    assert (found.by, found.at, found.authority, found.declared) == ("agent", 0, "generated", False)


def test_create_signs_with_the_actor_the_time_and_the_models_authority(api_store):
    created = api.create_document(api_store.store, "TicketDoc", api_store.root / "new.md", PAYLOAD, "new", api_store.pythonpath, actor="agent:test")
    text = created.path.read_text(encoding="utf-8")
    found = provenance_of(text)
    assert (found.by, found.authority, found.via, found.declared) == ("agent:test", "generated", "create_document", True)
    assert str(found.at).endswith("Z")
    assert extract_model_data(api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath), text) == PAYLOAD, "the block is not a field"


def test_a_save_that_changes_nothing_keeps_the_block_and_one_that_does_restamps(api_store):
    model = api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    api.save_document_payload(api_store.store, "TicketDoc", "login", PAYLOAD, api_store.pythonpath, actor="agent:one")
    path = api_store.root / "login.md"
    first = read_block(path.read_text(encoding="utf-8"))
    api.save_document_payload(api_store.store, "TicketDoc", "login", PAYLOAD, api_store.pythonpath, actor="agent:two")
    assert read_block(path.read_text(encoding="utf-8")) == first, "nothing changed: the signature stays"
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "Other"}, api_store.pythonpath, actor="agent:two")
    second = read_block(path.read_text(encoding="utf-8"))
    assert second["by"] == "agent:two" and second["via"] == "save_document_payload"
    assert extract_model_data(model, path.read_text(encoding="utf-8"))["title"] == "Other"


def test_a_declared_authority_survives_a_save_and_a_stamp_moves_only_the_text_hash(api_store):
    from sldb.store.hashing import hash_fields, hash_text

    model = api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    path = api_store.root / "login.md"
    path.write_text(attach_block(path.read_text(encoding="utf-8"), {**BLOCK, "authority": "source_raw"}), encoding="utf-8")
    before = path.read_text(encoding="utf-8")
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "Edited"}, api_store.pythonpath)
    after = path.read_text(encoding="utf-8")
    assert provenance_of(after).authority == "source_raw" and provenance_of(after).by == "agent"
    stamped_twice = stamped(strip_block(after), model, "x", "agent:z", previous=before)
    assert hash_fields(model, stamped_twice) == hash_fields(model, after) and hash_text(stamped_twice) != hash_text(after)


def test_the_block_is_never_an_undeclared_frontmatter_key(api_store):
    model = api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    assert undeclared_frontmatter_keys(model, attach_block("# T\n\nStatus: open\n\n## Tags\n\n- a\n", BLOCK)) == []
    path = api_store.root / "hand.md"
    path.write_text(attach_block("# Hand\n\nStatus: open\n\n## Tags\n\n- a\n", BLOCK), encoding="utf-8")
    api.track_document_file(api_store.store, "TicketDoc", path, "hand", api_store.pythonpath)
    assert provenance_of(path.read_text(encoding="utf-8")).by == "human:jp", "track does not rewrite the file"


def test_the_cli_actor_flag_and_the_env_sign_every_write(api_store, capsys, monkeypatch):
    assert current_actor() == "agent"
    monkeypatch.setenv("SLDB_ACTOR", "agent:env")
    assert current_actor() == "agent:env" and current_actor("agent:explicit") == "agent:explicit"
    args = ["--store", str(api_store.store), "--pythonpath", api_store.pythonpath]
    assert cli_main(["--actor", "human:cli", "docs", "update", "login", json.dumps({**PAYLOAD, "title": "From cli"}), *args]) == 0
    assert provenance_of((api_store.root / "login.md").read_text(encoding="utf-8")).by == "human:cli"
    capsys.readouterr()
    assert cli_main(["docs", "show", "login", *args, "--format", "json"]) == 0
    shown = json.loads(capsys.readouterr().out)["document"]
    assert shown["provenance"]["by"] == "human:cli" and shown["provenance"]["declared"] is True
