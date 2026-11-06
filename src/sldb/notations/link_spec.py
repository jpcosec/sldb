"""`LinkSpec`: como se ve cada relacion de una notacion."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from sldb.notations.link_end_spec import LinkEndSpec
from sldb.notations.notation_constants import _ID, ANY_RELATION, TERMINALS


class LinkSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    title: str = ""
    relation: str
    model: str = ""
    draw: Literal["line", "nest", "lane", "cell", "axis"] = "line"
    line: Literal["solid", "dashed", "dotted"] = "solid"
    source_end: str = "none"
    target_end: str = "open-arrow"
    label: str = ""
    source_label: str = ""
    target_label: str = ""
    ends: dict[str, LinkEndSpec] = Field(default_factory=dict)
    form: str = ""
    description: str = ""
    color: str | dict[str, str] = ""  # color de la linea: token, `#rrggbb` o `{light, dark}`; vacio = el de la superficie

    @field_validator("id")
    @classmethod
    def _id(cls, v: str) -> str:
        if not _ID.match(v):
            raise ValueError(f"link id {v!r} must match {_ID.pattern}")
        return v

    @field_validator("relation")
    @classmethod
    def _relation(cls, v: str) -> str:
        if v != ANY_RELATION and not _ID.match(v):
            raise ValueError(f"relation {v!r} must be a vocabulary token ({_ID.pattern}) or '*'")
        return v

    @field_validator("source_end", "target_end")
    @classmethod
    def _terminal(cls, v: str) -> str:
        if v not in TERMINALS:
            raise ValueError(f"terminal {v!r} is not one of {', '.join(TERMINALS)}")
        return v

    @model_validator(mode="after")
    def _reified_has_ends(self) -> "LinkSpec":
        if self.model and not self.ends:
            raise ValueError(f"link {self.id!r} names a reified model {self.model!r} but declares no ends")
        return self
