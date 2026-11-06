"""Render a payload to a new Markdown file and track it as a document of a registered model."""

from __future__ import annotations
from sldb.api.stores.declaration_sync import declare_tracked, project_relative

from pathlib import Path
from typing import Any

from sldb.api.documents.document_reference import DocumentReference
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.documents.refuse_structural_noise import refuse_structural_noise
from sldb.api.documents.frontmatter_keys import refuse_undeclared_frontmatter
from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.api.rules.rule_writes import refuse_unknown_family
from sldb.api.stores.open_store import open_store
from sldb.core.exceptions import SLDBValidationError
from sldb.api.documents.provenance_stamp import stamped
from sldb.runtime.validation import render_model_markdown, validate_model_input_roundtrip
from sldb.store.ops import track_document


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
    refuse_noise(registered.model_type, rendered, doc_name, location.store_path)
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text(stamped(rendered + "\n", registered.model_type, "create_document", actor), encoding="utf-8")
    _track(location.store_path, location.project_root, registered, doc_path, doc_name, pythonpath)
    return DocumentReference(model=registered.entry.name, name=doc_name, path=doc_path)


def refuse_noise(model_type: type, markdown: str, name: str, store_path: Path | None = None) -> None:
    """Refuse a document whose headings (unless the store's policy allows them) or frontmatter
    keys the model never declares."""
    from sldb.api.stores.policy import Policy

    refuse_structural_noise(model_type, markdown, name, Policy.of_store(store_path) if store_path else None)
    refuse_undeclared_frontmatter(model_type, markdown, name)


def _resolve_path(raw: str | Path, root: Path) -> Path:
    raw_path = Path(raw)
    return raw_path.resolve() if raw_path.is_absolute() else (root / raw_path).resolve()


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
