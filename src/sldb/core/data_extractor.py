from typing import Any
from sldb.core.node import SLDBNode
from sldb.core.extractor.recipe_matcher import RecipeMatcher
from sldb.core.node_handler import SharedNodeHandler

class DataExtractor:
    """Applies compiled template recipes to parsed SLDBNodes."""

    def __init__(self):
        self.matcher = RecipeMatcher()
        self.node_handler = SharedNodeHandler()

    def _find_next_matching_block(self, data_blocks: list[SLDBNode], recipe: dict[str, Any], start_index: int) -> int | None:
        for block_idx in range(start_index, len(data_blocks)):
            if self.matcher.match_recipe_at_block(data_blocks[block_idx], recipe)[0]: return block_idx
        return None

    def _capture_markdown_slice(self, data_blocks: list[SLDBNode], start_block_idx: int, end_block_idx: int, raw_markdown: str | None) -> str:
        if start_block_idx >= end_block_idx: return ""
        if raw_markdown is not None and (slice_str := self._try_capture_raw(data_blocks, start_block_idx, end_block_idx, raw_markdown)):
            return slice_str
        return self._fallback_capture(data_blocks, start_block_idx, end_block_idx)

    def _try_capture_raw(self, data_blocks: list[SLDBNode], start_block_idx: int, end_block_idx: int, raw_markdown: str) -> str | None:
        start_map, end_map = data_blocks[start_block_idx].map, data_blocks[end_block_idx - 1].map
        if start_map and end_map:
            return "\n".join(raw_markdown.splitlines()[start_map[0] : end_map[1]]).strip()
        return None

    def _fallback_capture(self, data_blocks: list[SLDBNode], start_block_idx: int, end_block_idx: int) -> str:
        rendered_blocks = []
        for block in data_blocks[start_block_idx:end_block_idx]:
            if text := self.node_handler.handlers["text"].get_text(block).strip(): rendered_blocks.append(text)
        return "\n\n".join(rendered_blocks).strip()

    def _current_block_matches_future_recipe(self, data_blocks: list[SLDBNode], recipes: list[dict[str, Any]], recipe_idx: int, block_idx: int) -> bool:
        for future_recipe in recipes[recipe_idx + 1 :]:
            if not future_recipe.get("anchor", False): continue
            if self.matcher.block_matches_recipe_for_position(data_blocks[block_idx], future_recipe): return True
        return False

    def extract_values(self, data_blocks: list[SLDBNode], recipes: list[dict[str, Any]], raw_markdown: str | None = None) -> dict[str, Any]:
        state = {"extracted": {}, "search": 0, "last_outer": -1, "curr_block": -1}
        for r_idx, recipe in enumerate(recipes):
            self._update_search_index(state, recipe)
            if recipe.get("capture_mode") == "section_body":
                self._handle_section_body(data_blocks, recipes, r_idx, raw_markdown, state)
            else: self._process_recipe_blocks(data_blocks, recipes, r_idx, state)
        return state["extracted"]

    def _update_search_index(self, state: dict[str, Any], recipe: dict[str, Any]) -> None:
        if recipe["outer_index"] != state["last_outer"]:
            state["search"] = max(state["search"], state["curr_block"] + 1)
            state["last_outer"] = recipe["outer_index"]
            state["curr_block"] = -1

    def _handle_section_body(self, data_blocks: list[SLDBNode], recipes: list[dict[str, Any]], r_idx: int, raw_markdown: str | None, state: dict[str, Any]) -> None:
        boundary_idx = self._find_boundary_idx(data_blocks, recipes, r_idx, state["search"])
        val = self._capture_markdown_slice(data_blocks, state["search"], boundary_idx, raw_markdown)
        state["extracted"][recipes[r_idx]["props"][0]] = val
        state["curr_block"] = max(state["search"], boundary_idx - 1)

    def _find_boundary_idx(self, data_blocks: list[SLDBNode], recipes: list[dict[str, Any]], r_idx: int, search_index: int) -> int:
        for future_recipe in recipes[r_idx + 1 :]:
            if (match_idx := self._find_next_matching_block(data_blocks, future_recipe, search_index)) is not None:
                return match_idx
        return len(data_blocks)

    def _process_recipe_blocks(self, data_blocks: list[SLDBNode], recipes: list[dict[str, Any]], r_idx: int, state: dict[str, Any]) -> None:
        block_range = self._get_block_range(data_blocks, recipes[r_idx], state["search"])
        for b_idx in block_range:
            if state["curr_block"] != -1 and b_idx != state["curr_block"]: break
            if data_blocks[b_idx].type != recipes[r_idx]["outer_type"]: continue
            if self._apply_recipe_to_block(data_blocks, recipes, r_idx, b_idx, state): break

    def _get_block_range(self, data_blocks: list[SLDBNode], recipe: dict[str, Any], search_index: int) -> range:
        if recipe.get("optional_block"): return range(search_index, min(search_index + 1, len(data_blocks)))
        return range(search_index, len(data_blocks))

    def _apply_recipe_to_block(self, data_blocks: list[SLDBNode], recipes: list[dict[str, Any]], r_idx: int, b_idx: int, state: dict[str, Any]) -> bool:
        matched, values = self.matcher.match_recipe_at_block(data_blocks[b_idx], recipes[r_idx])
        if not matched: return False
        if recipes[r_idx].get("optional_block") and self._current_block_matches_future_recipe(data_blocks, recipes, r_idx, b_idx): return True
        if recipes[r_idx].get("anchor", False): state["curr_block"] = b_idx; return True
        if values: state["extracted"].update(values); state["curr_block"] = b_idx; return True
        return False
