"""Where a registered model class is defined, as returned by `locate_model_source`."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field


class ModelSource(BaseModel):
    """The source file and import path of the class that defines a registered model."""

    path: Path = Field(description="Resolved source file that defines the model class (the active contract).")
    module_name: str = Field(description="Module the defining class is imported from.")
    attr_path: str = Field(description="Dotted attribute path of the class inside its module.")

    @property
    def class_name(self) -> str:
        """Name of the class statement to edit in the source file."""
        return self.attr_path.split(".")[-1]

    @property
    def draft_path(self) -> Path:
        """The `.py.temp` sibling where edits accumulate until the draft is promoted."""
        return self.path.with_name(self.path.name + ".temp")

    @property
    def editable_path(self) -> Path:
        """The draft when one exists, else the active source: where the next edit starts from."""
        return self.draft_path if self.draft_path.exists() else self.path
