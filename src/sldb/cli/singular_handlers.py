"""Handlers of the pre-redesign singular groups (`store`, `model`, `doc`).

They are hidden from help but still parsed, so they need their handlers: without them
`sldb doc untrack` answered `Unknown command: doc` while `sldb doc --help` listed it.
"""

from __future__ import annotations

from typing import Any, Callable


def singular_handlers() -> dict[str, Callable[[Any], int]]:
    from sldb.cli.commands.doc import DocCLI
    from sldb.cli.commands.model import ModelCLI
    from sldb.cli.commands.store import StoreCLI

    return {"store": StoreCLI().run, "model": ModelCLI().run, "doc": DocCLI().run}
