"""Keep `.sldb/store.yaml` true when a document is tracked or untracked through the API.

A declaration lists files by path where no glob says it; a file tracked or untracked by any
command (`docs track`, `docs untrack`, `deskops retire`...) that left the file stale made a
clean clone fail to rebuild. A store without a declaration is left alone.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.declared_files import declared_files
from sldb.api.stores.store_declaration import declaration_path, load_declaration, save_declaration


def declare_tracked(store_path: Path, root: Path, model: str, path: str, name: str) -> None:
    """Add `(model, path, name)` to the declaration unless a rule already names it."""
    if not declaration_path(store_path).is_file():
        return
    declaration = load_declaration(store_path)
    if (model, path, name) in declared_files(root, declaration):
        return
    _path_rule(declaration, model)["paths"].append(path if Path(path).stem == name else {"path": path, "name": name})
    save_declaration(store_path, declaration)


def _path_rule(declaration, model: str) -> dict:
    """The model's path-list rule, created at the end when it has none."""
    rule = next((r for r in declaration.include if r.get("model") == model and "paths" in r), None)
    if rule is None:
        declaration.include.append(rule := {"model": model, "paths": []})
    return rule


def forget_tracked(store_path: Path, path: str) -> None:
    """Drop `path` from every path list of the declaration; a rule left empty goes too."""
    if not declaration_path(store_path).is_file():
        return
    declaration = load_declaration(store_path)
    for rule in declaration.include:
        if "paths" in rule:
            rule["paths"] = [e for e in rule["paths"] if (e if isinstance(e, str) else e["path"]) != path]
    declaration.include = [r for r in declaration.include if "paths" not in r or r["paths"]]
    save_declaration(store_path, declaration)
