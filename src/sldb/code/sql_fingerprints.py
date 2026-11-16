"""The four fingerprints of a SQL object, over the same hashing and token walk as Python's
(`fingerprints.py`, normalization 1): `signature` is the whole `CREATE` statement (or column
definition), whitespace collapsed; `shape` the same with the name taken out; `docstring` the `--`
comment; `body` the leaf tokens after the name, without comments. The module's signature is
`module` and its body is the whole file.
"""

from __future__ import annotations

from typing import Any

from sldb.code.fingerprints import _sha, _tokens
from sldb.code.sql_readers import sql_norm


def sql_fingerprints(node: Any, name: Any, doc: str | None, src: bytes) -> dict[str, str | None]:
    signature = sql_norm(node, src) if name is not None else "module"
    shape = signature.replace(sql_norm(name, src), "_", 1) if name is not None else signature
    after = [c for c in node.children if name is None or c.start_byte >= name.end_byte]
    body = [t for c in after for t in _tokens(c, src, None)]
    return {"signature": _sha(signature), "shape": _sha(shape), "docstring": _sha(doc) if doc is not None else None, "body": _sha(" ".join(body))}
