"""Import targets resolved through explicit re-export chains (spec section 4.1).

`from sldb.api import open_store` binds a name that `sldb.api` itself only imports from
`sldb.api.stores.open_store`. The binding's target is the definition at the end of that chain,
followed through module-level imports only, with the chain kept as evidence (`via`). A star
import, a cycle or a module outside the scan ends the chain unresolved: the last module, or an
external target, is reported instead of a guessed definition.
"""

from __future__ import annotations

from .python_source_values import relative_module

_DEPTH = 16


def module_bindings(files: list[dict]) -> dict[tuple[str, str], tuple[str, str | None]]:
    """`(module, local name) -> (imported module, imported name)` for every module-level import."""
    found = {}
    for file in files:
        for b in file["imports"]:
            if b["owner"] == file["id"] and b["name"] != "*":
                found[(file["module"], b["local"])] = (relative_module(file["module"], b["module"], b["level"], file["path"].endswith("__init__.py")), b["name"])
    return found


def resolve_import(module: str, name: str | None, modules: dict, symbols: dict, bindings: dict) -> tuple[str, list[str]]:
    """(target node id, modules re-exporting it on the way)."""
    via: list[str] = []
    for _ in range(_DEPTH):
        if (found := _defined(module, name, modules, symbols)) is not None:
            return found, via
        if not name or (module, name) not in bindings or module in via:
            break
        via.append(module)
        module, name = bindings[(module, name)]
    return modules.get(module, f"python:external:{module}:{name or ''}"), via


def _defined(module: str, name: str | None, modules: dict, symbols: dict) -> str | None:
    """The symbol `module` defines as `name`, or the submodule `module.name` (`from pkg import sub`)."""
    if name and f"{module}:{name}" in symbols:
        return symbols[f"{module}:{name}"]
    return modules.get(f"{module}.{name}") if name else None
