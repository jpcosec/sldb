from pydantic import BaseModel, Field


class StoreEntry(BaseModel):
    name: str
    path: str


class ModelEntry(BaseModel):
    name: str
    model_ref: str
    path: str
    models_index: str
    canonical: bool = False
    family: str | None = None
    semantics: list[str] = Field(default_factory=list)


class StoreIndex(BaseModel):
    stores: list[StoreEntry] = Field(default_factory=list)
    models: list[ModelEntry] = Field(default_factory=list)
    hash_a: str = ""


class ModelsIndex(BaseModel):
    name: str
    model_ref: str
    path: str
    documents_index: str
    hash_b: str = ""
    canonical: bool = False
    family: str | None = None
    semantics: list[str] = Field(default_factory=list)
    base_models: list[str] = Field(default_factory=list)


class DocumentEntry(BaseModel):
    name: str
    path: str
    hash_c: str = ""
    hash_d: str = ""
    semantic_tags: list[str] = Field(default_factory=list)


class DocumentsIndex(BaseModel):
    documents: list[DocumentEntry] = Field(default_factory=list)


class SemanticNode(BaseModel):
    id: str
    parents: list[str] = Field(default_factory=list)


class SemanticDAG(BaseModel):
    nodes: list[SemanticNode] = Field(default_factory=list)
    equivalences: dict[str, list[str]] = Field(default_factory=dict)


class SemanticDocumentRecord(BaseModel):
    model: str
    path: str
    tags: list[str] = Field(default_factory=list)


class SemanticIndex(BaseModel):
    tags: dict[str, list[str]] = Field(default_factory=dict)
    documents: dict[str, SemanticDocumentRecord] = Field(default_factory=dict)
