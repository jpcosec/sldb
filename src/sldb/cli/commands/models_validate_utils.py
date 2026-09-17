"""Compatibility bridge: draft contract checks and promotion rollback now live in `sldb.api.model_drafts`."""
from sldb.api.model_drafts.draft_contract import _add_marker_names, _extract_referenced_fields, validate_template_contract  # noqa: F401
from sldb.api.model_drafts.draft_restore import _restore, restored_on_failure, store_index_files  # noqa: F401
