"""One measured child process: wall time, CPU and maximum RSS from `os.wait4`."""

from __future__ import annotations

import os
import subprocess
import time
from pathlib import Path


def run_measured(argv: list[str], cwd: Path, env: dict[str, str], timeout: float) -> dict:
    """Run `argv` to completion and return its rc and resource use (children included)."""
    start = time.perf_counter()
    proc = subprocess.Popen(argv, cwd=cwd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    status, usage = _wait(proc, timeout)
    wall = time.perf_counter() - start
    rc = os.waitstatus_to_exitcode(status) if status is not None else -9
    return _sample(argv, rc, wall, usage)


def _wait(proc: subprocess.Popen, timeout: float):
    """`os.wait4` with a deadline; a child past it is killed and reaped (status None)."""
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        pid, status, usage = os.wait4(proc.pid, os.WNOHANG)
        if pid:
            proc.returncode = os.waitstatus_to_exitcode(status)
            return status, usage
        time.sleep(0.005)
    proc.kill()
    proc.returncode = -9
    return None, os.wait4(proc.pid, 0)[2]


def _sample(argv: list[str], rc: int, wall: float, usage) -> dict:
    cpu = usage.ru_utime + usage.ru_stime
    return {"argv": argv, "rc": rc, "wall_s": round(wall, 3), "user_s": round(usage.ru_utime, 3),
            "sys_s": round(usage.ru_stime, 3), "cpu_s": round(cpu, 3), "maxrss_mb": round(usage.ru_maxrss / 1024, 1)}
