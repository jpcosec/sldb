"""The public store fingerprint: the Merkle tree as one value, matching the index walk."""

from __future__ import annotations

from sldb.api import load_runtime_documents, store_fingerprint
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.layout import project_root


def _walk(store):
    root = project_root(store)
    idx = load_store_index(store)
    model = load_models_index(root / idx.models[0].models_index)
    docs = load_documents_index(root / model.documents_index)
    return idx, model, docs


def test_store_fingerprint_matches_the_index_walk(api_store):
    idx, model, docs = _walk(api_store.store)
    fp = store_fingerprint(api_store.store)
    assert fp.store_hash == idx.store_hash
    assert fp.models == {model.name: model.model_hash}
    assert set(fp.documents) == {f"{model.name}:{d.name}" for d in docs.documents}


def test_store_fingerprint_document_hashes_match_their_shards(api_store):
    _idx, model, docs = _walk(api_store.store)
    fp = store_fingerprint(api_store.store)
    for doc in docs.documents:
        entry = fp.documents[f"{model.name}:{doc.name}"]
        assert (entry.source_hash, entry.content_hash) == (doc.source_hash, doc.content_hash)


def test_runtime_documents_carry_their_index_hashes(api_store):
    _idx, _model, docs = _walk(api_store.store)
    loaded = load_runtime_documents(api_store.store, api_store.pythonpath)
    assert [(d.name, d.source_hash, d.content_hash) for d in loaded] == [
        (d.name, d.source_hash, d.content_hash) for d in docs.documents
    ]
