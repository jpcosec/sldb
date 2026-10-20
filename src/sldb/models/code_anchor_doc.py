"""sldb's own anchor to code (docs/architecture/anchoring.md §5, owner's decision 1).

Grounds a claim in a Python symbol and keeps what it saw of it: one fingerprint per node
(signature, shape, docstring, body). pron's `AnchorDoc` is a lexicon alias and stays as it is;
verifying is this model's job. A document of this model is `theorem` by authority: derived
from a source it names in `ref`.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from sldb.models.structured_doc import StructuredNLDoc


class CodeAnchorDoc(StructuredNLDoc):
    __authority__ = "theorem"
    __semantics__ = {
        "type": ["knowledge", "anchor", "code"],
        "workspace": ["knowledge", "anchors"],
    }
    __template__ = """---
ref: ⸢rev•ref⸥
kind: ⸢rev•kind⸥
seen: ⸢rev,dict•seen⸥
normalization: ⸢rev•normalization⸥
recorded_with: ⸢rev•recorded_with⸥
history: ⸢optrev,list•history⸥
---

# ⸢render•ref⸥

## Claim

⸢rev•claim⸥
""".strip()

    ref: str = Field(description="`code:<path>::<qualified_name>`: the symbol the claim stands on, resolved by name.")
    kind: str = Field(description="What the symbol was when recorded: module | class | function | method.")
    seen: dict[str, Any] = Field(description="One fingerprint per node as recorded: signature, shape, docstring (null when none) and body.")
    normalization: int = Field(description="Version of the fingerprint rules the anchor was recorded under (code-anchoring.md §3).")
    recorded_with: str = Field(description="The scanner and grammar that produced `seen`, e.g. `treesitter-symbols/1 (tree-sitter-python 0.25)`.")
    history: list[dict[str, Any]] = Field(default_factory=list, description="What happened to the reference, never erased: `{event: reconnected, from, to, at}`, `{event: recorded, at}`.")
    claim: str = Field(description="What is being said because of this symbol: the statement the anchor grounds.")
