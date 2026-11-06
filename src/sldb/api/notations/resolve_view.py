"""The view of a SpecDoc according to its notation, ready to draw."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.notations.resolve_documents import resolve_documents
from sldb.api.notations.store_docs import load_docs
from sldb.api.notations.view_error import ViewError


def _same_type(notation_ref: str, notation: dict, sp: dict, spec_ref: str) -> None:
    """ViewError if the notation draws another diagram type than the spec."""
    found = notation["payload"].get("diagram_type")
    if found != sp.get("diagram_type"):
        raise ViewError(f"{notation_ref} draws `{found}` specs and {spec_ref} is a `{sp.get('diagram_type')}` spec")


def _notation_ref(docs: dict, sp: dict, spec_ref: str) -> str:
    """The notation ref of the spec, checked to exist and to match its diagram type."""
    notation_ref = sp.get("notation") or ""
    if not notation_ref:
        raise ViewError(f"{spec_ref} has no notation; sync it with `sldb notations sync --notation <name>`")
    notation = docs.get(notation_ref)
    if notation is None:
        raise ViewError(f"{spec_ref} points at {notation_ref}, which is not in the store")
    _same_type(notation_ref, notation, sp, spec_ref)
    return notation_ref


def resolve_view(store: Path | str, spec_ref: str, pythonpath: str | None = None) -> dict[str, Any]:
    """The view of a spec according to its notation, ready to draw; ViewError if spec or notation is unusable."""
    store_path = Path(store)
    if not spec_ref.startswith("SpecDoc:"):
        spec_ref = f"SpecDoc:{spec_ref}"
    docs = load_docs(store_path, pythonpath)
    if spec_ref not in docs:
        raise ViewError(f"{spec_ref} is not in the store")
    sp = docs[spec_ref]["payload"]
    notation_ref = _notation_ref(docs, sp, spec_ref)
    view = resolve_documents(store_path, notation_ref, list(sp.get("nodes") or []), spec_style=sp.get("style"), docs=docs)
    return {"spec": spec_ref, "title": sp.get("title", ""), "diagram_type": sp.get("diagram_type", ""), **view}
