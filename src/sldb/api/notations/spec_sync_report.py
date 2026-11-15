"""El informe de una sincronizacion: una linea por spec o notacion, y sus avisos como findings.

`format_report` y `format_notation_report` migrados de `spec2viz.sldb_sync`; leen el campo
`problems` del `SyncReport` de sldb. `report_findings` da los avisos en el formato de sldb.
"""

from __future__ import annotations

from sldb.api.notations.spec_catalog_sync import ORPHAN_PREFIX
from sldb.api.notations.sync_report import SyncReport
from sldb.core.finding import Finding, alert


def _count(report: SyncReport, prefix: str) -> int:
    return sum(1 for d in [*report.created, *report.updated] if d.startswith(prefix))


def _tail(report: SyncReport, line: str) -> str:
    """Cierra la linea y agrega un `! problema` por renglon."""
    line += ")"
    for problem in report.problems:
        line += f"\n  ! {problem}"
    return line


def _counts(report: SyncReport) -> str:
    line = f"({len(report.created)} created, {len(report.updated)} updated, {len(report.deleted)} deleted"
    return line + (f", relation types added: {', '.join(report.relation_types_added)}" if report.relation_types_added else "")


def format_report(report: SyncReport) -> str:
    """Una linea por spec, con lo que paso."""
    head = f"Synced {report.spec_id}: {_count(report, 'SpecNodeDoc:')} nodes, {_count(report, 'RelationDoc:')} edges "
    notation = f", notation {report.notation}" if report.notation else ""
    return _tail(report, head + _counts(report) + notation)


def format_notation_report(report: SyncReport) -> str:
    """Una linea por notacion, con lo que paso."""
    head = f"Synced notation {report.spec_id}: {_count(report, 'GlyphDoc:')} glyphs, {_count(report, 'LinkDoc:')} links "
    return _tail(report, head + _counts(report))


def _unresolved(report: SyncReport, problem: str) -> Finding:
    if problem.startswith(ORPHAN_PREFIX):
        return alert("spec-sync/orphan-spec", report.spec_id, problem, "sldb notations sync --catalog <vistas.yml> --prune")
    return alert("spec-sync/unresolved-ref", report.spec_id, problem, "crear el documento referido o quitar la ref del spec")


def report_findings(report: SyncReport) -> list[Finding]:
    """Los avisos del informe: refs sin resolver, SpecDoc huerfanos y errores del indice de aristas."""
    edge = [alert("spec-sync/edge-error", report.spec_id, e, "sldb edges check") for e in report.edge_errors]
    return [*(_unresolved(report, p) for p in report.unresolved), *edge]
