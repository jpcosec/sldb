"""`check_catalog`: valida cada entrada de un `vistas.yml` sin escribir nada.

Migrado de `spec2viz.sldb_sync.check_catalog`; el spec se carga y valida con los modelos de
sldb (`load_spec`, `validate_spec`, D3) en vez de `spec2viz.loader` y `spec2viz.validator`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.notations.spec_catalog import catalog_entries
from sldb.api.notations.spec_models import load_spec, validate_spec
from sldb.api.notations.spec_notation import resolve_spec_notation
from sldb.notations.notation import DEFAULT_NOTATIONS


def _check_entry(entry: dict[str, Any], store_path: Path | None, pythonpath: str | None, include_src: bool) -> None:
    """Lanza el primer error de la entrada: ruta, `src`, spec o notacion."""
    if entry["errors"]:
        raise entry["errors"][0]
    if include_src and entry["src_error"] is not None:
        raise entry["src_error"]
    diagram = load_spec(entry["spec"])
    validate_spec(diagram)
    kind = diagram.type.value
    chosen = DEFAULT_NOTATIONS.get(kind) if entry["notation"] is None else entry["notation"]
    resolve_spec_notation(chosen, kind, diagram.id, store_path, pythonpath)


def check_catalog(config: Path, store_path: Path | None = None, pythonpath: str | None = None,
                  include_src: bool = True) -> list[tuple[dict[str, Any], Exception | None]]:
    """Valida cada entrada de un `vistas.yml` sin escribir nada: sus rutas resuelven sin
    ambiguedad, el spec valida y su notacion resuelve y dibuja su tipo de diagrama. Una tupla
    (entrada, primer error o None) por spec."""
    results: list[tuple[dict[str, Any], Exception | None]] = []
    for entry in catalog_entries(config):
        try:
            _check_entry(entry, store_path, pythonpath, include_src)
            results.append((entry, None))
        except Exception as exc:  # cada entrada informa su propio error tipado
            results.append((entry, exc))
    return results
