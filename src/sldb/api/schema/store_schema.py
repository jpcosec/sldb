"""Every registered model described, with the broken ones declared explicitly.

One model whose module does not import used to take the whole ``/schema``
response down: a store with twenty models and one broken returned zero. That is
silent degradation inverted — instead of swallowing the error it swallowed the
answer. Here each model is described independently, and a failure lands in
``unavailable`` with its reason so the consumer knows the listing is partial.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field

from sldb.api.schema.unavailable_model import UnavailableModel


class StoreSchema(BaseModel):
    """The describable models of a store plus the ones that failed to load."""

    models: list[dict[str, Any]] = Field(default_factory=list, description="Schema descriptor of every model that could be described.")
    unavailable: list[UnavailableModel] = Field(default_factory=list, description="Registered models that could not be loaded, each with its reason.")
