"""The contract hash of rules-language.md §5: sha256 over a model's contract fields.

`__contract__` absent means every field of the subject's payload (the keys of its
`field_hashes`); declared and empty is an error (H11: `ValueError`); a listed field the
payload lacks contributes `<field>=` with an empty hash.
"""

from __future__ import annotations

import hashlib


def contract_hash(model_type: type, field_hashes: dict[str, str]) -> str:
    """The sha256 of `<field>=<hash>` lines ordered by the field name's UTF-8 bytes."""
    fields = contract_fields(model_type, field_hashes)
    lines = [f"{name}={field_hashes.get(name, '')}" for name in sorted(fields, key=lambda n: n.encode("utf-8"))]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()


def contract_fields(model_type: type, field_hashes: dict[str, str]) -> list[str]:
    """The fields a model's contract covers."""
    if not hasattr(model_type, "__contract__"):
        return list(field_hashes)
    declared = list(getattr(model_type, "__contract__"))
    if not declared:
        raise ValueError(f"{getattr(model_type, '__name__', model_type)}.__contract__ is empty: declare at least one field or leave it out")
    return declared
