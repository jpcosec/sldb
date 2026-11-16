"""`sldb stores merge-driver --install`: register the driver for this clone, idempotently.

`.gitattributes` (versioned, so one install covers every clone's attributes) names the store's
derived indexes and `store.yaml`; `.git/config` (per clone) says what `merge=sldb` runs."""

from __future__ import annotations

import subprocess
from pathlib import Path

DRIVER = "sldb stores merge-driver %O %A %B %P"
DRIVER_NAME = "sldb: derived store indexes and store.yaml includes"


def install_merge_driver(store_path: Path) -> dict[str, list[str]]:
    """Write the missing `.gitattributes` lines and the git config keys.

    Returns:
        `attributes`: lines added to `.gitattributes`; `config`: keys set (empty when already there).
    """
    top = Path(_git(store_path.parent, "rev-parse", "--show-toplevel").strip())
    rel = store_path.resolve().relative_to(top.resolve()).as_posix()
    wanted = [f"{rel}/core/store_index.yaml merge=sldb", f"{rel}/core/models/*.yaml merge=sldb", f"{rel}/store.yaml merge=sldb"]
    return {"attributes": _add_lines(top / ".gitattributes", wanted), "config": _configure(top)}


def _add_lines(path: Path, wanted: list[str]) -> list[str]:
    present = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    missing = [line for line in wanted if line not in present]
    if missing:
        body = "\n".join(present + missing) + "\n"
        path.write_text(body, encoding="utf-8")
    return missing


def _configure(top: Path) -> list[str]:
    changed = []
    for key, value in (("merge.sldb.name", DRIVER_NAME), ("merge.sldb.driver", DRIVER)):
        if _git(top, "config", "--get", key, check=False).strip() != value:
            _git(top, "config", key, value)
            changed.append(key)
    return changed


def _git(cwd: Path, *args: str, check: bool = True) -> str:
    run = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True, check=False)
    if check and run.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed in {cwd}: {run.stderr.strip()}")
    return run.stdout
