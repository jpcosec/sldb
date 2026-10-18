"""Project static Python facts into a KGDB GraphSnapshot payload."""
from __future__ import annotations

from datetime import datetime, timezone

from .python_source_values import relative_module
from .python_reexports import module_bindings, resolve_import
from .python_tag_inheritance import apply_effective_tags


def source_snapshot(files: list[dict], system: str) -> dict:
    """Build a self-contained, regenerable source graph snapshot."""
    symbols = {f"{file['module']}:{symbol['name']}": symbol["id"] for file in files for symbol in file["symbols"]}
    modules = {file["module"]: file["id"] for file in files}
    nodes = {file["id"]: _module_node(file, system) for file in files}
    nodes.update({symbol["id"]: _symbol_node(file, symbol, system) for file in files for symbol in file["symbols"]})
    apply_effective_tags(files, nodes)
    reexports = module_bindings(files)
    for file in files:
        _edges(file, nodes, modules, symbols, reexports)
    return {"version": "1.0", "created_at": _now(), "nodes": list(nodes.values()), "metadata": _metadata(files, system)}


def _module_node(file: dict, system: str) -> dict:
    return _node(file["id"], "python_module", file["metadata"], file, system)


def _symbol_node(file: dict, symbol: dict, system: str) -> dict:
    return _node(symbol["id"], "python_symbol", symbol["metadata"], file, system, symbol)


def _node(identity, kind, metadata, file, system, symbol=None) -> dict:
    ast = {"module": file["module"], "path": file["path"], "kind": kind}
    if symbol:
        ast.update({"name": symbol["name"], "node_kind": symbol["kind"], "line_start": symbol["line"], "line_end": symbol["end"]})
    return {"identity": {"node_id": identity, "node_type": kind}, "edges": [], "semantics": metadata,
            "ast": ast, "source": {"producer": "sldb.python_ast", "system": system, "sha256": file["hash"], "path": file["path"]}}


def _edges(file, nodes, modules, symbols, reexports) -> None:
    for symbol in file["symbols"]:
        _edge(nodes, symbol["parent"], symbol["id"], "contains", _evidence(file, symbol))
    bindings = _binding_targets(file, modules, symbols, reexports)
    for binding in bindings:
        _edge(nodes, binding["owner"], binding["target"], "imports", binding)
    parents = {symbol["id"]: symbol["parent"] for symbol in file["symbols"]}
    for reference in file["references"]:
        target = _reference_target(reference, bindings, parents)
        if target:
            _edge(nodes, reference["owner"], target, "references", {**reference, **_evidence(file, reference)})


def _reference_target(reference, bindings, parents) -> str | None:
    owner = reference["owner"]
    while owner:
        target = next((item["target"] for item in bindings if item["owner"] == owner and item["local"] == reference["name"]), None)
        if target:
            return target
        owner = parents.get(owner)
    return None


def _binding_targets(file, modules, symbols, bindings) -> list[dict]:
    found = []
    for binding in file["imports"]:
        module = relative_module(file["module"], binding["module"], binding["level"], file["path"].endswith("__init__.py"))
        target, via = resolve_import(module, binding["name"], modules, symbols, bindings)
        found.append({**binding, "module": module, "target": target, **({"via": via} if via else {}), **_evidence(file, binding)})
    return found


def _edge(nodes, source, target, relation, metadata) -> None:
    if target not in nodes:
        nodes[target] = {"identity": {"node_id": target, "node_type": "python_external"}, "edges": [],
                         "semantics": {}, "ast": {}, "source": {"producer": "sldb.python_ast"}}
    nodes[source]["edges"].append({"target_id": target, "relation_type": relation, "metadata": metadata})


def _evidence(file, fact) -> dict:
    return {"origin": "python_ast", "path": file["path"], "sha256": file["hash"], "line_start": fact["line"], "line_end": fact["end"]}


def _metadata(files: list[dict], system: str) -> dict:
    return {"generated_from": "sldb_python_ast", "system": system, "files": len(files), "extractor_version": 1}


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
