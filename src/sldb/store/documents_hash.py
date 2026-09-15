"""A model's hash_b, kept without re-reading every document shard on every write (PLAN 15
capa 7): the child-hash map (name -> (hash_c, hash_d)) for a model is built once per
operation (the same "operation" `new_operation` already scopes for runtime_cache_signature
— once per Store/World opened, once per sldb CLI command), by reading every one of that
model's document shards once; from there, this module's own `note`/`forget` update the map
in memory as this operation's own writes touch shards, and `hash_b_of`/`count_of` recompute
from the map — no further shard reads until the next operation. Values match
`hashing.hash_document_entries` — the same a full scan (stores update) would give for the
same set of documents."""

from __future__ import annotations

from pathlib import Path

from sldb.store.hashing import hash_document_entries
from sldb.store.io.shard_compose import compose_documents_entries

_MAPS: dict[tuple[str, str], dict[str, tuple[str, str]]] = {}


def new_operation(s_path: Path | None = None) -> None:
    """Drop every remembered map so the next use rebuilds it from the shards on disk."""
    if s_path is None:
        _MAPS.clear()
        return
    prefix = str(s_path)
    for key in [k for k in _MAPS if k[0] == prefix]:
        del _MAPS[key]


def invalidate(s_path: Path, model_name: str) -> None:
    """Drop one model's remembered map (sldb.cli.commands.store_update recomputes hash_b by
    a full scan of every document's actual file content — a hand edit can change hash_c/
    hash_d there without going through `note`/`forget`; the next use rebuilds from shards)."""
    _MAPS.pop((str(s_path), model_name), None)


def _map_for(s_path: Path, model_name: str) -> dict[str, tuple[str, str]]:
    key = (str(s_path), model_name)
    if key not in _MAPS:
        _MAPS[key] = {e.name: (e.hash_c, e.hash_d) for e in compose_documents_entries(s_path, model_name)}
    return _MAPS[key]


def note(s_path: Path, model_name: str, doc_name: str, hash_c: str, hash_d: str) -> None:
    """This document's shard was just written with these hashes."""
    _map_for(s_path, model_name)[doc_name] = (hash_c, hash_d)


def forget(s_path: Path, model_name: str, doc_name: str) -> None:
    """This document's shard was just deleted."""
    _map_for(s_path, model_name).pop(doc_name, None)


def hash_b_of(s_path: Path, model_name: str) -> str:
    return hash_document_entries((n, hc, hd) for n, (hc, hd) in _map_for(s_path, model_name).items())


def count_of(s_path: Path, model_name: str) -> int:
    return len(_map_for(s_path, model_name))
