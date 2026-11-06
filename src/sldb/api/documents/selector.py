"""The selector of `select_documents`: a mapping of keys combined by conjunction."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Selector(BaseModel):
    """What a document is chosen by; every key given must hold (`docs/architecture/selectors.md`).

    An unknown key, or a key given as an empty or blank string, is rejected: a blank selector
    would silently choose everything (or nothing), as the deskops rule it replaces refused.
    """

    model_config = ConfigDict(extra="forbid")

    ref: str | None = Field(default=None, description="`name`, `Model/name`, `Model:name` or a tracked path, optionally behind `alias:` of a directly linked store (what `doc_status` accepts).")
    prefix: str | None = Field(default=None, description="Name prefix; with `expect='one'` an exact name wins over the prefix matches.")
    path_glob: str | None = Field(default=None, description="Shell pattern over the path relative to the project root; `**` crosses directories.")
    model: str | None = Field(default=None, description="A model name: the model and every model extending it.")
    where: str | None = Field(default=None, description="A predicate of the rules language over the edge index's payload projection.")
    include_linked: bool = Field(default=False, description="Also read every store linked directly to this one; their rows carry `alias:`.")

    @field_validator("ref", "prefix", "path_glob", "model", "where")
    @classmethod
    def _not_blank(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            raise ValueError("a selector key cannot be empty or blank")
        return value

    def describe(self) -> str:
        """The keys given, as `key='value'` pairs (the text an error names the selector by)."""
        given = {key: value for key, value in self.model_dump().items() if value not in (None, False)}
        return ", ".join(f"{key}={value!r}" for key, value in given.items()) or "{}"
