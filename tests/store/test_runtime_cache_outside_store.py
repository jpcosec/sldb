"""A read of a store must not write into the store: the extracted-payload cache now lives in
the user's cache dir, not under `<store>/runtime/cache/`."""

from __future__ import annotations

import json
from pathlib import Path

from sldb.cli.model_utils import resolve_model_ref
from sldb.store import runtime_cache, runtime_cache_disk, user_cache
from sldb.store.query import _extract_doc, load_runtime_documents
from tests.store.test_cli_store import _SRC, _doc_track, _init, _model_add


def _tree(path: Path) -> dict:
    entries = {}
    for p in sorted(path.rglob("*")):
        rel = str(p.relative_to(path))
        if p.is_file():
            st = p.stat()
            entries[rel] = ("f", st.st_size, st.st_mtime_ns)
        else:
            entries[rel] = ("d",)
    return entries


def _make_store(tmp_path: Path) -> Path:
    _init(tmp_path)
    _model_add(tmp_path)
    doc = tmp_path / "book.md"
    doc.write_text("# My Book\n", encoding="utf-8")
    _doc_track(tmp_path, doc)
    return tmp_path / ".sldb"


def _read(store: Path) -> list:
    return load_runtime_documents(store, resolve_model_ref, _SRC)


def test_read_leaves_store_tree_identical(tmp_path):
    store = _make_store(tmp_path)
    runtime_cache.invalidate_runtime_cache()
    before = _tree(store)
    assert _read(store)
    assert _tree(store) == before


def test_cache_hits_new_location_and_second_read_does_not_reextract(tmp_path, monkeypatch):
    cache_dir = tmp_path / "cache"
    monkeypatch.setenv("XDG_CACHE_HOME", str(cache_dir))
    store = _make_store(tmp_path)
    runtime_cache.invalidate_runtime_cache()
    assert len(_read(store)) == 1

    cache_file = runtime_cache_disk.cache_file(store)
    assert cache_file == user_cache.extracted_cache_file(store)
    assert cache_file is not None
    assert cache_file.parent == cache_dir / "sldb" / "runtime-cache-extracted"
    assert cache_file.exists()
    assert json.loads(cache_file.read_text(encoding="utf-8"))

    runtime_cache.invalidate_runtime_cache()
    calls: list[int] = []
    real = _extract_doc

    def spy(*args, **kwargs):
        calls.append(1)
        return real(*args, **kwargs)

    monkeypatch.setattr("sldb.store.query._extract_doc", spy)
    assert len(_read(store)) == 1
    assert calls == []


def test_unwritable_cache_read_still_works(tmp_path, monkeypatch):
    store = _make_store(tmp_path)
    runtime_cache.invalidate_runtime_cache()
    monkeypatch.setattr(user_cache, "cache_root", lambda: None)
    assert runtime_cache_disk.cache_file(store) is None
    assert len(_read(store)) == 1
