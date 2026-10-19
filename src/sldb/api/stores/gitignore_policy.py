"""Whether the repository's ignore rules match the store's split.

A store with a declaration (`.sldb/store.yaml`) versions only the declaration: `.sldb/core`
and `.sldb/runtime` are derived and ignored (docs/architecture/derived-store-boundary.md).
A store without one keeps the older split: `.sldb/core` versionable, `.sldb/runtime` ignored. Rules are evaluated with
`git check-ignore --no-index`, so a tracked file does not hide a rule that would ignore it.
"""

from __future__ import annotations

import subprocess
from pathlib import Path


def gitignore_policy(store_path: Path) -> dict[str, bool] | None:
    """`{core_ignored, runtime_ignored, declared, ok}` for the store's repository (plus
    `declaration_ignored` when declared); None outside a git work tree."""
    root = store_path.resolve().parent
    if _git(root, "rev-parse", "--is-inside-work-tree") != 0:
        return None
    core = _ignored(root, store_path / "core" / "store_index.yaml")
    runtime = _ignored(root, store_path / "runtime" / "locks" / "store.lock")
    if not (store_path / "store.yaml").is_file():
        return {"core_ignored": core, "runtime_ignored": runtime, "declared": False, "ok": runtime and not core}
    declaration = _ignored(root, store_path / "store.yaml")
    return {"core_ignored": core, "runtime_ignored": runtime, "declared": True, "declaration_ignored": declaration, "ok": runtime and core and not declaration}


def _ignored(root: Path, path: Path) -> bool:
    return _git(root, "check-ignore", "--quiet", "--no-index", str(path.resolve().relative_to(root.resolve()))) == 0


def _git(root: Path, *argv: str) -> int:
    try:
        return subprocess.run(["git", *argv], cwd=root, capture_output=True, check=False).returncode
    except OSError:
        return 1
