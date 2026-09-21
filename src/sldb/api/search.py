"""HTTP-ready wrapper for the CLI's real find pipeline, exposed via sldb.api.

The matching itself is the CLI's machinery — ``iter_search_records``,
``search_records``, ``FindFilters`` and the formatter's serializer — composed
here in the exact order ``FindCLI.run`` composes it, so a serve response is the
same shape as `sldb find --format json`. ``compile_where`` runs first, so an
unparseable ``--where`` raises ``WherePredicateError`` (the parser's real
message) before any matching happens.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any


def search(
    store_path: Path,
    term: str,
    search_in: str = "both",
    kinds: set[str] | None = None,
    where: str | None = None,
    select: str | None = None,
    limit: int | None = None,
    pythonpath: str | None = None,
    regex: bool = False,
    fuzzy: bool = False,
    include_linked: bool = False,
) -> dict[str, Any]:
    """Match records exactly as `sldb find` matches, serialized as its JSON results."""
    from sldb.store.query_engine.where_parse import compile_where

    if where:
        compile_where(where)
    records = _records(store_path, pythonpath, include_linked)
    matched = _match(records, term, search_in, regex, fuzzy, kinds)
    if where:
        matched = _filtered(matched, where, pythonpath)
    return _serialize(matched, select, limit)


def _records(store_path: Path, pythonpath: str | None, include_linked: bool) -> list[Any]:
    from sldb.cli.graph_ops import iter_search_records

    return iter_search_records(str(store_path), pythonpath, include_linked=include_linked)


def _match(records: list[Any], term: str, search_in: str, regex: bool, fuzzy: bool, kinds: set[str] | None) -> list[Any]:
    from sldb.cli.graph_ops import search_records

    return search_records(records, term, search_in, regex, fuzzy, kinds)


def _filtered(matched: list[Any], where: str, pythonpath: str | None) -> list[Any]:
    from sldb.cli.commands.find_filters import FindFilters

    filters = FindFilters(pythonpath)
    return [record for record in matched if filters.matches(record, where)]


def _serialize(matched: list[Any], select: str | None, limit: int | None) -> dict[str, Any]:
    from sldb.cli.commands.find_format import FindFormatter

    formatter = FindFormatter()
    payload = [formatter._serialize(record) for record in matched]
    if select:
        payload = formatter._apply_select(payload, select)
    if limit is not None:
        payload = payload[:limit]
    return {"results": payload}