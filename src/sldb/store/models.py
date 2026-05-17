from pydantic import BaseModel, Field


class StoreEntry(BaseModel):
    name: str
    path: str


class ModelEntry(BaseModel):
    name: str
    model_ref: str
    path: str
    models_index: str
    version: int = 1
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
    sections_index: str = ""
    hash_b: str = ""
    version: int = 1
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


class SectionContextRecord(BaseModel):
    path: str
    title: str
    breadcrumbs: list[str] = Field(default_factory=list)
    about: list[str] = Field(default_factory=list)
    semantic_tags: list[str] = Field(default_factory=list)
    slug: str = ""
    level: int = 0
    line_start: int | None = None
    line_end: int | None = None


class DocSections(BaseModel):
    doc_name: str
    sections: list[SectionContextRecord] = Field(default_factory=list)


class SectionsIndex(BaseModel):
    documents: list[DocSections] = Field(default_factory=list)


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
