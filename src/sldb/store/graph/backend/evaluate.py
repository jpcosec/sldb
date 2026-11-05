"""Evaluate the small AST of the GO02 subset, keeping the clause and `seen` of the decision."""

from __future__ import annotations

from typing import Any


def evaluate(node: tuple, payload: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    """`(holds, clause, seen)` for one AST node over a payload."""
    tag = node[0]
    if tag == "leaf":
        return _leaf(node, payload)
    if tag == "not":
        return _not(node, payload)
    return _bool(node, payload)


def _leaf(node: tuple, payload: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    holds, seen = node[4](payload)
    return holds, node[3], seen


def _not(node: tuple, payload: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    holds, clause, seen = evaluate(node[3], payload)
    return not holds, clause, seen


def _bool(node: tuple, payload: dict[str, Any]) -> tuple[bool, str, dict[str, Any]]:
    tag, _, _, clause, left, right = node
    left_result = evaluate(left, payload)
    if tag == "and" and not left_result[0]:
        return left_result
    if tag == "or" and left_result[0]:
        return left_result
    return _combine(tag, clause, left_result, evaluate(right, payload))


def _combine(tag: str, clause: str, left: tuple, right: tuple) -> tuple[bool, str, dict[str, Any]]:
    seen = {**left[2], **right[2]}
    if tag == "and":
        return right if not right[0] else (True, clause, seen)
    return right if right[0] else (False, clause, seen)
