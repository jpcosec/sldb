"""A store's signature (PLAN 15 capa 6): hash_a and every model's hash_b (a write through
sldb always moves these — cheap, a handful of file stats, not one per document) plus the
current operation's document leaf sweep. One concession to Markdown edited by hand: the
leaves are also stat-ed (mtime and size) so an edit made behind sldb's back is seen — once
per operation (`new_operation`, called from `get_store_context`: once per Store/World
opened, i.e. once per pron session, once per sldb CLI command), not once per call (that was
one stat per tracked document, every time — 7 calls in one pron turn measured as ~0.3s at
1500 documents). A hand edit made mid-operation is not required to be seen until the next
one — `stores update`/`stores check` give the same guarantee unconditionally regardless (they
always re-read and re-hash every file directly, untouched by any of this). A store that is
only written through sldb can set SLDB_TRUST_CHAIN=1 and skip the sweep entirely.

`leaf()` is also what `runtime_cache.cached_document` calls once per document on every
reload it does (a reload is triggered whenever hash_a moved — every write): without its own
per-path stat cache, a store with several writes in one operation (each forcing at least one
reload of the whole document list, to find the one or two documents that actually changed)
would still re-stat every tracked document once per reload, several times over in one
operation. `_STAT_CACHE` makes that one stat per path per operation too, regardless of which
of the two callers (the sweep, or a reload's per-document lookup) asks first."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.layout import project_root

_FORCE_SWEEP: set[str] = set()          # store paths whose next signature() re-stats every leaf
_LAST_LEAVES: dict[str, tuple] = {}     # store path -> leaves signature() last actually swept
_STAT_CACHE: dict[str, tuple[int, int]] = {}   # absolute doc path -> (mtime_ns, size), this operation


def trust_chain() -> bool:
    return os.environ.get("SLDB_TRUST_CHAIN", "") not in ("", "0")


def new_operation(s_path: Path) -> None:
    """The start of a top-level operation on this store: the next `signature()`/`leaf()` call
    re-stats every tracked document once; calls within the same operation reuse those stats."""
    _FORCE_SWEEP.add(str(s_path))
    _STAT_CACHE.clear()


def forget(s_path: Path | None) -> None:
    """Drop the remembered sweep so the next signature() redoes it (invalidate_runtime_cache)."""
    if s_path is None:
        _LAST_LEAVES.clear(); _FORCE_SWEEP.clear(); _STAT_CACHE.clear()
        return
    _LAST_LEAVES.pop(str(s_path), None)
    _FORCE_SWEEP.add(str(s_path))
    _STAT_CACHE.clear()


def _stat(path: Path) -> tuple[int, int]:
    key = str(path)
    hit = _STAT_CACHE.get(key)
    if hit is None:
        try:
            st = path.stat()
            hit = (st.st_mtime_ns, st.st_size)
        except OSError:
            hit = (0, 0)
        _STAT_CACHE[key] = hit
    return hit


def leaf(root: Path, entry: Any) -> tuple:
    """A document's place in the chain, plus its file state unless the chain is trusted —
    stat-ed at most once per path per operation (both the sweep below and a reload's own
    per-document lookup, sldb.store.runtime_cache.cached_document, call this)."""
    if trust_chain():
        return (entry.path, entry.hash_c)
    mtime, size = _stat(root / entry.path)
    return (entry.path, entry.hash_c, mtime, size)


def _leaves(s_path: Path, root: Path, idx) -> tuple:
    key = str(s_path)
    if trust_chain():
        return ()
    if key not in _LAST_LEAVES or key in _FORCE_SWEEP:
        _LAST_LEAVES[key] = _sweep_leaves(root, idx)
        _FORCE_SWEEP.discard(key)
    return _LAST_LEAVES[key]


def _sweep_leaves(root: Path, idx) -> tuple:
    leaves: list = []
    for m in idx.models:
        m_idx = load_models_index(root / m.models_index)
        leaves.extend(leaf(root, d) for d in load_documents_index(root / m_idx.documents_index).documents)
    return tuple(leaves)


def signature(s_path: Path) -> tuple:
    root = project_root(s_path)
    idx = load_store_index(s_path)
    parts: list = [idx.hash_a]
    parts.extend((m.name, load_models_index(root / m.models_index).hash_b) for m in idx.models)
    parts.append(_leaves(s_path, root, idx))
    return tuple(parts)
