from typing import Any, Dict, Tuple, Type

from sldb import AST_Handler, DataExtractor, TemplateExtractor
from sldb.renderer import SLDBRenderer
from sldb.structuredNLDoc import StructuredNLDoc


class _RenderModel:
    def __init__(self, template: str, data: Dict[str, Any]):
        self.__template__ = template
        self._data = data

    def model_dump(self, mode: str = "json") -> Dict[str, Any]:
        return self._data


def extract_payload(template: str, markdown: str) -> Dict[str, Any]:
    ast = AST_Handler()
    recipes = TemplateExtractor().extract_nodes(ast.split_nodes(template))
    return DataExtractor().extract_values(ast.split_nodes(markdown), recipes)


def extract_model_data(
    model_type: Type[StructuredNLDoc], markdown: str
) -> Dict[str, Any]:
    payload = extract_payload(model_type.__template__, markdown)
    model = model_type(**payload)
    return model.model_dump(mode="json")


def render_markdown(template: str, data: Dict[str, Any]) -> str:
    return SLDBRenderer().render(_RenderModel(template, data))


def render_model_markdown(
    model_type: Type[StructuredNLDoc], data: Dict[str, Any]
) -> str:
    model = model_type(**data)
    return SLDBRenderer().render(model)


def validate_input_roundtrip(
    template: str, markdown: str
) -> Tuple[bool, Dict[str, Any]]:
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
    template: str, data: Dict[str, Any]
) -> Tuple[bool, Dict[str, Any]]:
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
    model_type: Type[StructuredNLDoc], markdown: str
) -> Tuple[bool, Dict[str, Any]]:
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
    model_type: Type[StructuredNLDoc], data: Dict[str, Any]
) -> Tuple[bool, Dict[str, Any]]:
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
