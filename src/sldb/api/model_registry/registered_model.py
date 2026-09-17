"""A model registered in a store, resolved to its class, as returned by `load_registered_model`."""

from __future__ import annotations

from pydantic import BaseModel, Field

from sldb.models.structured_doc import StructuredNLDoc
from sldb.store.models.model_entry import ModelEntry
from sldb.store.models.store_index import StoreIndex


class RegisteredModel(BaseModel):
    """A registered model's class together with the registry records that name it."""

    model_type: type[StructuredNLDoc] = Field(description="The imported model class documents of this model validate against.")
    entry: ModelEntry = Field(description="The store index entry registering the model; the same object held in `store_index.models`.")
    store_index: StoreIndex = Field(description="The store index the entry was read from, to pass on to store writes such as tracking.")
