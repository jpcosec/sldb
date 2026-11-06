"""Keep `.sldb/store.yaml` true when a model is registered or a document is tracked or
untracked through the API.

A declaration lists files by path where no glob says it; a file tracked or untracked by any
command (`docs track`, `docs untrack`, `deskops retire`...) that left the file stale made a
clean clone fail to rebuild. So did a model registered or inherited without being declared
(`deskops desk update --apply` after new task types: `Model 'TaskCodeDoc' not registered.`).
A store without a declaration is left alone.
"""

from __future__ import annotations

from pathlib import Path

from sldb.api.stores.declared_files import declared_files
from sldb.api.stores.store_declaration import declaration_path, load_declaration, save_declaration


def model_declaration(entry, root: Path) -> dict:
    """How the declaration names a registered model: `origin` for an inherited one, `path` for
    a source the project holds, `model_ref` alone for one outside it (sldb's own models, from
    the installed package: an absolute path would pin one checkout)."""
    declared = {"name": entry.name, "model_ref": entry.model_ref}
    if entry.origin:
        declared["origin"] = entry.origin
    elif _inside(root, entry.path):
        declared["path"] = Path(entry.path).as_posix()
    if getattr(entry, "canonical", False):
        declared["canonical"] = True
    return declared


def _inside(root: Path, path: str) -> bool:
    if not path:
        return False
    source = Path(path) if Path(path).is_absolute() else root / path
    return source.resolve().is_relative_to(root.resolve()) and not Path(path).is_absolute()


def declare_model(store_path: Path, root: Path, entry) -> None:
    """Add the registered model to the declaration; a declared copy that became inherited
    takes its `origin`. A model declared as it already is is left as authored."""
    if not declaration_path(store_path).is_file():
        return
    declaration = load_declaration(store_path)
    if _set_model(declaration.models, model_declaration(entry, root)):
        save_declaration(store_path, declaration)


def _set_model(models: list[dict], wanted: dict) -> bool:
    """Put `wanted` in `models`; False when it was already declared with the same origin."""
    current = next((m for m in models if m.get("name") == wanted["name"]), None)
    if current is None:
        models.append(wanted)
    elif current.get("origin") == wanted.get("origin"):
        return False
    else:
        models[models.index(current)] = wanted
    return True


def declare_tracked(store_path: Path, root: Path, model: str, path: str | None, name: str) -> None:
    """Add `(model, path, name)` to the declaration unless a rule already names it."""
    if not declaration_path(store_path).is_file() or path is None:
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


def project_relative(root: Path, doc_path: Path) -> str | None:
    """`doc_path` relative to the project, or None for a file outside it, which a declaration
    cannot name (and a rebuild could not reach)."""
    resolved = doc_path.resolve()
    return resolved.relative_to(root.resolve()).as_posix() if resolved.is_relative_to(root.resolve()) else None


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
