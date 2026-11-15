"""Un elemento de un spec como dict comun: id, label, kind, collection, contains, atoms, refs, description y data.

Migrado de `spec2viz.sldb_sync._element`.
"""

from __future__ import annotations

from typing import Any

from sldb.api.notations.spec_refs import plain
from sldb.api.notations.spec_sync_constants import _ELEMENT_OWN_FIELDS


def _texts(eid: Any, el: dict) -> dict[str, str]:
    """Id, etiqueta y kind del elemento."""
    return {"id": str(eid), "label": str(el.get("label") or el.get("name") or eid), "kind": str(el.get("kind") or el.get("type") or "")}


def _lists(el: dict) -> dict[str, list[str]]:
    """`contains`, `atoms` y `refs` del elemento como listas de texto."""
    return {key: [str(v) for v in (el.get(key) or [])] for key in ("contains", "atoms", "refs")}


def element(eid: Any, el: Any, collection: str, extra_flags: dict[str, Any] | None = None) -> dict:
    """El elemento `eid` de `collection`; lo que no tiene sitio propio va a `data`, con `extra_flags`."""
    el = el if isinstance(el, dict) else {}
    extra = {str(k): plain(v) for k, v in el.items() if k not in _ELEMENT_OWN_FIELDS and v is not None}
    extra.update(extra_flags or {})
    description = str(el.get("description") or el.get("docstring") or "")
    return {**_texts(eid, el), "collection": collection, **_lists(el), "description": description, "data": extra}


def pairs(raw: Any) -> Any:
    """`(id, elemento)` de una coleccion escrita como mapa o como lista con `id`."""
    return raw.items() if isinstance(raw, dict) else [(e.get("id"), e) for e in raw if isinstance(e, dict)]
