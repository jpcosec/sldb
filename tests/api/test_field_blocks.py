"""Regression: `insert_field_block` must not corrupt sources whose last line lacks a newline."""

from __future__ import annotations

import ast

import pytest

from sldb.api.model_drafts.field_blocks import field_block, insert_field_block, remove_field_block


def _model_source(with_final_newline: bool) -> str:
    """A minimal valid model module, with or without a trailing newline."""
    parts = [
        "from pydantic import Field",
        "from sldb import StructuredNLDoc",
        "",
        "",
        "class T(StructuredNLDoc):",
        '    __template__ = "x"',
        '    a: str = Field(description="a")',
    ]
    return "\n".join(parts) + ("\n" if with_final_newline else "")


def _write_model(tmp_path, name: str, with_final_newline: bool) -> "Path":
    path = tmp_path / name
    path.write_text(_model_source(with_final_newline), encoding="utf-8")
    return path


def _field_names(source: str) -> list:
    tree = ast.parse(source)
    cls = next(node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "T")
    return [node.target.id for node in cls.body if isinstance(node, ast.AnnAssign)]


def test_insert_field_block_with_and_without_final_newline(tmp_path):
    for with_final_newline in (True, False):
        path = _write_model(tmp_path, f"model_{with_final_newline}.py", with_final_newline)
        original = path.read_text(encoding="utf-8")
        block = field_block("b", "str", "desc", False, None)

        result = insert_field_block(path, "T", "b", block)

        # The result is parseable, ends in a newline, and both declarations end
        # up on separate lines (the block is the first thing on its own line).
        assert _field_names(result) == ["a", "b"]
        assert result.endswith("\n")
        block_at = result.index(block)
        assert block_at > 0 and result[block_at - 1] == "\n"

        # No byte other than the inserted block changed: dropping the block back
        # reproduces the original source with only the final-newline
        # normalization applied.
        expected_original = original if original.endswith("\n") else original + "\n"
        assert result.replace(block, "", 1) == expected_original


def test_remove_field_block_with_and_without_final_newline(tmp_path):
    for with_final_newline in (True, False):
        path = _write_model(tmp_path, f"model_{with_final_newline}.py", with_final_newline)

        result = remove_field_block(path, "T", "a")

        # Symmetry check: removal never leaves trailing garbage either.
        assert _field_names(result) == []
        assert result.endswith("\n")
        assert ast.parse(result) is not None
