from __future__ import annotations
import argparse
from .basic import add_basic_commands
from .project import add_project_commands
from .public import add_public_group_commands
from .misc import add_misc_commands
from .find import add_find_commands
from .legacy import add_legacy_commands
from .serve import add_serve_commands
from .selfdoc import add_selfdoc_commands
from .hidden import add_hidden_compat_commands

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sldb", description="SLDB: structured Markdown models plus an optional store.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    s = p.add_subparsers(dest="command", required=True)
    _add_commands(s)
    return p

def _add_commands(s: argparse._SubParsersAction) -> None:
    add_basic_commands(s)
    add_project_commands(s)
    add_public_group_commands(s)
    add_misc_commands(s)
    add_find_commands(s)
    add_legacy_commands(s)
    add_serve_commands(s)
    add_selfdoc_commands(s)
    add_hidden_compat_commands(s)
