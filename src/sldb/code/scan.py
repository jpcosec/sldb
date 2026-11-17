"""Scan source files into symbol facts; `.ts`, `.tsx`, `.js` and `.jsx` go to `lang_ts`, `.sql` to `lang_sql`. A Python file gives its
module, classes, functions and methods (qualified name, span, docstring, signature, fingerprints; from kimun's adapter), with their
bases, decorators and calls (`py_calls`), then its module- and class-level `assignment` and `call` facts (`py_statements`), whose ids
come in a second pass over the whole scan (`Ids.flush`). A definition under `if`, `try` or any statement other than a class or
function body is not a symbol (its owner chain is not a chain of definitions), exactly like `ast`-based scanners.
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from sldb.code.facts import fact, key_of, rels
from sldb.code.files import find_files
from sldb.code.fingerprints import fingerprints
from sldb.code.ids import Ids
from sldb.code.imports import py_module_name
from sldb.code.readers import field_text, py_doc, py_end_line, py_native_kind, py_signature
from sldb.code.lang_sql import scan_sql_file
from sldb.code.lang_ts import scan_ts_file
from sldb.code.py_calls import definition_extras
from sldb.code.py_module import module_fact
from sldb.code.py_statements import class_owners, statement_facts
from sldb.code.runtime import TS_SUFFIXES, parse, runtime

QUERY = "(class_definition) @class (function_definition) @function"
_TRANSPARENT = {"block", "decorated_definition"}


def scan_tree(root: Path) -> list[dict[str, Any]]:
    """Every source file under `root` (see `find_files`), facts sorted by id; one id space for the whole tree."""
    idgen, facts = Ids(), []
    for rel in find_files(root):
        facts.extend(scan_file(rel, root, idgen))
    return sorted(idgen.flush(facts), key=lambda f: f["id"])


def scan_file(rel: str, root: Path, idgen: Ids | None = None) -> list[dict[str, Any]]:
    """The facts of one file: the module, its definitions in source order, then its statements. With the caller's `idgen` the
    statements' ids wait for its `flush` (`scan_tree`, `code_facts`); without one, they are given before returning."""
    if idgen is None:
        return (ids := Ids()).flush(scan_file(rel, root, ids))
    if rel.endswith(TS_SUFFIXES + (".sql",)):
        return (scan_sql_file if rel.endswith(".sql") else scan_ts_file)(rel, root, idgen)
    return _scan_python(rel, root, idgen)


def _scan_python(rel: str, root: Path, idgen: Ids) -> list[dict[str, Any]]:
    src = (root / rel).read_bytes()
    rootn, module = parse(src).root_node, py_module_name(rel)
    digest = "sha256:" + hashlib.sha256(src).hexdigest()
    mid = idgen.take(module or "__init__")
    items, owners, names, captured = _analysis(rootn, src)
    defs, ids = _definition_facts(items, owners, names, captured, src, module, mid, rel, digest, idgen)
    ctx = {"src": src, "module": module, "rel": rel, "digest": digest}
    return [module_fact(mid, module, rel, rootn, src, digest)] + defs + statement_facts([(rootn, mid, "")] + class_owners(items, names, ids), ctx, idgen)


def _analysis(rootn: Any, src: bytes) -> tuple[list, dict, dict, dict]:
    """The captured definitions in source order, the owner of each and their qualified names."""
    captured = _captures(rootn)
    items = sorted(captured.values(), key=lambda cn: (cn[1].start_byte, -cn[1].end_byte))
    owners = {key_of(n): _owner_of(n, captured) for _, n in items}
    return items, owners, _qualified_names(items, owners, captured, src), captured


def _captures(rootn: Any) -> dict[tuple, tuple[str, Any]]:
    ts, language = runtime()
    captured = {}
    for cap, nodes in ts.QueryCursor(ts.Query(language, QUERY)).captures(rootn).items():
        for n in nodes:
            captured[key_of(n)] = (cap, n)
    return captured


def _owner_of(n: Any, captured: dict) -> Any:
    """`"root"`, the key of the owning definition, or None when something else sits between."""
    p = n.parent
    while p is not None and p.type in _TRANSPARENT:
        p = p.parent
    if p is None:
        return None
    return "root" if p.type == "module" else (key_of(p) if key_of(p) in captured else None)


def _qualified_names(items: list, owners: dict, captured: dict, src: bytes) -> dict[tuple, str | None]:
    qual: dict[tuple, str | None] = {}
    for _cap, n in items:
        _resolve(key_of(n), owners, captured, src, qual)
    return qual


def _resolve(k: tuple, owners: dict, captured: dict, src: bytes, qual: dict) -> str | None:
    if k in qual:
        return qual[k]
    o, name = owners.get(k), field_text(captured[k][1], src, "name")
    parent = None if o in (None, "root") else _resolve(o, owners, captured, src, qual)
    qual[k] = None if o is None or name is None or (o != "root" and parent is None) else (name if o == "root" else f"{parent}.{name}")
    return qual[k]


def _definition_facts(items, owners, names, captured, src, module, mid, rel, digest, idgen) -> tuple[list[dict[str, Any]], dict]:
    ids, facts = {}, []
    for cap, n in items:
        k, q = key_of(n), names.get(key_of(n))
        if q is None:
            continue
        kind = "method" if cap == "function" and owners[k] != "root" and captured[owners[k]][0] == "class" else cap
        ids[k] = idgen.take(f"{module}.{q}" if module else q)
        facts.append(_definition_fact(n, ids[k], kind, q, mid if owners[k] == "root" else ids.get(owners[k]), src, module, rel, digest))
    return facts, ids


def _definition_fact(n, fid, kind, q, owner_id, src, module, rel, digest) -> dict[str, Any]:
    extra_rels, extra_attrs = definition_extras(n, src)
    return fact(id=fid, kind=kind, name=field_text(n, src, "name"), qualified_name=q, path=rel, span={"start_line": n.start_point[0] + 1, "end_line": py_end_line(n)},
                source_hash=digest, signature=py_signature(n, src), doc=py_doc(n, src), relations=sorted(rels(owner_id) + extra_rels, key=lambda r: (r["type"], r["target"])),
                attrs={"native_kind": py_native_kind(n, src), "module": module, **extra_attrs}, fingerprints=fingerprints(n, src))
