"""Effective tags of each declaration, inherited along its lexical chain (spec section 3).

Package -> module -> class/function -> nested declaration, within the selected scan only (an
ancestor package outside it, an import, a base class or a sibling never contributes):
`system:*` and `workspace:*` take the nearest declaration's value, `topic:*` is the union of
ancestors and the declaration, every other tag is local. Each effective tag names the
declaration it comes from, so removing an ancestor's tag removes it from the descendants on
the next sync; nothing is written back into a docstring.
"""

from __future__ import annotations

NEAREST = ("system", "workspace")
UNION = ("topic",)


def effective_tags(local: list[str], inherited: list[dict], origin: dict) -> list[dict]:
    """`[{tag, origin, at}]`: the inherited ones the local tags do not override, then the local
    ones; `origin` is `{origin: <declaring node id>, at: <path:line>}`."""
    local_spaces = {tag.split(":", 1)[0] for tag in local}
    kept = [item for item in inherited if _passes(item["tag"], local_spaces)]
    own = [{"tag": tag, **origin} for tag in local if tag not in {item["tag"] for item in kept}]
    return kept + own


def _passes(tag: str, local_spaces: set[str]) -> bool:
    space = tag.split(":", 1)[0]
    return space in UNION or (space in NEAREST and space not in local_spaces)


def package_chain(module: str, packages: dict[str, str]) -> list[str]:
    """Node ids of the module's ancestor packages present in the scan, outermost first."""
    parts = module.split(".")
    return [packages[".".join(parts[:i])] for i in range(1, len(parts)) if ".".join(parts[:i]) in packages]


def apply_effective_tags(files: list[dict], nodes: dict[str, dict]) -> None:
    """Give every module and symbol node its `local_tags` and `effective_tags`, outermost first."""
    packages = {f["module"]: f["id"] for f in files if f["path"].endswith("__init__.py")}
    for file in sorted(files, key=lambda f: f["module"].count(".")):
        chain = package_chain(file["module"], packages)
        _tag(nodes[file["id"]], nodes[chain[-1]]["semantics"]["effective_tags"] if chain else [], {"origin": file["id"], "at": f"{file['path']}:1"})
        for symbol in file["symbols"]:  # in source order, so a parent is tagged before its children
            _tag(nodes[symbol["id"]], nodes[symbol["parent"]]["semantics"]["effective_tags"], {"origin": symbol["id"], "at": f"{file['path']}:{symbol['line']}"})


def _tag(node: dict, inherited: list[dict], origin: dict) -> None:
    local = list(node["semantics"].get("tags", []))
    node["semantics"] = {**node["semantics"], "local_tags": local, "effective_tags": effective_tags(local, inherited, origin)}
