"""tree-sitter and the Python grammar, imported lazily: the optional extra `[code]`."""

from __future__ import annotations

import importlib
from typing import Any

_RUNTIME: list[tuple[Any, Any]] = []


class TreeSitterUnavailable(ImportError):
    """tree-sitter or its Python grammar is not installed: `pip install 'structuredLanguageDB[code]'`."""


def runtime() -> tuple[Any, Any]:
    """`(tree_sitter module, Python Language)`, imported once per process."""
    if not _RUNTIME:
        try:
            ts, grammar = importlib.import_module("tree_sitter"), importlib.import_module("tree_sitter_python")
        except ImportError as exc:
            raise TreeSitterUnavailable(f"tree-sitter runtime missing ({exc.name}): pip install 'structuredLanguageDB[code]'") from exc
        _RUNTIME.append((ts, ts.Language(grammar.language())))
    return _RUNTIME[0]


def available() -> bool:
    try:
        runtime()
    except TreeSitterUnavailable:
        return False
    return True


def parse(src: bytes) -> Any:
    """The tree of `src`; `tree.root_node.has_error` says whether it parsed clean."""
    ts, language = runtime()
    return ts.Parser(language).parse(src)
