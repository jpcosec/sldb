"""Node kinds, document refs and safe ids of the component spec (migrated from `spec2viz.graph_import`)."""

from __future__ import annotations

import re
from typing import Iterable

from sldb.api.notations.component_spec_constants import _RESERVED_IDS, SLDB_SCHEME


def _normalize_type(node_type: str) -> str:
    """`sldb_document` -> `document`; los demas tipos quedan igual."""
    return node_type[5:] if node_type.startswith("sldb_") else node_type


def node_kind(node_id: str, node_type: str) -> str:
    """Tipo canonico del nodo: el segmento tras `sldb://` (document, model, ...).

    Cae al `node_type` de la fuente (sin el prefijo `sldb_`) cuando el id no sigue
    el esquema; el store index tipa los documentos con el nombre del modelo, por eso
    el id manda.
    """
    if node_id.startswith(SLDB_SCHEME):
        head = node_id[len(SLDB_SCHEME):].split("/", 1)[0]
        if head:
            return head
    return _normalize_type(node_type)


def _id_tail(node_id: str) -> str:
    """Parte del id despues de `sldb://<kind>/` (o el id completo si no aplica)."""
    if node_id.startswith(SLDB_SCHEME):
        rest = node_id[len(SLDB_SCHEME):]
        return rest.split("/", 1)[1] if "/" in rest else rest
    return node_id


def document_ref(node_id: str, node_type: str = "") -> tuple[str | None, str | None]:
    """(modelo, nombre) de un nodo documento `sldb://document/[store:]Model:name`.

    Devuelve `(None, None)` si el nodo no es un documento. El modelo cae al
    `node_type` cuando el id no trae la parte `Model:` (store index tipa asi).
    """
    if node_kind(node_id, node_type) != "document":
        return None, None
    tail = _id_tail(node_id)
    parts = tail.split(":")
    if len(parts) >= 3:
        return parts[-2], parts[-1]
    if len(parts) == 2:
        return parts[0], parts[1]
    model = _normalize_type(node_type) if node_type and node_type != "document" else None
    return model, tail


def sanitize_id(node_id: str) -> str:
    """Identificador seguro `[A-Za-z0-9_]` a partir de un id `sldb://...`."""
    text = node_id[len(SLDB_SCHEME):] if node_id.startswith(SLDB_SCHEME) else node_id
    text = re.sub(r"[^A-Za-z0-9_]+", "_", text).strip("_")
    if not text:
        text = "node"
    if text[0].isdigit() or text in _RESERVED_IDS:
        text = f"n_{text}"
    return text


def _unique_ids(node_ids: Iterable[str]) -> dict[str, str]:
    """Mapa id original -> id seguro, unico dentro del spec (sufijo `_2`, `_3`, ...)."""
    mapping: dict[str, str] = {}
    taken: set[str] = set()
    for node_id in node_ids:
        mapping[node_id] = _free_id(sanitize_id(node_id), taken)
    return mapping


def _free_id(base: str, taken: set[str]) -> str:
    """`base`, o `base_2`, `base_3`, ... el primero libre; queda tomado."""
    candidate = base
    n = 1
    while candidate in taken:
        n += 1
        candidate = f"{base}_{n}"
    taken.add(candidate)
    return candidate


def _label_and_kind(node_id: str, node_type: str) -> tuple[str, str]:
    """Etiqueta y `kind` del nodo: documentos -> (name, Model); modelos -> (Model, model)."""
    kind = node_kind(node_id, node_type)
    if kind == "document":
        model, name = document_ref(node_id, node_type)
        return name or _id_tail(node_id), model or "document"
    if kind == "model":
        return _id_tail(node_id), "model"
    return _id_tail(node_id) or node_id, kind
