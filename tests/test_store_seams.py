"""The store imports the rest of sldb through three seams only.

`sldb.store` is a typed-document engine sldb's models feed. Its other modules import nothing
from `sldb.core`, `sldb.models` or `sldb.runtime`, and nothing at all from `sldb.api`,
`sldb.cli` or `sldb.selfdoc`: errors come from `store/exceptions.py`, extraction from the
codec (`store/runtime_codec.py`), and what a model class says from `store/model_contract.py`.
A store packaged on its own replaces those three (task: desacoplar el store dentro de sldb).
"""

from __future__ import annotations

import ast
from pathlib import Path

STORE = Path(__file__).resolve().parents[1] / "src" / "sldb" / "store"
SEAMS = {"exceptions.py", "runtime_codec.py", "model_contract.py"}
LOWER = ("sldb.core", "sldb.models", "sldb.runtime")
UPPER = ("sldb.api", "sldb.cli", "sldb.selfdoc")


def _imports(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    return [n.module for n in ast.walk(tree) if isinstance(n, ast.ImportFrom) and n.module] + [a.name for n in ast.walk(tree) if isinstance(n, ast.Import) for a in n.names]


def _offenders(prefixes: tuple[str, ...], skip_seams: bool) -> list[str]:
    found = []
    for path in sorted(STORE.rglob("*.py")):
        if skip_seams and path.relative_to(STORE).as_posix() in SEAMS:
            continue
        found += [f"{path.relative_to(STORE)}: {m}" for m in _imports(path) if m.startswith(prefixes)]
    return found


def test_only_the_seams_import_the_core_the_models_or_the_runtime():
    assert _offenders(LOWER, skip_seams=True) == []


def test_nothing_in_the_store_imports_the_layers_above_it():
    assert _offenders(UPPER, skip_seams=False) == []
