"""An import target follows explicit re-export chains to the definition (spec section 4.1),
and what cannot be proven statically stays unresolved instead of guessed."""

from __future__ import annotations

from pathlib import Path

from sldb.selfdoc.python_source_graph import source_snapshot
from sldb.selfdoc.python_source_scan import scan_source_facts


def _imports(root: Path, owner: str) -> dict[str, tuple[str, list[str]]]:
    nodes = {n["identity"]["node_id"]: n for n in source_snapshot(scan_source_facts(root, None), "demo")["nodes"]}
    return {e["metadata"]["local"]: (e["target_id"], e["metadata"].get("via", [])) for e in nodes[owner]["edges"] if e["relation_type"] == "imports"}


def _write(root: Path, files: dict[str, str]) -> None:
    for rel, text in files.items():
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_text(text, encoding="utf-8")


def test_a_chain_of_reexports_reaches_the_definition(tmp_path):
    _write(tmp_path, {
        "pkg/__init__.py": "from pkg.inner import Thing as Thing\n",
        "pkg/inner/__init__.py": "from .impl import Thing\n",
        "pkg/inner/impl.py": "class Thing:\n    pass\n",
        "user.py": "from pkg import Thing as T\nfrom pkg import inner\n",
    })
    found = _imports(tmp_path, "python:user")
    assert found["T"] == ("python:pkg.inner.impl:Thing", ["pkg", "pkg.inner"])
    assert found["inner"] == ("python:pkg.inner", [])                 # `from pkg import submodule`


def test_star_imports_cycles_and_outside_modules_stay_unresolved(tmp_path):
    _write(tmp_path, {
        "a.py": "from b import loop\nfrom c import *\n",
        "b.py": "from a import loop\n",
        "c.py": "class Hidden:\n    pass\n",
        "user.py": "from a import loop\nfrom a import Hidden\nfrom yaml import safe_load\n",
    })
    found = _imports(tmp_path, "python:user")
    assert found["loop"][0] in ("python:a", "python:b")           # a cycle ends at a module, never invents a definition
    assert found["Hidden"] == ("python:a", [])                    # a star import is not expanded
    assert found["safe_load"] == ("python:external:yaml:safe_load", [])
