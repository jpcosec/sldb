"""`sldb find` as a library call: match records and serialize them.

The matching pipeline — ``iter_search_records``, ``search_records``,
``where_records`` (``sldb.api.where``) and the record serializer — are
composed here in the exact order ``FindCLI.run`` composes them, so a serve response is
the same shape as `sldb find --format json`. ``parse_predicate`` runs first, so an
unparseable ``--where`` raises ``WherePredicateError`` (the parser's real message)
before any matching happens.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from sldb.api.records import (
    SearchRecord,
    iter_search_records,
    search_records,
    select_keys,
    serialize_records,
)
from sldb.api.where import where_records


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
    from sldb.store.graph.language.predicate_parser import parse_predicate

    if where:
        parse_predicate(where)
    records = _records(store_path, pythonpath, include_linked)
    matched = _match(records, term, search_in, regex, fuzzy, kinds)
    if where:
        matched = where_records(matched, where, store_path, pythonpath, include_linked)[0]
    return _serialize(matched, select, limit)


def _records(store_path: Path, pythonpath: str | None, include_linked: bool) -> list[SearchRecord]:
    return iter_search_records(str(store_path), pythonpath, include_linked=include_linked)


def _match(records: list[SearchRecord], term: str, search_in: str, regex: bool, fuzzy: bool, kinds: set[str] | None) -> list[SearchRecord]:
    return search_records(records, term, search_in, regex, fuzzy, kinds)


def _serialize(matched: list[SearchRecord], select: str | None, limit: int | None) -> dict[str, Any]:
    payload = serialize_records(matched)
    if select:
        payload = select_keys(payload, select)
    if limit is not None:
        payload = payload[:limit]
    return {"results": payload}
