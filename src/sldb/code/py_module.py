"""The fact a Python module becomes: its name, whole-file span, docstring, imports (top-level as relations and
`attrs.imports`, nested ones in `attrs.nested_imports`) and fingerprints."""

from __future__ import annotations

from typing import Any

from sldb.code.facts import fact, rels
from sldb.code.fingerprints import fingerprints
from sldb.code.imports import py_imports, py_nested_imports
from sldb.code.readers import py_doc


def module_fact(mid: str, module: str, rel: str, rootn: Any, src: bytes, digest: str) -> dict[str, Any]:
    nlines = len(src.decode("utf-8", "replace").splitlines())
    imports, nested = sorted(py_imports(rootn, src)), sorted(py_nested_imports(rootn, src))
    return fact(id=mid, kind="module", name=module.rsplit(".", 1)[-1] if module else "__init__", qualified_name=module, path=rel,
                span={"start_line": 1, "end_line": max(nlines, 1)}, source_hash=digest, doc=py_doc(rootn, src), relations=rels(None, imports),
                attrs={"native_kind": rootn.type, "module": module, "imports": imports, "nested_imports": nested, "has_error": rootn.has_error}, fingerprints=fingerprints(rootn, src))
