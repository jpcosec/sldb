"""CLI adapter over `sldb.api.save_document_payload`: prints progress and exits on a failed save."""
from typing import Any
from sldb.api.documents.payload_save import save_document_payload
from sldb.core.exceptions import SLDBPayloadSaveError
from sldb.cli.commands.inbox_core import print_payload

def save_payload(runtime_doc: Any, payload: dict[str, Any], store_arg: str | None, pythonpath: str | None,
                 fmt: str = "text", change: str = "") -> int:
    """Save a runtime document's new payload; an unregistered model/document or a broken
    round-trip exits with the error message, as the `fields` commands always have."""
    try:
        save_document_payload(store_arg, runtime_doc.model_name, runtime_doc.name, payload, pythonpath)
    except SLDBPayloadSaveError as exc:
        raise SystemExit(str(exc)) from exc
    if fmt != "text":
        mode, _, field = change.partition(":")
        print_payload({"document": runtime_doc.name, "model": runtime_doc.model_name, "field": field, "action": mode, "saved": True}, fmt)
        return 0
    print(f"Updated field payload for '{runtime_doc.name}'")
    return 0
