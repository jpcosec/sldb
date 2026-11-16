"""Command lines and environments for the two tools under measure."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import sldb
from sldb.cli.bench.operations import COMMANDS

#: The `src` directory of the sldb that runs the benchmark: the sldb under measure.
SLDB_SRC = Path(sldb.__file__).resolve().parents[1]


def argv_for(op: str, deskops: str) -> list[str]:
    tool, args = COMMANDS[op]
    head = [sys.executable, "-m", "sldb"] if tool == "sldb" else [deskops]
    return head + args


def env_for(op: str, xdg: Path) -> dict[str, str]:
    """sldb runs from SLDB_SRC; deskops runs as installed, with its own sldb (no PYTHONPATH)."""
    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    env["XDG_CACHE_HOME"] = str(xdg)
    if COMMANDS[op][0] == "sldb":
        env["PYTHONPATH"] = str(SLDB_SRC)
    return env
