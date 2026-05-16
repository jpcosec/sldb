from __future__ import annotations

from jinja2 import Environment

from sldb.core.ast import AST_Handler
from sldb.core.handlers.router import SharedNodeHandler
from sldb.core.renderer_engine.list import ListRenderer
from sldb.core.renderer_engine.table import TableRenderer
from sldb.core.renderer_engine.yaml import YamlRenderer
from sldb.models.structured_doc import StructuredNLDoc


class SLDBRenderer:
    """
    Renders a StructuredNLDoc back into Markdown using its template.
    """

    def __init__(self):
        self.jinja_env = Environment(autoescape=False)
        self.ast_handler = AST_Handler()
        self.node_handler = SharedNodeHandler()
        self.list_renderer = ListRenderer(self.jinja_env)
        self.table_renderer = TableRenderer(self.jinja_env)
        self.yaml_renderer = YamlRenderer(self.jinja_env)

    def render(self, model: StructuredNLDoc) -> str:
        """Renders the model to a Markdown string."""
        template = model.__template__
        data = model.model_dump(mode="json")
        blocks = self.ast_handler.split_nodes(template)
        template_lines = template.splitlines()

        output_parts = []
        for block in blocks:
            if not block.map:
                continue
            start_line, end_line = block.map
            block_text = "\n".join(template_lines[start_line:end_line])

            handler_key = self.node_handler.get_handler_for_node(block)

            if handler_key in ("list", "bullet_list", "ordered_list"):
                rendered = self.list_renderer.render(block, block_text, data, start_line)
            elif handler_key in ("table", "table_cell"):
                rendered = self.table_renderer.render(block, block_text, data)
            elif handler_key in ("yaml", "fence", "front_matter"):
                rendered = self.yaml_renderer.render(block, block_text, data)
            else:
                rendered = self.yaml_renderer.replace_markers(block_text, data)

            output_parts.append(rendered)

        return "\n\n".join(output_parts).strip()
