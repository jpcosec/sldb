"""`sldb.api.replace_text(store, ref, old, new, *, count=1, transaction=None)` (GD27): exactly
`count` literal occurrences of `old` become `new` in a tracked document or in a plain file
under the project root, inside a transaction (docs/architecture/transactions.md).

`ref` is what `doc_status` resolves (`name`, `Model/name` or a tracked path); when it names no
document it is a path relative to the project root, which must exist inside it. The count is
`str.count` over the UTF-8 text as it is; another number is an error naming it, and nothing is
written. A tracked document is validated as any write (round-trip under its model, then the
`on_write` rules) before its bytes are rewritten and it is tracked again with the same model
and name; any error leaves the file as it was.
"""

from __future__ import annotations

import hashlib
from contextlib import nullcontext
from pathlib import Path
from typing import Any

from sldb.api.documents.transaction import Transaction, transaction as open_transaction
from sldb.api.documents.transaction_paths import inside
from sldb.api.model_registry.load_registered_model import load_registered_model
from sldb.api.rules.rules_on_write import check_on_write
from sldb.api.stores.doc_ref import LOCAL
from sldb.api.stores.doc_status import doc_status
from sldb.api.stores.open_store import open_store
from sldb.api.stores.store_location import StoreLocation
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBValidationError
from sldb.runtime.validation import validate_model_input_roundtrip
from sldb.store.source_read import refuse_unreadable


def replace_text(store: str | Path | None, ref: str, old: str, new: str, *, count: int = 1, transaction: Transaction | None = None, pythonpath: str | None = None) -> dict[str, Any]:
    """Replace `old` by `new` exactly `count` times in `ref` (see the module).

    With `transaction`, the writes join it (it must be open over `store`); without one, the
    call opens its own. Returns `{ref, path, tracked, model, name, count}`, `path` relative to
    the project root. Raises `SLDBValidationError` (count, arguments, a document that no
    longer validates), `SLDBDocumentTargetError` (an unknown or ambiguous `ref`),
    `SLDBStoreError` (a path outside the root) or `SLDBRuleViolationError` (an `on_write` rule).
    """
    _check_arguments(old, count)
    location = open_store(store)
    status = _status(location, ref)
    path = location.project_root / status.path if status.exists else _plain_path(location.project_root, ref)
    refuse_unreadable(location.project_root, path)  # a tracked symlink is neither read nor rewritten
    data, text = _read(path, ref)
    replaced = _replaced(text, old, new, count, ref).encode("utf-8")
    with nullcontext(transaction) if transaction is not None else open_transaction(location.store_path, pythonpath) as tx:
        _write(tx, location, status, path, data, replaced, pythonpath)
    return {"ref": ref, "path": path.relative_to(location.project_root).as_posix(), "tracked": status.exists, "model": status.model, "name": status.name, "count": count}


def _check_arguments(old: str, count: int) -> None:
    if not old:
        raise SLDBValidationError("replace_text: old must not be empty")
    if not isinstance(count, int) or count < 1:
        raise SLDBValidationError(f"replace_text: count must be an integer >= 1, not {count!r}")


def _status(location: StoreLocation, ref: str) -> Any:
    status = doc_status(location.store_path, ref)
    if status.status == "ambiguous":
        raise SLDBDocumentTargetError(f"Ambiguous document target: {ref} ({status.detail})")
    if status.exists and status.store != LOCAL:
        raise SLDBDocumentTargetError(f"Unknown document target: {ref} (a linked store's document is replaced from its own store)")
    return status


def _plain_path(root: Path, ref: str) -> Path:
    path = inside(root, ref)
    if not path.is_file():
        raise SLDBDocumentTargetError(f"Unknown document target: {ref} (no tracked document, no file under {root})")
    return path


def _read(path: Path, ref: str) -> tuple[bytes, str]:
    data = path.read_bytes()
    try:
        return data, data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise SLDBValidationError(f"{ref} is not UTF-8 text: {exc}") from exc


def _replaced(text: str, old: str, new: str, count: int, ref: str) -> str:
    seen = text.count(old)
    if seen != count:
        raise SLDBValidationError(f"{ref}: {old!r} occurs {seen} time(s), not {count}; nothing written", {"seen": seen, "expected": count})
    return text.replace(old, new, count)


def _write(tx: Transaction, location: StoreLocation, status: Any, path: Path, data: bytes, replaced: bytes, pythonpath: str | None) -> None:
    """The plain file rewritten, or the document validated, rewritten and tracked again."""
    digest = hashlib.sha256(data).hexdigest()
    if not status.exists:
        tx.write_file(path, replaced, digest)
        return
    node, model_type = f"{status.model}:{status.name}", load_registered_model(location.store_path, status.model, pythonpath).model_type
    check_on_write(location.store_path, model_type, node, _payload(model_type, replaced.decode("utf-8"), node))
    tx.untrack(status.path)
    tx.write_file(path, replaced, digest)
    tx.track(path, status.model, status.name)


def _payload(model_type: type, text: str, node: str) -> dict[str, Any]:
    """The payload the replaced text extracts under the model, once it round-trips."""
    try:
        valid, details = validate_model_input_roundtrip(model_type, text)
    except ValueError as exc:
        raise SLDBValidationError(f"{node}: the replaced text does not validate under {model_type.__name__}: {exc}") from exc
    if not valid:
        raise SLDBValidationError(f"{node}: the replaced text does not round-trip under {model_type.__name__}; nothing written", details)
    return details["input_data"]
