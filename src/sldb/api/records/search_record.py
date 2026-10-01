from __future__ import annotations
from dataclasses import dataclass
from typing import Any

@dataclass
class SearchRecord:
    kind: str
    store_name: str
    name: str
    physical: list[str]
    semantic: list[str]
    payload: dict[str, Any]
    value: Any = None
    model_name: str | None = None
    doc_name: str | None = None
    field_path: str | None = None
    path: str | None = None
    title: str | None = None
    about: list[str] | None = None
    owning_section: str | None = None
    model_type: Any = None

    def as_dict(self) -> dict[str, Any]:
        d = {"kind": self.kind, "store": self.store_name, "name": self.name, "model": self.model_name, "doc": self.doc_name, "field": self.field_path, "path": self.path, "title": self.title, "value": self.value, "semantic": self.semantic, "about": self.about or []}
        if self.kind == "section": d["breadcrumbs"] = self.payload.get("breadcrumbs", [])
        if self.kind == "field": d["owning_section"] = self.owning_section
        return d
