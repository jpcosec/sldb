"""Check the [[links]] of many documents at once (what `docs recover --all` and /lint report)."""
from __future__ import annotations
from pathlib import Path
from .recovery import recover_links

def _problems(name: str, links: list[dict]) -> list[dict]:
    out = [{"doc": name, "kind": "unresolved", "target": l["target"], "predicate": l["predicate"]} for l in links if not l["resolved"]]
    return out + [{"doc": name, "kind": "custom", "target": l["target"], "predicate": l["predicate"]} for l in links if l["w5h1_type"] == "CUSTOM"]

def audit_links(store_path: Path | None, docs: list[tuple[str, Path]]) -> list[dict]:
    """One problem per unresolved link (`unresolved`) or per predicate missing from the store (`custom`)."""
    return [p for name, path in docs if path.exists() for p in _problems(name, recover_links(path, store_path, depth=1)["links"])]
