"""`Metadata`."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator

from sldb.models.notation.diagram_specs.base.extensions import move_extensions

class Metadata(BaseModel):
    """Authorship and description, plus the project's own annotations as ``x-*`` keys.

    ``metadata`` is the only place a project may add keys of its own, and only with the ``x-`` prefix
    (``x-fuentes``, ``x-estado``): they are kept as written under ``extensions``. Any other unknown key is
    an error with its path, like everywhere else in a spec (a typo there is caught, not silently kept)."""

    model_config = ConfigDict(extra="forbid")

    author: str | None = Field(
        default=None,
        description="Name of the person or team responsible for the diagram spec.",
    )
    description: str | None = Field(
        default=None,
        description="Free-form summary that explains the intent of the diagram.",
    )
    preguntas_abiertas: list[str] | None = Field(
        default=None,
        description=(
            "Open questions about the diagram. A single string is taken as a one-item list. The bpmn viewer "
            "shows them under the description."
        ),
    )
    legend: dict[str, str] | None = Field(
        default=None,
        description=(
            "Label per colour in the bpmn viewer legend, keyed by tone (`success`, `rule2`, `gateway`, ...); "
            "a tone without a label keeps its generic Spanish one."
        ),
    )
    extensions: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Project annotations: every `metadata` key that starts with `x-`, kept as written (renderers ignore "
            "them). Any other unknown key under `metadata` is an error."
        ),
    )

    @model_validator(mode="before")
    @classmethod
    def _extensions(cls, value: Any) -> Any:
        value = move_extensions(value)
        if isinstance(value, dict) and isinstance(value.get("preguntas_abiertas"), str):
            value["preguntas_abiertas"] = [value["preguntas_abiertas"]]
        return value
