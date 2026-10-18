"""Where a captured section ends: the first block a later recipe claims.

Past a heading the document does not have, only later headings count. A field of a missing
section (`## When` and its paragraph, in a document that ends at `## Why`) matched the last
section's own paragraph and left that section empty, so a rewrite erased it (deskops' pill
written by hand; the `purpose` of three rituals).
"""

from __future__ import annotations

from typing import Any, Callable


def find_boundary_idx(find_next: Callable[[dict[str, Any], int], int | None], recipes: list[dict[str, Any]], r_idx: int, search_index: int, end: int) -> int:
    """`find_next(recipe, start)` is the extractor's own block search; `end` the block count."""
    section_missing = False
    for future_recipe in recipes[r_idx + 1 :]:
        heading = future_recipe.get("anchor", False) and future_recipe.get("outer_type") == "heading"
        if section_missing and not heading:
            continue
        if (match_idx := find_next(future_recipe, search_index)) is not None:
            return match_idx
        section_missing = section_missing or heading
    return end
