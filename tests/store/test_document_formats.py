from sldb.models.python_symbol_doc import PythonSymbolDoc
from sldb.models.structured_doc import StructuredNLDoc
from sldb.store.semantic_tags import flatten_model_semantics


def test_document_format_is_inherited_and_code_adapter_overrides_source():
    assert flatten_model_semantics(StructuredNLDoc) == [
        "representation.markdown",
        "source.document.markdown",
    ]
    assert flatten_model_semantics(PythonSymbolDoc) == [
        "representation.markdown",
        "source.code.python",
        "type.knowledge.code_symbol",
        "workspace.knowledge.symbols",
    ]
