"""Store-only documents for `sldb notations validate`: lookup and validation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

_STORE_MODELS = {"notation": "NotationDoc", "palette": "PaletteDoc"}


def _store_has(store: str | None, kind: str, name: str) -> bool:
    """True when the store tracks a `NotationDoc`/`PaletteDoc` called `name` (its file is not read)."""
    if not store:
        return False
    import sldb.api as api

    try:
        rows = api.select_documents(store, {"model": _STORE_MODELS[kind]})
    except Exception:
        return False
    return any(row["name"] == name for row in rows)


def _store_payload(model: str, name: str, store: str) -> Any:
    import sldb.api as api

    docs = api.load_runtime_documents(Path(store), None, include_linked=False)
    return next(d.payload for d in docs if str(d.model_name) == model and str(d.name) == name)


def _check_palette_payload(payload: Any) -> None:
    from sldb.notations.palette_checks import check_palette
    from sldb.notations.palette_spec import PaletteSpec

    check_palette(PaletteSpec.model_validate({k: v for k, v in dict(payload).items() if k != "id"}))


def _check_store_document(kind: str, name: str, store: str) -> None:
    """Validate a document that lives only in the store.

    A store document is a markdown file whose front matter is the payload (a notation's glyphs
    and links are separate documents), so `load_notation`/`load_palette` cannot read it by path.
    The store's own model validates it; a palette payload is then rebuilt as a `PaletteSpec`
    and checked like a palette file (contrast included).
    """
    import sldb.api as api

    model = _STORE_MODELS[kind]
    row = api.select_documents(store, {"ref": f"{model}:{name}", "model": model}, expect="one")[0]
    try:
        payload = _store_payload(model, name, store)
        if kind == "palette":
            _check_palette_payload(payload)
    except Exception as exc:
        raise ValueError(f"{row['path']}: {exc}") from exc
