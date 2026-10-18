"""`models show`, `models template show` and `docs update` take `--format`, and an argument a
subcommand does not know is reported with that subcommand's usage, not the root's.

The issue (issue-sldb-cli-format-json-coverage-gaps): the three rejected `--format json` with
the whole `sldb` usage dump, so an integrator could tell neither which command refused it nor
what that command accepts.
"""

from __future__ import annotations

import json
import sys

import pytest
import yaml

from sldb import api
from sldb.cli import main

MODULE = "sldb_format_coverage_models"
_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


@pytest.fixture
def store(tmp_path):
    (tmp_path / f"{MODULE}.py").write_text(_MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    root = tmp_path / "world"
    root.mkdir()
    sp = api.init_store(root).store_path
    api.add_model(sp, f"{MODULE}:Note", str(tmp_path))
    api.create_document(sp, "Note", root / "n.md", {"title": "first"}, "n", str(tmp_path))
    yield sp, str(tmp_path)
    sys.path.remove(str(tmp_path))
    sys.modules.pop(MODULE, None)


def _json(capsys) -> dict:
    return json.loads(capsys.readouterr().out)


def test_models_show_speaks_json_and_keeps_yaml_by_default(store, capsys):
    sp, py = store
    assert main(["models", "show", "Note", "--store", str(sp), "--pythonpath", py, "--format", "json"]) == 0
    assert _json(capsys)["model"]["name"] == "Note"
    assert main(["models", "show", "Note", "--store", str(sp), "--pythonpath", py]) == 0
    assert yaml.safe_load(capsys.readouterr().out)["model"]["name"] == "Note"


def test_models_template_show_wraps_the_template(store, capsys):
    sp, py = store
    assert main(["models", "template", "show", "Note", "--store", str(sp), "--pythonpath", py, "--format", "json"]) == 0
    payload = _json(capsys)
    assert (payload["model"], payload["draft"], payload["template"]) == ("Note", False, "# ⸢rev•title⸥")


def test_docs_update_reports_what_it_changed(store, capsys):
    sp, py = store
    assert main(["docs", "update", "n", '{"title": "second"}', "--store", str(sp), "--pythonpath", py, "--format", "json"]) == 0
    assert _json(capsys) == {"updated": "n", "model": "Note", "path": "n.md"}


def test_an_unknown_flag_shows_the_subcommands_usage(store, capsys):
    sp, py = store
    assert main(["models", "show", "Note", "--store", str(sp), "--bogus"]) == 2
    err = capsys.readouterr().err
    assert err.startswith("usage: sldb models show") and "unrecognized arguments: --bogus" in err
