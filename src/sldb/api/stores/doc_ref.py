"""Document references that may name a linked store: `deskops:task-x`, `deskops:TaskDoc/task-x`.

The prefix is the alias of a DIRECT link of the store (`stores add --name`); links of links are
never followed, so two stores linking each other cannot loop and an alias means one thing.
A bare reference never leaves the local store (equal names in two stores are not the same
document), and `local:` names the local store explicitly. A prefix that names no link leaves
the reference whole, so a local document whose name holds a colon resolves as before.
"""

from __future__ import annotations

import re
from pathlib import Path

from sldb.api.stores.store_links import find_link

LINK_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
LOCAL = "local"
_QUALIFIED = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*):(.+)$")


def qualifier(ref: str) -> str | None:
    """The store prefix `ref` is written with (`deskops` for `deskops:x`), linked or not."""
    m = _QUALIFIED.match(ref.strip("/"))
    return m.group(1) if m else None


def split_doc_ref(store_path: Path, ref: str) -> tuple[str | None, str]:
    """(link alias, reference inside that store); the alias is None for the local store.

    Args:
        store_path: The store the reference is read from; its links give prefixes meaning.
        ref: `name`, `Model/name`, a tracked path, or any of those behind `alias:`.
    """
    ref = ref.strip("/")
    name = qualifier(ref)
    rest = ref[len(name) + 1:] if name else ref
    if name == LOCAL:
        return None, rest
    return (name, rest) if name and find_link(store_path, name) else (None, ref)


def matches_doc_ref(ref: str, name: str, path: str, model: str) -> bool:
    """Whether `ref` (already unqualified) names the document by name, path or `Model/name`."""
    return ref in (name, path, f"{model}/{name}")
