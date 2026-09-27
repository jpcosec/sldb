from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class DocumentEntry(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    path: str
    source_hash: str = Field(default='', validation_alias=AliasChoices('source_hash', 'hash_c'))
    content_hash: str = Field(default='', validation_alias=AliasChoices('content_hash', 'hash_d'))
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
