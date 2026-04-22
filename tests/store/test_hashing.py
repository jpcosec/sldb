from pathlib import Path
from pydantic import Field
from sldb import StructuredNLDoc
from sldb.store.hashing import hash_text, hash_fields, hash_documents_index, hash_models_layer
from sldb.store.models import DocumentEntry, DocumentsIndex, ModelsIndex


class TitleDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Document title.")


def test_hash_text_deterministic():
    assert hash_text("hello") == hash_text("hello")


def test_hash_text_sensitive():
    assert hash_text("hello") != hash_text("world")


def test_hash_text_hex_64():
    h = hash_text("hello")
    assert len(h) == 64
    int(h, 16)


def test_hash_fields_deterministic():
    assert hash_fields(TitleDoc, "# Hello") == hash_fields(TitleDoc, "# Hello")


def test_hash_fields_ignores_non_field_content():
    assert hash_fields(TitleDoc, "# Hello\n\nextra text") == hash_fields(TitleDoc, "# Hello")


def test_hash_fields_differs_on_data_change():
    assert hash_fields(TitleDoc, "# Hello") != hash_fields(TitleDoc, "# World")


def test_hash_documents_index_deterministic():
    idx = DocumentsIndex(documents=[DocumentEntry(name="a", path="a.md", hash_c="cc", hash_d="dd")])
    assert hash_documents_index(idx) == hash_documents_index(idx)


def test_hash_documents_index_changes_on_inventory_change():
    idx1 = DocumentsIndex(documents=[DocumentEntry(name="a", path="a.md", hash_c="cc", hash_d="dd")])
    idx2 = DocumentsIndex(documents=[
        DocumentEntry(name="a", path="a.md", hash_c="cc", hash_d="dd"),
        DocumentEntry(name="b", path="b.md", hash_c="ee", hash_d="ff"),
    ])
    assert hash_documents_index(idx1) != hash_documents_index(idx2)


def test_hash_models_layer_deterministic():
    indices = [ModelsIndex(name="Book", model_ref="m:Book", path="p.py", documents_index="d.yaml", hash_b="hb1")]
    assert hash_models_layer(indices) == hash_models_layer(indices)


def test_hash_models_layer_changes_on_hash_b_change():
    a = [ModelsIndex(name="Book", model_ref="m:Book", path="p.py", documents_index="d.yaml", hash_b="hb1")]
    b = [ModelsIndex(name="Book", model_ref="m:Book", path="p.py", documents_index="d.yaml", hash_b="hb2")]
    assert hash_models_layer(a) != hash_models_layer(b)
