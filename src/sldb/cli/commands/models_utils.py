"""Model source helpers for the `models` commands.

Compatibility bridge: the source location, draft loading and source editing helpers now live
in `sldb.api.model_drafts`; they are re-exported here for existing importers.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.model_drafts.draft_loading import extract_attr, load_model_from_path, setup_sys_path  # noqa: F401
from sldb.api.model_drafts.source_editing import find_class_node, remove_node_block, replace_rhs_expression  # noqa: F401
from sldb.api.model_drafts.source_location import draft_path, locate_model_source  # noqa: F401
from sldb.cli.store_context import get_store_context

def registered_model_source(args: Any) -> tuple[Path, str, str]:
    source = locate_model_source(args.store, args.model, getattr(args, "pythonpath", None))
    return source.path, source.module_name, source.attr_path

def tracked_docs_for_model(args: Any) -> list[tuple[str, str]]:
    from sldb.store.facade import get_tracked_docs
    sp, root = get_store_context(args.store)
    return get_tracked_docs(args.model, sp, root)
