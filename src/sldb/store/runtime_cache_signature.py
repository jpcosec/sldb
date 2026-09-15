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
only written through sldb can set SLDB_TRUST_CHAIN=1 and skip the sweep entirely."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.layout import project_root

_FORCE_SWEEP: set[str] = set()          # store paths whose next signature() re-stats every leaf
_LAST_LEAVES: dict[str, tuple] = {}     # store path -> leaves signature() last actually swept


def trust_chain() -> bool:
    return os.environ.get("SLDB_TRUST_CHAIN", "") not in ("", "0")


def new_operation(s_path: Path) -> None:
    """The start of a top-level operation on this store: the next `signature()` call re-stats
    every tracked document once; calls within the same operation reuse that sweep."""
    _FORCE_SWEEP.add(str(s_path))


def forget(s_path: Path | None) -> None:
    """Drop the remembered sweep so the next signature() redoes it (invalidate_runtime_cache)."""
    if s_path is None:
        _LAST_LEAVES.clear(); _FORCE_SWEEP.clear()
        return
    _LAST_LEAVES.pop(str(s_path), None)
    _FORCE_SWEEP.add(str(s_path))


def leaf(root: Path, entry: Any) -> tuple:
    """A document's place in the chain, plus its file state unless the chain is trusted."""
    if trust_chain():
        return (entry.path, entry.hash_c)
    try:
        st = (root / entry.path).stat()
        return (entry.path, entry.hash_c, st.st_mtime_ns, st.st_size)
    except OSError:
        return (entry.path, entry.hash_c, 0, 0)


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
