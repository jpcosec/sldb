"""Stamp a model's node and its two children onto its index, in one place.

Six call sites used to each set `model_hash` on their own, from whatever they happened to
have at hand; none of them recorded the contract. A model node is now
`hash_model_layer(roster_hash, contract_hash)`, and both children are persisted beside it, so
`stores check` can attribute a disagreeing node to the roster or to the contract instead of
reporting a bare mismatch. Every writer goes through here, so the three can never disagree.
"""

from __future__ import annotations

from typing import Any

from sldb.store.hashing import hash_model_contract, hash_model_layer


def stamp_model_node(m_idx: Any, roster_hash: str, model_type: Any | None, entry: Any | None = None) -> None:
    """Record this model's roster, its contract and the node the two make up.

    `model_type` is None when the class cannot be imported (a broken or federated model): the
    contract already recorded is kept rather than being blanked, so an unimportable model does
    not report its contract as having changed. `entry`, the model's line in the store index,
    gets the family too: both record it.
    """
    m_idx.roster_hash = roster_hash
    m_idx.family = _declared_family(model_type) if model_type is not None else m_idx.family
    m_idx.contract_hash = hash_model_contract(model_type) if model_type is not None else m_idx.contract_hash
    m_idx.model_hash = hash_model_layer(m_idx.roster_hash, m_idx.contract_hash)
    if entry is not None:
        entry.family = m_idx.family


def _declared_family(model_type: Any) -> str | None:
    """The class's `__family__` as it is now: it used to be read only at `models add`, so a
    family changed in the class never reached the store (AgentsKBs, 2026-10-03)."""
    from sldb.api.model_registry.model_lineage import model_family

    return model_family(model_type)


def contract_moved(m_idx: Any, model_type: Any | None) -> bool:
    """Whether the class's contract now differs from the one the index recorded."""
    if model_type is None or not m_idx.contract_hash:
        return False
    return hash_model_contract(model_type) != m_idx.contract_hash
