"""AnchorDoc document contract."""
from __future__ import annotations

from pydantic import Field
from sldb.models.structured_doc import StructuredNLDoc
from .knowledge_tag import KnowledgeTag


class AnchorDoc(StructuredNLDoc):
    """Binds a grammar symbol to a semantic motive and a resolvable referent.

    Implements the knowledge core anchor contract: kind partitions what the
    symbol can refer to, ref is a typed string with a kind-specific scheme,
    and motive keeps the grammar legible and auditable.
    """

    __semantics__ = {
        "type": ["knowledge", "anchor"],
        "workspace": ["knowledge", "anchors"],
    }
    __template__ = """---
id: ⸢rev•id⸥
symbol: ⸢rev•symbol⸥
kind: ⸢rev•kind⸥
ref: ⸢rev•ref⸥
tags: ⸢rev•tags⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢render•symbol⸥

## Motive

⸢rev•motive⸥
""".strip()

    id: str = Field(
        description="Stable id, conventionally 'anchor-<symbol>'."
    )
    symbol: str = Field(
        description="The grammar symbol this anchor defines (e.g. user, check, preferences)."
    )
    kind: str = Field(
        pattern=r"^(model|doc|relation|operation|projection|expr)$",
        description="What class of referent the symbol names: model | doc | relation | operation | projection | expr (a derived relation: an s-expression template with _ holes).",
    )
    ref: str = Field(
        pattern=r"^(model:[A-Za-z_][A-Za-z0-9_]*|doc:[a-z0-9-]+|edge:[a-z_]+(:(in|out))?|op:[a-z_]+|fields:[a-z_,]+|view:[a-z_]+|expr:[(].+[)])$",
        description="Typed referent: model:<Name> | doc:<name> | edge:<rel>[:dir] | op:<fn> | fields:<f1,f2> | view:<name> | expr:(<s-expression with _ holes>).",
    )
    motive: str = Field(
        description="Natural-language meaning of the symbol: what it refers to and why, legible to humans."
    )
    tags: list[KnowledgeTag] = Field(
        default_factory=list,
        description="Namespaced semantic tags for retrieval and grouping.",
    )
    provenance: str | None = Field(
        default=None,
        description="Source of this anchor definition (spec section or code path).",
    )
