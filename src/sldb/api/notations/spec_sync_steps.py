"""Los pasos de `SpecSync.sync` despues de la notacion: nodos, spec, aristas, borrado y refs.

Migrado del cuerpo de `spec2viz.sldb_sync.SpecSync.sync`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from sldb.api.notations.spec_edges import spec_edges
from sldb.api.notations.spec_elements import spec_elements
from sldb.api.notations.spec_refs import to_slash_ref
from sldb.api.notations.spec_sync_docs import upsert_nodes, upsert_spec_doc
from sldb.api.notations.spec_sync_edges import ensure_spec_relations, upsert_edges
from sldb.api.notations.sync_report import SyncReport
from sldb.notations.exceptions import ParseError

_OWNED = ("SpecNodeDoc", "RelationDoc")


def check_yaml_and_id(path: Path) -> None:
    """La validacion previa por defecto: el YAML se lee y es un mapa con `id`."""
    spec = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    if not isinstance(spec, dict) or not spec.get("id"):
        raise ParseError(f"{path}: a diagram spec is a mapping with an `id`")


def write_spec(writer: Any, existing: dict, report: SyncReport, source: tuple, catalog: dict | None) -> None:
    """Nodos, spec y aristas; borra lo que salio del spec y anota las refs que no existen."""
    spec, out = source[2], source[3]
    elements, edges = spec_elements(spec), spec_edges(spec)
    ensure_spec_relations(writer, existing, report, edges)
    current = upsert_nodes(writer, existing, report, report.spec_id, elements, out)
    upsert_spec_doc(writer, existing, report, source, catalog, elements)
    current |= upsert_edges(writer, existing, report, edges, out)
    prune_spec(writer, existing, report, report.spec_id, current)
    report_unresolved(writer, report, elements)


def prune_spec(writer: Any, existing: dict, report: SyncReport, spec_id: str, current: set[tuple[str, str]]) -> None:
    """Borra los `SpecNodeDoc` y `RelationDoc` de `spec_id` que ya no estan en `current`."""
    prefix = f"{spec_id}."
    for model, name in list(existing):
        if model in _OWNED and name.startswith(prefix) and (model, name) not in current:
            writer.delete(existing, report, model, name)


def report_unresolved(writer: Any, report: SyncReport, elements: list[dict]) -> None:
    """Refs y atoms que no existen: aristas de schema, el indice no las reporta."""
    import sldb.api as api

    for el in elements:
        for ref in [*el["refs"], *(f"AtomDoc:{a}" for a in el["atoms"])]:
            if not api.doc_exists(writer.store_path, to_slash_ref(ref)):
                report.unresolved.append(f"{report.spec_id}.{el['id']}: '{ref}' no existe en el store")


def with_problems(report: SyncReport) -> SyncReport:
    """`problems` = `unresolved` + `edge_errors` (en spec2viz era una propiedad)."""
    report.problems = [*report.unresolved, *report.edge_errors]
    return report
