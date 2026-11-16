"""The benchmark's settings, as parsed from the command line."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from sldb.cli.bench.operations import parse_ops


@dataclass
class BenchConfig:
    """Desks to copy, operations, modes and limits of one benchmark run."""

    desks: dict[str, Path]
    workdir: Path
    deskops: str
    ops: tuple[str, ...]
    modes: tuple[str, ...] = ("cold", "warm")
    repeat: int = 1
    timeout: float = 7200.0
    keep: bool = False
    touch: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_args(cls, args) -> "BenchConfig":
        return cls(desks=_pairs(args.desk, lambda v: Path(v).resolve()), workdir=_workdir(args.workdir), deskops=_deskops(args.deskops),
                   ops=parse_ops(args.ops), modes=_modes(args.modes), repeat=max(1, args.repeat),
                   timeout=args.timeout, keep=args.keep, touch=_pairs(args.touch or [], str))


def _pairs(items: list[str], kind) -> dict:
    """`NAME=VALUE` items to a dict; the name is also the copy's directory."""
    bad = [item for item in items if "=" not in item or not _safe_name(item.split("=", 1)[0])]
    if bad:
        raise ValueError(f"expected NAME=PATH with a plain NAME, got: {', '.join(bad)}")
    return {name: kind(value) for name, value in (item.split("=", 1) for item in items)}


def _safe_name(name: str) -> bool:
    """A copy's directory name: one plain path segment, and not the bench's own `xdg`."""
    return bool(name) and name not in (".", "..", "xdg") and "/" not in name


def _workdir(value: str | None) -> Path:
    base = os.environ.get("TMPDIR", "/tmp")
    return Path(value or Path(base) / "sldb-bench").resolve()


def _deskops(value: str | None) -> str:
    return value or shutil.which("deskops") or "deskops"


def _modes(value: str) -> tuple[str, ...]:
    modes = tuple(m.strip() for m in value.split(",") if m.strip())
    if not modes or set(modes) - {"cold", "warm"}:
        raise ValueError(f"--modes takes cold, warm or both; got: {value}")
    return modes
