"""A store link recorded in another store's index, as returned by `link_store`."""

from __future__ import annotations

from pydantic import BaseModel, Field


class LinkedStore(BaseModel):
    """One store linked into another under a name."""

    name: str = Field(description="Alias the linking store uses to address the linked store's documents.")
    path: str = Field(
        description="Linked `.sldb` path as recorded: relative to the linking project's root when inside it, else absolute."
    )
