"""What `sldb.api.rewrite_references` did, or would do under `dry_run` (GD22)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class RewriteReport(BaseModel):
    """Every reference rewritten or removed, and every one left as it was with the reason."""

    changed: list[dict[str, Any]] = Field(default_factory=list, description="`{source, field, index, location, before, after}` per reference: `after` is None when it was removed.")
    skipped: list[dict[str, Any]] = Field(default_factory=list, description="`{source, location, reason}` per reference left alone: a mention with no replacement (prose is never deleted), or a mention whose text is no longer a whole token on its line.")

    def to_dict(self) -> dict[str, Any]:
        """The report as plain data."""
        return self.model_dump()
