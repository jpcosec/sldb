"""More than one submodel of the asked model tracks a document with that name."""

from __future__ import annotations


class AmbiguousDocument(LookupError):
    """`Model:name` asked under a base model matches documents of several of its submodels."""

    def __init__(self, model: str, name: str, models: list[str]) -> None:
        self.model, self.name, self.models = model, name, models
        found = ", ".join(f"{m}:{name}" for m in models)
        super().__init__(f"{model}:{name} is ambiguous: tracked as {found}; ask for one of them by its own model.")
