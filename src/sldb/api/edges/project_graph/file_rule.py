"""A path rule that makes a project file a graph node (source, test, config, spec...)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FileRule(BaseModel):
    """One rule of the ordered list that classifies project files; the first match wins."""

    model_config = ConfigDict(frozen=True)

    kind: str = Field(description="Node kind of a matching file; the node id is `kind:path`.")
    file_kind: str = Field(description="What the file is to the project (source, test, config, spec).")
    path_prefixes: tuple[str, ...] = Field(default=(), description="Directories the file must sit under; empty matches anywhere.")
    suffixes: tuple[str, ...] = Field(description="File suffixes the rule accepts.")
    hidden_name: bool = Field(default=False, description="Only file names starting with a dot.")
    stem_keywords: tuple[str, ...] = Field(default=(), description="Only files whose lower-cased stem holds one of these words.")

    def matches(self, relative_path: str, name: str, suffix: str) -> bool:
        """Whether a repo-relative POSIX path is a file of this rule.

        Args:
            relative_path: The file path relative to the project root.
            name: The file name.
            suffix: The file suffix (`PurePath.suffix`).

        Returns:
            True when every condition of the rule holds.
        """
        if suffix not in self.suffixes or (self.hidden_name and not name.startswith(".")):
            return False
        if self.path_prefixes and not any(relative_path.startswith(f"{prefix}/") for prefix in self.path_prefixes):
            return False
        stem = name[: -len(suffix)].lower()
        return not self.stem_keywords or any(word in stem for word in self.stem_keywords)
