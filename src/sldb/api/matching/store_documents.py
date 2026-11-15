"""Los documentos de un store (y de sus stores enlazados) como los lee el emparejamiento.

Migrado de `spec2viz.deskops.SldbAtomResolver` (`_load_store_documents`, `resolve_ref`,
`_ref_payload`) sobre `load_runtime_documents` y `open_store` de sldb.api; el descubrimiento
del store no se migra: la vista trae su `store`.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.runtime_documents import load_runtime_documents
from sldb.api.stores.open_store import open_store

_SUMMARY_FIELDS = ("summary", "answer", "content", "purpose", "docstring", "goal", "description")


def _document(doc, root: Path) -> dict:
    store_name = str(getattr(doc, "store_name", "") or "local")
    ref = f"{doc.model_name}:{doc.name}" if store_name == "local" else f"{store_name}:{doc.model_name}:{doc.name}"
    payload = dict(doc.payload or {})
    return {"ref": ref, "store": str(doc.store_path), "store_name": store_name, "model": str(doc.model_name), "name": str(doc.name),
            "title": str(payload.get("title") or doc.name), "path": str(root / doc.path), "payload": payload}


def store_documents(store_path: Path, pythonpath: str | None = None) -> list[dict]:
    """Cada documento con `ref` (`Model:name`, o `alias:Model:name` si es de un store enlazado),
    `store`, `store_name`, `model`, `name`, `title`, `path` absoluto y `payload`."""
    roots: dict[str, Path] = {}
    docs: list[dict] = []
    for doc in load_runtime_documents(Path(store_path).resolve(), pythonpath, include_linked=True):
        key = str(doc.store_path)
        if key not in roots:
            roots[key] = Path(open_store(Path(key)).project_root)
        docs.append(_document(doc, roots[key]))
    return docs


def resolve_ref(docs: list[dict], ref: str) -> dict | None:
    """El documento `Model:name` (o `alias:Model:name`) entre `docs`, o None."""
    return next((doc for doc in docs if doc["ref"] == ref), None)


def ref_payload(doc: dict) -> dict:
    """Lo que el catálogo muestra de una ref: ref, model, name, title, path, store y summary (300 car.)."""
    payload = doc.get("payload") or {}
    summary = next((str(payload[f]).strip() for f in _SUMMARY_FIELDS if payload.get(f)), "")
    return {key: doc.get(key, "") for key in ("ref", "model", "name", "title", "path", "store")} | {"summary": summary[:300]}
