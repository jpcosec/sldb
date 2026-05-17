from __future__ import annotations

from typing import Any, cast, Literal

from sldb.core.ast import AST_Handler
from sldb.core.data_extractor import DataExtractor
from sldb.core.renderer import SLDBRenderer
from sldb.core.template_extractor import TemplateExtractor
from sldb.models.structured_doc import StructuredNLDoc


class Validator:
    """
    Handles validation of SLDB documents and data.
    """

    def __init__(self, model_type: type[StructuredNLDoc]):
        self.model_type = model_type
        self.ast_handler = AST_Handler()
        self.template_extractor = TemplateExtractor()
        self.data_extractor = DataExtractor()
        self.renderer = SLDBRenderer()

    def _get_recipes(self) -> list[dict[str, Any]]:
        return self.template_extractor.extract_nodes(
            self.ast_handler.split_nodes(self.model_type.__template__)
        )

    def extract(self, markdown: str) -> dict[str, Any]:
        """Extracts and validates data from markdown."""
        payload = self.data_extractor.extract_values(
            self.ast_handler.split_nodes(markdown),
            self._get_recipes(),
            raw_markdown=markdown,
        )
        # Normalize through Pydantic
        return self.model_type(**payload).model_dump(mode="json")

    def render(self, data: dict[str, Any]) -> str:
        """Renders data to markdown."""
        model = self.model_type(**data)
        return self.renderer.render(model)

    def validate(
        self,
        markdown: str | None = None,
        data: dict[str, Any] | None = None,
        mode: Literal["render_validity", "strict_roundtrip"] = "render_validity",
    ) -> tuple[bool, dict[str, Any]]:
        """
        Performs validation in the specified mode.
        """
        if markdown is not None:
            input_data = self.extract(markdown)
        elif data is not None:
            input_data = self.model_type(**data).model_dump(mode="json")
        else:
            raise ValueError("Either markdown or data must be provided for validation.")

        rendered = self.render(input_data)
        extracted = self.extract(rendered)

        if mode == "strict_roundtrip":
            is_valid = input_data == extracted
        else:
            # Render validity: only fields with 'rev' markers must match
            recipes = self._get_recipes()
            rev_fields = set()
            for r in recipes:
                # Text recipes have props_info (list of Marker)
                # List, Yaml recipes have a 'marker' key
                # Table recipes have 'col_markers' (dict of {idx: {'marker': Marker}})
                markers = r.get("props_info", [])
                if "marker" in r:
                    markers.append(r["marker"])
                if "col_markers" in r:
                    for cm in r["col_markers"].values():
                        markers.append(cm["marker"])

                for m in markers:
                    if hasattr(m, "is_reversible") and m.is_reversible:
                        rev_fields.add(m.name)
                    elif isinstance(m, dict) and m.get("kind") == "rev":
                        rev_fields.add(m.get("name"))

            is_valid = all(input_data.get(f) == extracted.get(f) for f in rev_fields)

        details = {
            "mode": "input" if markdown is not None else "data",
            "validation_mode": mode,
            "model": f"{self.model_type.__module__}:{self.model_type.__name__}",
            "input_data": input_data,
            "rendered_markdown": rendered,
            "extracted_payload": extracted,
        }

        return is_valid, details


def extract_model_data(
    model_type: type[StructuredNLDoc], markdown: str
) -> dict[str, Any]:
    """Utility to extract model data."""
    return Validator(model_type).extract(markdown)


def validate_model_input_roundtrip(
    model_type: type[StructuredNLDoc], markdown: str
) -> tuple[bool, dict[str, Any]]:
    """Public API for input roundtrip validation."""
    return Validator(model_type).validate(markdown=markdown)


def validate_model_data_roundtrip(
    model_type: type[StructuredNLDoc], data: dict[str, Any]
) -> tuple[bool, dict[str, Any]]:
    """Public API for data roundtrip validation."""
    return Validator(model_type).validate(data=data)


def extract_payload(template: str, markdown: str) -> dict[str, Any]:
    """Backward compatible extractor."""
    from sldb.core.ast import AST_Handler
    from sldb.core.data_extractor import DataExtractor
    from sldb.core.template_extractor import TemplateExtractor

    ast = AST_Handler()
    recipes = TemplateExtractor().extract_nodes(ast.split_nodes(template))
    return DataExtractor().extract_values(
        ast.split_nodes(markdown), recipes, raw_markdown=markdown
    )


def render_markdown(template: str, data: dict[str, Any]) -> str:
    """Backward compatible renderer."""
    from sldb.core.renderer import SLDBRenderer
    from sldb.models.structured_doc import StructuredNLDoc

    class _RenderModel:
        def __init__(self, template: str, data: dict[str, Any]):
            self.__template__ = template
            self._data = data

        def model_dump(self, mode: str = "json") -> dict[str, Any]:
            return self._data

    return SLDBRenderer().render(cast(StructuredNLDoc, _RenderModel(template, data)))


def render_model_markdown(
    model_type: type[StructuredNLDoc], data: dict[str, Any]
) -> str:
    """Backward compatible model renderer."""
    return Validator(model_type).render(data)
