"""Render a payload to a new Markdown file and track it as a document of a registered model."""

from __future__ import annotations
from sldb.api.stores.declaration_sync import declare_tracked, project_relative

from pathlib import Path
from typing import Any

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.documents.on_write_gate import check_entering
from sldb.api.documents.refuse_structural_noise import refuse_structural_noise
from sldb.api.documents.frontmatter_keys import refuse_undeclared_frontmatter
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.rules.rule_writes import refuse_unknown_family
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBValidationError
from sldb.api.documents.provenance_stamp import stamped
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.ops import track_document
from sldb.store.source_guard import READ_CODES, write_source_text
from sldb.store.source_read import SYMLINK


def create_document(store: str | Path | None, model_name: str, path: str | Path, payload: dict[str, Any], name: str | None = None, pythonpath: str | None = None, actor: str | None = None) -> DocumentReference:
    """Write the Markdown a model renders from `payload` and start tracking it.

    Args:
        store: The store to track in (path, alias, or None to discover it).
        model_name: Registered model name, or `alias:ModelName` for a linked store's model.
        path: The Markdown file to write (parents are created, an existing file is
            overwritten); a relative path is relative to the project root, not the cwd.
        payload: The document's field values; it has no fixed schema beyond the model's own.
        name: Document name; defaults to the file stem.
        pythonpath: Directory to import the model module from.
        actor: Optional caller label, stamped into the document's provenance block.

    Returns:
        The created document.

    Raises:
        SLDBStoreError: When the model is not registered, or a RuleDoc's subject names a model
            the store does not register.
        SLDBValidationError: When the rendered Markdown does not round-trip under the model,
            or when it carries headings the model does not declare; nothing is written then.
    """
    location = open_store(store)
    registered = load_registered_model(location.store_path, model_name, pythonpath)
    rendered = _rendered(location, registered.model_type, payload, pythonpath)
    doc_path = _resolve_path(path, location.project_root)
    doc_name = name or doc_path.stem
    _admit(location.store_path, registered, rendered, doc_name, payload)
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    write_source_text(doc_path, stamped(rendered + "\n", registered.model_type, "create_document", actor))
    _track(location.store_path, location.project_root, registered, doc_path, doc_name, pythonpath)
    return DocumentReference(model=registered.entry.name, name=doc_name, path=doc_path)


def refuse_noise(model_type: type, markdown: str, name: str, store_path: Path | None = None) -> None:
    """Refuse a document whose headings (unless the store's policy allows them) or frontmatter
    keys the model never declares."""
    from sldb.api.stores.policy import Policy

    refuse_structural_noise(model_type, markdown, name, Policy.of_store(store_path) if store_path else None)
    refuse_undeclared_frontmatter(model_type, markdown, name)


def _resolve_path(raw: str | Path, root: Path) -> Path:
    """The new document's path, resolved; a symlink there is refused BEFORE resolving (the write
    would go where it points). A plain path outside the project is still created (spec2viz)."""
    raw_path = Path(raw) if Path(raw).is_absolute() else root / raw
    if raw_path.is_symlink():
        raise SLDBDocumentTargetError(f"[{READ_CODES[SYMLINK]}] {raw}: the path is a symlink; sldb does not write it")
    return raw_path.resolve()


def _track(sp: Path, root: Path, registered, doc_path: Path, doc_name: str, pythonpath: str | None) -> None:
    track_document(sp, root, registered.store_index, registered.model_type, registered.entry, doc_path, doc_name, resolve_model_ref, pythonpath)
    declare_tracked(sp, root, registered.entry.name, project_relative(root, doc_path), doc_name)


def _rendered(location, model_type: type, payload: dict[str, Any], pythonpath: str | None) -> str:
    """The round-tripped Markdown, once a RuleDoc's subject names only registered models."""
    rendered = _render_roundtrip(model_type, payload, location.project_root)
    refuse_unknown_family(location.store_path, model_type, payload, pythonpath)
    return rendered


def _render_roundtrip(model_type: type, payload: dict[str, Any], ref_root: Path) -> str:
    """The payload rendered to Markdown, refused unless it extracts back identically.

    `ref_root` is the project root, so a composed field resolves its refs the way the project
    names them; without it they would resolve against whatever directory the caller runs in.
    """
    rendered = render_model_markdown(model_type, payload, ref_root)
    valid, details = validate_model_input_roundtrip(model_type, rendered)
    if not valid:
        raise SLDBValidationError("Idempotency fail", details)
    return rendered


def _admit(sp: Path, registered, rendered: str, doc_name: str, payload: dict[str, Any]) -> None:
    """Refuse a document the model's structure or an `on_write` rule (H4) does not admit."""
    refuse_noise(registered.model_type, rendered, doc_name, sp)
    check_entering(sp, registered.model_type, registered.entry.name, doc_name, payload)
