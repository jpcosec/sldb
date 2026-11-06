"""Class-level attributes and draft status of a registered model, for its description."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def model_class_attrs(model_type: type) -> dict[str, Any]:
    """Containment, references, compositions, semantics map, authority and template."""
    return {
        "containment": dict(getattr(model_type, "__containment__", {}) or {}),
        "references": list(getattr(model_type, "__references__", []) or []),
        "compositions": dict(getattr(model_type, "__compositions__", {}) or {}),
        "semantics_map": dict(getattr(model_type, "__semantics__", {}) or {}),
        "authority": str(getattr(model_type, "__authority__", "generated")),
        "template": str(getattr(model_type, "__template__", "")),
    }


def draft_status(store_path: Path, model_name: str, pythonpath: str | None) -> dict[str, Any]:
    """Whether the model has a draft file, and where; unlocatable sources mean no draft."""
    from sldb.api.model_drafts.source_location import locate_model_source

    try:
        src = locate_model_source(store_path, model_name, pythonpath)
        if src.draft_path.exists():
            return {"has_draft": True, "draft_path": str(src.draft_path)}
    except Exception:
        pass
    return {"has_draft": False, "draft_path": None}
