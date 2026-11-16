"""The runtime load that leaves out (and names) each document its model rejects."""

from __future__ import annotations

from pydantic import ValidationError


def load_accepted(load_doc, *args, rejected: list[tuple[str, str, str]] | None = None):
    """`load_doc(*args)`, None for a document its model rejects: `stores check` names it once,
    as `store/doc-invalid` (inbox 3895e9f7 H1), and its scans read the rest. A caller that
    wants them named passes `rejected`: each one is added as (path, model, message)."""
    try:
        return load_doc(*args)
    except ValidationError as exc:
        if rejected is not None:
            doc, m_entry = args[0], args[3]
            rejected.append((str(doc.path), m_entry.name, str(exc)))
        return None
