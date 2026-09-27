from pydantic import AliasChoices, BaseModel, ConfigDict, Field
from sldb.store.models.model_entry import ModelEntry
from sldb.store.models.store_entry import StoreEntry
from sldb.store.models.predicate_entry import PredicateEntry


class StoreIndex(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    stores: list[StoreEntry] = Field(default_factory=list)
    models: list[ModelEntry] = Field(default_factory=list)
    predicates: list[PredicateEntry] = Field(default_factory=list)
    store_hash: str = Field(default='', validation_alias=AliasChoices('store_hash', 'hash_a'))

    @property
    def hash_a(self) -> str:
        return self.store_hash

    @hash_a.setter
    def hash_a(self, value: str) -> None:
        self.store_hash = value
