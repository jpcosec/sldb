from __future__ import annotations
from typing import Any
from jinja2 import Environment
from sldb.core.segments.sentinel_decoder import decode_sentinels, strip_with_offsets
from sldb.core.ast import AST_Handler
from sldb.core.handlers.router import SharedNodeHandler
from sldb.core.renderer_engine.list import ListRenderer
from sldb.core.renderer_engine.payload_call import render_payload_of
from sldb.core.renderer_engine.table import TableRenderer
from sldb.core.renderer_engine.yaml import YamlRenderer
from sldb.models.structured_doc import StructuredNLDoc
from sldb.core.node import SLDBNode

class SLDBRenderer:
    """Renders a StructuredNLDoc back into Markdown using its template."""

    def __init__(self, recorder: Any = None):
        self.jinja_env = Environment(autoescape=False)
        self.ast_handler = AST_Handler()
        self.node_handler = SharedNodeHandler()
        self.recorder = recorder
        self.spans: list[tuple[int, int, int]] = []
        self.list_renderer = ListRenderer(self.jinja_env, recorder)
        self.table_renderer = TableRenderer(self.jinja_env, recorder)
        self.yaml_renderer = YamlRenderer(self.jinja_env, recorder)

    def render(self, model: StructuredNLDoc) -> str:
        """Renders the model to a Markdown string."""
        raw = self.render_raw(model)
        if self.recorder is None:
            return raw.strip()
        text, spans = decode_sentinels(raw)
        text, self.spans = strip_with_offsets(text, spans)
        return text

    def render_raw(self, model: StructuredNLDoc) -> str:
        """The joined blocks before stripping, sentinels included when recording.

        Args:
            model: The document instance to render.

        Returns:
            The rendered blocks joined by blank lines, not yet stripped.
        """
        template = model.__template__
        data = render_payload_of(model, self.recorder)
        blocks = self.ast_handler.split_nodes(template)
        return "\n\n".join(self._render_blocks(blocks, template.splitlines(), data))

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
