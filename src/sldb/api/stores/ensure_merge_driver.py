"""The merge driver of a store inside a git repository: installed when the store is prepared
by the CLI commands (`stores init`, `scaffold`, `build`; never by the API functions, which
transactions call and roll back) and reported by `stores check` when it is missing."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from sldb.api.stores.merge_driver_install import DRIVER, DRIVER_NAME, install_merge_driver
from sldb.core.finding import Finding, alert

FIX = "sldb stores merge-driver --install"


def ensure_merge_driver(store_path: Path) -> dict[str, list[str]] | None:
    """Install the driver when `store_path` is in a git repo (idempotent); never raises.

    Returns:
        What `install_merge_driver` changed, or None outside git or when git failed (a warning
        goes to stderr then, the calling command goes on).
    """
    store_path = Path(store_path)
    if _top(store_path) is None:
        return None
    try:
        return install_merge_driver(store_path)
    except (RuntimeError, OSError, ValueError) as exc:
        sys.stderr.write(f"warning: could not install the sldb merge driver ({exc}); run `{FIX}`\n")
        return None


def missing_merge_driver(store_path: Path) -> list[str]:
    """The `.gitattributes` lines and config keys the driver lacks; empty outside git or when complete."""
    store_path = Path(store_path)
    top = _top(store_path)
    rel = _relative(store_path, top)
    if top is None or rel is None:
        return []
    return _missing_lines(top, rel) + _missing_keys(top)


def _relative(store_path: Path, top: Path | None) -> str | None:
    if top is None:
        return None
    try:
        return store_path.resolve().relative_to(top.resolve()).as_posix()
    except ValueError:
        return None


def _missing_lines(top: Path, rel: str) -> list[str]:
    wanted = [f"{rel}/core/store_index.yaml merge=sldb", f"{rel}/core/models/*.yaml merge=sldb", f"{rel}/store.yaml merge=sldb"]
    attrs = top / ".gitattributes"
    present = attrs.read_text(encoding="utf-8").splitlines() if attrs.is_file() else []
    return [f".gitattributes: {line}" for line in wanted if line not in present]


def _missing_keys(top: Path) -> list[str]:
    keys = (("merge.sldb.name", DRIVER_NAME), ("merge.sldb.driver", DRIVER))
    return [f"git config {key}" for key, value in keys if _config(top, key) != value]


def merge_driver_finding(store_path: Path) -> list[Finding]:
    """`merge-driver-missing` (alert) when the store is in a git repo and the driver is incomplete."""
    missing = missing_merge_driver(store_path)
    if not missing:
        return []
    return [alert("merge-driver-missing", ".gitattributes", f"the sldb merge driver is not installed ({'; '.join(missing)})", FIX)]


def _top(path: Path) -> Path | None:
    cwd = path.parent if path.parent.is_dir() else path
    try:
        run = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=cwd, capture_output=True, text=True, check=False)
    except OSError:
        return None
    return Path(run.stdout.strip()) if run.returncode == 0 and run.stdout.strip() else None


def _config(top: Path, key: str) -> str:
    run = subprocess.run(["git", "config", "--get", key], cwd=top, capture_output=True, text=True, check=False)
    return run.stdout.strip()
