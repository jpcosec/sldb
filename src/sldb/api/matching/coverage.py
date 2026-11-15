"""Cobertura por vista a partir de un snapshot de grafo con nodos `view`.

Migrado de `spec2viz.deskops` (`build_coverage_by_view`, `_discover_snapshot_path`,
`_project_root_from_snapshot`, `_item_source_ref`), sobre `SpecView`. Sin snapshot, o si no se
puede leer, la proyección queda vacía y se avisa con un finding.
"""

from __future__ import annotations

import json
from pathlib import Path

from sldb.api.matching.coverage_views import empty_coverage_payload, view_payload
from sldb.api.matching.matching_findings import finding
from sldb.api.matching.spec_view import SpecView
from sldb.core.finding import Finding

SNAPSHOT = Path(".sldb") / "runtime" / "knowledge_graph.kg.json"


def discover_snapshot_path(views: list[SpecView]) -> Path | None:
    """El primer `.sldb/runtime/knowledge_graph.kg.json` hacia arriba desde la carpeta de cada vista."""
    seen: set[Path] = set()
    for view in views:
        base = Path(view.base_dir or Path(view.source.split("#", 1)[0]).parent).resolve()
        for candidate in (c for c in (base, *base.parents) if c not in seen):
            seen.add(candidate)
            if (candidate / SNAPSHOT).exists():
                return candidate / SNAPSHOT
    return None


def source_ref(view: SpecView, project_root: Path) -> str:
    """El origen de la vista relativo a la raíz del proyecto del snapshot, con su `#fragmento`."""
    if not view.source:
        return ""
    path_text, _, fragment = view.source.partition("#")
    resolved = (Path(view.base_dir) / path_text).resolve()
    relative = resolved.relative_to(project_root).as_posix() if resolved.is_relative_to(project_root) else resolved.as_posix()
    return f"{relative}#{fragment}" if fragment else relative


def _view_nodes(snapshot: dict) -> tuple[dict[str, dict], dict[str, dict]]:
    """Nodos del snapshot por id, y los nodos `view` por su `source_ref`."""
    nodes = {n.get("identity", {}).get("node_id"): n for n in snapshot.get("nodes", []) if n.get("identity", {}).get("node_id")}
    views = {str(n.get("semantics", {}).get("source_ref") or "").strip(): n for n in nodes.values() if n.get("identity", {}).get("node_type") == "view"}
    return nodes, {ref: node for ref, node in views.items() if ref}


def _read(snapshot_path: Path | None, findings: list[Finding]) -> dict | None:
    if snapshot_path is None or not snapshot_path.exists():
        findings.append(finding("coverage-snapshot-missing", "snapshot", "Graph snapshot not found; coverage projection is empty.", "construir el grafo del store"))
        return None
    try:
        return json.loads(snapshot_path.read_text(encoding="utf-8"))
    except Exception as exc:
        findings.append(finding("coverage-snapshot-unreadable", str(snapshot_path), f"Failed to read graph snapshot: {exc}", "regenerar el snapshot del grafo"))
        return None


def _project(view: SpecView, view_node: dict | None, nodes: dict[str, dict]) -> dict:
    return view_payload(view, view_node, nodes) if view_node else empty_coverage_payload(view)


def build_coverage_by_view(
    views: list[SpecView], snapshot_path: Path | None = None, kgdb_snapshot_path: Path | None = None
) -> tuple[dict[str, dict], list[Finding]]:
    """`vista -> cobertura` desde el snapshot (o el que se encuentre hacia arriba) y los findings.
    `kgdb_snapshot_path` se acepta como alias, como en spec2viz."""
    findings: list[Finding] = []
    path = snapshot_path or kgdb_snapshot_path or discover_snapshot_path(views)
    snapshot = _read(path, findings)
    if snapshot is None:
        return {view.key: empty_coverage_payload(view) for view in views}, findings
    nodes, by_source = _view_nodes(snapshot)
    root = path.resolve().parents[2]
    return {view.key: _project(view, by_source.get(source_ref(view, root)), nodes) for view in views}, findings
