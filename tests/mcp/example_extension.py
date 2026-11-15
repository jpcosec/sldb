"""A consumer's extension, the way specIR would write one: domain tools on the server of sldb.

Loaded by the tests with `--extension example_extension:register`."""

from __future__ import annotations

from typing import Any

import sldb.api as api
from sldb.mcp.mutability import LEVELS
from sldb.mcp.paging import DEFAULT_LIMIT, page


def register(server: Any, context: Any) -> None:
    """Two tools over the store of the context: one that pages, one that misses on purpose."""

    @server.tool()
    def count_by_model(model: str | None = None, offset: int = 0, limit: int = DEFAULT_LIMIT) -> dict[str, Any]:
        """How many documents each registered model tracks (or one model's), as a page."""
        rows = api.select_documents(context.store_path, {"include_linked": True})
        counts = {m.name: sum(1 for r in rows if r["model"] == m.name) for m in api.registered_models(context.store_path) if model in (None, m.name)}
        return page([{"model": name, "documents": total} for name, total in sorted(counts.items())], offset, limit)

    @server.tool()
    def whoami() -> dict[str, Any]:
        """The level and the actor this server was started with."""
        return {"level": context.level, "level_name": LEVELS[context.level], "actor": context.actor}

    @server.tool()
    def find_model(name: str) -> dict[str, Any]:
        """A registered model by name; a name it does not know is a signal, not an error."""
        known = [m.name for m in api.registered_models(context.store_path)]
        return {"found": True, "name": name} if name in known else {"found": False, "name": name, "explanation": f"no model {name!r}", "signal": {"class": "unknown_model", "name": name}}
