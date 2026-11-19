"""Which indexed documents `docs show` cannot resolve, and why.

`indexed_documents` reads the indexes alone; `runtime_document` (what `docs show` uses) also needs
the tracked file to exist and be readable, and drops the document when not (a model that does not
import is a caller's path problem, not a property of the document, and is not judged here). This names the indexed documents in that gap, so `docs list` does not offer a name that
`docs show` answers with 'Unknown document target'.
"""

from __future__ import annotations

from pathlib import Path

from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.layout import project_root
from sldb.store.source_read import unreadable_reason
from sldb.store.source_guard import READ_CODES

FILE_MISSING = "file-missing"


def unresolvable_documents(store_path: Path) -> dict[tuple[str, str], str]:
    """`{(model, name): cause}` for each indexed document that `docs show` would not find.

    The cause is `file-missing` or the read-guard code
    (`store/path-outside-root`, `store/symlink-not-read`). Resolvable documents are absent.
    """
    root = project_root(store_path)
    found: dict[tuple[str, str], str] = {}
    for entry in load_store_index(store_path).models:
        index = load_documents_index(root / load_models_index(root / entry.models_index).documents_index)
        for doc in index.documents:
            if cause := _cause(root, doc.path):
                found[(entry.name, doc.name)] = cause
    return found


def _cause(root: Path, path: str) -> str | None:
    if (reason := unreadable_reason(root, root / path)) is not None:
        return READ_CODES[reason]
    return None if (root / path).exists() else FILE_MISSING
