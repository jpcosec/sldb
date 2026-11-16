"""The four fingerprints of a TypeScript/JavaScript declaration, over the same hashing and token walk
as Python's (`fingerprints.py`, normalization 1): `signature` is the text before the body, whitespace
collapsed; `shape` the same without the name; `docstring` the JSDoc; `body` the body's leaf tokens
without comments. The module's signature is `module` and its body is the whole program.
"""

from __future__ import annotations

from typing import Any

from sldb.code.fingerprints import _sha, _tokens
from sldb.code.readers import py_norm


def ts_fingerprints(name: str | None, node: Any, fn: Any, doc: str | None, src: bytes) -> dict[str, str | None]:
    body = body_of(node, fn)
    signature = signature_text(node, body, src)
    shape = signature.replace(name, "_", 1) if name else signature
    return {"signature": _sha(signature), "shape": _sha(shape), "docstring": _sha(doc) if doc is not None else None, "body": _sha(" ".join(_tokens(body, src, None)))}


def body_of(node: Any, fn: Any) -> Any:
    """The program for the module; the function's body; a type's value or interface body."""
    if node.type == "program":
        return node
    owner = fn if fn is not None else node
    return owner.child_by_field_name("body") or owner.child_by_field_name("value")


def signature_text(node: Any, body: Any, src: bytes) -> str:
    if node.type == "program":
        return "module"
    end = body.start_byte if body is not None else node.end_byte
    return py_norm(src[node.start_byte:end].decode("utf-8", "replace"))
