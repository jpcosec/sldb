"""The anchor documents of a store, and the two writes anchoring makes: a reconnection, and a
(re)recorded anchor written through the documents API, so it is signed like any document."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sldb.api.documents.payload_save import save_document_payload
from sldb.api.stores.open_store import open_store
from sldb.store.layout import project_root

MODEL = "CodeAnchorDoc"


@dataclass
class AnchorDocument:
    root: Path
    name: str
    path: str
    payload: dict[str, Any]


def anchor_documents(store: str | Path | None, pythonpath: str | None) -> list[AnchorDocument]:
    """Every tracked `CodeAnchorDoc`, extracted; none when the model is not registered."""
    from sldb.api.model_registry.model_reference import resolve_model_ref
    from sldb.store.query import load_runtime_documents

    location = open_store(store, mode="readonly")
    root = project_root(location.store_path)
    docs = load_runtime_documents(location.store_path, resolve_model_ref, pythonpath)
    return [AnchorDocument(root, d.name, d.path, dict(d.payload)) for d in docs if d.model_name == MODEL]


def record_reconnection(store: str | Path | None, pythonpath: str | None, doc: AnchorDocument, to: str) -> None:
    """The anchor now points at `to`, and its signature and shape are the new name's (the
    docstring and body it saw stay: a body that moved is still reported); where it pointed
    before stays in `history`."""
    from sldb.api.anchors.record_anchor import record_anchor

    now = record_anchor(doc.root, to)["seen"]
    seen = {**doc.payload.get("seen", {}), "signature": now["signature"], "shape": now["shape"]}
    event = {"event": "reconnected", "from": doc.payload["ref"], "to": to, "at": _now()}
    payload = {**doc.payload, "ref": to, "seen": seen, "history": [*doc.payload.get("history", []), event]}
    save_document_payload(store, MODEL, doc.name, payload, pythonpath, actor=None)


def write_anchor(store: str | Path | None, pythonpath: str | None, path: Path, block: dict[str, Any], claim: str, name: str | None = None) -> Any:
    """Create the anchor document, or re-record an existing one (its claim and history kept)."""
    from sldb.api.documents.create_document import create_document

    existing = next((d for d in anchor_documents(store, pythonpath) if (project_root(open_store(store, mode="readonly").store_path) / d.path).resolve() == path.resolve()), None)
    if existing is None:
        return create_document(store, MODEL, path, {**block, "claim": claim, "history": [{"event": "recorded", "at": _now()}]}, name, pythonpath)
    payload = {**existing.payload, **block, "claim": claim or existing.payload.get("claim", ""), "history": [*existing.payload.get("history", []), {"event": "recorded", "at": _now()}]}
    return save_document_payload(store, MODEL, existing.name, payload, pythonpath)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
