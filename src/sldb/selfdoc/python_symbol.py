"""---
id: sldb.selfdoc.python_symbol
kind: core
tags: [system:sldb, workspace:knowledge, topic:selfdoc]

---
Define the typed source-symbol record shared by Python scanning and materialization.

This module declares the data boundary for static source facts. It does not
execute scanned code, persist graph relationships, or assign architectural roles.
"""
from __future__ import annotations

from pydantic import BaseModel, Field


class PythonSymbol(BaseModel):
    """---
    id: sldb.selfdoc.python_symbol.PythonSymbol
    kind: core
    tags: [type:code.symbol]

    ---
    Validate and carry the static facts extracted from one Python declaration.

    The scanner supplies lexical identity, AST kind, source location, signature,
    docstring, enclosing-module imports, and a hash of the entire source file.
    The materializer consumes these fields to build a tracked reference document.
    The record does not resolve imports or establish runtime dependencies; its
    file hash is not a symbol-level fingerprint. Field ``kind`` describes the AST
    node, independently of the semantic ``kind`` in this docstring's metadata.
    """

    id: str = Field(description="Stable module-qualified symbol identifier.")
    kind: str = Field(description="Python AST node kind for the symbol.")
    module: str = Field(description="Importable module name relative to source root.")
    qualname: str = Field(description="Lexical qualified name within the module.")
    path: str = Field(description="Source path relative to the selected root.")
    line_start: int = Field(description="One-based source start line.")
    line_end: int = Field(description="One-based source end line.")
    signature: str | None = Field(description="Syntactic callable signature when applicable.")
    docstring: str | None = Field(description="Declared docstring without semantic inference.")
    source_sha256: str = Field(description="Hash of the source file containing the symbol.")
    imports: list[str] = Field(description="Imports declared by the enclosing module.")
