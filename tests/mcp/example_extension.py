"""A consumer's extension, the way specIR would write one: domain tools on the server of sldb.

Loaded by the tests with `--extension example_extension:register`."""

from __future__ import annotations

from typing import Any

import sldb.api as api
from sldb.mcp.mutability import LEVELS
from sldb.mcp.paging import DEFAULT_LIMIT, page


def register(server: Any, context: Any) -> None:
    """Three tools over the store of the context (one that pages, one that misses on purpose, one
    that sets the domain check) and a batch validator that runs before propose and apply."""
    check: dict[str, str | None] = {"level": None}

    def domain_check(changes: list[Any], context: Any) -> list[dict[str, Any]]:
        """One finding per change, at the level `set_domain_check` fixed; none while it is off."""
        if check["level"] is None:
            return []
        subjects = [getattr(c, "name", None) or getattr(c, "id", None) for c in changes]
        return [{"code": "example_domain_check", "level": check["level"], "what": f"{subject} is checked by the example domain", "subject": subject} for subject in subjects]

    context.add_batch_validator(domain_check)

    @server.tool()
    def set_domain_check(level: str | None = None) -> dict[str, Any]:
        """What the example validator finds in every change from now on: "error", "alert" or nothing."""
        check["level"] = level
        return {"level": level}

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
