"""Follow public model re-exports when locating an editable class definition.

Compatibility bridge: `resolve_definition` now lives in `sldb.api.model_drafts.source_location`.
"""
from sldb.api.model_drafts.source_location import resolve_definition  # noqa: F401
