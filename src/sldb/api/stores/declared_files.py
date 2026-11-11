"""The `(model, path, name)` rows a declaration's `include` rules name: one per path.

A path that several rules name resolves to a single row (`include_resolution`). A row from an
explicit `paths` list wins over a `glob` row when its model inherits the glob's model. When the
rules name the same model, they make one row. Anything else is a conflict, and its path gets no row.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.store_declaration import StoreDeclaration


def declared_files(root: Path, declaration: StoreDeclaration, bases: dict[str, list[str]] | None = None) -> list[tuple[str, str, str]]:
    """Each glob match under its file stem, each listed path under its given or stem name.

    `bases` holds each model's bases (`indexed_model_bases`). Without it no model inherits,
    so two models naming one path are a conflict."""
    from sldb.api.stores.include_resolution import resolved_rows

    return resolved_rows(rule_rows(root, declaration), bases or {})[0]


def rule_rows(root: Path, declaration: StoreDeclaration) -> list[tuple[bool, str, str, str]]:
    """`(listed, model, path, name)` of every rule, in rule order; `listed` for a `paths` rule."""
    rows: list[tuple[bool, str, str, str]] = []
    for rule in declaration.include:
        rows += [("glob" not in rule, rule["model"], path, name) for path, name in _entries(root, rule)]
    return rows


def _entries(root: Path, rule: dict) -> list[tuple[str, str]]:
    if "glob" in rule:
        return [(p.relative_to(root).as_posix(), p.stem) for p in sorted(root.glob(rule["glob"])) if p.is_file()]
    return [_listed(item) for item in rule.get("paths", [])]


def _listed(item) -> tuple[str, str]:
    if isinstance(item, str):
        return item, Path(item).stem
    return item["path"], item.get("name") or Path(item["path"]).stem
