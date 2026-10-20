"""One fingerprint per node of a definition (docs/architecture/code-anchoring.md §3, normalization 1).

`signature`: the decorators, in order, and the `def`/`class` line, whitespace collapsed.
`shape`: the signature with the name taken out, for a reconnection that allows a rename.
`docstring`: the literal's value through `inspect.cleandoc`; None when there is none.
`body`: the body's leaf tokens without the docstring and without comments, joined by one
space; a nested definition is reduced to its name and its signature fingerprint, so a
class's fingerprint moves with its methods' signatures and not with their bodies.
"""

from __future__ import annotations

import hashlib
from typing import Any

from sldb.selfdoc.treesitter.readers import docstring_node, field_text, py_doc, py_norm, text

NORMALIZATION = 1
_DEFINITIONS = ("function_definition", "class_definition", "decorated_definition")


def fingerprints(node: Any, src: bytes) -> dict[str, str | None]:
    """`{signature, shape, docstring, body}` of a `function_definition`/`class_definition` node."""
    doc = py_doc(node, src)
    signature = signature_text(node, src)
    return {"signature": _sha(signature), "shape": _sha(shape_text(node, src)), "docstring": _sha(doc) if doc is not None else None, "body": _sha(body_text(node, src))}


def signature_text(node: Any, src: bytes) -> str:
    """Decorators and the header line, normalized; the module is its name alone."""
    header = text(node, src)[: _header_end(node, src)].rstrip(":").strip() if node.type != "module" else "module"
    return "\n".join([*_decorators(node, src), py_norm(header)])


def shape_text(node: Any, src: bytes) -> str:
    name = field_text(node, src, "name")
    return signature_text(node, src).replace(name, "_", 1) if name else signature_text(node, src)


def body_text(node: Any, src: bytes) -> str:
    body = node if node.type == "module" else node.child_by_field_name("body")
    skip = docstring_node(node)
    return " ".join(_tokens(body, src, skip))


def _tokens(node: Any, src: bytes, skip: Any) -> list[str]:
    if node is None or node.type == "comment" or (skip is not None and node.id == skip.id):
        return []
    if node.type in _DEFINITIONS:
        inner = node.children[-1] if node.type == "decorated_definition" else node
        return [f"<{inner.type.split('_')[0]} {field_text(inner, src, 'name')} {_sha(signature_text(inner, src))[:12]}>"]
    if not node.children:
        return [text(node, src)]
    return [t for child in node.children for t in _tokens(child, src, skip)]


def _decorators(node: Any, src: bytes) -> list[str]:
    parent = node.parent
    if parent is None or parent.type != "decorated_definition":
        return []
    return [py_norm(text(d, src)) for d in parent.children if d.type == "decorator"]


def _header_end(node: Any, src: bytes) -> int:
    body = node.child_by_field_name("body")
    return (body.start_byte - node.start_byte) if body is not None else len(text(node, src))


def _sha(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()
