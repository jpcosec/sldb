"""Untrack the rows a path's winning `include` rule beat, leaving the file alone.

A store built before `include_resolution` existed tracks a file in a parent's glob and a
child's `paths` twice. The losing row is recognised from the declaration's rules, never from
the cache. Only the store index is touched, not `store.yaml`: `docs untrack` would drop the
path from every `paths` list, and with it the winner's. Idempotent: a second pass finds nothing.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.declared_files import rule_rows
from sldb.api.stores.declared_includes import tracked_rows
from sldb.api.stores.include_resolution import resolved_rows, store_bases
from sldb.api.stores.store_declaration import declaration_path, load_declaration
from sldb.store.io import load_documents_index, load_models_index, load_store_index


def losing_rows(store_path: Path, root: Path) -> list[tuple[str, str, str]]:
    """Tracked `(model, path, name)` that a rule names and that another rule's row beat."""
    if not declaration_path(store_path).is_file():
        return []
    named = rule_rows(root, load_declaration(store_path))
    won = {row[1]: row for row in resolved_rows(named, store_bases(store_path))[0]}
    tracked = set(tracked_rows(store_path, root))
    return sorted({r[1:] for r in named if r[2] in won and r[1:] != won[r[2]] and r[1:] in tracked})


def untrack_losers(store_path: Path, root: Path, pythonpath: str | None = None) -> list[str]:
    """Untrack every losing row; returns them as `model:path`."""
    losers = losing_rows(store_path, root)
    for model, _path, name in losers:
        _forget(store_path, root, model, name, pythonpath or str(root))
    return [f"{model}:{path}" for model, path, _ in losers]


def _forget(store_path: Path, root: Path, model: str, name: str, pythonpath: str) -> None:
    from sldb.api.documents.untrack_document import forget_document

    idx = load_store_index(store_path)
    entry = next(e for e in idx.models if e.name == model)
    m_idx = load_models_index(root / entry.models_index)
    doc = next(d for d in load_documents_index(root / m_idx.documents_index).documents if d.name == name)
    forget_document(store_path, root, idx, entry, m_idx, doc, pythonpath)
