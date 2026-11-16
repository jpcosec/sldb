from __future__ import annotations
import argparse

from sldb.cli.bench.operations import ALL_OPS, DEFAULT_OPS

_EPILOG = """Each --desk is cloned (git clone --no-hardlinks, committed HEAD) into WORKDIR/NAME; the
source is only read. Cold: .sldb_cache of the copy and WORKDIR/xdg (the XDG_CACHE_HOME of
every child) are deleted before each measured run. Warm: one unmeasured run first.
sldb runs from the sldb running this command; deskops runs as installed, as a consumer.

Example:
  sldb bench --desk sldb=../sldb --desk deskops=../deskops --output bench.json
  flock LOCK sldb bench --desk sldb=. --ops build-check --output build.json"""


def add_bench_commands(s: argparse._SubParsersAction) -> None:
    p = s.add_parser("bench", help="Measure sldb and deskops speed on desk copies, cold and warm.",
                     epilog=_EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--desk", action="append", required=True, metavar="NAME=PATH", help="Desk to copy and measure; repeatable.")
    p.add_argument("--ops", help=f"Comma list from: {', '.join(ALL_OPS)}. Default: {', '.join(DEFAULT_OPS)}.")
    p.add_argument("--modes", default="cold,warm", help="cold, warm or both (default: cold,warm).")
    p.add_argument("--repeat", type=int, default=1, help="Measured runs per operation and mode (default 1).")
    p.add_argument("--timeout", type=float, default=7200.0, help="Seconds before one run is killed (default 7200).")
    _add_places(p)


def _add_places(p: argparse.ArgumentParser) -> None:
    p.add_argument("--touch", action="append", metavar="NAME=PATH", help="Document changed by update-one (default: first tracked .md).")
    p.add_argument("--workdir", help="Where the copies go (default: $TMPDIR/sldb-bench); deleted at the end.")
    p.add_argument("--keep", action="store_true", help="Keep the work directory.")
    p.add_argument("--deskops", help="deskops executable (default: the one on PATH).")
    p.add_argument("--output", help="Write the JSON result to this file.")
    p.add_argument("--format", choices=("text", "json"), default="text", help="stdout: table (text) or the JSON.")
