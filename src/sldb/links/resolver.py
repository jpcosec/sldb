"""Resolve `[[x]]` targets and the document a links command names.

Every candidate is checked by the read guard (`sldb.store.source_read`) BEFORE it is resolved
(SEGURIDAD resto 2): resolving first lost the symlink and handed the reader, and `--render-links`,
the path outside the root. A target the guard refuses stays unresolved, written as it was."""
from __future__ import annotations
from pathlib import Path
from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.store.layout import project_root
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.source_guard import unread_line
from sldb.store.source_read import unreadable_reason
from .resolved_link import ResolvedLink
from .sections import split_anchor

def _tracked_paths(store_path: Path) -> dict[str, Path]:
    """Each tracked document's path under the root, NOT resolved."""
    root, store_idx = project_root(store_path), load_store_index(store_path)
    return {d.name: root / d.path for m in store_idx.models for d in load_documents_index(root / load_models_index(root / m.models_index).documents_index).documents}

def _tracked_documents(store_path: Path) -> dict[str, str]:
    """The tracked documents the guard lets be read, by name, resolved."""
    root = project_root(store_path)
    return {name: str(path.resolve()) for name, path in _tracked_paths(store_path).items() if unreadable_reason(root, path) is None}

def _guard_root(store_path: Path | None, path: Path) -> Path:
    """The root a target must stay in: the store's project, or (no store) the target's own folder."""
    return project_root(store_path) if store_path else path.absolute().parent

def _readable(path: Path, store_path: Path | None) -> bool:
    """`path` exists and the read guard lets it be read, checked before resolving."""
    return path.exists() and unreadable_reason(_guard_root(store_path, path), path) is None

def _refuse(root: Path, path: Path, doc_ref: str) -> None:
    if (line := unread_line(root, path, doc_ref)) is not None: raise SLDBDocumentTargetError(line)

def resolve_document_input(doc_ref: str, store_path: Path | None) -> Path:
    """The document a command names (a path, or a tracked name); `SLDBDocumentTargetError` when the
    read guard refuses it (outside the root, or a symlink), before anything is resolved or opened."""
    if (c := Path(doc_ref)).exists() or not store_path:
        _refuse(_guard_root(store_path, c), c, doc_ref)
        return c.resolve()
    if (raw := _tracked_paths(store_path).get(doc_ref)) is None: return c.resolve()
    _refuse(project_root(store_path), raw, doc_ref)
    return raw.resolve()

def _mk_res(tgt: str, prd: str | None, w5h1: str | None, pth: str | None, src: str | None) -> ResolvedLink:
    return ResolvedLink(f"[{prd}:: [[{tgt}]]]" if prd else f"[[{tgt}]]", tgt, "predicate_link" if prd else "link", bool(pth), pth, src, prd, w5h1)

def resolve_link_target(tgt: str, cur_doc: Path, store_path: Path | None, predicate: str | None = None, w5h1_type: str | None = None) -> ResolvedLink:
    """Resolve `doc` or `doc#Section`; the section itself is checked by recovery/compose."""
    res = _resolve(tgt, cur_doc, store_path, predicate, w5h1_type)
    base, anchor = split_anchor(tgt)
    if res.resolved or anchor is None: return res
    found = _resolve(base, cur_doc, store_path, predicate, w5h1_type)
    return ResolvedLink(res.raw, tgt, res.kind, found.resolved, found.path, found.source, predicate, w5h1_type)

def _resolve(tgt: str, cur_doc: Path, store_path: Path | None, predicate: str | None = None, w5h1_type: str | None = None) -> ResolvedLink:
    if store_path and tgt in (trk := _tracked_documents(store_path)) and Path(trk[tgt]).exists(): return _mk_res(tgt, predicate, w5h1_type, trk[tgt], "store")
    if _readable(c := cur_doc.resolve().parent / tgt, store_path): return _mk_res(tgt, predicate, w5h1_type, str(c.resolve()), "path")
    if _readable(d := Path(tgt), store_path): return _mk_res(tgt, predicate, w5h1_type, str(d.resolve()), "path")
    return _mk_res(tgt, predicate, w5h1_type, None, None)
