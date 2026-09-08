"""Store-qualified structural addresses: `<store>:st.{Model+}.doc.field` reaches a linked
store the way `st.…` reaches the local one. The prefix is a store name from
`store_index.yaml` (`local` is the local store and may be omitted); results that come
from a linked store carry the same prefix back, the form `gse.` already uses."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

_PREFIX = re.compile(r"^([A-Za-z0-9_.\-]+):(st\..*)$")


def split_store(address: str) -> tuple[str | None, str]:
    """('B', 'st.{M}.doc') for 'B:st.{M}.doc'; (None, address) for a local address."""
    m = _PREFIX.match(address)
    if not m:
        return None, address
    name = m.group(1)
    return (None if name == "local" else name), m.group(2)


def with_store(store: str | None, address: str) -> str:
    return address if store is None else f"{store}:{address}"


def scoped_docs(store_path: Path, store: str | None, resolve_model_ref, pythonpath: str | None) -> list[Any]:
    """The runtime documents of one store: the local one, or a linked one by name."""
    from sldb.store.query import load_runtime_documents

    if store is None:
        return load_runtime_documents(store_path, resolve_model_ref, pythonpath)
    docs = load_runtime_documents(store_path, resolve_model_ref, pythonpath, include_linked=True)
    return [d for d in docs if d.store_name == store]
