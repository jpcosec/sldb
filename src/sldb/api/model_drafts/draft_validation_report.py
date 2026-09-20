"""Outcome of validating (and possibly promoting) a model draft."""

from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel, Field

from sldb.api.model_drafts.draft_document_check import DraftDocumentCheck


class DraftValidationReport(BaseModel):
    """What was validated, against which documents, and whether it was installed.

    A draft that fails validation raises instead of producing a report, so `valid` is
    always True; it is kept so the report reads like `sldb models validate --format json`.
    """

    valid: bool = Field(default=True, description="Always True: an invalid contract raises instead of reporting.")
    model: str = Field(description="Registered model name validated.")
    draft: bool = Field(description="True when a draft existed and was the contract validated; False when the active model was.")
    path: Path = Field(description="The source file that was validated (the draft or the active model).")
    documents: list[DraftDocumentCheck] = Field(description="Every tracked document of the model, checked under the contract.")
    backfill: list[str] = Field(default_factory=list, description="Tracked documents a backfill promote would rewrite (their re-render differs).")
    promoted: bool = Field(description="True when the draft was installed over the active model and the model reindexed.")
    version: int = Field(description="The model's contract version after the operation.")
