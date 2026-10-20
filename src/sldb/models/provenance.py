"""Who wrote a document, when, through what, and with which authority (docs/architecture/provenance.md).

Carried by every document in a reserved `sldb` frontmatter block; declared here, next to the
base model, so every reader shares one schema. A document without the block reads as
`agent`, `0`, `generated`: the least authority possible, until someone signs it.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

Authority = Literal["source_raw", "authored", "theorem", "generated", "cache"]
AUTHORITIES: tuple[str, ...] = ("source_raw", "authored", "theorem", "generated", "cache")
BLOCK_KEY = "sldb"


class Provenance(BaseModel):
    """The `sldb` block of a document; `declared` says whether the document carried one."""

    by: str = Field(default="agent", description="Who wrote this version: `human:<id>` or `agent:<id>`; bare `agent` when unknown.")
    at: str | int = Field(default=0, description="When, as an ISO-8601 UTC instant; 0 when unknown.")
    via: str | None = Field(default=None, description="The operation or tool that wrote: `save_document_payload`, `deskops retire`...")
    authority: Authority = Field(default="generated", description="How much the content is to be trusted and who may change it (docs/architecture/provenance.md §2).")
    from_: list[str] = Field(default_factory=list, alias="from", description="What this document derives from (theorem, generated): `code:<path>::<name>`, `doc:<Model:name>`.")
    declared: bool = Field(default=False, exclude=True, description="True when the document carried a block; False when these are the defaults.")

    model_config = {"populate_by_name": True}

    def as_block(self) -> dict[str, Any]:
        """The mapping written under the `sldb` key; `from` only when it names something."""
        block: dict[str, Any] = {"by": self.by, "at": self.at, "authority": self.authority}
        if self.via:
            block["via"] = self.via
        if self.from_:
            block["from"] = list(self.from_)
        return block

    @classmethod
    def of_model(cls, model_type: type) -> tuple[str, bool]:
        """`(authority, declared)` of a model class: its `__authority__`, and whether some class
        of its own (not the base) set it."""
        declared = any("__authority__" in vars(c) for c in model_type.__mro__ if c.__name__ != "StructuredNLDoc")
        return getattr(model_type, "__authority__", None) or "generated", declared

    @classmethod
    def from_block(cls, block: dict[str, Any] | None) -> Provenance:
        """A block as read, or the defaults when there is none (or it is not a mapping)."""
        if not isinstance(block, dict):
            return cls()
        known = {k: v for k, v in block.items() if k in ("by", "at", "via", "authority", "from")}
        return cls(**known, declared=True)
