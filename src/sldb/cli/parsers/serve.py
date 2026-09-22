from __future__ import annotations

import argparse


def add_serve_commands(s: argparse._SubParsersAction) -> None:
    _serve_flags(s.add_parser("serve", help=_serve_help()))


def _serve_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    parser.add_argument("--store", help="Store path")
    parser.add_argument("--pythonpath", help="Project path")
    parser.add_argument("--cors", action="store_true", help="Send permissive CORS headers (for browser clients)")
    parser.add_argument("--token", help="Require 'Authorization: Bearer <TOKEN>' on every request (default: $SLDB_SERVE_TOKEN, or no auth)")


def _serve_help() -> str:
    return "Serve the store over HTTP using the same methods as the CLI."
