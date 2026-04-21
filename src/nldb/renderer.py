import re
from typing import Any, Dict, List
from jinja2 import Environment
from nldb.structuredNLDoc import StructuredNLDoc
from nldb.ast_handler import AST_Handler
from nldb.node_handler import SharedNodeHandler, parse_marker


class NLDBRenderer:
    """
    Renders a Pydantic model (StructuredNLDoc) back into Markdown
    using its __template__ and mapping data into markers.
    """

    def __init__(self):
        self.ast_handler = AST_Handler()
        self.node_handler = SharedNodeHandler()
        self.jinja_env = Environment(autoescape=False)

    def render(self, model: StructuredNLDoc) -> str:
        template = model.__template__
        data = model.model_dump(mode="json")
        blocks = self.ast_handler.split_nodes(template)
        template_lines = template.splitlines()

        output_parts = []

        for block in blocks:
            start_line, end_line = block.map
            block_lines = template_lines[start_line:end_line]
            block_text = "\n".join(block_lines)

            handler_key = self.node_handler.get_handler_for_node(block)

            if handler_key == "list":
                rendered = self._render_list_block(block, block_text, data)
                output_parts.append(rendered)
            elif handler_key == "table":
                rendered = self._render_table_block(block, block_text, data)
                output_parts.append(rendered)
            elif handler_key == "yaml":
                rendered = self._render_yaml_block(block, block_text, data)
                output_parts.append(rendered)
            else:
                rendered = self._replace_markers(block_text, data)
                output_parts.append(rendered)

        return "\n\n".join(output_parts).strip()

    def _render_yaml_block(self, node, block_text: str, data: Dict[str, Any]) -> str:
        is_front_matter = node.type == "front_matter"
        if is_front_matter:
            front_matter_body = re.sub(r"^---\n?", "", block_text.strip())
            front_matter_body = re.sub(r"\n?---$", "", front_matter_body)
            content = self._replace_markers(front_matter_body, data)
            return f"---\n{content}\n---"
        content = self._replace_markers(block_text, data)
        return content

    def _replace_markers(self, text: str, data: Dict[str, Any]) -> str:
        def sub_marker(match):
            marker = parse_marker(match.group(1))
            kind = marker["kind"]
            prop = marker["name"]
            traits = marker["traits"]

            if kind == "py":
                return self._render_python_expression(prop, data, match.group(0))

            val = data.get(prop)
            if val is None:
                if kind in {"optrev", "render"}:
                    return ""
                return match.group(0)

            if "dict" in traits or isinstance(val, (dict, list)):
                import yaml

                return yaml.dump(val, allow_unicode=True, sort_keys=False).strip()

            return str(val)

        rendered = re.sub(r"⸢([^⸥]+)⸥", sub_marker, text)
        return self.jinja_env.from_string(rendered).render(**data)

    def _render_python_expression(
        self, expression: str, data: Dict[str, Any], fallback: str
    ) -> str:
        safe_builtins = {
            "str": str,
            "int": int,
            "float": float,
            "len": len,
            "min": min,
            "max": max,
            "sum": sum,
            "sorted": sorted,
            "list": list,
            "dict": dict,
            "set": set,
            "tuple": tuple,
            "enumerate": enumerate,
        }
        try:
            value = eval(expression, {"__builtins__": safe_builtins}, dict(data))
        except Exception:
            return fallback
        return "" if value is None else str(value)

    def _render_list_block(self, node, block_text: str, data: Dict[str, Any]) -> str:
        if not node.children:
            return self._replace_markers(block_text, data)

        first_item = node.children[0]
        item_text = self._get_node_source(first_item, block_text, node.map[0])

        match = re.search(r"⸢([^⸥]+)⸥", item_text)
        if not match:
            return self._replace_markers(block_text, data)

        inner = match.group(1)
        root_prop = inner.split("•", 1)[-1].strip() if "•" in inner else inner.strip()

        list_items_data = data.get(root_prop, [])
        if not isinstance(list_items_data, list):
            return ""

        rendered_items = []
        for item_data in list_items_data:
            if isinstance(item_data, dict):
                rendered_items.append(self._replace_markers(item_text, item_data))
            else:
                rendered_items.append(
                    self._replace_markers(item_text, {root_prop: item_data})
                )

        return "\n".join(rendered_items)

    def _render_table_block(self, node, block_text: str, data: Dict[str, Any]) -> str:
        lines = block_text.splitlines()
        if len(lines) < 3:
            return self._replace_markers(block_text, data)

        header = lines[0]
        separator = lines[1]
        row_template = lines[2]

        match = re.search(r"⸢([^⸥]+)⸥", row_template)
        if not match:
            return self._replace_markers(block_text, data)

        inner = match.group(1)
        root_prop = inner.split("•", 1)[-1].strip() if "•" in inner else inner.strip()

        rows_data = data.get(root_prop, {})
        items_to_render = []
        if isinstance(rows_data, dict):
            sorted_keys = sorted(
                rows_data.keys(), key=lambda x: int(x) if str(x).isdigit() else x
            )
            items_to_render = [rows_data[k] for k in sorted_keys]
        elif isinstance(rows_data, list):
            items_to_render = rows_data

        rendered_rows = []
        for item in items_to_render:
            item_data = item.model_dump() if hasattr(item, "model_dump") else item
            rendered_rows.append(self._replace_markers(row_template, item_data))

        if rendered_rows:
            return "\n".join([header, separator] + rendered_rows)

        return self._replace_markers(block_text, data)

    def _get_node_source(self, node, block_text: str, block_start_line: int) -> str:
        lines = block_text.splitlines()
        start = node.map[0] - block_start_line
        end = node.map[1] - block_start_line
        return "\n".join(lines[start:end])
