"""The resolved location of one sldb store, as returned by `open_store`."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class StoreLocation(BaseModel):
    """Where a store lives once a store argument (path, alias or nothing) has been resolved."""

    store_path: Path = Field(
        description="Absolute path of the store's `.sldb` directory, where its indexes live."
    )
    project_root: Path = Field(
        description="Directory that document and model paths recorded in the store are relative to."
    )
