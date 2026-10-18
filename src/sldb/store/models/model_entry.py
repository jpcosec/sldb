from typing import Any

from pydantic import BaseModel, Field, SerializationInfo, SerializerFunctionWrapHandler, model_serializer


class ModelEntry(BaseModel):
    name: str
    model_ref: str
    path: str
    models_index: str
    version: int = 1
    canonical: bool = False
    family: str | None = None
    semantics: list[str] = Field(default_factory=list)
    # The alias of the linked store that owns this model (see sldb.store.model_origin). An
    # inherited entry keeps no source path of its own: the class imports from the owner's root.
    origin: str | None = None

    @model_serializer(mode="wrap")
    def _omit_absent_origin(self, handler: SerializerFunctionWrapHandler, info: SerializationInfo) -> dict[str, Any]:
        """A model the store owns writes no `origin` key, so no existing store index changes."""
        data = handler(self)
        if data.get("origin") is None:
            data.pop("origin", None)
        return data
