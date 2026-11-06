"""A registered model's contract and documents, as returned by `describe_model`."""

from __future__ import annotations

from pydantic import BaseModel, Field

from sldb.api.model_registry.model_document_summary import ModelDocumentSummary
from sldb.api.model_registry.model_field_summary import ModelFieldSummary


class ModelDescription(BaseModel):
    """Everything the store knows about one model; `model_dump()` equals the `models show` AST entry."""

    name: str = Field(description="Registered model name.")
    model_ref: str = Field(description="`module:ClassName` reference the model class is imported from.")
    path: str = Field(description="Model source file as recorded in the store index.")
    version: int = Field(description="Contract version; bumped each time a draft is promoted.")
    canonical: bool = Field(description="Whether the model is the canonical one of its family.")
    family: str | None = Field(description="Root branch of the model hierarchy the model declares, if any.")
    semantics: list[str] = Field(description="Semantic tags the model contributes to its documents.")
    base_models: list[str] = Field(description="StructuredNLDoc bases above the model, nearest first.")
    fields: list[ModelFieldSummary] = Field(description="The model's fields in declaration order.")
    documents: list[ModelDocumentSummary] = Field(description="Tracked documents of the model, sorted by name.")
    containment: dict[str, list[str]] = Field(default_factory=dict, description="Visual containment mapping field to allowed target models.")
    references: list[str] = Field(default_factory=list, description="Fields holding doc ids that are not containment.")
    compositions: dict[str, dict] = Field(default_factory=dict, description="Composition specifications for fields.")
    semantics_map: dict[str, list[str]] = Field(default_factory=dict, description="Declared __semantics__ mapping.")
    authority: str = Field(default="generated", description="The authority a document of this model has.")
    template: str = Field(default="", description="The model Markdown template.")
    has_draft: bool = Field(default=False, description="Whether a pending draft exists.")
    draft_path: str | None = Field(default=None, description="Path to the draft file if one exists.")
