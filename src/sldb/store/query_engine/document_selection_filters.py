"""The filters of `document_selection`, one per selector key, each over the candidate rows."""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path
from typing import Any, Callable

from sldb.store.edge_index.compose import compose_edge_index
from sldb.store.graph.backend.index_view import index_view
from sldb.store.graph.language.predicate_api import findings

_GLOB_TOKENS = re.compile(r"(\*\*/|\*\*|\*|\?)")
_GLOB_REGEX = {"**/": "(?:.*/)?", "**": ".*", "*": "[^/]*", "?": "[^/]"}


def keep_matching(
    store_path: Path, rows: list[dict[str, Any]], ref: tuple[str | None, str] | None, path_glob: str | None,
    model: str | None, where: str | None, model_type_of: Callable[..., Any] | None,
) -> list[dict[str, Any]]:
    """The rows every given key keeps: `ref`, then `path_glob`, `model` and `where`."""
    if ref is not None:
        rows = [row for row in rows if row["store"] == ref[0] and names_document(ref[1], row)]
    if path_glob is not None:
        rows = [row for row in rows if glob_regex(path_glob).fullmatch(row["path"])]
    if model is not None:
        rows = [row for row in rows if row["model"] == model or model in row["bases"]]
    if where is not None:
        held = holding(store_path, where, any(row["store"] for row in rows), model_type_of)
        rows = [row for row in rows if row["export_id"] in held]
    return rows


def names_document(reference: str, row: dict[str, Any]) -> bool:
    """Whether an unqualified reference names the row's document (as `doc_status` reads it)."""
    return reference in (row["name"], row["path"], f"{row['model']}/{row['name']}", f"{row['model']}:{row['name']}")


def glob_regex(pattern: str) -> re.Pattern[str]:
    """A shell pattern as a regex over posix paths: `*` and `?` stop at `/`, `**` crosses it
    (`sub/**/*.md` is every `.md` under `sub/`, at any depth); `[seq]` as in `fnmatch`."""
    parts = [_GLOB_REGEX.get(token) or fnmatch.translate(token)[4:-3] for token in _GLOB_TOKENS.split(pattern) if token]
    return re.compile("".join(parts))


def holding(store_path: Path, where: str, linked: bool, model_type_of: Callable[..., Any] | None) -> set[str]:
    """The export ids of the documents the predicate holds on, read from the edge index's
    payload projection (never from the files). An unparseable predicate raises
    `WherePredicateError` before anything is read."""
    index = compose_edge_index(store_path, linked, (), model_type_of)
    return {found["node"] for found in findings(where, index_view(index)) if found["holds"] == "true"}


def prefix_tier(rows: list[dict[str, Any]], prefix: str | None, expect: str) -> list[dict[str, Any]]:
    """`expect="many"`: every name starting with the prefix (the exact name included).
    `expect="one"`: the exact name when there is one, else the prefix matches (the caller
    decides what more than one means)."""
    if prefix is None:
        return rows
    exact = [row for row in rows if row["name"] == prefix]
    if expect == "one" and exact:
        return exact
    return [row for row in rows if row["name"].startswith(prefix)]
