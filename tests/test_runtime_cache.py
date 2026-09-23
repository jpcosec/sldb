"""The runtime document cache: repeated loads share documents, a write to one document
re-extracts only that one, and a save that changes nothing leaves the file alone.

PLAN 15 capa 6 changed the hand-edit guarantee: `signature()` used to stat every tracked
document's file on every call (the cost this capa removes — 0.3s at 1500 documents, 7 calls
in one pron turn). Now it stats them once per "operation" (`new_operation`, called from
`get_store_context`: once per Store/World opened — once per pron session — or once per sldb
CLI command) and reuses that sweep for calls within the same operation. The guarantee is now
exactly what the module docstring promises: a hand edit is seen at the start of the next
operation (a fresh session, or any sldb CLI command, since both call `get_store_context`),
and unconditionally by `stores update`/`stores check` (which always re-read and re-hash every
file directly, never through this cache) — not necessarily by the very next library call in
a row within the same operation, which is what the old, stricter test below used to assert."""

from __future__ import annotations

import os
import sys
from pathlib import Path

from sldb import api
from sldb.cli import main as sldb_main
from sldb.cli.model_utils import resolve_model_ref
from sldb.cli.store_context import get_store_context
from sldb.store.codec import default_codec
from sldb.store.io import load_documents_index, load_models_index, load_store_index, save_documents_index
from sldb.store.layout import documents_shard_path
from sldb.store.query import load_runtime_documents
from sldb.store.runtime_cache import invalidate_runtime_cache, new_operation

MODEL = "cachefix_models:NoteDoc"


def _world(tmp_path: Path) -> Path:
    (tmp_path / "cachefix_models.py").write_text(
        "from sldb.models import StructuredNLDoc\nfrom pydantic import Field\n\n"
        "class NoteDoc(StructuredNLDoc):\n    __template__ = '# ⸢rev•title⸥\\n\\n⸢rev•body⸥\\n'\n"
        "    title: str = Field(description='the title')\n    body: str = Field(description='the body')\n"
    )
    assert sldb_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert sldb_main(["models", "add", MODEL, "--store", str(tmp_path / ".sldb"), "--pythonpath", str(tmp_path)]) == 0
    for name in ("one", "two"):
        (tmp_path / f"{name}.md").write_text(f"# {name}\n\nbody of {name}\n")
        assert sldb_main(["docs", "track", str(tmp_path / f"{name}.md"), "--model", "NoteDoc", "--store", str(tmp_path / ".sldb"), "--pythonpath", str(tmp_path)]) == 0
    return tmp_path


def test_repeated_loads_share_documents(tmp_path: Path):
    root = _world(tmp_path)
    invalidate_runtime_cache()
    first = load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))
    second = load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))
    assert [id(d) for d in first] == [id(d) for d in second]


def test_a_contract_change_invalidates_document_cache_entries_without_editing_the_markdown(tmp_path: Path):
    """A payload is a function of (document, model contract), but the document cache used to
    key only on the document's leaf: a contract that gained a field kept serving the old
    payload forever, from `_DOCS` in memory and from `.sldb/runtime/cache/extracted.json`
    on disk (queried before the loader). The key now carries the model's hash_b — the same
    value `signature()` signs the store with — so a chain that moved misses both levels
    even when the .md did not, while an entry whose hash_b did not move stays a hit."""
    root = _world(tmp_path)
    invalidate_runtime_cache()
    first = {d.name: d for d in load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))}
    assert "status" not in first["one"].payload          # the old contract has no such field

    # the contract gains a field; one.md/two.md are never touched again
    sys.modules.pop("cachefix_models", None)              # what a fresh process would import
    (root / "cachefix_models.py").write_text(
        "from sldb.models import StructuredNLDoc\nfrom pydantic import Field\n\n"
        "class NoteDoc(StructuredNLDoc):\n    __template__ = '# ⸢rev•title⸥\\n\\n⸢rev•body⸥\\n'\n"
        "    title: str = Field(description='the title')\n    body: str = Field(description='the body')\n"
        "    status: str = Field(default='open', description='the status')\n"
    )
    # a real store write moves the model's hash_b: track computes hash_d with the new contract
    api.create_document(root / ".sldb", "NoteDoc", root / "three.md", {"title": "three", "body": "body of three"}, "three", str(root))
    assert (root / "one.md").read_text(encoding="utf-8") == "# one\n\nbody of one\n"  # untouched

    second = {d.name: d for d in load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))}
    # validated against the real contract: what the current class extracts from this text
    contract = resolve_model_ref(MODEL, str(root))
    expected = default_codec.extract(contract, (root / "one.md").read_text(encoding="utf-8"))
    assert second["one"].payload == expected
    assert second["one"].payload["status"] == contract.model_fields["status"].default

    # hash_b has not moved again: the next load is still a cache hit (same shared objects)
    third = {d.name: d for d in load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))}
    assert [id(third[n]) for n in ("one", "two", "three")] == [id(second[n]) for n in ("one", "two", "three")]

    # a real reload with hash_b unmoved (a hand edit re-extracts only the edited document):
    # the other entries hit the in-memory cache again, never recomputing
    (root / "one.md").write_text("# one\n\nbody of one, edited\n")
    new_operation(root / ".sldb")
    after_edit = {d.name: d for d in load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))}
    assert after_edit["one"].payload["body"] == "body of one, edited"
    assert after_edit["one"].payload["status"] == contract.model_fields["status"].default
    assert id(after_edit["two"]) == id(second["two"]) and id(after_edit["three"]) == id(second["three"])


