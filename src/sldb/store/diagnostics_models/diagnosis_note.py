from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum


class DiagnosisNote(str, Enum):
    """Enumeration of diagnostic outcomes for documents."""
    OK = 'ok'
    BENIGN_MUTATION = 'benign_mutation'
    DATA_MUTATION = 'data_mutation'
    CONTRACT_MUTATION = 'contract_mutation'
    MISSING = 'missing'
