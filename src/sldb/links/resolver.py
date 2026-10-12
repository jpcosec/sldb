from __future__ import annotations
from pathlib import Path
from sldb.store.layout import project_root
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from .resolved_link import ResolvedLink
from .sections import split_anchor

def _tracked_documents(store_path: Path) -> dict[str, str]:
    root, store_idx = project_root(store_path), load_store_index(store_path)
    tracked = {}
    for m in store_idx.models:
        for d in load_documents_index(root / load_models_index(root / m.models_index).documents_index).documents:
            tracked[d.name] = str((root / d.path).resolve())
    return tracked

def resolve_document_input(doc_ref: str, store_path: Path | None) -> Path:
    if (c := Path(doc_ref)).exists(): return c.resolve()
    if store_path and doc_ref in (t := _tracked_documents(store_path)): return Path(t[doc_ref]).resolve()
    return c.resolve()

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
    if (c := (cur_doc.resolve().parent / tgt).resolve()).exists(): return _mk_res(tgt, predicate, w5h1_type, str(c), "path")
    if (d := Path(tgt)).exists(): return _mk_res(tgt, predicate, w5h1_type, str(d.resolve()), "path")
    return _mk_res(tgt, predicate, w5h1_type, None, None)
