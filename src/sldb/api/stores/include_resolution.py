"""One row per path when several `include` rules name it, or a `store/include-conflict`.

The more specific rule wins (coordinator's call, 2026-11-11). A model's descent is its
recorded `base_models`, the walk `sldb.store.model_contract.base_names` makes over the class.
- The rules name one model: one row. A `paths` entry gives the name.
- `paths` rules of one model and `glob` rules of one model it inherits: the `paths` row wins.
- Anything else (two `paths` or two `glob` models, models with no descent between them): no
  row is chosen. `build` and `stores check` report an error.
"""

from __future__ import annotations

from pathlib import Path

from sldb.core.finding import Finding, error

Row = tuple[str, str, str]
_FIX = "name the file in one rule, or list it under `paths` of a model that inherits the glob's"


def resolved_rows(named: list[tuple[bool, str, str, str]], bases: dict[str, list[str]]) -> tuple[list[Row], list[dict]]:
    """The winning `(model, path, name)` per path, in rule order, and `{path, models}` per conflict."""
    by_path: dict[str, list[tuple[bool, str, str, str]]] = {}
    for row in named:
        by_path.setdefault(row[2], []).append(row)
    kept: list[Row] = []
    conflicts: list[dict] = []
    for path, rows in by_path.items():
        winner = _winner(rows, bases)
        kept += [winner] if winner else []
        conflicts += [] if winner else [{"path": path, "models": sorted({r[1] for r in rows})}]
    return kept, conflicts


def _winner(rows: list[tuple[bool, str, str, str]], bases: dict[str, list[str]]) -> Row | None:
    listed = [r for r in rows if r[0]]
    if len({r[1] for r in rows}) == 1:
        return (listed or rows)[0][1:]
    children, globbed = {r[1] for r in listed}, {r[1] for r in rows if not r[0]}
    if len(children) == 1 and len(globbed) == 1 and globbed <= set(bases.get(listed[0][1], [])):
        return listed[0][1:]
    return None


def include_conflicts(store_path: Path, root: Path) -> list[dict]:
    """The declaration's conflicting paths as `{path, models}`; [] for a store with no declaration."""
    from sldb.api.stores.declared_files import rule_rows
    from sldb.api.stores.store_declaration import declaration_path, load_declaration

    if not declaration_path(store_path).is_file():
        return []
    return resolved_rows(rule_rows(root, load_declaration(store_path)), store_bases(store_path))[1]


def conflict_finding(conflict: dict) -> Finding:
    what = f"include rules name it under {', '.join(conflict['models'])}, and no `paths` model inherits a single `glob` model"
    return error("store/include-conflict", conflict["path"], what, _FIX)


def store_bases(store_path: Path) -> dict[str, list[str]]:
    """Each registered model's bases (`indexed_model_bases`); {} for a store not built yet."""
    from sldb.api.stores.resolve_indexed_document import indexed_model_bases
    from sldb.store.layout import store_exists

    return indexed_model_bases(store_path) if store_exists(store_path) else {}
