"""One `eval` finding: fill the subject's braces, parse, evaluate, keep the GO02 shape."""

from __future__ import annotations

from typing import Any

from sldb.store.graph.backend.evaluate import evaluate
from sldb.store.graph.backend.parser import parse
from sldb.store.query_engine.where_subject import fill_braces


def evaluate_finding(predicate: Any, payload: dict[str, Any], node: str) -> dict[str, Any]:
    """The finding for this payload; a missing or non-scalar brace makes it false."""
    text = predicate if isinstance(predicate, str) else str(predicate)
    filled, complete = fill_braces(text, payload)
    holds, clause, seen = evaluate(parse(filled, text), payload)
    return {"node": node, "holds": _holds(holds and complete), "clause": clause, "seen": seen}


def _holds(value: bool) -> str:
    return "true" if value else "false"
