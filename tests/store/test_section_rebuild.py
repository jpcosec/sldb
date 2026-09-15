from __future__ import annotations

from sldb.cli.graph_ops.extract import extract_sections
from sldb.store.section_rebuild import _extract_sections


def test_persisted_section_rebuild_matches_ir_paths_for_repeated_headings():
    markdown = "# Same\nfirst\n## Child\nbody\n# Same\nsecond\n"
    ir_paths = [section.path for section in extract_sections(markdown)]
    persisted_paths = [section["path"] for section in _extract_sections(markdown)]
    assert persisted_paths == ir_paths == ["same", "same/child", "same-2"]
