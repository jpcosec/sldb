"""What `scaffold_store` found or did, path by path (`docs/architecture/store-declaration.md`)."""

from __future__ import annotations

from pydantic import BaseModel, Field

OUTCOMES = ("created", "rewritten", "present", "conflicts")


class ScaffoldReport(BaseModel):
    """Four lists of project-relative paths, and whether they were acted on or only planned."""

    created: list[str] = Field(default_factory=list, description="Folders and files that were missing: written with `applied`, pending otherwise.")
    rewritten: list[str] = Field(default_factory=list, description="Managed files whose bytes differed from the source: restored with `applied`, pending otherwise.")
    present: list[str] = Field(default_factory=list, description="Folders that exist and files that are as the declaration wants them (or `if_missing` files that exist).")
    conflicts: list[str] = Field(default_factory=list, description="A folder path held by a file, or a file path held by a directory; never touched.")
    applied: bool = Field(default=False, description="True when the writes happened; False when the lists say what a run with `apply` would do.")

    def add(self, outcome: str, path: str) -> None:
        """Put `path` in the list `outcome` names."""
        getattr(self, outcome).append(path)

    def lists(self) -> dict[str, list[str]]:
        """The four lists alone, the shape `stores build` reports under `scaffold`."""
        return {outcome: list(getattr(self, outcome)) for outcome in OUTCOMES}
