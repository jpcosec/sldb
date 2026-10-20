"""The tree-sitter scanner agrees with sldb's `ast` scanner on the shared fixture trees (ported
from kimun's agreement test): same symbols, same docstrings, same start lines."""
from __future__ import annotations

from pathlib import Path

import pytest

from sldb.selfdoc.python_scanner import PythonScanner
from sldb.selfdoc.treesitter.runtime import available

pytestmark = pytest.mark.skipif(not available(), reason="tree-sitter runtime not installed (extra [code])")
FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "treesitter"


def _ts(root: Path) -> dict[str, dict]:
    from sldb.selfdoc.treesitter.scan import scan_tree

    return {f["id"].split("~")[0]: f for f in scan_tree(root) if f["kind"] != "module" and "~" not in f["id"]}


def _ast(root: Path) -> dict[str, dict]:
    return {f"{s.module}.{s.qualname}": s for s in PythonScanner().scan(root)}


@pytest.mark.parametrize("tree, at_least", [("pytree", 3), ("pytree_ts", 12)])
def test_both_scanners_see_the_same_definitions(tree, at_least):
    ts, ast_facts = _ts(FIXTURES / tree), _ast(FIXTURES / tree)
    assert sorted(ts) == sorted(ast_facts), "symbol sets differ"
    assert len(ts) > at_least
    for fid, a in ast_facts.items():
        t = ts[fid]
        assert (t["doc"], t["span"]["start_line"], t["signature"] is None) == (a.docstring, a.line_start, a.signature is None), fid
        assert t["signature"] is None or t["signature"].replace(" ", "") == a.signature.replace(" ", ""), fid
