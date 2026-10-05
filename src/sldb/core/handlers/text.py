from __future__ import annotations
import re
from typing import Any
from sldb.core.handlers.base import BaseNodeHandler
from sldb.core.handlers.utils import parse_marker
from sldb.core.node import SLDBNode

MARKER_PATTERN = r"⸢([^⸥]+)⸥"
INLINE_RENDER_PATTERN = r"{{\s*.*?\s*}}"

def build_text_pattern(content: str) -> dict[str, Any]:
    props, regex, cursor, dynamic = [], [], 0, False
    for m in re.finditer(f"{MARKER_PATTERN}|{INLINE_RENDER_PATTERN}", content):
        regex.append(re.escape(content[cursor : m.start()]))
        dynamic = _process_token(m.group(0), m, regex, props) or dynamic
        cursor = m.end()
    regex.append(re.escape(content[cursor:]))
    return {"props_info": props, "regex": f"^{''.join(regex)}$", "dynamic_found": dynamic}

def _process_token(token: str, match: re.Match, regex_parts: list[str], props_info: list[Any]) -> bool:
    if token.startswith("{{"):
        regex_parts.append(".*?")
        return True
    marker = parse_marker(match.group(1))
    if marker.is_reversible or marker.is_optional:
        regex_parts.append("(.*?)")
        props_info.append(marker)
        return True
    regex_parts.append(".*?")
    return True

class TextNodeHandler(BaseNodeHandler):
    def compile_recipe(self, node: SLDBNode) -> list[dict[str, Any]]:
        content = self.get_text(node).strip()
        if not content or ("⸢" not in content and "{{" not in content):
            return []
        pd = build_text_pattern(content)
        if not pd["dynamic_found"]:
            return []
        if (tbl := self._try_build_table_recipe(content, pd)):
            return tbl
        return [self._build_text_recipe(content, pd)]

    def _try_build_table_recipe(self, content: str, pattern_data: dict[str, Any]) -> list[dict[str, Any]] | None:
        if len(pattern_data["props_info"]) == 1 and content.startswith("⸢") and content.endswith("⸥"):
            marker = pattern_data["props_info"][0]
            if (table_columns := self._table_columns(marker)) is not None:
                return [{"name": marker.name, "marker": marker, "table_columns": table_columns, "props": [marker.name], "handler": "table", "match_outer_type": "table", "match_outer_tag": "table"}]
        return None

    def _build_text_recipe(self, content: str, pd: dict[str, Any]) -> dict[str, Any]:
        props = pd["props_info"]
        recipe = {"props": [m.name for m in props], "props_info": props, "regex": pd["regex"], "handler": "text"}
        if props and all(m.is_optional for m in props):
            recipe["all_optional"] = True
        if self._is_optional_block(content, pd):
            recipe["optional_block"] = True
        if not props:
            recipe["anchor"] = True
        return recipe

    def _is_optional_block(self, content: str, pattern_data: dict[str, Any]) -> bool:
        props = pattern_data["props_info"]
        return len(props) == 1 and props[0].is_optional and content.startswith("⸢") and content.endswith("⸥")

    def _table_columns(self, marker: Any) -> list[str] | None:
        for trait in marker.traits:
            if trait == "table":
                return []
            if trait.startswith("table[") and trait.endswith("]"):
                return [col.strip() for col in trait[6:-1].split(",") if col.strip()]
        return None

    def match_text(self, text: str, recipe: dict[str, Any]) -> re.Match[str] | None:
        """The single executor of the recipe regex, deliberately WITHOUT `re.S`.

        This path is only for inline markers, which are single-line; a lone
        marker never reaches it because it captures by block range instead.
        `re.S` is absent on purpose: with DOTALL a lone `^(.*?)$` would swallow
        the next section, which is worse than losing a field.
        """
        return re.fullmatch(recipe["regex"], text.strip())

    def matches(self, text: str, recipe: dict[str, Any]) -> bool:
        return self.match_text(text, recipe) is not None

    def extract_data(self, node: SLDBNode, recipe: dict[str, Any]) -> Any:
        match = self.match_text(self.get_text(node), recipe)
        if not match:
            return None
        return {recipe["props_info"][idx].name: val for idx, val in enumerate(match.groups())}
