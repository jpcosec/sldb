"""`stores check`'s notes on documents' content: headings their model does not declare, and
blocks a rewrite would lose. Diagnosis, never a failure."""

from __future__ import annotations

from typing import Any


def print_content_notes(sp: Any, root: Any, pythonpath: str | None) -> None:
    from sldb.api.stores.scan_rewrite_loss import scan_rewrite_loss
    from sldb.api.stores.scan_structural_noise import scan_structural_noise

    _print_noise(scan_structural_noise(sp, root, pythonpath))
    _print_rewrite_loss(scan_rewrite_loss(sp, root, pythonpath))


def _print_noise(reports: list[Any]) -> None:
    """Name every noisy document and the headings behind the verdict, never a count alone."""
    if not reports:
        return
    print(f"\nruido estructural: {len(reports)} documento(s) trackeado(s) traen headings que su modelo no declara")
    for report in reports:
        print(f"  {report.document} ({report.model}): {len(report.undeclared)} heading(s) sin declarar")
        for line in report.undeclared:
            print(f"      {line}")
    print("  fix     : creá un modelo que herede y declare esas secciones como campos optrev")


def _print_rewrite_loss(found: list[dict[str, Any]]) -> None:
    """Name each document and the blocks its own rewrite would drop."""
    if not found:
        return
    print(f"\nnote: {len(found)} documento(s) perderían contenido al reescribirse: su modelo no lee estos bloques")
    for item in found:
        print(f"  {item['document']} ({item['model']}, {item['path']}): {len(item['lost'])} bloque(s)")
        print("\n".join(f"      {block.splitlines()[0][:100]}" for block in item["lost"]))
    print("    fix     : pasa ese contenido a un campo que el modelo declare, o declara el campo; hasta entonces no lo reescribas con sldb ni deskops")
