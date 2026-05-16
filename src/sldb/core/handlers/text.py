from __future__ import annotations

import re
from typing import Any

from sldb.core.handlers.base import BaseNodeHandler
from sldb.core.handlers.utils import parse_marker
from sldb.core.node import SLDBNode

MARKER_PATTERN = r"⸢([^⸥]+)⸥"
INLINE_RENDER_PATTERN = r"{{\s*.*?\s*}}"


def build_text_pattern(content: str) -> dict[str, Any]:
    """
    Builds a regex pattern and metadata for text extraction.
    """
    props_info = []
    regex_parts = []
    cursor = 0
    dynamic_found = False

    token_pattern = re.compile(f"{MARKER_PATTERN}|{INLINE_RENDER_PATTERN}")
    for match in token_pattern.finditer(content):
        regex_parts.append(re.escape(content[cursor : match.start()]))
        token = match.group(0)

        if token.startswith("{{"):
            regex_parts.append(".*?")
            dynamic_found = True
        else:
            marker = parse_marker(match.group(1))
            if marker.is_reversible or marker.is_optional:
                regex_parts.append("(.*?)")
                props_info.append(marker)
                dynamic_found = True
                dynamic_found = True
            else:
                regex_parts.append(".*?")
                dynamic_found = True

        cursor = match.end()

    regex_parts.append(re.escape(content[cursor:]))
    return {
        "props_info": props_info,
        "regex": f"^{''.join(regex_parts)}$",
        "dynamic_found": dynamic_found,
    }


class TextNodeHandler(BaseNodeHandler):
    """
    Handler for extracting data from plain text nodes.
    """

    def compile_recipe(self, node: SLDBNode) -> list[dict[str, Any]]:
        content = self.get_text(node).strip()
        if not content or ("⸢" not in content and "{{" not in content):
            return []

        pattern_data = build_text_pattern(content)
        if not pattern_data["dynamic_found"]:
            return []

        recipe = {
            "props": [m.name for m in pattern_data["props_info"]],
            "props_info": pattern_data["props_info"],
            "regex": pattern_data["regex"],
            "handler": "text",
        }
        if not pattern_data["props_info"]:
            recipe["anchor"] = True

        return [recipe]

    def extract_data(self, node: SLDBNode, recipe: dict[str, Any]) -> Any:
        content = self.get_text(node).strip()
        match = re.fullmatch(recipe["regex"], content)
        if not match:
            return None

        results = {}
        for idx, val in enumerate(match.groups()):
            marker = recipe["props_info"][idx]
            results[marker.name] = val

        return results
