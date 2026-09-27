from pydantic import BaseModel, Field

from sldb.store.models.document_hashes import DocumentHashes


class StoreFingerprint(BaseModel):
    store_hash: str
    models: dict[str, str] = Field(default_factory=dict)
    documents: dict[str, DocumentHashes] = Field(default_factory=dict)
