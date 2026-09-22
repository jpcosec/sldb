from __future__ import annotations
from typing import Any, cast, Literal
from sldb.core.ast import AST_Handler
from sldb.core.data_extractor import DataExtractor
from sldb.core.renderer import SLDBRenderer
from sldb.core.template_extractor import TemplateExtractor
from sldb.models.structured_doc import StructuredNLDoc

class Validator:
    def __init__(self, model_type: type[StructuredNLDoc]):
        self.model_type, self.ast_handler, self.template_extractor, self.data_extractor, self.renderer = model_type, AST_Handler(), TemplateExtractor(), DataExtractor(), SLDBRenderer()

    def _get_recipes(self) -> list[dict[str, Any]]:
        return self.template_extractor.extract_nodes(self.ast_handler.split_nodes(self.model_type.__template__))

    def extract(self, markdown: str) -> dict[str, Any]:
        return self.model_type(**self.data_extractor.extract_values(self.ast_handler.split_nodes(markdown), self._get_recipes(), raw_markdown=markdown)).model_dump(mode="json", exclude_none=True)

    def render(self, data: dict[str, Any]) -> str:
        return self.renderer.render(self.model_type(**data))

    def _get_input_data(self, markdown: str | None, data: dict[str, Any] | None) -> dict[str, Any]:
        if markdown is not None: return self.extract(markdown)
        if data is not None: return self.model_type(**data).model_dump(mode="json", exclude_none=True)
        raise ValueError("Either markdown or data must be provided for validation.")

    def _get_rev_fields(self) -> set[str]:
        recipes, rev_fields = self._get_recipes(), set()
        for r in recipes:
            markers = r.get("props_info", []) + ([r["marker"]] if "marker" in r else [])
            markers.extend(item["marker"] for item in r.get("markers", []))
            markers.extend(cm["marker"] for cm in r.get("col_markers", {}).values())
            for m in markers:
                if getattr(m, "is_reversible", False): rev_fields.add(m.name)
                elif isinstance(m, dict) and m.get("kind") == "rev": rev_fields.add(m.get("name"))
        return rev_fields

    def _check_render_validity(self, input_data: dict[str, Any], extracted: dict[str, Any]) -> bool:
        def _norm(val): return val.strip() if isinstance(val, str) else val
        return all(_norm(input_data.get(f)) == _norm(extracted.get(f)) for f in self._get_rev_fields())

    def validate(self, markdown: str | None = None, data: dict[str, Any] | None = None, mode: Literal["render_validity", "strict_roundtrip"] = "render_validity") -> tuple[bool, dict[str, Any]]:
        input_data = self._get_input_data(markdown, data)
        rendered, extracted = self.render(input_data), self.extract(self.render(input_data))
        is_valid = input_data == extracted if mode == "strict_roundtrip" else self._check_render_validity(input_data, extracted)
        details = {"mode": "input" if markdown is not None else "data", "validation_mode": mode, "model": f"{self.model_type.__module__}:{self.model_type.__name__}", "input_data": input_data, "rendered_markdown": rendered, "extracted_payload": extracted}
        return is_valid, details

def extract_model_data(m: type[StructuredNLDoc], md: str) -> dict[str, Any]: return Validator(m).extract(md)
def validate_model_input_roundtrip(m: type[StructuredNLDoc], md: str) -> tuple[bool, dict[str, Any]]: return Validator(m).validate(markdown=md)
def validate_model_data_roundtrip(m: type[StructuredNLDoc], d: dict[str, Any]) -> tuple[bool, dict[str, Any]]: return Validator(m).validate(data=d)
def render_model_markdown(m: type[StructuredNLDoc], d: dict[str, Any]) -> str: return Validator(m).render(d)

def extract_payload(template: str, markdown: str) -> dict[str, Any]:
    ast = AST_Handler()
    return DataExtractor().extract_values(ast.split_nodes(markdown), TemplateExtractor().extract_nodes(ast.split_nodes(template)), raw_markdown=markdown)

def render_markdown(template: str, data: dict[str, Any]) -> str:
    R = type("_R", (), {"__template__": template, "model_dump": lambda s, mode="json": data})
    return SLDBRenderer().render(cast(StructuredNLDoc, R()))
