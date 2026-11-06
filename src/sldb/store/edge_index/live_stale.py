"""What the shards cannot say about themselves (inbox 20261102-065705): a Markdown file edited
from outside sldb (its text no longer hashes to the `source_hash` its shard was built from) and
a model whose contract moved (its fields or declared reference names: a new `__references__`
entry moves no document hash). Checked on every read of the index, not kept with the composed
index: neither moves a shard file. A file's hash is kept while its mtime and size hold."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from sldb.store import documents_hash
from sldb.store.edge_index.node_ids import doc_node_id
from sldb.store.hashing import hash_text
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
    root = project_root(store_path)
    stale: list[str] = []
    for m in load_store_index(store_path).models:
        signature = _signature(m.model_ref, root, model_type_of)
        paths = {e.name: root / e.path for e in documents_hash.entries_of(store_path, m.name)}
        shards = [s for s in compose_edges_documents(store_path, m.name) if s.doc_name in paths]
        stale += [f"{m.name}:{s.doc_name}" for s in shards if _moved(s, doc_node_id(f"{m.name}:{s.doc_name}"), paths[s.doc_name], signature)]
    return stale


def _signature(model_ref: str, root: Path, model_type_of: ModelTypeOf | None) -> str | None:
    from sldb.store.model_contract import contract_signature

    return None if model_type_of is None else contract_signature(model_type_of(model_ref, root))


def _moved(shard: DocEdges, node_id: str, path: Path, signature: str | None) -> bool:
    current = _file_hash(path)
    if current is not None and current != shard.source_hash:
        return True
    node = next((n for n in shard.nodes if n.id == node_id), None)
    return signature is not None and node is not None and node.contract_signature != signature


def _file_hash(path: Path) -> str | None:
    """The file's source_hash as sldb computes it on track; None when it cannot be read."""
    try:
        st = path.stat()
        key = (st.st_mtime_ns, st.st_size)
        hit = _FILE_HASHES.get(str(path))
        if hit is None or hit[0] != key:
            hit = _FILE_HASHES[str(path)] = (key, hash_text(path.read_text(encoding="utf-8")))
        return hit[1]
    except (OSError, UnicodeDecodeError):
        return None
