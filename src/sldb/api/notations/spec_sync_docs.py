"""Los `SpecNodeDoc` y el `SpecDoc` de un spec sincronizado.

Migrado del cuerpo de `spec2viz.sldb_sync.SpecSync.sync` (nodos y el spec).
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from sldb.api.notations.spec_refs import node_ref, spec_style_kinds
from sldb.api.notations.sync_report import SyncReport

_CATALOG_KEYS = ("category", "nav", "summary")


def node_payload(spec_id: str, el: dict) -> dict[str, Any]:
    """El payload del `SpecNodeDoc` de un elemento."""
    return {
        "id": f"{spec_id}.{el['id']}", "title": el["label"], "spec": f"SpecDoc:{spec_id}", "element": el["id"], "kind": el["kind"],
        "collection": el["collection"], "refs": el["refs"], "atom_refs": [f"AtomDoc:{a}" for a in el["atoms"]],
        "contains": [node_ref(spec_id, c) for c in el["contains"]], "data": el["data"], "description": el["description"],
    }


def upsert_nodes(writer: Any, existing: dict, report: SyncReport, spec_id: str, elements: list[dict], out: Path) -> set[tuple[str, str]]:
    """Upsert de un `SpecNodeDoc` por elemento; devuelve sus claves `(modelo, nombre)`."""
    for el in elements:
        payload = node_payload(spec_id, el)
        writer.upsert(existing, report, "SpecNodeDoc", payload["id"], out / "nodes" / f"{payload['id']}.md", payload)
    return {("SpecNodeDoc", f"{spec_id}.{el['id']}") for el in elements}


def kept_catalog(existing: dict, spec_id: str, catalog: dict[str, str] | None) -> dict[str, str] | None:
    """Sin catalogo (sync de un spec), el SpecDoc conserva la categoria, la nav y el resumen que le
    dio el sync del catalogo en vez de borrarlos."""
    if catalog is None and ("SpecDoc", spec_id) in existing:
        previous = existing[("SpecDoc", spec_id)].payload
        return {k: previous.get(k) or "" for k in _CATALOG_KEYS}
    return catalog


def _relative(spec_path: Path, root: Path) -> str:
    try:
        return str(spec_path.relative_to(root))
    except ValueError:
        return str(spec_path)


def _spec_head(spec: dict, spec_id: str, spec_path: Path, root: Path, text: str) -> dict[str, Any]:
    """Identidad del `SpecDoc`: id, titulo, tipo, version, ruta y hash del YAML."""
    return {
        "id": spec_id, "title": str(spec.get("title") or spec_id), "diagram_type": str(spec.get("type") or ""),
        "version": str(spec.get("version") or ""), "spec_path": _relative(spec_path, root),
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
    }


def upsert_spec_doc(writer: Any, existing: dict, report: SyncReport, source: tuple, catalog: dict | None, elements: list[dict]) -> None:
    """Upsert del `SpecDoc`; `source` es `(spec_path, text, spec, out)`."""
    spec_path, text, spec, out = source
    spec_id = report.spec_id
    catalog = kept_catalog(existing, spec_id, catalog) or {}
    payload = {
        **_spec_head(spec, spec_id, spec_path, writer.root, text), "notation": report.notation,
        **{k: str(catalog.get(k) or "") for k in _CATALOG_KEYS}, "style": spec_style_kinds(spec) or None,
        "nodes": [node_ref(spec_id, el["id"]) for el in elements], "description": str((spec.get("metadata") or {}).get("description") or ""),
    }
    writer.upsert(existing, report, "SpecDoc", spec_id, out / f"{spec_id}.md", payload)
