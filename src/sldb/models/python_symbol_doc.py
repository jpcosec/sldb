"""Tracked documentation contract for a Python AST symbol."""
from __future__ import annotations

from pydantic import Field

from .knowledge_tag import KnowledgeTag
from .structured_doc import StructuredNLDoc


class PythonSymbolDoc(StructuredNLDoc):
    """Static Python facts with explicitly authored semantic context."""

    __semantics__ = {
        "type": ["knowledge", "code_symbol"],
        "workspace": ["knowledge", "symbols"],
        "source": ["code", "python"],
    }
    __template__ = """---
id: ⸢rev•id⸥
system: ⸢rev•system⸥
module: ⸢rev•module⸥
qualname: ⸢rev•qualname⸥
kind: ⸢rev•kind⸥
source_path: ⸢rev•source_path⸥
source_span: ⸢rev•source_span⸥
source_sha256: ⸢rev•source_sha256⸥
architecture_spec: ⸢rev•architecture_spec⸥
tags: ⸢rev•tags⸥
provenance: ⸢rev•provenance⸥
---

# ⸢render•qualname⸥

## Signature

⸢rev•signature⸥

## Docstring

⸢rev•docstring⸥

## Imports

⸢rev•imports⸥

## Purpose

⸢rev•purpose⸥

## Architecture

⸢rev•architecture⸥
""".strip()

    id: str = Field(description="Stable Python symbol identity.")
    system: str = Field(description="System owning the scanned source tree.")
    module: str = Field(description="Importable module containing the symbol.")
    qualname: str = Field(description="Lexical qualified name inside the module.")
    kind: str = Field(description="AST declaration kind.")
    source_path: str = Field(description="Path relative to the scanned root.")
    source_span: str = Field(description="Inclusive one-based source line span.")
    source_sha256: str = Field(description="Hash of the containing source file.")
    architecture_spec: str | None = Field(default="Not declared.", description="Explicit architecture-spec reference and hash.")
    signature: str = Field(description="Syntactic callable signature, when applicable.")
    docstring: str = Field(description="Declared source docstring, when applicable.")
    imports: str = Field(description="JSON import facts for the containing module.")
    purpose: str = Field(description="Authored explanation of why this symbol exists.")
    architecture: str = Field(description="Authored architectural role or boundary.")
    tags: list[KnowledgeTag] = Field(default_factory=list, description="Authored semantic tags.")
    provenance: str = Field(description="Scanner contract and source identity.")
