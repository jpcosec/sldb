from __future__ import annotations

import pytest
from sldb.cli import main as cli_main
from pathlib import Path

def test_store_check_yaml_format(tmp_path, capsys):
    root = tmp_path / "root"
    root.mkdir()
    cli_main(["stores", "init", "--path", str(root)])
    
    # A new, empty store is sealed at init, so it checks valid
    assert cli_main(["stores", "check", "--store", str(root / ".sldb"), "--format", "yaml"]) == 0
    
    captured = capsys.readouterr()
    assert "hash_a_ok: true" in captured.out
    assert "models:" in captured.out

def test_recover_links_only(tmp_path, capsys):
    doc = tmp_path / "test.md"
    doc.write_text("# Test\n[[target1]]\n[[target2]]")
    
    exit_code = cli_main(["docs", "recover", str(doc), "--links-only"])
    assert exit_code == 1 # unresolved
    captured = capsys.readouterr()
    assert "target1" in captured.out
    assert "target2" in captured.out
    assert "link:" not in captured.out

def test_recover_depth(tmp_path, capsys):
    doc1 = tmp_path / "doc1.md"
    doc2 = tmp_path / "doc2.md"
    doc1.write_text("# Doc 1\n[[doc2.md]]")
    doc2.write_text("# Doc 2\n[[target3]]")
    
    # depth 1 (default) only sees doc2
    cli_main(["docs", "recover", str(doc1)])
    captured = capsys.readouterr()
    assert "doc2.md" in captured.out
    assert "target3" not in captured.out
    
    # depth 2 sees both
    cli_main(["docs", "recover", str(doc1), "--depth", "2"])
    captured = capsys.readouterr()
    assert "doc2.md" in captured.out
    assert "target3" in captured.out
