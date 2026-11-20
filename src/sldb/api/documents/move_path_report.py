"""What `move_path` moved and every reference it rewrote (or would, with `dry_run`)."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class MovePathReport(BaseModel):
    """The plan `move_path` carried out, or only listed when `dry_run` is true."""

    source: str = Field(description="The moved path, relative to the project root.")
    destination: str = Field(description="Where it goes, relative to the project root.")
    dry_run: bool = Field(description="True when nothing was touched.")
    moves: list[dict[str, str]] = Field(default_factory=list, description="Each file moved: `{source, destination}`.")
    fields: list[dict[str, Any]] = Field(default_factory=list, description="Each field rewritten: `{document, field, old, new}`.")
    links: list[dict[str, Any]] = Field(default_factory=list, description="Each Markdown link rewritten: `{file, line, old, new}`.")

    def to_dict(self) -> dict[str, Any]:
        """The report as plain data, every key present."""
        return self.model_dump()
