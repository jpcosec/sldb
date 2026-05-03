from typing import Any

from sldb.core.ast import AST_Handler
from sldb.core.data_extractor import DataExtractor
from sldb.core.renderer import SLDBRenderer
from sldb.core.template_extractor import TemplateExtractor
from sldb.models.structured_doc import StructuredNLDoc


class _RenderModel:
    def __init__(self, template: str, data: dict[str, Any]):
        self.__template__ = template
        self._data = data

    def model_dump(self, mode: str = "json") -> dict[str, Any]:
        return self._data


def extract_payload(template: str, markdown: str) -> dict[str, Any]:
    ast = AST_Handler()
    recipes = TemplateExtractor().extract_nodes(ast.split_nodes(template))
    return DataExtractor().extract_values(ast.split_nodes(markdown), recipes)


def extract_model_data(
    model_type: type[StructuredNLDoc], markdown: str
) -> dict[str, Any]:
    payload = extract_payload(model_type.__template__, markdown)
    model = model_type(**payload)
    return model.model_dump(mode="json")


def render_markdown(template: str, data: dict[str, Any]) -> str:
    return SLDBRenderer().render(_RenderModel(template, data))


def render_model_markdown(
    model_type: type[StructuredNLDoc], data: dict[str, Any]
) -> str:
    model = model_type(**data)
    return SLDBRenderer().render(model)


def validate_input_roundtrip(
    template: str, markdown: str
) -> tuple[bool, dict[str, Any]]:
    first_payload = extract_payload(template, markdown)
    rendered_markdown = render_markdown(template, first_payload)
    second_payload = extract_payload(template, rendered_markdown)
    is_valid = first_payload == second_payload
    return is_valid, {
        "mode": "input",
        "first_payload": first_payload,
        "rendered_markdown": rendered_markdown,
        "second_payload": second_payload,
    }


def validate_data_roundtrip(
    template: str, data: dict[str, Any]
) -> tuple[bool, dict[str, Any]]:
    rendered_markdown = render_markdown(template, data)
    extracted_payload = extract_payload(template, rendered_markdown)
    is_valid = data == extracted_payload
    return is_valid, {
        "mode": "data",
        "input_data": data,
        "rendered_markdown": rendered_markdown,
        "extracted_payload": extracted_payload,
    }


def validate_model_input_roundtrip(
    model_type: type[StructuredNLDoc], markdown: str
) -> tuple[bool, dict[str, Any]]:
    first_payload = extract_model_data(model_type, markdown)
    rendered_markdown = render_model_markdown(model_type, first_payload)
    second_payload = extract_model_data(model_type, rendered_markdown)
    is_valid = first_payload == second_payload
    return is_valid, {
        "mode": "input",
        "model": f"{model_type.__module__}:{model_type.__name__}",
        "first_payload": first_payload,
        "rendered_markdown": rendered_markdown,
        "second_payload": second_payload,
    }


def validate_model_data_roundtrip(
    model_type: type[StructuredNLDoc], data: dict[str, Any]
) -> tuple[bool, dict[str, Any]]:
    normalized_input = model_type(**data).model_dump(mode="json")
    rendered_markdown = render_model_markdown(model_type, normalized_input)
    extracted_payload = extract_model_data(model_type, rendered_markdown)
    is_valid = normalized_input == extracted_payload
    return is_valid, {
        "mode": "data",
        "model": f"{model_type.__module__}:{model_type.__name__}",
        "input_data": normalized_input,
        "rendered_markdown": rendered_markdown,
        "extracted_payload": extracted_payload,
    }
