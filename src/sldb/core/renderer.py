from __future__ import annotations
from pathlib import Path
from jinja2 import Environment
from sldb.core.ast import AST_Handler
from sldb.core.handlers.router import SharedNodeHandler
from sldb.core.renderer_engine.list import ListRenderer
from sldb.core.renderer_engine.table import TableRenderer
from sldb.core.renderer_engine.yaml import YamlRenderer
from sldb.models.structured_doc import StructuredNLDoc
from sldb.core.node import SLDBNode

class SLDBRenderer:
    """Renders a StructuredNLDoc back into Markdown using its template."""

    def __init__(self):
        self.jinja_env = Environment(autoescape=False)
        self.ast_handler = AST_Handler()
        self.node_handler = SharedNodeHandler()
        self.list_renderer = ListRenderer(self.jinja_env)
        self.table_renderer = TableRenderer(self.jinja_env)
        self.yaml_renderer = YamlRenderer(self.jinja_env)

    def render(self, model: StructuredNLDoc, ref_root: Path | None = None) -> str:
        """Renders the model to a Markdown string. `ref_root` resolves composition refs."""
        template = model.__template__
        data = model.render_payload(ref_root)
        blocks = self.ast_handler.split_nodes(template)
        template_lines = template.splitlines()

        output_parts = self._render_blocks(blocks, template_lines, data)
        return "\n\n".join(output_parts).strip()

    def _render_blocks(self, blocks: list[SLDBNode], template_lines: list[str], data: dict) -> list[str]:
        output_parts = []
        for block in blocks:
            if not block.map:
                continue
            rendered = self._render_block(block, template_lines, data)
            output_parts.append(rendered)
        return output_parts

    def _render_block(self, block: SLDBNode, template_lines: list[str], data: dict) -> str:
        start_line, end_line = block.map
        block_text = "\n".join(template_lines[start_line:end_line])
        handler_key = self.node_handler.get_handler_for_node(block)
        return self._dispatch_render(handler_key, block, block_text, data, start_line)

    def _dispatch_render(self, handler_key: str, block: SLDBNode, block_text: str, data: dict, start_line: int) -> str:
        if handler_key in ("list", "bullet_list", "ordered_list"):
            return self.list_renderer.render(block, block_text, data, start_line)
        if handler_key in ("table", "table_cell"):
            return self.table_renderer.render(block, block_text, data)
        if handler_key in ("yaml", "fence", "front_matter"):
            return self.yaml_renderer.render(block, block_text, data)
        return self.yaml_renderer.replace_markers(block_text, data)
