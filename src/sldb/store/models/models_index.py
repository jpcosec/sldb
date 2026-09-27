from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class ModelsIndex(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    model_ref: str
    path: str
    documents_index: str
    sections_index: str = ''
    # The model node and its two children: `model_hash` is hash_model_layer(roster, contract).
    model_hash: str = Field(default='', validation_alias=AliasChoices('model_hash', 'hash_b'))
    roster_hash: str = ''    # signs the document list: (name, source_hash, content_hash)
    contract_hash: str = ''  # signs the model's field schema and its __template__
    documents_count: int = 0  # PLAN 15 capa 7: a cheap summary of the sharded documents index
    version: int = 1
    canonical: bool = False
    family: str | None = None
    semantics: list[str] = Field(default_factory=list)
    base_models: list[str] = Field(default_factory=list)

    @property
    def hash_b(self) -> str:
        return self.model_hash

    @hash_b.setter
    def hash_b(self, value: str) -> None:
        self.model_hash = value
