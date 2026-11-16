"""Bulk runtime load through sldb.api: every tracked document, payload and both hashes.

``sldb r…``/serve consumers used to import ``sldb.store.query.load_runtime_documents``
directly; this wrapper supplies the model resolver the store function takes as a parameter,
so a consumer names only a store path, an optional pythonpath and whether to follow links.

One document its model rejects used to abort the whole load with a ValidationError that named
no file. By default (``on_invalid="raise"``) it still aborts, as an SLDBValidationError whose
message starts with the document's path; ``on_invalid="skip"`` returns the sound documents and
names the rejected ones instead (``RuntimeDocuments``).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, overload

from pydantic import ValidationError

from sldb.api.model_registry.model_reference import resolve_model_ref
from sldb.core.exceptions import SLDBValidationError
from sldb.store.query import load_runtime_documents as _load_runtime_documents

__all__ = ["InvalidDocument", "RuntimeDocuments", "load_runtime_documents"]


@dataclass(frozen=True)
class InvalidDocument:
    """A tracked document its model rejects: path relative to its project root, the model's
    name and the text of the validation error."""

    path: str
    model: str
    error: str


@dataclass
class RuntimeDocuments:
    """What ``load_runtime_documents(..., on_invalid="skip")`` returns: the documents that
    load, and the ones left out because their model rejects them."""

    documents: list[Any] = field(default_factory=list)
    invalid: list[InvalidDocument] = field(default_factory=list)


@overload
def load_runtime_documents(store_path: Path, pythonpath: str | None = ..., include_linked: bool = ..., on_invalid: Literal["raise"] = ...) -> list[Any]: ...
@overload
def load_runtime_documents(store_path: Path, pythonpath: str | None = ..., include_linked: bool = ..., *, on_invalid: Literal["skip"]) -> RuntimeDocuments: ...
def load_runtime_documents(store_path: Path, pythonpath: str | None = None, include_linked: bool = False, on_invalid: Literal["raise", "skip"] = "raise") -> list[Any] | RuntimeDocuments:
    """Every runtime document of `store_path`, extracted, with its two index hashes.

    `on_invalid="raise"` (default): a list, as always; a document its model rejects raises
    SLDBValidationError("<path>: <original message>"). `on_invalid="skip"`: RuntimeDocuments
    with the sound documents and each rejected one as InvalidDocument, without raising."""
    if on_invalid == "skip":
        return _skipping(store_path, pythonpath, include_linked)
    if on_invalid != "raise":
        raise ValueError(f"on_invalid must be 'raise' or 'skip', not {on_invalid!r}")
    try:
        return _load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=include_linked)
    except ValidationError as exc:
        invalid = _skipping(store_path, pythonpath, include_linked).invalid
        if not invalid:
            raise
        raise SLDBValidationError(f"{invalid[0].path}: {exc}", {"path": invalid[0].path, "model": invalid[0].model}) from exc


def _skipping(store_path: Path, pythonpath: str | None, include_linked: bool) -> RuntimeDocuments:
    """The load with each rejected document left out and named (uncached, as `stores check`)."""
    rejected: list[tuple[str, str, str]] = []
    documents = _load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=include_linked, accepted_only=True, rejected=rejected)
    return RuntimeDocuments(documents=documents, invalid=[InvalidDocument(*r) for r in rejected])
