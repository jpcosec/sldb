from __future__ import annotations

import pytest
from sldb.core.ast import AST_Handler
from sldb.core.template_extractor import TemplateExtractor
from sldb.core.exceptions import SLDBASTError

def test_duplicate_rev_markers_fail():
    template = "⸢rev•field1⸥ and ⸢rev•field1⸥"
    ast = AST_Handler()
    extractor = TemplateExtractor()
    
    with pytest.raises(SLDBASTError, match="Multiple canonical 'rev' markers found for field 'field1'"):
        extractor.extract_nodes(ast.split_nodes(template))

def test_orphaned_optrev_fails():
    template = "⸢optrev•field1⸥ without rev"
    ast = AST_Handler()
    extractor = TemplateExtractor()
    
    with pytest.raises(SLDBASTError, match="Optional 'optrev' markers found for fields without a canonical 'rev' source: field1"):
        extractor.extract_nodes(ast.split_nodes(template))

def test_valid_rev_and_optrev_pass():
    template = "⸢rev•field1⸥ and ⸢optrev•field1⸥"
    ast = AST_Handler()
    extractor = TemplateExtractor()
    
    recipes = extractor.extract_nodes(ast.split_nodes(template))
    assert len(recipes) == 1 # Combined in one text block
    assert len(recipes[0]["props"]) == 2

def test_multiple_optrev_with_one_rev_pass():
    template = "⸢rev•field1⸥ then ⸢optrev•field1⸥ then ⸢optrev•field1⸥"
    ast = AST_Handler()
    extractor = TemplateExtractor()
    
    recipes = extractor.extract_nodes(ast.split_nodes(template))
    assert len(recipes) == 1
