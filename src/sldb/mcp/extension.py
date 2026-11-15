"""The extension point: a consumer registers its own tools on the server of sldb."""

from __future__ import annotations

import importlib
from typing import Any, Callable

#: `extension(server, context)`: `server.add_tool(fn, name=..., annotations=...)` (or the `tool`
#: decorator) registers a tool that inherits the guard, the paging helpers (`sldb.mcp.paging`),
#: the actor and the signal log; `context` is a `ServerContext`.
Extension = Callable[[Any, Any], None]


def load_extension(spec: str) -> Extension:
    """The function named by `module:function`."""
    module, _, function = spec.partition(":")
    if not module or not function:
        raise ValueError(f"an extension is written module:function, not {spec!r}")
    found = getattr(importlib.import_module(module), function, None)
    if not callable(found):
        raise ValueError(f"{spec!r}: {module} has no callable {function!r}")
    return found
