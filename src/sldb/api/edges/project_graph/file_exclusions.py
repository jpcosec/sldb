"""Files and trees a project graph never reads."""

from __future__ import annotations

from pathlib import PurePosixPath

from pydantic import BaseModel, ConfigDict, Field

from sldb.api.edges.project_graph.path_text import has_path_prefix, path_suffix


class FileExclusions(BaseModel):
    """Directory names, path prefixes, suffixes and endings left out of the file walk."""

    model_config = ConfigDict(frozen=True)

    directories: tuple[str, ...] = Field(default=(), description="Directory names never walked, at any depth.")
    path_prefixes: tuple[str, ...] = Field(default=(), description="Repo-relative trees never walked.")
    suffixes: tuple[str, ...] = Field(default=(), description="File suffixes never read.")
    path_endings: tuple[str, ...] = Field(default=(), description="Path endings never read (generated graph outputs).")

    def prunes(self, relative_directory: str, name: str) -> bool:
        """Whether a directory (`name`, below `relative_directory`) is left unwalked."""
        if name in self.directories:
            return True
        path = f"{relative_directory}/{name}" if relative_directory else name
        return any(has_path_prefix(path, prefix) for prefix in self.path_prefixes)

    def excludes(self, relative_path: str) -> bool:
        """Whether a repo-relative POSIX file path is left out.

        Args:
            relative_path: The path, normalized as `PurePosixPath` normalizes it.

        Returns:
            True when a directory part, suffix, prefix or ending excludes it.
        """
        path = PurePosixPath(relative_path)
        if any(part in self.directories for part in path.parts) or path_suffix(path.name) in self.suffixes:
            return True
        if any(has_path_prefix(relative_path, prefix) for prefix in self.path_prefixes):
            return True
        return any(relative_path.endswith(ending) for ending in self.path_endings)
