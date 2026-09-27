from pydantic import BaseModel


class DocumentHashes(BaseModel):
    source_hash: str
    content_hash: str
