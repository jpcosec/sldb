from pydantic import BaseModel, Field
from sldb.store.models.section_context_record import SectionContextRecord


class DocSections(BaseModel):
    doc_name: str
    sections: list[SectionContextRecord] = Field(default_factory=list)
    source_hash: str = ""  # the document's source_hash this was parsed from (PLAN 15 capa 5: also the
    # per-document shard's own shape, .sldb/runtime/sections/<Model>/<doc>.yaml)
    sections_version: str = ""  # section_paths.SECTION_INDEX_VERSION it was parsed under; a new
    # identity rule (unique slugs, spans) re-parses the shard even when source_hash is unchanged
