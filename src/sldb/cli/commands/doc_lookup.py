"""Compatibility bridge: `find_doc` now lives in `sldb.api.documents.document_lookup`.

PLAN 15 capa 7: finding a tracked document by name or path, split out of `doc.py` to keep
that file under the clean-code line limit — `_find_doc` was a plain lookup with no state of
its own, so a module-level function serves it exactly as well as a method would."""

from sldb.api.documents.document_lookup import find_doc  # noqa: F401
