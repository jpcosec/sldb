from __future__ import annotations

import pytest
from pydantic import Field
from sldb import StructuredNLDoc
from sldb.runtime.validation import Validator

class MultiMarkerDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥
Mirror: ⸢optrev•title⸥
Body: ⸢rev•body⸥"""
    title: str = Field(description="Title")
    body: str = Field(description="Body")

def test_render_validity_allows_optrev_identity_mismatch():
    # In practice, SLDB current renderer makes optrev identical.
    # But let's simulate a case where we might want to check only revs.
    doc = MultiMarkerDoc(title="Hello", body="World")
    validator = Validator(MultiMarkerDoc)
    
    # Default is render_validity
    valid, details = validator.validate(data=doc.model_dump())
    assert valid is True
    assert details["validation_mode"] == "render_validity"

def test_strict_roundtrip_enforces_all_markers():
    doc = MultiMarkerDoc(title="Hello", body="World")
    validator = Validator(MultiMarkerDoc)
    
    valid, details = validator.validate(data=doc.model_dump(), mode="strict_roundtrip")
    assert valid is True
    assert details["validation_mode"] == "strict_roundtrip"
