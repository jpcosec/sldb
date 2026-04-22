from pydantic import BaseModel, Field


class StoreEntry(BaseModel):
    name: str
    path: str


class ModelEntry(BaseModel):
    name: str
    model_ref: str
    path: str
    models_index: str


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


class DocumentEntry(BaseModel):
    name: str
    path: str
    hash_c: str = ""
    hash_d: str = ""


class DocumentsIndex(BaseModel):
    documents: list[DocumentEntry] = Field(default_factory=list)
