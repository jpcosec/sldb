"""tree-sitter and its grammars, imported lazily: the optional extra `[code]`.

One runtime per grammar, chosen by the file's extension: `.py` reads with tree-sitter-python;
`.ts` with the `typescript` grammar of tree-sitter-typescript, and `.tsx`, `.js` and `.jsx` with
its `tsx` grammar, which parses JavaScript too.
"""

from __future__ import annotations

import importlib
import os
from typing import Any

_TSX = ("tsx", "tree_sitter_typescript", "language_tsx")
GRAMMARS = {".py": ("python", "tree_sitter_python", "language"), ".ts": ("typescript", "tree_sitter_typescript", "language_typescript"),
            ".tsx": _TSX, ".js": _TSX, ".jsx": _TSX}
TS_SUFFIXES = (".ts", ".tsx", ".js", ".jsx")
_RUNTIME: dict[str, tuple[Any, Any]] = {}


class TreeSitterUnavailable(ImportError):
    """tree-sitter or a grammar is not installed: `pip install 'structuredLanguageDB[code]'`."""


def grammar_of(path: str) -> tuple[str, str, str]:
    """`(grammar, module, language function)` for the extension of `path` (a path or a bare `.tsx`); Python for any other."""
    return GRAMMARS.get(os.path.splitext("_" + os.path.basename(path))[1], GRAMMARS[".py"])


def runtime(path: str = ".py") -> tuple[Any, Any]:
    """`(tree_sitter module, Language)` for the grammar of `path`, imported once per process."""
    name, module, attr = grammar_of(path)
    if name not in _RUNTIME:
        try:
            ts, grammar = importlib.import_module("tree_sitter"), importlib.import_module(module)
        except ImportError as exc:
            raise TreeSitterUnavailable(f"tree-sitter runtime missing ({exc.name}): pip install 'structuredLanguageDB[code]'") from exc
        _RUNTIME[name] = (ts, ts.Language(getattr(grammar, attr)()))
    return _RUNTIME[name]


def available(path: str = ".py") -> bool:
    try:
        runtime(path)
    except TreeSitterUnavailable:
        return False
    return True


def parse(src: bytes, path: str = ".py") -> Any:
    """The tree of `src` with the grammar of `path`; `tree.root_node.has_error` says whether it parsed clean."""
    ts, language = runtime(path)
    return ts.Parser(language).parse(src)
