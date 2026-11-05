"""The kind a declared path that resolves to no node would have."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class MissingTargetKind(BaseModel):
    """A path-parts prefix (and optional ending) naming the kind of a dangling path target."""

    model_config = ConfigDict(frozen=True)

    parts: tuple[str, ...] = Field(description="Leading path parts of the target; the first rule matching wins.")
    one_of_first: tuple[str, ...] = Field(default=(), description="Alternatives for the first part, when `parts` is empty.")
    ending: str = Field(default="", description="Required path ending ('' for any).")
    kind: str = Field(description="Kind the missing target id gets: `kind:path`.")

    def matches(self, parts: tuple[str, ...], path: str) -> bool:
        """Whether a target path (as parts and as text) falls under this rule."""
        if self.parts and parts[: len(self.parts)] != self.parts:
            return False
        if self.one_of_first and (not parts or parts[0] not in self.one_of_first):
            return False
        return path.endswith(self.ending)
