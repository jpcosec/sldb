"""The guard of a field write: it refuses to drop what the file carries and the model does not declare."""

from __future__ import annotations

from collections import Counter
from pathlib import Path

from sldb.api.documents.frontmatter_keys import _frontmatter_keys, undeclared_frontmatter_keys
from sldb.api.documents.heading_scan import format_heading, scan_headings
from sldb.api.documents.structural_noise import find_structural_noise
from sldb.api.documents.structural_noise_report import StructuralNoiseReport
from sldb.api.stores.policy import Policy, Subject
from sldb.core.exceptions import SLDBValidationError
from sldb.store.models.document_entry import DocumentEntry
from sldb.store.source_read import guarded_text


def refuse_lossy_overwrite(store_path: Path, root: Path, doc_entry: DocumentEntry, model_type: type, rendered: str) -> None:
    """Refuse, before anything is written, a field write that would silently drop what the file
    now carries and the model does not declare (headings or frontmatter keys).

    Only what is lost is refused: an undeclared heading that lives inside a field's value and
    survives in `rendered` (the text about to be written) does not block the write.

    Raises:
        SLDBValidationError: Naming the undeclared headings or keys that would be lost.
    """
    from sldb.models.provenance import Provenance

    current = guarded_text(root, root / doc_entry.path)
    if current is None:
        return
    report = find_structural_noise(model_type, current, doc_entry.name)
    kept = Counter(format_heading(lv, ti) for lv, ti in scan_headings(rendered))
    lost = []
    for line in report.undeclared:
        if kept[line] > 0:
            kept[line] -= 1
        else:
            lost.append(line)
    if lost:
        lost_report = StructuralNoiseReport(document=report.document, model=report.model, undeclared=lost, narrative=report.narrative)
        authority, declared = Provenance.of_model(model_type)
        subject = Subject(authority=authority, declared=declared, narrative=lost_report.narrative)
        if Policy.of_store(store_path).response("structural-noise", lost_report.model, subject) not in ("allow", "ignore"):
            raise SLDBValidationError(lost_report.message(), lost_report.details())
    _refuse_lost_keys(model_type, current, rendered, doc_entry.name)


def _refuse_lost_keys(model_type: type, current: str, rendered: str, name: str) -> None:
    keys = [k for k in undeclared_frontmatter_keys(model_type, current) if k not in _frontmatter_keys(rendered, load_yaml=True)]
    if not keys:
        return
    raise SLDBValidationError(
        f"frontmatter no declarado en '{name}': {', '.join(keys)} — "
        f"el modelo {getattr(model_type, '__name__', '?')} no declara estas claves, "
        f"así que se pierden al re-renderizar. Declaralas en el template, o el "
        f"documento pertenece a otra versión del modelo.",
        {"document": name, "model": getattr(model_type, "__name__", "?"), "undeclared_keys": keys},
    )
