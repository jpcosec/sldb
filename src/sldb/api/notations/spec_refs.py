"""Ids y tokens de la sincronizacion de specs: relaciones, refs de nodos, aristas y etapas.

Migrado de `spec2viz.sldb_sync`; `find_store` reutiliza `sldb.store.resolver.find_local_store`.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from sldb.api.notations.spec_sync_constants import STYLE_KEYS
from sldb.store.resolver import find_local_store


def spec_style_kinds(spec: dict) -> dict[str, dict[str, str]]:
    """`style.kinds` del spec reducido a las claves neutrales: kind -> {fill, stroke, icon}."""
    kinds = ((spec.get("style") or {}).get("kinds") or {}) if isinstance(spec.get("style"), dict) else {}
    out: dict[str, dict[str, str]] = {}
    for kind, entry in kinds.items():
        if isinstance(entry, dict):
            neutral = {k: (dict(entry[k]) if isinstance(entry[k], dict) else str(entry[k])) for k in STYLE_KEYS if entry.get(k)}
            if neutral:
                out[str(kind)] = neutral
    return out


def relation_token(value: Any, default: str) -> str:
    """La relacion del spec como token de vocabulario sldb (`loads(path)` -> `loads_path`)."""
    token = re.sub(r"[^a-z0-9]+", "_", str(value or "").strip().lower()).strip("_")
    return token or default


def node_ref(spec_id: str, element_id: str) -> str:
    """El id `SpecNodeDoc:<spec>.<elemento>` de un elemento del spec."""
    return f"SpecNodeDoc:{spec_id}.{element_id}"


def to_slash_ref(ref: str) -> str:
    """`Model:name` (o `alias:Model:name`) en la forma `Model/name` que `doc_exists` entiende."""
    head, _, name = ref.rpartition(":")
    return f"{head}/{name}"


def plain(value: Any) -> Any:
    """Un valor del spec como dato YAML plano (sin tuplas)."""
    if isinstance(value, dict):
        return {str(k): plain(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [plain(v) for v in value]
    return value


def stage_id(view_id: str, stage: str) -> str:
    """Id de elemento de una etapa de una vista de matriz: `<vista>__<etapa>`."""
    return f"{view_id}__{stage}"


def edge_name(spec_id: str, index: int, count: int, edge: dict) -> str:
    """`<spec>.<nn>-<from>__<rel>__<to>`: el prefijo ordena las aristas y evita duplicados."""
    width = max(2, len(str(count)))
    return f"{spec_id}.{index:0{width}d}-{edge['from']}__{edge['relation']}__{edge['to']}"


def relation_doc_has_attributes() -> bool:
    """Si el `RelationDoc` instalado tiene el campo libre `attributes` (sldb >= 0.1.11)."""
    from sldb.models.relation_doc import RelationDoc

    return "attributes" in getattr(RelationDoc, "model_fields", {})


def find_store(start: Path) -> Path | None:
    """El `.sldb` mas cercano hacia arriba desde `start`, si sldb lo reconoce como store."""
    store = find_local_store(Path(start))
    return store.resolve() if store is not None else None
