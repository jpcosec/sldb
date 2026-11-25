"""A Python call carries its arguments: literals with their value, anything else marked `literal: false`.
Skipped without the `[code]` extra."""

from __future__ import annotations

from pathlib import Path

import pytest

from sldb.code.runtime import available
from sldb.code.scan import scan_file

pytestmark = pytest.mark.skipif(not available(), reason="tree-sitter runtime not installed (extra [code])")

ROOT = Path(__file__).resolve().parents[2]


def _facts(tmp_path: Path, source: str) -> dict[str, dict]:
    (tmp_path / "m.py").write_text(source)
    return {f["qualified_name"]: f for f in scan_file("m.py", tmp_path)}


def test_add_parser_carries_the_command_name_and_its_help():
    facts = scan_file("src/sldb/cli/parsers/graph_project.py", ROOT)
    calls = [c for f in facts for c in f["attrs"].get("calls", []) if c["name"] == "inner.add_parser"]
    nodes = next(c for c in calls if c["args"] and c["args"][0]["value"] == "nodes")
    assert nodes["args"][0] == {"text": "'nodes'", "value": "nodes"}
    assert nodes["kwargs"]["help"]["value"].startswith("Every document and file node")
    assert nodes["kwargs"]["help"]["text"].startswith("'Every document and file node")


def test_a_variable_argument_is_not_literal_and_the_call_key_is_unchanged(tmp_path):
    f = _facts(tmp_path, "def g(x):\n    f(x, 1, k=[1, 'a'], v=x, *r, **kw)\n    return f'{x}'\n")["g"]
    (call,) = f["attrs"]["calls"]
    assert call["name"] == "f" and call["line"] == 2
    assert call["args"][0] == {"text": "x", "literal": False}
    assert call["args"][1] == {"text": "1", "value": 1}
    assert call["args"][2] == {"text": "*r", "literal": False}
    assert call["kwargs"]["k"] == {"text": "[1, 'a']", "value": [1, "a"]}
    assert call["kwargs"]["v"] == {"text": "x", "literal": False}
    assert call["args"][3] == {"text": "**kw", "literal": False}
    assert {"type": "calls", "target": "f"} in f["relations"] and call["name"] == "f"


def test_literal_kinds(tmp_path):
    f = _facts(tmp_path, "def g():\n    h(None, True, 2.5, (1, 2), {'a': 1}, f'{g}')\n")["g"]
    values = [a.get("value", "NOT") for a in f["attrs"]["calls"][0]["args"]]
    assert values == [None, True, 2.5, (1, 2), {"a": 1}, "NOT"]
    assert f["attrs"]["calls"][0]["args"][5]["literal"] is False


def test_a_decorator_with_arguments_uses_the_same_shape(tmp_path):
    f = _facts(tmp_path, "@route('/x', methods=['GET'], cb=handler)\ndef v(): pass\n")["v"]
    assert f["attrs"]["decorators"] == [{"name": "route", "args": [{"text": "'/x'", "value": "/x"}],
                                         "kwargs": {"methods": {"text": "['GET']", "value": ["GET"]}, "cb": {"text": "handler", "literal": False}}}]
