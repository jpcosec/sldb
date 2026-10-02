from __future__ import annotations
import sys
from typing import Any
from sldb.cli.commands.help_texts import SHORT_ARGPARSE_HELP
from sldb.core.exceptions import SLDBError
from sldb.cli.dispatcher import CLI
from sldb.cli.warning_output import install_warning_handler

def main(argv: Any = None) -> int:
    """CLI entry point with error handling."""
    install_warning_handler()
    try:
        if argv is None and sys.argv[1:] in (["-h"], ["--help"]): print(SHORT_ARGPARSE_HELP); return 0
        return CLI().run(argv)
    except Exception as e: return _handle_error(e)

def _handle_error(e: Exception) -> int:
    if isinstance(e, SLDBError): raise SystemExit(str(e))
    elif isinstance(e, SystemExit): raise
    raise SystemExit(f"Unexpected: {e}")
