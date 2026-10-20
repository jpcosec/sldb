"""`code:<path>::<qualified_name>`: an anchor's reference to a Python symbol, by name, never by line.

`<path>` is relative to the project root, with `/`; `<qualified_name>` is the lexical owner
chain the tree-sitter scanner emits (`Class.method`, `function.nested`), empty for the module
itself; a repeated name carries the scanner's `~2`, `~3` suffix.
"""

from __future__ import annotations

PREFIX = "code:"
SEPARATOR = "::"


def parse_code_ref(ref: str) -> tuple[str, str] | None:
    """`(path, qualified_name)`, or None when `ref` does not have the form."""
    if not isinstance(ref, str) or not ref.startswith(PREFIX) or SEPARATOR not in ref:
        return None
    path, _, name = ref[len(PREFIX):].partition(SEPARATOR)
    if not path or path.startswith("/") or ".." in path.split("/") or not path.endswith(".py"):
        return None
    return path, name.strip()


def code_ref(path: str, qualified_name: str) -> str:
    return f"{PREFIX}{path}{SEPARATOR}{qualified_name}"
