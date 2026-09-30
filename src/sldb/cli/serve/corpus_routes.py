"""GET /corpus/rank: documents (or fields) ranked by similarity to a query, over `sldb.api.Corpus`."""

from __future__ import annotations

from dataclasses import asdict
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from sldb.api.corpus.corpus import Corpus
from sldb.cli.serve.corpus_projection import HTTP_PROJECTION
from sldb.cli.serve.params import query_params
from sldb.cli.serve.rank_request import RankRequest
from sldb.core.exceptions import SLDBError

NOT_INDEXED = {"ok": False, "error": "corpus no indexado", "kind": "not_indexed"}


def corpus_rank(handler: BaseHTTPRequestHandler, store_path: Path, pythonpath: str) -> tuple[dict[str, Any], int]:
    """Serve `?q=&k=&threshold=&among=&fields=&refresh=`.

    Returns `{"hits": [Hit...]}` (or `[FieldHit...]` with `fields=1`) and 200; 400 for a
    missing or invalid parameter; 409 `{"ok": false, "error": "corpus no indexado",
    "kind": "not_indexed"}` when the index does not exist yet and `refresh` is off.

    `refresh=0` (default) only reads the index: it never embeds or writes, so it is fast, and it
    ranks what was indexed last (documents added since are not found until a refresh).
    `refresh=1` runs `refresh_if_stale`: it builds the index when absent and re-embeds only what
    drifted, so the call that does it can be slow. An empty `hits` always means "no matches".
    """
    request, error = _parsed(handler)
    if error is not None:
        return error, 400
    corpus = Corpus(store_path, pythonpath, store_path / "runtime" / "corpus", HTTP_PROJECTION)
    index_path = corpus.field_index_path if request.fields else corpus.index_path
    if not request.refresh and not index_path.exists():
        return NOT_INDEXED, 409
    return _ranked(corpus, request)


def _parsed(handler: BaseHTTPRequestHandler) -> tuple[RankRequest, dict[str, Any] | None]:
    params = query_params(handler)
    if not params.get("q"):
        return RankRequest.model_construct(), {"ok": False, "error": "Missing parameter: q"}
    try:
        return RankRequest.model_validate(params), None
    except ValidationError as exc:
        first = exc.errors()[0]
        return RankRequest.model_construct(), {"ok": False, "error": f"Invalid parameter {first['loc'][0]}: {first['msg']}"}


def _ranked(corpus: Corpus, request: RankRequest) -> tuple[dict[str, Any], int]:
    rank = corpus.rank_fields if request.fields else corpus.rank
    try:
        hits = rank(request.q, request.k, request.threshold, request.among, request.refresh)
    except SLDBError as exc:
        return {"ok": False, "error": str(exc)}, 400
    return {"hits": [asdict(hit) for hit in hits]}, 200
