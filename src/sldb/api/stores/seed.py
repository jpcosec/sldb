"""One `seeds` entry of a store declaration: a file the store scaffolds from a declared source
(`docs/architecture/store-declaration.md`). `mode` says whether an existing file is kept
(`if_missing`) or made to match the source (`managed`); a `document` source is rendered through
its model and, with `track`, tracked under the declared model and name."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

SOURCES = ("text", "file", "document")
DOCUMENT_KEYS = {"model", "name", "payload"}


class Seed(BaseModel):
    """`{path, mode, <one source>, track?}`; an unknown key is rejected by name."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(description="Where the file goes, relative to the project root.")
    mode: Literal["if_missing", "managed"] = Field(default="if_missing", description="`if_missing` never overwrites; `managed` rewrites a file whose bytes differ from the source.")
    text: str | None = Field(default=None, description="Literal content, written in UTF-8 as is.")
    file: str | None = Field(default=None, description="A template: a path relative to the template root, or `pkg:module/path` inside an importable package.")
    document: dict[str, Any] | None = Field(default=None, description="`{model, name, payload}` rendered through the model's template.")
    track: bool | None = Field(default=None, description="Track the written document under its model and name; defaults to true for a `document` source and is refused for the others.")

    @model_validator(mode="after")
    def _one_source(self) -> Seed:
        given = [key for key in SOURCES if getattr(self, key) is not None]
        if len(given) != 1:
            raise ValueError(f"seed {self.path!r} needs exactly one source of {list(SOURCES)}, got {given}")
        return self

    @model_validator(mode="after")
    def _document_shape(self) -> Seed:
        if self.document is not None and set(self.document) != DOCUMENT_KEYS:
            raise ValueError(f"seed {self.path!r}: document needs exactly the keys {sorted(DOCUMENT_KEYS)}, got {sorted(self.document)}")
        if self.track and self.document is None:
            raise ValueError(f"seed {self.path!r}: track applies to a document source only")
        return self

    @property
    def tracked(self) -> bool:
        """Whether the written file is tracked: `track`, or true for a document source."""
        return self.document is not None if self.track is None else self.track
