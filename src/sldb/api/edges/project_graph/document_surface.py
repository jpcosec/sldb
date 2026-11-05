"""Where a project keeps one kind of document, as a project graph reads it."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DocumentSurface(BaseModel):
    """A glob of document files that become graph nodes of one kind."""

    model_config = ConfigDict(frozen=True)

    kind: str = Field(description="Node kind of every document found here; the node id is `kind:identity`.")
    directory: str = Field(description="Directory searched, relative to the project root ('' for the root).")
    pattern: str = Field(description="Glob, relative to `directory`, of the files that are documents.")
    suffixes: tuple[str, ...] = Field(default=(), description="Only files with one of these suffixes; empty keeps every match.")
    excluded_names: tuple[str, ...] = Field(default=(), description="File names that are not documents of this surface.")
    excluded_parts: tuple[str, ...] = Field(default=(), description="Path parts (below `directory`) whose files are left out.")
    identity: Literal["document_id", "document_id_or_slug", "path"] = Field(
        default="path",
        description="What names the node: the document id (falling back to the path), the id or the slug of its title, or the path.",
    )

    def keeps(self, relative_to_directory: tuple[str, ...], name: str, suffix: str) -> bool:
        """Whether a file the glob found is a document of this surface.

        Args:
            relative_to_directory: The file's path parts below `directory`.
            name: The file name.
            suffix: The file suffix.

        Returns:
            False when a suffix, name or part rule leaves it out.
        """
        if self.suffixes and suffix not in self.suffixes:
            return False
        if name in self.excluded_names:
            return False
        return not any(part in self.excluded_parts for part in relative_to_directory)
