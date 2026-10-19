"""The `(model, path, name)` rows a declaration's `include` rules name, in rule order."""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.store_declaration import StoreDeclaration


def declared_files(root: Path, declaration: StoreDeclaration) -> list[tuple[str, str, str]]:
    """Each glob match under its file stem, each listed path under its given or stem name."""
    rows: list[tuple[str, str, str]] = []
    for rule in declaration.include:
        rows += [(rule["model"], path, name) for path, name in _entries(root, rule)]
    return rows


def _entries(root: Path, rule: dict) -> list[tuple[str, str]]:
    if "glob" in rule:
        return [(p.relative_to(root).as_posix(), p.stem) for p in sorted(root.glob(rule["glob"])) if p.is_file()]
    return [_listed(item) for item in rule.get("paths", [])]


def _listed(item) -> tuple[str, str]:
    if isinstance(item, str):
        return item, Path(item).stem
    return item["path"], item.get("name") or Path(item["path"]).stem
