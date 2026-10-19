"""Run a declaration's generators: sldb commands that write derived documents before tracking.

A generator is `{command: "selfdoc python-sync", args: [...]}`, run from the project root
against the store being built, its report discarded. It must succeed: a build that tracks
the previous generation of derived documents would pass a check it should fail.
"""

from __future__ import annotations

import contextlib
import io
from pathlib import Path

from sldb.api.stores.store_declaration import StoreDeclaration
from sldb.core.exceptions import SLDBStoreError


def run_generators(store: Path, root: Path, declaration: StoreDeclaration) -> list[str]:
    """Run each generator in order; the commands run, for the report."""
    for generator in declaration.generate:
        _run(store, root, generator)
    return [generator["command"] for generator in declaration.generate]


def _run(store: Path, root: Path, generator: dict) -> None:
    from sldb.cli.main import main

    argv = [*generator["command"].split(), *generator.get("args", []), "--store", str(store)]
    with contextlib.chdir(root), contextlib.redirect_stdout(io.StringIO()):
        code = main(argv)
    if code != 0:
        raise SLDBStoreError(f"generator `sldb {generator['command']}` exited {code}")
