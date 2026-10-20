from __future__ import annotations
import sys
from typing import Any
from sldb.cli.commands.help_texts import SHORT_ARGPARSE_HELP
from sldb.core.exceptions import SLDBError
from sldb.cli.dispatcher import CLI
from sldb.cli.warning_output import install_warning_handler
from sldb.cli.envelope import FLAG, run_enveloped

def main(argv: Any = None) -> int:
    """CLI entry point with error handling."""
    install_warning_handler()
    try:
        if argv is None and sys.argv[1:] in (["-h"], ["--help"]): print(SHORT_ARGPARSE_HELP); return 0
        args = _take_actor(list(sys.argv[1:] if argv is None else argv))
        if FLAG in args:
            return run_enveloped([a for a in args if a != FLAG], lambda a: _plain(a))
        return CLI().run(args)
    except Exception as e: return _handle_error(e)

def _take_actor(args: list) -> list:
    """The global `--actor <id>` (who signs every write), taken off the arguments."""
    from sldb.api.actor import set_actor
    if "--actor" in args[:-1] and (i := args.index("--actor")) is not None:
        set_actor(args[i + 1]); return args[:i] + args[i + 2:]
    return args

def _handle_error(e: Exception) -> int:
    if isinstance(e, SLDBError): raise SystemExit(str(e))
    elif isinstance(e, SystemExit): raise
    raise SystemExit(f"Unexpected: {e}")


def _plain(argv: list[str]) -> int:
    """One run with the plain error handling, so the envelope sees what a caller would."""
    try:
        return CLI().run(argv)
    except Exception as e: return _handle_error(e)
