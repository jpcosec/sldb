"""Per-document results of the content scans of `stores check`, reused while nothing they
depend on moved.

A document's rewrite loss (and its structural noise) is a function of its text, its model's
contract and the sldb that reads it: the key is those three, so an unchanged store is not
re-rendered on every check (2500 symbol documents cost ~18 s a pass). The cache lives in the
user's cache directory, never inside the store; losing it only costs one cold pass.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Callable

SCAN_VERSION = "1"  # bump when what a scan reports changes for the same text and contract


def cached_per_document(store_path: Path, kind: str, docs: list[tuple[Any, str]], compute: Callable[[Any, str], Any]) -> list[tuple[Any, Any]]:
    """`(doc, result)` for each `(doc, text)`: the stored result when its key still holds."""
    path = _file(store_path, kind)
    cache, contracts, fresh = _load(path), {"": _reader()}, {}
    out = [(doc, _result(doc, text, cache, fresh, contracts, compute)) for doc, text in docs]
    _save(path, fresh)
    return out


def _result(doc: Any, text: str, cache: dict, fresh: dict, contracts: dict[str, str], compute: Callable[[Any, str], Any]) -> Any:
    """The cached result when its key holds, computed otherwise; recorded in `fresh` either way."""
    key, slot = _key(doc, text, contracts), f"{doc.model_name}:{doc.name}"
    hit = cache.get(slot)
    result = hit["result"] if hit and hit.get("key") == key else compute(doc, text)
    fresh[slot] = {"key": key, "result": result}
    return result


def _key(doc: Any, text: str, contracts: dict[str, str]) -> str:
    from sldb.store.hashing import hash_model_contract

    if doc.model_name not in contracts:
        contracts[doc.model_name] = hash_model_contract(doc.model_type)
    return f"{hashlib.sha256(text.encode('utf-8')).hexdigest()}|{contracts[doc.model_name]}|{contracts['']}|{SCAN_VERSION}"


def _reader() -> str:
    """The sldb that reads the documents: its version, and a fingerprint of the code that
    extracts and renders them (a development checkout keeps one version across fixes)."""
    import sldb
    from sldb.store.package_version import package_version

    base = Path(sldb.__file__).parent
    files = sorted(p for d in ("core", "runtime", "models") for p in (base / d).rglob("*.py"))
    files += [base / "api" / "documents" / "rewrite_loss.py", base / "api" / "documents" / "structural_noise.py"]
    stamp = "|".join(f"{p.relative_to(base)}:{p.stat().st_size}:{p.stat().st_mtime_ns}" for p in files if p.exists())
    return f"{package_version()}:{hashlib.sha256(stamp.encode()).hexdigest()[:16]}"


def _file(store_path: Path, kind: str) -> Path | None:
    from sldb.store.user_cache import cache_root

    root = cache_root()
    digest = hashlib.sha256(str(Path(store_path).resolve()).encode("utf-8")).hexdigest()
    return None if root is None else root / "content-scans" / kind / f"{digest}.json"


def _load(path: Path | None) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path else {}
    except (OSError, ValueError):
        return {}


def _save(path: Path | None, data: dict) -> None:
    if path is None:
        return
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data), encoding="utf-8")
    except OSError:
        pass
