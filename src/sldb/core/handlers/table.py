from __future__ import annotations

import re
from typing import Any

from sldb.core.handlers.base import BaseNodeHandler
from sldb.core.handlers.utils import parse_marker
from sldb.core.node import SLDBNode


class TableNodeHandler(BaseNodeHandler):
    """
    Handler for extracting data from table nodes as structured row records.
    """

    def compile_recipe(self, node: SLDBNode) -> list[dict[str, Any]]:
        # Find all rows in the table
        rows = []
        for child in node.children:
            if child.type in ["thead", "tbody"]:
                rows.extend([tr for tr in child.children if tr.type == "tr"])
            elif child.type == "tr":
                rows.append(child)

        if len(rows) < 2:
            return []

        # The last row is treated as the template row
        template_row = rows[-1]
        col_markers: dict[int, Any] = {}

        for col_idx, cell in enumerate(template_row.children):
            text = self.get_text(cell).strip()
            match = re.search(r"⸢([^⸥]+)⸥", text)
            if match:
                marker = parse_marker(match.group(1))
                if marker.is_reversible or marker.is_optional:
                    col_markers[col_idx] = {
                        "marker": marker,
                        "cell_template": text,
                    }

        if not col_markers:
            return []

        # Use the name of the first marker as the primary field name for the record set
        first_marker_name = list(col_markers.values())[0]["marker"].name

        return [
            {
                "name": first_marker_name,
                "handler": "table",
                "col_markers": col_markers,
                "props": [m["marker"].name for m in col_markers.values()],
            }
        ]

    def extract_data(self, node: SLDBNode, recipe: dict[str, Any]) -> Any:
        from sldb.core.handlers.text import build_text_pattern

        rows = []
        for child in node.children:
            if child.type in ["thead", "tbody"]:
                rows.extend([tr for tr in child.children if tr.type == "tr"])
            elif child.type == "tr":
                rows.append(child)

        # Skip header and template rows? No, in data nodes there is no template row.
        # But in extraction, we don't know if it's a template or data.
        # DataExtractor passes data nodes.
        data_rows = rows[1:] if len(rows) > 1 else []

        col_markers = recipe["col_markers"]
        patterns = {
            idx: build_text_pattern(m["cell_template"])["regex"]
            for idx, m in col_markers.items()
        }

        results = []
        for row in data_rows:
            row_record = {}
            row_has_data = False
            for col_idx, meta in col_markers.items():
                if col_idx < len(row.children):
                    cell = row.children[col_idx]
                    text = self.get_text(cell).strip()
                    match = re.fullmatch(patterns[col_idx], text)
                    if match:
                        row_record[meta["marker"].name] = match.group(1)
                        row_has_data = True

            if row_has_data:
                # If only one marker in the row, we might want to return just the scalar
                # but "row records" usually implies a dict.
                # In SLDBGuide, 'commands' marker is just one, but others follow.
                results.append(row_record)

        return {recipe["name"]: results} if results else None
