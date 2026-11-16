"""The extension point: a consumer registers its own tools on the server of sldb."""

from __future__ import annotations

import importlib
from typing import Any, Callable

#: `extension(server, context)`: `server.add_tool(fn, name=..., annotations=...)` (or the `tool`
#: decorator) registers a tool that inherits the guard, the paging helpers (`sldb.mcp.paging`),
#: the actor and the signal log; `context` is a `ServerContext`.
Extension = Callable[[Any, Any], None]

#: `validator(changes, context) -> findings`: registered with `context.add_batch_validator`, it
#: runs on every `propose_changes` (over its typed changes) and `apply_changes` (over the
#: proposal's `BatchChange`s) before anything is sealed or written. A finding is
#: `{"code", "level", "what", "subject"}` with `level` "error" (the batch is rejected as
#: `domain`, nothing written) or "alert" (returned as `domain_alerts`, the batch goes on).
BatchValidator = Callable[[list[Any], Any], list[dict[str, Any]]]


def load_extension(spec: str) -> Extension:
    """The function named by `module:function`."""
    module, _, function = spec.partition(":")
    if not module or not function:
        raise ValueError(f"an extension is written module:function, not {spec!r}")
    found = getattr(importlib.import_module(module), function, None)
    if not callable(found):
        raise ValueError(f"{spec!r}: {module} has no callable {function!r}")
    return found
