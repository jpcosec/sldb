"""Isolated projects for CLI self-documentation tests."""
import importlib
import json
import sys

import pytest

from sldb.cli.main import main


@pytest.fixture
def project(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    sys.modules.pop("selfdoc_test_factory", None)
    (tmp_path / "selfdoc_test_factory.py").write_text(
        "import argparse\nDEFAULT = 3\nREMOVED = False\n"
        "def build():\n"
        "    parser = argparse.ArgumentParser(prog='widget')\n"
        "    sub = parser.add_subparsers(dest='command')\n"
        "    if not REMOVED:\n"
        "        run = sub.add_parser('run', help='Run a widget.')\n"
        "        run.add_argument('--limit', type=int, default=DEFAULT)\n"
        "    return parser\n",
        encoding="utf-8",
    )
    assert main(["stores", "init"]) == 0
    capsys.readouterr()
    yield tmp_path
    sys.modules.pop("selfdoc_test_factory", None)


@pytest.fixture
def invoke(capsys):
    def run(operation, *extra):
        code = main(["selfdoc", operation, "--factory", "selfdoc_test_factory:build",
                     *([] if operation == "scan" else ["--system", "widget"]), *extra])
        output = capsys.readouterr()
        return code, json.loads(output.out)
    return run
