from pydantic import BaseModel, Field


class SemanticDocumentRecord(BaseModel):
    model: str
    path: str
    tags: list[str] = Field(default_factory=list)
    hash_c: str = ""  # the document's hash_c this record was extracted from (PLAN 15 capa 5:
    # this is also the per-document shard's own shape, .sldb/runtime/semantic/<Model>/<doc>.yaml)
