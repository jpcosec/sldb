"""What the shards cannot say about themselves (inbox 20261102-065705): a Markdown file edited
from outside sldb (its text no longer hashes to the `source_hash` its shard was built from) and
a model whose contract moved (its fields or declared reference names: a new `__references__`
entry moves no document hash). Checked on every read of the index, not kept with the composed
index: neither moves a shard file.

Reading the index opens as little as it can (SEGURIDAD, inbox 9c9dac6b): a tracked path that
resolves outside the project root, or is a symlink, is never opened (`source_read.unreadable_reason`): its
document counts as moved, and `stores check` names why. A file whose `lstat` still matches the
`source_stat` its shard was built with is not opened either; only a file whose stat moved is
read and hashed (and its hash kept, per process, while its stat holds)."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.store import documents_hash
from sldb.store.edge_index.node_ids import doc_node_id
from sldb.store.hashing import hash_text
from sldb.store.source_read import read_source_text, source_stat, unreadable_reason
from sldb.store.io import load_store_index
from sldb.store.io.shard_compose import compose_edges_documents
from sldb.store.layout import project_root
from sldb.store.models import DocEdges

#: (model_ref, the store's project root) -> the model class, or None when it cannot be loaded.
ModelTypeOf = Callable[[str, Path], Any]
_FILE_HASHES: dict[str, tuple[tuple[int, int], str]] = {}


def live_stale(store_path: Path, model_type_of: ModelTypeOf | None) -> list[str]:
    """Export ids whose file or model contract moved since their shard was built. Without
    `model_type_of` the contract is not compared (the store alone cannot import a class)."""
    return stale_of_facts(store_path, live_facts(store_path), model_type_of)


def live_facts(store_path: Path) -> list[dict[str, Any]]:
    """What `stale_of_facts` needs of the shards, per model: `{model, model_ref, docs: [[name,
    path, source_stat, source_hash, has_node, contract_signature]]}`. Plain data, so the
    composed index keeps it beside itself and a later process never re-reads the shards."""
    facts = []
    for m in load_store_index(store_path).models:
        paths = {e.name: e.path for e in documents_hash.entries_of(store_path, m.name)}
        shards = [s for s in compose_edges_documents(store_path, m.name, copy=False) if s.doc_name in paths]
        facts.append({"model": m.name, "model_ref": m.model_ref, "docs": [_doc_fact(m.name, s, paths[s.doc_name]) for s in shards]})
    return facts


def _doc_fact(model: str, shard: DocEdges, path: str) -> list[Any]:
    node = next((n for n in shard.nodes if n.id == doc_node_id(f"{model}:{shard.doc_name}")), None)
    stat = None if shard.source_stat is None else list(shard.source_stat)
    return [shard.doc_name, path, stat, shard.source_hash, node is not None, node.contract_signature if node else None]


def stale_of_facts(store_path: Path, facts: list[dict[str, Any]], model_type_of: ModelTypeOf | None) -> list[str]:
    """`live_stale` over facts: the files' stats now, and the models' contracts now."""
    root = project_root(store_path)
    stale: list[str] = []
    for fact in facts:
        signature = _signature(fact["model_ref"], root, model_type_of)
        stale += [f"{fact['model']}:{d[0]}" for d in fact["docs"] if _moved(d, root, signature)]
    return stale


def _signature(model_ref: str, root: Path, model_type_of: ModelTypeOf | None) -> str | None:
    from sldb.store.model_contract import contract_signature

    return None if model_type_of is None else contract_signature(model_type_of(model_ref, root))


def _moved(doc: list[Any], root: Path, signature: str | None) -> bool:
    name, rel, stat, source_hash, has_node, node_signature = doc
    path = root / rel
    if unreadable_reason(root, path) is not None or _text_moved(stat, source_hash, path):
        return True
    return signature is not None and has_node and node_signature != signature


def _text_moved(shard_stat: list[int] | None, source_hash: str, path: Path) -> bool:
    """Whether the file's text left the shard's `source_hash`; read only when its stat moved."""
    current_stat = source_stat(path)
    if current_stat is None:
        return False  # missing: the shard reader and `stores check` name it, as before
    if shard_stat is not None and shard_stat == current_stat:
        return False
    current = _file_hash(path, current_stat)
    return current is not None and current != source_hash


def _file_hash(path: Path, current_stat: list[int]) -> str | None:
    """The file's source_hash as sldb computes it on track; None when it cannot be read."""
    key = (current_stat[0], current_stat[1])
    hit = _FILE_HASHES.get(str(path))
    if hit is None or hit[0] != key:
        try:
            hit = _FILE_HASHES[str(path)] = (key, hash_text(read_source_text(path)))
        except (OSError, UnicodeDecodeError):
            return None
    return hit[1]
