"""The guard of a field write: it refuses to drop what the file carries and the model does not declare."""

from __future__ import annotations

from pathlib import Path

from sldb.api.documents.frontmatter_keys import refuse_undeclared_frontmatter
from sldb.api.documents.refuse_structural_noise import refuse_structural_noise
from sldb.api.stores.policy import Policy
from sldb.store.models.document_entry import DocumentEntry
from sldb.store.source_read import guarded_text


def refuse_lossy_overwrite(store_path: Path, root: Path, doc_entry: DocumentEntry, model_type: type) -> None:
    """Refuse, before anything is rendered or written, a field write that would silently drop
    what the file now carries and the model does not declare (headings or frontmatter keys):
    the same guard `docs create` and `docs track` apply, over the file's current text.

    Raises:
        SLDBValidationError: Naming the undeclared headings or keys that would be lost.
    """
    current = guarded_text(root, root / doc_entry.path)
    if current is None:
        return
    refuse_structural_noise(model_type, current, doc_entry.name, Policy.of_store(store_path))
    refuse_undeclared_frontmatter(model_type, current, doc_entry.name)
