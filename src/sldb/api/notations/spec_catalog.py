"""`catalog_entries`: las entradas de un `vistas.yml`, con sus rutas resueltas y sus errores.

Migrado de `spec2viz.sldb_sync.catalog_entries`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from sldb.api.notations.catalog_paths import resolve_catalog_path, split_fragment
from sldb.api.notations.spec_notation import looks_like_path
from sldb.notations.exceptions import AmbiguousPathError, UnknownNotationError, UnknownReferenceError


def _resolve(value: str, base: Path, field: str, missing: type[Exception] | None = None) -> tuple[Path | None, Exception | None]:
    """`(ruta, None)` o `(None, error)`: AmbiguousPathError, UnknownReferenceError, UnknownNotationError."""
    try:
        return resolve_catalog_path(value, base, field, missing or UnknownReferenceError), None
    except Exception as exc:
        return None, exc


def _view_notation(vista: dict, base: Path, errors: list[Exception]) -> str | Path | None:
    """La notacion de la vista: una ruta resuelta, un nombre o None (la builtin del tipo)."""
    if not vista.get("notation"):
        return None
    text = str(vista["notation"])
    if not looks_like_path(text):
        return text
    notation, error = _resolve(text, base, "notation", UnknownNotationError)
    if error:
        errors.append(error)
    return notation


def _view_src(vista: dict, base: Path, errors: list[Exception]) -> tuple[Path | None, Exception | None]:
    """El `src`/`mmd` de la vista, sin fragmento; ambiguo bloquea, ausente queda en `src_error`."""
    if not (vista.get("src") or vista.get("mmd")):
        return None, None
    src, src_error = _resolve(split_fragment(str(vista.get("src") or vista.get("mmd")))[0], base, "src")
    # el sync no lee `src` (es la fuente del catalogo HTML): un src que falta lo informa
    # `--check`; uno ambiguo bloquea igual que spec y notation
    if isinstance(src_error, AmbiguousPathError):
        errors.append(src_error)
        src_error = None
    return src, src_error


def _catalog_meta(vista: dict) -> dict[str, str]:
    return {"category": str(vista.get("category") or ""), "nav": str(vista.get("nav") or ""),
            "summary": str(vista.get("desc") or vista.get("title") or "")}


def _view_entries(vista: dict, base: Path) -> list[dict[str, Any]]:
    errors: list[Exception] = []
    notation = _view_notation(vista, base, errors)
    src, src_error = _view_src(vista, base, errors)
    out: list[dict[str, Any]] = []
    for spec in vista.get("specs") or []:
        path, error = _resolve(str(spec), base, "spec")
        out.append({"spec": path if path is not None else Path(str(spec)), "vista": str(vista.get("id") or ""), "notation": notation,
                    "src": src, "src_error": src_error, "errors": [*errors, *([error] if error else [])], "catalog": _catalog_meta(vista)})
    return out


def catalog_entries(config: Path) -> list[dict[str, Any]]:
    """Las entradas de un `vistas.yml`: por cada spec listado, su ruta, sus metadatos de catalogo,
    la notacion de la vista y su `src`.

    Todas las rutas (`specs`, `notation`, `src`/`mmd`) siguen la regla de `catalog_paths`. Un
    `notation` que no parece ruta es un nombre (builtin o `NotationDoc` del store); sin campo, la
    builtin del tipo. Los errores de ruta no se lanzan aqui: quedan en `errors` de la entrada,
    para que `check_catalog` los informe todos y `sync_catalog` no escriba nada.
    """
    config = Path(config).resolve()
    raw = yaml.safe_load(config.read_text(encoding="utf-8")) or {}
    return [entry for vista in raw.get("vistas") or [] if isinstance(vista, dict) for entry in _view_entries(vista, config.parent)]
