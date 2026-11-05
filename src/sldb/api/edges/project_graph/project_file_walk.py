"""One walk of the project tree, keeping the files a rule classifies."""

from __future__ import annotations

import os
from pathlib import Path

from sldb.api.edges.project_graph.file_exclusions import FileExclusions
from sldb.api.edges.project_graph.file_rule import FileRule
from sldb.api.edges.project_graph.path_text import path_suffix


class ProjectFileWalk:
    """`os.walk` over string paths: excluded trees are pruned, not walked and filtered.

    Symlinked directories are not followed, as `Path.rglob` does not follow them.
    """

    def __init__(self, exclusions: FileExclusions, rules: tuple[FileRule, ...]) -> None:
        """Keep the exclusions and the ordered rules.

        Args:
            exclusions: Trees and files never read.
            rules: Rules classifying files; the first match wins.
        """
        self.exclusions = exclusions
        self.rules = rules

    def __call__(self, root: Path) -> list[tuple[str, FileRule]]:
        """(repo-relative path, rule) of every classified file, sorted by path."""
        if not root.exists():
            return []
        found: list[tuple[str, FileRule]] = []
        for dirpath, dirnames, filenames in os.walk(str(root)):
            relative_dir = os.path.relpath(dirpath, str(root)).replace(os.sep, "/")
            relative_dir = "" if relative_dir == "." else relative_dir
            dirnames[:] = [name for name in dirnames if not self.exclusions.prunes(relative_dir, name)]
            found.extend(self._classified(dirpath, relative_dir, filenames))
        return sorted(found, key=lambda item: item[0])

    def _classified(self, dirpath: str, relative_dir: str, filenames: list[str]) -> list[tuple[str, FileRule]]:
        found: list[tuple[str, FileRule]] = []
        for name in filenames:
            relative_path = f"{relative_dir}/{name}" if relative_dir else name
            rule = self.rule_for(relative_path, name)
            if rule is None or self.exclusions.excludes(relative_path):
                continue
            if os.path.isfile(os.path.join(dirpath, name)):
                found.append((relative_path, rule))
        return found

    def rule_for(self, relative_path: str, name: str) -> FileRule | None:
        """The first rule that classifies a repo-relative path, or None."""
        suffix = path_suffix(name)
        return next((rule for rule in self.rules if rule.matches(relative_path, name, suffix)), None)
