from __future__ import annotations

import argparse


def add_mcp_commands(s: argparse._SubParsersAction) -> None:
    _mcp_flags(s.add_parser("mcp", help="Serve the store to an MCP client over stdio (needs the `mcp` extra)."))


def _mcp_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--store", required=True, help="The store directory (`<project>/.sldb`).")
    parser.add_argument("--level", type=int, choices=(0, 1, 2), default=0, help="Write level: 0 read only (default), 1 content, 2 rules as data.")
    parser.add_argument("--actor", default=None, help="Who signs what this server writes (the global --actor, default agent:sldb-mcp).")
    parser.add_argument("--extension", action="append", default=[], metavar="MODULE:FUNCTION", help="Register the tools of a consumer: MODULE:FUNCTION is called as function(server, context). Repeatable.")
