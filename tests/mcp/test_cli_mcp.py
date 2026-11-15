"""`sldb mcp` without the `mcp` extra: sldb keeps working and the command says how to install it."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from mcp_session import server_env

WITHOUT_EXTRA = "import sys; sys.modules['mcp'] = None; from sldb.cli import main; raise SystemExit(main({argv!r}))"


def run_without_extra(argv: list[str], cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-c", WITHOUT_EXTRA.format(argv=argv)], capture_output=True, text=True, timeout=120, cwd=cwd, env=server_env())


def test_sldb_mcp_says_how_to_install_the_extra(tmp_path: Path) -> None:
    done = run_without_extra(["mcp", "--store", str(tmp_path / ".sldb")], tmp_path)
    assert done.returncode == 2 and "structuredLanguageDB[mcp]" in done.stderr and done.stdout == "", (done.stdout, done.stderr)


def test_the_rest_of_sldb_does_not_need_the_extra(tmp_path: Path) -> None:
    done = run_without_extra(["stores", "--help"], tmp_path)
    assert done.returncode == 0 and "Traceback" not in done.stderr, done.stderr
    assert "mcp" in run_without_extra(["--help"], tmp_path).stdout


def test_the_package_imports_the_mcp_library_only_in_the_server(tmp_path: Path) -> None:
    code = "import sys; sys.modules['mcp'] = None; import sldb.mcp, sldb.mcp.read, sldb.mcp.write, sldb.mcp.signals; print('ok')"
    done = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=120, cwd=tmp_path, env=server_env())
    assert done.returncode == 0 and done.stdout.strip() == "ok", done.stderr
