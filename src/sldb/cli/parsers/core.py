from __future__ import annotations
import argparse
from .basic import add_basic_commands
from .project import add_project_commands
from .public import add_public_group_commands
from .misc import add_misc_commands
from .find import add_find_commands
from .legacy import add_legacy_commands
from .serve import add_serve_commands
from .mcp import add_mcp_commands
from .selfdoc import add_selfdoc_commands
from .hidden import add_hidden_compat_commands

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="sldb", description="SLDB: structured Markdown models plus an optional store.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    p.add_argument("--version", action=_VersionAction, help="print the version and the git revision, then exit")
    s = p.add_subparsers(dest="command", required=True)
    _add_commands(s)
    return p


class _VersionAction(argparse.Action):
    """`--version`: the package version plus the checkout's `git describe`, then exit 0."""

    def __init__(self, option_strings, dest=argparse.SUPPRESS, default=argparse.SUPPRESS, help=None):
        super().__init__(option_strings, dest=dest, default=default, nargs=0, help=help)

    def __call__(self, parser, namespace, values, option_string=None):
        from sldb.store import package_version as pv
        print(pv.version_line())
        parser.exit(0)

def _add_commands(s: argparse._SubParsersAction) -> None:
    add_basic_commands(s)
    add_project_commands(s)
    add_public_group_commands(s)
    add_misc_commands(s)
    add_find_commands(s)
    add_legacy_commands(s)
    add_serve_commands(s)
    add_mcp_commands(s)
    add_selfdoc_commands(s)
    add_hidden_compat_commands(s)
