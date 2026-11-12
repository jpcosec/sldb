"""H5: `stores declare --write` keeps every key the author wrote, not only generate and derived."""

from __future__ import annotations

from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import Seed, StoreDeclaration, TagNamespace, load_declaration, save_declaration


def test_declare_write_keeps_tags_policy_scaffold_and_graph(api_store):
    authored = declare_store(api_store.store, api_store.root).model_copy(update={
        "tag_namespaces": [TagNamespace(name="topic", hierarchical=False)],
        "tag_models": ["TicketDoc"],
        "policy": {"*": {"stale": "alert"}},
        "graph_backend": "networkx",
        "folders": ["inbox"],
        "seeds": [Seed(path="inbox/.keep", text="")],
        "project_graph": {"nodes": []},
        "derived": ["out/"],
    })
    save_declaration(api_store.store, authored)
    save_declaration(api_store.store, declare_store(api_store.store, api_store.root))
    again = load_declaration(api_store.store)
    assert isinstance(again, StoreDeclaration)
    assert again.model_dump() == authored.model_dump()
