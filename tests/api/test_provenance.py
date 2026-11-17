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


ANCHOR_CODE = 'def one(x):\n    """One doc."""\n    return x\n\n\ndef two(x):\n    """Two doc."""\n    return x\n'


@pytest.fixture
def anchored(tmp_path, monkeypatch):
    from sldb.code.runtime import available

    if not available():
        pytest.skip("tree-sitter runtime not installed (extra [code])")
    monkeypatch.delenv("SLDB_ACTOR", raising=False)
    root = tmp_path / "repo"
    (root / "src").mkdir(parents=True)
    (root / "src" / "x.py").write_text(ANCHOR_CODE, encoding="utf-8")
    store = api.init_store(root).store_path
    api.add_model(store, "sldb.models.code_anchor_doc:CodeAnchorDoc")
    return root, store


def test_write_anchor_signs_with_its_actor_when_it_creates_and_when_it_re_records(anchored):
    from sldb.api.anchors import record_anchor, write_anchor

    root, store = anchored
    path = root / "anchors" / "one.md"
    block = record_anchor(root, "code:src/x.py::one")
    write_anchor(store, None, path, block, "one returns x", actor="agent:anchor")
    assert (provenance_of(path.read_text(encoding="utf-8")).by, provenance_of(path.read_text(encoding="utf-8")).via) == ("agent:anchor", "create_document")
    write_anchor(store, None, path, block, "one echoes x", actor="human:jp")
    assert (provenance_of(path.read_text(encoding="utf-8")).by, provenance_of(path.read_text(encoding="utf-8")).via) == ("human:jp", "save_document_payload")
    write_anchor(store, None, path, block, "one is identity")
    assert provenance_of(path.read_text(encoding="utf-8")).by == "agent", "actor=None signs as before: the process actor"


def test_a_reconnection_is_signed_by_the_actor_it_is_given(anchored):
    from sldb.api.anchors import record_anchor, write_anchor
    from sldb.api.anchors.anchor_docs import anchor_documents, record_reconnection

    root, store = anchored
    write_anchor(store, None, root / "anchors" / "one.md", record_anchor(root, "code:src/x.py::one"), "one returns x")
    [doc] = anchor_documents(store, None)
    record_reconnection(store, None, doc, "code:src/x.py::two", actor="agent:reconnect")
    text = (root / "anchors" / "one.md").read_text(encoding="utf-8")
    assert provenance_of(text).by == "agent:reconnect" and "code:src/x.py::two" in text


def test_no_public_write_function_drops_its_actor_without_saying_so():
    """Every public function of sldb.api taking `actor` passes it on, or its docstring says why
    it is not recorded (no document to sign)."""
    import ast
    import re
    from pathlib import Path

    silent = []
    for path in sorted(Path(api.__file__).parent.rglob("*.py")):
        for node in ast.walk(ast.parse(path.read_text(encoding="utf-8"))):
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_") and "actor" in [a.arg for a in node.args.args + node.args.kwonlyargs]:
                passed = any(isinstance(n, ast.Name) and n.id == "actor" and isinstance(n.ctx, ast.Load) for n in ast.walk(node))
                said = re.search(r"(not|no longer) recorded", " ".join((ast.get_docstring(node) or "").split()))
                if not passed and not said:
                    silent.append(f"{path.name}:{node.name}")
    assert silent == []
