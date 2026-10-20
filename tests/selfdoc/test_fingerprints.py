"""Fingerprints per node (docs/architecture/code-anchoring.md §3): the docstring, the body and the
signature are distinct nodes; formatting is not a mutation; a nested definition does not drag its owner."""
from __future__ import annotations

import pytest

from sldb.selfdoc.treesitter.runtime import available

pytestmark = pytest.mark.skipif(not available(), reason="tree-sitter runtime not installed (extra [code])")

BASE = 'class K:\n    """K doc."""\n\n    def m(self, x: int = 1) -> int:\n        """M doc."""\n        y = x + 1  # a comment\n        return y\n'


def _fp(source: str, name: str) -> dict:
    from sldb.selfdoc.treesitter.fingerprints import fingerprints
    from sldb.selfdoc.treesitter.runtime import parse

    src = source.encode("utf-8")
    root = parse(src).root_node
    return fingerprints(_find(root, name, src), src)


def _find(node, name: str, src: bytes):
    for child in node.children:
        label = child.child_by_field_name("name") if child.type in ("function_definition", "class_definition") else None
        if label is not None and src[label.start_byte:label.end_byte] == name.encode():
            return child
        found = _find(child, name, src)
        if found is not None:
            return found
    return None


def _changed(before: dict, after: dict) -> set[str]:
    return {node for node in ("signature", "docstring", "body") if before[node] != after[node]}


def test_rule_1_docstring_and_body_are_distinct_nodes():
    base = _fp(BASE, "m")
    assert _changed(base, _fp(BASE.replace("M doc.", "Other doc."), "m")) == {"docstring"}
    assert _changed(base, _fp(BASE.replace("return y", "return y + 1"), "m")) == {"body"}
    assert _changed(base, _fp(BASE.replace("M doc.", "Other doc.").replace("return y", "return y + 1"), "m")) == {"docstring", "body"}
    assert _changed(base, _fp(BASE.replace("x: int = 1", "x: int = 2"), "m")) == {"signature"}


def test_formatting_and_comments_are_not_mutations():
    base = _fp(BASE, "m")
    reformatted = BASE.replace("y = x + 1  # a comment\n        return y", "y   =   x+1\n\n        return   y")
    assert _changed(base, _fp(reformatted, "m")) == set()
    assert _changed(base, _fp(BASE.replace("# a comment", "# another"), "m")) == set()


def test_a_method_body_does_not_move_its_class_but_its_signature_does():
    base = _fp(BASE, "K")
    assert _changed(base, _fp(BASE.replace("return y", "return y + 1"), "K")) == set()
    assert _changed(base, _fp(BASE.replace("x: int = 1", "x: int = 2"), "K")) == {"body"}
    assert _changed(base, _fp(BASE.replace("K doc.", "Changed."), "K")) == {"docstring"}


def test_the_shape_survives_a_rename_and_the_signature_does_not():
    base = _fp(BASE, "m")
    renamed = _fp(BASE.replace("def m(", "def renamed("), "renamed")
    assert renamed["shape"] == base["shape"] and renamed["signature"] != base["signature"]
    assert _fp(BASE, "m")["docstring"] is not None and _fp(BASE.replace('        """M doc."""\n', ""), "m")["docstring"] is None
