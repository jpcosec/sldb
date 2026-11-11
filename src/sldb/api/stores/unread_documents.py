"""A tracked (or declared) document the store does not read (SEGURIDAD resto, after live_stale).

Its path resolves outside the project root or is a symlink (`source_read.unreadable_reason`):
`stores update` and `stores build` name it with the finding `stores check` already gives it
(`store/path-outside-root`, `store/symlink-not-read`, by `store_findings._DOC_CODES`) and go on
with the other documents, instead of reading it or stopping."""

from __future__ import annotations

import logging
from pathlib import Path

from sldb.api.stores.declared_files import rule_rows
from sldb.api.stores.store_declaration import StoreDeclaration
from sldb.api.stores.store_findings import _DOC_CODES
from sldb.core.finding import Finding, alert
from sldb.store.diagnostics_models.document_verdicts import EXPLANATIONS, REMEDIES
from sldb.store.diagnostics_models.unread_verdict import unread_note
from sldb.store.source_read import read_source_text

logger = logging.getLogger(__name__)


def unread_finding(root: Path, path: Path, subject: str, document: str | None = None) -> Finding | None:
    """The alert of a document at `path` that must not be read; None when it may be read."""
    if (note := unread_note(root, path)) is None:
        return None
    return alert(_DOC_CODES[note], subject, EXPLANATIONS[note], REMEDIES[note], document)


def warn_unread(root: Path, path: Path, subject: str, document: str | None = None) -> str | None:
    """`unread_finding`, logged as a warning; its code, or None when the document may be read."""
    if (found := unread_finding(root, path, subject, document)) is None:
        return None
    logger.warning(found.line())
    return found.code


def unread_declared(root: Path, declaration: StoreDeclaration) -> list[dict]:
    """The declared paths `stores build` does not read (nor track), as alert dicts, by path (`stores build --check` reports them)."""
    paths = sorted({path for _, _, path, _ in rule_rows(root, declaration)})
    return [f.as_dict() for path in paths if (f := unread_finding(root, root / path, path)) is not None]


def tracked_text(root: Path, doc, model: str, skipped: list[str]) -> str | None:
    """The tracked document's text, or None and its name added to `skipped`: missing, or not read
    (`name (code)`, warned with its finding) because its path escapes the root or is a symlink."""
    doc_path = root / doc.path
    if (code := warn_unread(root, doc_path, f"{model}:{doc.name}", doc.name)) is not None:
        skipped.append(f"{doc.name} ({code})")
        return None
    if not doc_path.exists():
        skipped.append(doc.name)
        return None
    return read_source_text(doc_path)
