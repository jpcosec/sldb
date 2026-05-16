from __future__ import annotations

import re
from typing import Any

import yaml

from sldb.core.exceptions import SLDBASTError
from sldb.core.handlers.base import BaseNodeHandler
from sldb.core.handlers.utils import parse_marker
from sldb.core.node import SLDBNode

MARKER_PATTERN = r"⸢([^⸥]+)⸥"


class YamlNodeHandler(BaseNodeHandler):
    """
    Handler for extracting data from YAML, front-matter, and fence nodes.
    """

    def compile_recipe(self, node: SLDBNode) -> list[dict[str, Any]]:
        content = node.content.strip()
        match = re.search(MARKER_PATTERN, content)
        if match:
            marker = parse_marker(match.group(1))
            if (marker.is_reversible or marker.is_optional) and "dict" in marker.traits:
                return [
                    {
                        "name": marker.name,
                        "marker": marker,
                        "handler": "yaml",
                    }
                ]
        return []

    def extract_data(self, node: SLDBNode, recipe: dict[str, Any]) -> Any:
        if node.type not in ["fence", "front_matter"]:
            return None

        content = node.content.strip()
        try:
            clean_content = re.sub(MARKER_PATTERN, "", content).strip()
            if not clean_content:
                clean_content = content

            data = yaml.safe_load(clean_content)
            return {recipe["name"]: data}
        except Exception as e:
            raise SLDBASTError(f"Failed to parse YAML content for {recipe['name']}") from e
