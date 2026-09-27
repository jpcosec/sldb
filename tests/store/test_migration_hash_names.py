"""The persisted letter keys still load as deprecated aliases of the semantic names."""

from __future__ import annotations

from sldb.store.models import DocumentEntry, ModelsIndex, StoreIndex


def test_store_letter_alias_still_loads():
    index = StoreIndex(**{"hash_a": "root"})
    assert index.store_hash == "root"
    assert index.hash_a == "root"


def test_model_letter_alias_still_loads():
    index = ModelsIndex(name="A", model_ref="a:A", path="p", documents_index="d", hash_b="roster")
    assert index.model_hash == "roster"


def test_document_letter_aliases_still_load():
    entry = DocumentEntry(name="n", path="p", hash_c="text", hash_d="fields")
    assert (entry.source_hash, entry.content_hash) == ("text", "fields")
