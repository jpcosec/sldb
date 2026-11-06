"""One parameter of a composed `ViewDoc` (GD25): what `{name}` in a section's `select` reads."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class ViewParam(BaseModel):
    """A named value the caller gives when the view runs (`--param name=value`, `?name=value`);
    always a string. `required` makes its absence an error; `default` fills it when absent."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(description="Identifier the sections reference as `{name}`.")
    required: bool = Field(default=False, description="Whether running the view without it is an error.")
    default: str | None = Field(default=None, description="The value used when the caller gives none.")

    @field_validator("name")
    @classmethod
    def _identifier(cls, value: str) -> str:
        if not value.isidentifier():
            raise ValueError(f"param name {value!r} must be an identifier")
        return value

    @model_validator(mode="after")
    def _required_has_no_default(self) -> "ViewParam":
        if self.required and self.default is not None:
            raise ValueError(f"param {self.name!r} cannot be required and have a default")
        return self
