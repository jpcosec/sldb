from __future__ import annotations
from importlib import import_module
from pathlib import Path
from typing import Any, TypeVar
from pydantic import BaseModel

class StructuredNLDoc(BaseModel):
    # Every tracked record is rendered as Markdown, but its subject can come from another
    # adapter. Subclasses override source when they describe code, data, or another
    # non-Markdown source format. Store semantic indexes expose both dimensions.
    __semantics__: dict[str, Any] = {
        "representation": ["markdown"],
        "source": ["document", "markdown"],
    }
    __template__: str = ""
    __compositions__: dict[str, dict[str, Any]] = {}
    # Declarative graph metadata: which fields hold document ids.
    # __containment__ maps field -> allowed target models (visual containment).
    # __references__ lists fields holding doc ids that are not containment.
    __containment__: dict[str, list[str]] = {}
    __references__: list[str] = []

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        super().__pydantic_init_subclass__(**kwargs)
        if cls is StructuredNLDoc: return
        missing_descriptions = sorted(name for name, info in cls.model_fields.items() if not info.description or not info.description.strip())
        if missing_descriptions: raise TypeError(f"{cls.__name__} fields must define a non-empty description: {', '.join(missing_descriptions)}")

    def render_payload(self) -> dict[str, Any]:
        payload = self.model_dump(mode="json")
        for name in self.__compositions__: payload[name] = self.compose_field(name)
        return payload

    def compose_field(self, name: str) -> str:
        spec = self.__compositions__.get(name, {})
        refs, model_type = getattr(self, spec.get("source_field") or "", []) or [], self._resolve_composition_model(spec.get("model"))
        if not spec.get("source_field") or not isinstance(refs, list) or model_type is None: return ""
        def _render(raw_ref):
            if not (path := Path(str(raw_ref).strip().strip("`"))).exists(): return ""
            try: return spec.get("template", "- {title}").format(**p) if (p := self._extract_composed_payload(model_type, path)) else ""
            except Exception: return ""
        return spec.get("separator", "\n").join(filter(None, map(_render, refs)))

    def _resolve_composition_model(self, value: Any):
        if value is None or isinstance(value, type): return value
        if isinstance(value, str) and ":" in value:
            obj: Any = import_module(value.split(":", 1)[0])
            for attr in value.split(":", 1)[1].split("."): obj = getattr(obj, attr)
            return obj
        return None

    def _extract_composed_payload(self, model_type: type[StructuredNLDoc], path: Path) -> dict[str, Any]:
        from sldb.runtime.validation import extract_model_data
        return extract_model_data(model_type, path.read_text(encoding="utf-8"))

M = TypeVar("M", bound="StructuredNLDoc")