def test_a_hand_edit_within_one_operation_is_not_required_to_be_seen(tmp_path: Path):
    """PLAN 15 capa 6: the leaf sweep runs once per operation, not once per call — a hand
    edit made between two calls that are still the same operation (no new_operation() in
    between) is not guaranteed to be picked up by the second call."""
    root = _world(tmp_path)
    invalidate_runtime_cache()
    first = load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))
    (root / "one.md").write_text("# one\n\nbody of one, changed\n")
    second = load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))
    by_name = {d.name: d for d in second}
    assert by_name["one"].payload["body"] == "body of one"   # not seen yet: same operation
    assert id(by_name["two"]) == id({d.name: d for d in first}["two"])


def test_a_hand_edit_is_seen_at_the_start_of_the_next_operation(tmp_path: Path):
    """new_operation() is what `get_store_context` calls once per Store/World opened (once
    per pron session) or once per sldb CLI command — simulated directly here."""
    root = _world(tmp_path)
    invalidate_runtime_cache()
    load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))
    (root / "one.md").write_text("# one\n\nbody of one, changed\n")
    new_operation(root / ".sldb")
    third = load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))
    assert {d.name: d for d in third}["one"].payload["body"] == "body of one, changed"


def test_a_hand_edit_is_seen_by_the_next_sldb_cli_command(tmp_path: Path):
    """get_store_context (every sldb CLI command, and pron.store.Store.__init__ — once per
    pron session) starts a fresh operation on its own, with no explicit new_operation() call
    needed from the caller."""
    root = _world(tmp_path)
    invalidate_runtime_cache()
    load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))
    (root / "one.md").write_text("# one\n\nbody of one, changed\n")
    get_store_context(str(root / ".sldb"))   # what opening a new session/CLI command does
    third = load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))
    assert {d.name: d for d in third}["one"].payload["body"] == "body of one, changed"


def test_a_hand_edit_is_always_seen_by_stores_update(tmp_path: Path):
    """stores update re-reads and re-hashes every tracked file directly (sldb.cli.commands.
    store_update._process_doc) — untouched by runtime_cache either way, in the same or a
    fresh operation."""
    root = _world(tmp_path)
    invalidate_runtime_cache()
    load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))   # same operation from here on
    (root / "one.md").write_text("# one\n\nbody of one, changed\n")
    assert sldb_main(["stores", "update", "--store", str(root / ".sldb"), "--pythonpath", str(root)]) == 0
    fresh = {d.name: d for d in load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))}
    assert fresh["one"].payload["body"] == "body of one, changed"


def test_a_save_that_changes_nothing_leaves_the_file_alone(tmp_path: Path):
    """PLAN 15 capa 7: the documents index is per-document shards now — the file the
    guarantee is about is one document's shard, not one file for the whole model."""
    root = _world(tmp_path)
    m = next(m for m in load_store_index(root / ".sldb").models if m.name == "NoteDoc")
    d_path = root / load_models_index(root / m.models_index).documents_index
    shard = documents_shard_path(root / ".sldb", "NoteDoc", "one")
    idx = load_documents_index(d_path)
    save_documents_index(d_path, idx)
    save_documents_index(d_path, idx)
    stamp = os.stat(shard).st_mtime_ns
    save_documents_index(d_path, load_documents_index(d_path))
    assert os.stat(shard).st_mtime_ns == stamp


def test_a_trusted_chain_skips_the_leaf_sweep(tmp_path: Path, monkeypatch):
    root = _world(tmp_path)
    invalidate_runtime_cache()
    monkeypatch.setenv("SLDB_TRUST_CHAIN", "1")
    load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))
    (root / "one.md").write_text("# one\n\nbody of one, edited by hand\n")
    stale = {d.name: d for d in load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))}
    assert stale["one"].payload["body"] == "body of one"   # the chain did not move, and it is trusted
    assert sldb_main(["stores", "update", "--store", str(root / ".sldb"), "--pythonpath", str(root)]) == 0
    fresh = {d.name: d for d in load_runtime_documents(root / ".sldb", resolve_model_ref, str(root))}
    assert fresh["one"].payload["body"] == "body of one, edited by hand"
