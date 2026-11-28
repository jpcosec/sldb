"""Text to payload and payload to text, from a template and nothing else: no model class.

`extract_payload(template, markdown)` and `render_markdown(template, data)` need only the
template and the text, so they live with the render axis (ring 0a). The functions that take a
model class stay in `sldb.runtime.validation`, which re-exports these two for its importers.
"""

from __future__ import annotations

from typing import Any

from sldb.core.ast import AST_Handler
from sldb.core.data_extractor import DataExtractor
from sldb.core.renderer import SLDBRenderer
from sldb.core.template_extractor import TemplateExtractor


def extract_payload(template: str, markdown: str) -> dict[str, Any]:
    ast = AST_Handler()
    return DataExtractor().extract_values(ast.split_nodes(markdown), TemplateExtractor().extract_nodes(ast.split_nodes(template)), raw_markdown=markdown)


def render_markdown(template: str, data: dict[str, Any]) -> str:
    R = type("_R", (), {"__template__": template, "model_dump": lambda s, mode="json": data})
    return SLDBRenderer().render(R())
