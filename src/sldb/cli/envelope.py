"""`sldb --envelope ...`: one JSON value on stdout, whatever the command, and typed exit codes.

    {"ok": true, "command": "stores check", "store": {"path": ...}, "revision": "<store_hash>",
     "data": ..., "warnings": [{"level": "alert", "code": "store/root-stale", ...}]}
    {"ok": false, "command": ..., "error": {"type": "store/busy", "message": ...}, "exit": 4, "warnings": []}

`warnings` are the alerts the command reported (`sldb.cli.alert_sink`), on success and failure:
an alert is never silent.
`data` is the command's own JSON when it printed JSON (pass `--format json` where the command
has it), else `{"text": ...}`. The exit codes are `sldb.cli.error_types`. Opt-in: without
`--envelope` the CLI prints and exits as it always did, because callers parse that today.
"""

from __future__ import annotations

import contextlib
import io
import json
from typing import Any, Callable

from sldb.cli.error_types import EXIT_CODES, error_type

FLAG = "--envelope"


def run_enveloped(argv: list[str], run: Callable[[list[str]], int]) -> int:
    """Run `argv` with `run`, print its envelope, and return the envelope's exit code."""
    from sldb.cli import alert_sink

    alert_sink.forget()
    code, failure, printed = _capture(argv, run)
    envelope = {**_envelope(argv, printed, code, failure), "warnings": alert_sink.kept()}
    print(json.dumps(envelope, ensure_ascii=False, default=str))
    return envelope.get("exit", 0)


def _capture(argv: list[str], run: Callable[[list[str]], int]) -> tuple[int | None, BaseException | None, str]:
    """`(exit code, failure, what it printed)` of one run, its output kept off the terminal."""
    out, err = io.StringIO(), io.StringIO()
    try:
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code, failure = run(argv), None
    except SystemExit as stop:
        code, failure = _from_exit(stop)
    except Exception as exc:  # noqa: BLE001 - every failure becomes a typed envelope
        code, failure = None, exc
    code, failure = _as_usage(code, failure, err.getvalue())
    return code, failure, out.getvalue() or err.getvalue()


def _as_usage(code: int | None, failure: BaseException | None, stderr: str) -> tuple[int | None, BaseException | None]:
    """The plain CLI turns argparse's rejection into a return of 2; the envelope names it."""
    if code != 2 or failure is not None or not _is_usage(stderr):
        return code, failure
    usage = SystemExit(2)
    usage.message = stderr.strip()
    return None, usage


def _from_exit(stop: SystemExit) -> tuple[int | None, BaseException | None]:
    """argparse exits 2 on bad usage; sldb's handlers exit with a message on an SLDBError."""
    if stop.code in (0, None):
        return 0, None
    return (None, stop) if isinstance(stop.code, str) or stop.code == 2 else (int(stop.code), None)


def _envelope(argv: list[str], printed: str, code: int | None, failure: BaseException | None) -> dict[str, Any]:
    base = {"command": _command(argv), **_store(argv)}
    if failure is None and code == 0:
        return {"ok": True, **base, "data": _data(printed)}
    if failure is None:
        group = argv[0] if argv else "cli"
        return {"ok": False, **base, "error": {"type": f"{group}/failed", "message": printed.strip()[-2000:]}, "data": _data(printed), "exit": code}
    kind, exit_code = ("cli/usage", EXIT_CODES["usage"]) if isinstance(failure, SystemExit) and failure.code == 2 else error_type(_cause(failure))
    return {"ok": False, **base, "error": {"type": kind, "message": _message(failure)}, "exit": exit_code}


def _command(argv: list[str]) -> str:
    """The command path: group and subcommand, the leading words before any option."""
    words = []
    for token in argv:
        if token.startswith("-"):
            break
        words.append(token)
    return " ".join(words[:2])


def _is_usage(stderr: str) -> bool:
    """argparse's rejection: a usage line and `error:` (the plain CLI turns it into exit 2)."""
    return stderr.lstrip().startswith("usage:") and ": error:" in stderr


def _message(failure: BaseException) -> str:
    if isinstance(failure, SystemExit):
        return getattr(failure, "message", None) or str(failure.code)
    return str(failure)


def _cause(failure: BaseException) -> BaseException:
    """The SLDBError a handler turned into `SystemExit(message)`, when it chained one."""
    return failure.__context__ if isinstance(failure, SystemExit) and failure.__context__ else failure


def _data(printed: str) -> Any:
    try:
        return json.loads(printed)
    except ValueError:
        return {"text": printed}


def _store(argv: list[str]) -> dict[str, Any]:
    from sldb.cli.envelope_store import envelope_store

    return envelope_store(argv)
