from typing import Any

from sldb.core.node import SLDBNode
from sldb.core.node_handler import SharedNodeHandler


class DataExtractor:
    """
    Applies compiled template recipes to parsed SLDBNodes.
    """

    def __init__(self):
        self.node_handler = SharedNodeHandler()

    def _find_leaf_text_node(self, node: SLDBNode) -> SLDBNode | None:
        if node.type == "text":
            return node
        if node.content:
            return node
        for child in node.children:
            result = self._find_leaf_text_node(child)
            if result:
                return result
        return None

    def _match_recipe_at_block(
        self, block: SLDBNode, recipe: dict[str, Any]
    ) -> tuple[bool, dict[str, Any] | None]:
        if block.type != recipe["outer_type"]:
            return False, None

        is_anchor = recipe.get("anchor", False)
        if not is_anchor and block.tag != recipe.get("outer_tag", ""):
            return False, None

        handler_key = recipe.get("handler", "text")
        current_node = block
        if handler_key == "text":
            current_node = self._find_leaf_text_node(block)

        if not current_node:
            if is_anchor:
                return True, {}
            return False, None

        values = self.node_handler.handlers[handler_key].extract_data(
            current_node, recipe
        )
        if is_anchor:
            return True, values
        if values:
            return True, values
        return False, None

    def _find_next_matching_block(
        self, data_blocks: list[SLDBNode], recipe: dict[str, Any], start_index: int
    ) -> int | None:
        for block_idx in range(start_index, len(data_blocks)):
            matched, _ = self._match_recipe_at_block(data_blocks[block_idx], recipe)
            if matched:
                return block_idx
        return None

    def _capture_markdown_slice(
        self,
        data_blocks: list[SLDBNode],
        start_block_idx: int,
        end_block_idx: int,
        raw_markdown: str | None,
    ) -> str:
        if start_block_idx >= end_block_idx:
            return ""

        if raw_markdown is not None:
            start_map = data_blocks[start_block_idx].map
            end_map = data_blocks[end_block_idx - 1].map
            if start_map and end_map:
                lines = raw_markdown.splitlines()
                return "\n".join(lines[start_map[0] : end_map[1]]).strip()

        rendered_blocks = []
        for block in data_blocks[start_block_idx:end_block_idx]:
            text = self.node_handler.handlers["text"].get_text(block).strip()
            if text:
                rendered_blocks.append(text)
        return "\n\n".join(rendered_blocks).strip()

    def extract_values(
        self,
        data_blocks: list[SLDBNode],
        recipes: list[dict[str, Any]],
        raw_markdown: str | None = None,
    ) -> dict[str, Any]:
        extracted_data = {}
        search_index = 0
        last_outer_index = -1
        current_block_idx = -1

        for recipe_idx, recipe in enumerate(recipes):
            target_type = recipe["outer_type"]
            recipe_outer_idx = recipe["outer_index"]

            if recipe_outer_idx != last_outer_index:
                search_index = max(search_index, current_block_idx + 1)
                last_outer_index = recipe_outer_idx
                current_block_idx = -1

            if recipe.get("capture_mode") == "section_body":
                boundary_idx = len(data_blocks)
                for future_recipe in recipes[recipe_idx + 1 :]:
                    match_idx = self._find_next_matching_block(
                        data_blocks, future_recipe, search_index
                    )
                    if match_idx is not None:
                        boundary_idx = match_idx
                        break

                extracted_data[recipe["props"][0]] = self._capture_markdown_slice(
                    data_blocks,
                    search_index,
                    boundary_idx,
                    raw_markdown,
                )
                current_block_idx = max(search_index, boundary_idx - 1)
                continue

            for block_idx in range(search_index, len(data_blocks)):
                if current_block_idx != -1 and block_idx != current_block_idx:
                    break

                block = data_blocks[block_idx]
                if block.type != target_type:
                    continue

                matched, values = self._match_recipe_at_block(block, recipe)
                if not matched:
                    continue

                if recipe.get("anchor", False):
                    current_block_idx = block_idx
                    break
                if values:
                    extracted_data.update(values)
                    current_block_idx = block_idx
                    break

        return extracted_data
