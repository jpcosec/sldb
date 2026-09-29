from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class DocumentEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    path: str
    source_hash: str = Field(default='', validation_alias=AliasChoices('source_hash', 'hash_c'))
    content_hash: str = Field(default='', validation_alias=AliasChoices('content_hash', 'hash_d'))
    # `content_hash` per field: which fields moved, not just that some did. Empty on a store
    # written before this existed (and on a document whose Markdown no longer extracts, exactly
    # like `content_hash`) — absent is "unknown", never "no fields", so a consumer with nothing
    # to compare against falls back to the whole document.
    field_hashes: dict[str, str] = Field(default_factory=dict)
    semantic_tags: list[str] = Field(default_factory=list)

    @property
    def hash_c(self) -> str:
        return self.source_hash

    @hash_c.setter
    def hash_c(self, value: str) -> None:
        self.source_hash = value

    @property
    def hash_d(self) -> str:
        return self.content_hash

    @hash_d.setter
    def hash_d(self, value: str) -> None:
        self.content_hash = value
