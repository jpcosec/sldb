"""TypeScript and JavaScript (`.ts`, `.tsx`, `.js`, `.jsx`) into facts of the same form as Python's: the
module, then its top-level declarations in source order (components, hooks, types and functions; rules
in `ts_readers`). One reader for the four; the grammar comes from the extension (`runtime.grammar_of`).
The module's qualified name is its path without extension, like `py_module_name`; a symbol's id is
`module.name`, and a repeated id takes the `~2`, `~3` suffix from `Ids`.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from sldb.code.facts import fact, rels
from sldb.code.ids import Ids
from sldb.code.imports import py_module_name
from sldb.code.runtime import parse
from sldb.code.ts_fingerprints import ts_fingerprints
from sldb.code.ts_readers import declarations, jsdoc, kind_of, ts_imports, ts_signature


def scan_ts_file(rel: str, root: Path, idgen: Ids) -> list[dict[str, Any]]:
    src = (root / rel).read_bytes()
    rootn, module = parse(src, rel).root_node, py_module_name(rel)
    ctx = {"rel": rel, "module": module, "src": src, "digest": "sha256:" + hashlib.sha256(src).hexdigest(), "mid": idgen.take(module or "__init__")}
    facts, typed = [_module_fact(rootn, ctx)], rel.endswith((".ts", ".tsx"))
    for stmt in rootn.named_children:
        for name, node, fn in declarations(stmt, module.rsplit(".", 1)[-1], typed, src):
            facts.append(_definition_fact(name, node, fn, jsdoc(stmt, src), idgen, ctx))
    return facts


def _module_fact(rootn: Any, ctx: dict[str, Any]) -> dict[str, Any]:
    src, module = ctx["src"], ctx["module"]
    imports, nlines = ts_imports(rootn, src), len(src.decode("utf-8", "replace").splitlines())
    return fact(id=ctx["mid"], kind="module", name=module.rsplit(".", 1)[-1] if module else "__init__", qualified_name=module, path=ctx["rel"],
                span={"start_line": 1, "end_line": max(nlines, 1)}, source_hash=ctx["digest"], doc=None, relations=rels(None, imports),
                attrs={"native_kind": rootn.type, "module": module, "imports": imports, "nested_imports": [], "has_error": rootn.has_error},
                fingerprints=ts_fingerprints(None, rootn, None, None, src))


def _definition_fact(name: str, node: Any, fn: Any, doc: str | None, idgen: Ids, ctx: dict[str, Any]) -> dict[str, Any]:
    module, src = ctx["module"], ctx["src"]
    return fact(id=idgen.take(f"{module}.{name}" if module else name), kind=kind_of(name, node, fn), name=name, qualified_name=name, path=ctx["rel"],
                span={"start_line": node.start_point[0] + 1, "end_line": node.end_point[0] + 1}, source_hash=ctx["digest"],
                signature=ts_signature(name, fn, src), doc=doc, relations=rels(ctx["mid"]),
                attrs={"native_kind": (fn if fn is not None else node).type, "module": module}, fingerprints=ts_fingerprints(name, node, fn, doc, src))
