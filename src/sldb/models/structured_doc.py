from __future__ import annotations

from importlib import import_module
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel


class StructuredNLDoc(BaseModel):
    __template__: str = ""
    __compositions__: dict[str, dict[str, Any]] = {}

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        super().__pydantic_init_subclass__(**kwargs)
        if cls is StructuredNLDoc:
            return

        missing_descriptions = sorted(
            field_name
            for field_name, field_info in cls.model_fields.items()
            if not field_info.description or not field_info.description.strip()
        )
        if missing_descriptions:
            formatted_fields = ", ".join(missing_descriptions)
            raise TypeError(
                f"{cls.__name__} fields must define a non-empty description: {formatted_fields}"
            )

    def render_payload(self) -> dict[str, Any]:
        payload = self.model_dump(mode="json")
        for name in self.__compositions__:
            payload[name] = self.compose_field(name)
        return payload

    def compose_field(self, name: str) -> str:
        spec = self.__compositions__.get(name, {})
        source_field = spec.get("source_field")
        if not source_field:
            return ""
        refs = getattr(self, source_field, []) or []
        if not isinstance(refs, list):
            return ""

        model_type = self._resolve_composition_model(spec.get("model"))
        line_template = spec.get("template", "- {title}")
        separator = spec.get("separator", "\n")
        rendered: list[str] = []
        for raw_ref in refs:
            ref = str(raw_ref).strip().strip("`")
            path = Path(ref)
            if not path.exists() or model_type is None:
                continue
            payload = self._extract_composed_payload(model_type, path)
            if not payload:
                continue
            rendered.append(line_template.format(**payload))
        return separator.join(rendered)

    def _resolve_composition_model(self, value: Any):
        if value is None:
            return None
        if isinstance(value, type):
            return value
        if isinstance(value, str) and ":" in value:
            module_name, attr_path = value.split(":", 1)
            obj: Any = import_module(module_name)
            for attr in attr_path.split("."):
                obj = getattr(obj, attr)
            return obj
        return None

    def _extract_composed_payload(
        self, model_type: type[StructuredNLDoc], path: Path
    ) -> dict[str, Any]:
        from sldb.runtime.validation import extract_model_data

        return extract_model_data(model_type, path.read_text(encoding="utf-8"))


M = TypeVar("M", bound="StructuredNLDoc")
