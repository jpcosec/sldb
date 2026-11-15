"""La notacion con que se sincroniza un spec: builtin, YAML propio o `NotationDoc` del store.

Migrado de `spec2viz.sldb_sync` (`resolve_spec_notation`, `_store_notation`, `_looks_like_path`).
"""

from __future__ import annotations

from pathlib import Path

from sldb.notations.exceptions import NotationMismatchError, UnknownNotationError, ValidationError
from sldb.notations.notation import builtin_notations, load_notation, notation_ref
from sldb.notations.notation_spec import NotationSpec


def looks_like_path(value: str) -> bool:
    """Si un valor de `notation` es una ruta y no un nombre."""
    return "/" in value or "\\" in value or value.endswith((".yml", ".yaml"))


def _from_file(chosen: str | Path, text: str, spec_id: str) -> tuple[str, NotationSpec]:
    """Una notacion builtin o un YAML: `(tipo que dibuja, notacion cargada)`."""
    if not (text in builtin_notations() or Path(text).is_file()):
        raise UnknownNotationError(f"notation {text!r} for `{spec_id}`: no such file")
    try:
        spec = load_notation(chosen)
    except ValidationError as exc:
        raise ValidationError(f"notation {text!r} for `{spec_id}` is not valid: {exc}") from exc
    return spec.diagram_type, spec


def _from_store(text: str, spec_id: str, store_path: Path | None, pythonpath: str | None) -> tuple[str, str]:
    """Un `NotationDoc` del store por nombre: `(tipo que dibuja, ref)`."""
    doc = _store_notation(store_path, text, pythonpath)
    if doc is None:
        where = f"the store {store_path}" if store_path else "any store (none given)"
        builtins = ", ".join(builtin_notations())
        raise UnknownNotationError(f"notation {text!r} for `{spec_id}` is not a builtin ({builtins}) nor a NotationDoc in {where}")
    return str(doc.get("diagram_type") or ""), notation_ref(text)


def resolve_spec_notation(chosen: str | Path | None, diagram_type: str, spec_id: str, store_path: Path | None = None,
                          pythonpath: str | None = None) -> NotationSpec | str | None:
    """La notacion con que se sincroniza un spec.

    Una ruta (un archivo) o un nombre builtin se cargan y validan (`NotationSpec`); un nombre que
    no es builtin resuelve contra los `NotationDoc` del store y devuelve su ref. `None`/`none` no
    lleva notacion. `UnknownNotationError` si no resuelve; `NotationMismatchError` si dibuja otro
    tipo de diagrama.
    """
    if not chosen or str(chosen) == "none":
        return None
    text = str(chosen)
    if isinstance(chosen, Path) or looks_like_path(text) or text in builtin_notations():
        drawn, result = _from_file(chosen, text, spec_id)
    else:
        drawn, result = _from_store(text, spec_id, store_path, pythonpath)
    if drawn != diagram_type:
        raise NotationMismatchError(f"notation {text!r} draws `{drawn}` specs, and `{spec_id}` is a `{diagram_type}` spec")
    return result


def _store_notation(store_path: Path | None, name: str, pythonpath: str | None) -> dict | None:
    if store_path is None:
        return None
    import sldb.api as api

    docs = api.load_runtime_documents(store_path, pythonpath, include_linked=True)
    return next((dict(doc.payload) for doc in docs if str(doc.model_name) == "NotationDoc" and doc.name == name), None)
