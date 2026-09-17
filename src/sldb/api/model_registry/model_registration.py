"""A model's registry record after registering or reindexing it."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ModelRegistration(BaseModel):
    """The registry facts of one model, as a store index records them."""

    name: str = Field(description="Model name documents and queries use to address the model.")
    model_ref: str = Field(description="`module:ClassName` reference the model class is imported from.")
    path: str = Field(description="Model source file, relative to the project root when inside it.")
    version: int = Field(description="Contract version; bumped each time a draft is promoted.")
