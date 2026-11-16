"""One measured child process: wall time, CPU and maximum RSS from `os.wait4`."""

from __future__ import annotations

import os
import subprocess
import tempfile
import time
from pathlib import Path


def run_measured(argv: list[str], cwd: Path, env: dict[str, str], timeout: float) -> dict:
    """Run `argv` to completion and return its rc and resource use (children included)."""
    with tempfile.TemporaryFile() as err:
        start = time.perf_counter()
        proc = subprocess.Popen(argv, cwd=cwd, env=env, stdout=subprocess.DEVNULL, stderr=err)
        status, usage = _wait(proc, timeout)
        wall = time.perf_counter() - start
        rc = os.waitstatus_to_exitcode(status) if status is not None else -9
        return {**_sample(argv, rc, wall, usage), **_failure(rc, err)}


def _failure(rc: int, err) -> dict:
    """A failed run keeps the last lines of its stderr, so a fast rc 1 is not read as speed."""
    if rc == 0:
        return {}
    err.seek(0)
    return {"stderr_tail": err.read().decode("utf-8", "replace").splitlines()[-5:]}


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
