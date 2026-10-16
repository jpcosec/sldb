"""Contract hashes written before the contract covered class metadata (cecd97b, 2026-10-05).

Until then a model's contract hashed only its field schema and template. A store indexed then
holds that hash, so under today's formula every one of its models read "contract moved" although
no class changed — and a consumer's CI went red on upgrading sldb alone. A stored hash equal to
the old formula over today's class says the fields and template are the ones indexed; only the
metadata added to the contract later was never signed. That is reported, not failed, and
`stores update` re-seals it under the current formula.
"""

from __future__ import annotations

from typing import Any

from sldb.store.hashing import _field_schema, hash_model_contract, hash_payload


def legacy_contract_hash(model_type: Any) -> str:
    """The contract hash as sldb wrote it before cecd97b: field schema and template only."""
    return hash_payload({"fields": _field_schema(model_type), "template": getattr(model_type, "__template__", "")})


def legacy_contract(m_idx: Any, model_type: Any | None) -> bool:
    """Whether the index holds the old-formula hash of this very class: unchanged, not yet re-sealed."""
    if model_type is None or not m_idx.contract_hash:
        return False
    stored = m_idx.contract_hash
    return stored != hash_model_contract(model_type) and stored == legacy_contract_hash(model_type)
