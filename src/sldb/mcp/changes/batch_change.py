"""One change in the form `apply_batch` takes."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class BatchChange(BaseModel):
    """One change in the form `sldb.api.apply_batch` takes, plus the model it touches."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(description="The document name.")
    action: Literal["create", "update", "delete"]
    model: str
    payload: dict[str, Any] | None = None
    path: str | None = None
    expected_source_hash: str | None = Field(default=None, description="The document's source hash when the change was proposed (filled by the server).")

    def batch_form(self) -> dict[str, Any]:
        """The dict `apply_batch` reads (it names the model only on create)."""
        form: dict[str, Any] = {"id": self.id, "action": self.action}
        optional = {"model": self.model if self.action == "create" else None, "payload": self.payload, "path": self.path, "expected_source_hash": self.expected_source_hash}
        return {**form, **{key: value for key, value in optional.items() if value is not None}}
