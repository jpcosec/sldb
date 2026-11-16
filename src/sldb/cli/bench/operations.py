"""What each benchmark operation runs. Global operations run once per mode, outside any desk."""

from __future__ import annotations

GLOBAL_OPS = ("sldb-help", "deskops-help")
DESK_OPS = ("update-noop", "update-one", "check", "doctor", "status", "build-check")
#: `build-check` rebuilds the whole store (about 50 min on the sldb store): only on request.
DEFAULT_OPS = GLOBAL_OPS + DESK_OPS[:-1]
ALL_OPS = GLOBAL_OPS + DESK_OPS

COMMANDS = {
    "sldb-help": ("sldb", ["--help"]),
    "deskops-help": ("deskops", ["--help"]),
    "update-noop": ("sldb", ["stores", "update"]),
    "update-one": ("sldb", ["stores", "update"]),
    "check": ("sldb", ["stores", "check"]),
    "build-check": ("sldb", ["stores", "build", "--check"]),
    "doctor": ("deskops", ["doctor", "--root", "."]),
    "status": ("deskops", ["status", "--root", "."]),
}


def parse_ops(spec: str | None) -> tuple[str, ...]:
    """`a,b,c` to an ordered tuple, rejecting unknown names; empty means the default set."""
    if not spec:
        return DEFAULT_OPS
    asked = [op.strip() for op in spec.split(",") if op.strip()]
    unknown = sorted(set(asked) - set(ALL_OPS))
    if unknown:
        raise ValueError(f"unknown bench operation(s): {', '.join(unknown)}; known: {', '.join(ALL_OPS)}")
    return tuple(op for op in ALL_OPS if op in asked)
