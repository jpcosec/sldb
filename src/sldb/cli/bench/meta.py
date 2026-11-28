"""What a benchmark result needs to be compared later: versions, machine and date."""

from __future__ import annotations

import os
import platform
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from sldb.cli.bench.environment import SLDB_SRC
from sldb.ports.git import dirty_paths, head_sha

_PROBE = "import sldb, deskops; print(sldb.__file__); print(deskops.__file__)"


def bench_meta(desks: dict[str, Path], deskops: str) -> dict:
    return {"started": datetime.now(timezone.utc).isoformat(timespec="seconds"), "machine": machine(),
            "sldb": {"src": str(SLDB_SRC), "sha": git_sha(SLDB_SRC)}, "deskops": deskops_meta(deskops),
            "desks": {name: {"source": str(path), "sha": git_sha(path), "dirty": git_dirty(path)} for name, path in desks.items()}}


def git_sha(path: Path) -> str:
    return head_sha(path) or "unknown"


def git_dirty(path: Path) -> int:
    """Uncommitted paths in the copied working tree: the copy is HEAD plus these."""
    return len(dirty_paths(path))


def machine() -> dict:
    return {"host": platform.node(), "system": platform.platform(), "python": platform.python_version(),
            "cpus": os.cpu_count(), "cpu": _cpu_model(), "mem_gb": _mem_gb()}


def deskops_meta(executable: str) -> dict:
    """The deskops executable and the sldb it imports, read through its own interpreter."""
    files = _probe(executable)
    sldb_src = Path(files[0]).parents[1] if len(files) == 2 else None
    return {"executable": executable, "deskops_module": files[1] if len(files) == 2 else "unknown",
            "sldb_src": str(sldb_src or "unknown"), "sldb_sha": git_sha(sldb_src) if sldb_src else "unknown"}


def _probe(executable: str) -> list[str]:
    try:
        shebang = Path(executable).read_text(encoding="utf-8", errors="replace").splitlines()[0]
        env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
        out = subprocess.run([shebang.removeprefix("#!").strip(), "-c", _PROBE], capture_output=True, text=True, env=env)
    except (OSError, IndexError, ValueError):
        return []
    return out.stdout.split()


def _cpu_model() -> str:
    try:
        lines = Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines()
    except OSError:
        return platform.processor() or "unknown"
    return next((l.split(":", 1)[1].strip() for l in lines if l.startswith("model name")), "unknown")


def _mem_gb() -> float:
    try:
        return round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024 ** 3, 1)
    except (ValueError, OSError):
        return 0.0
