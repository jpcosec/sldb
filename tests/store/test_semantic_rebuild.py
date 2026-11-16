from __future__ import annotations

import logging
import shutil
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.store.layout import cache_dir
from sldb.store.section_rebuild import rebuild_sections_indexes

from sldb.store.semantic import RebuildReport
from sldb.store.section_rebuild import _extract_sections


class TestExtractSectionsEdgeCases:
    def test_plain_paragraph_no_headings(self):
        md = "This is a plain paragraph with no headings.\n\nJust text."
        sections = _extract_sections(md)
        assert sections == []

    def test_empty_string(self):
        sections = _extract_sections("")
        assert sections == []

    def test_only_thematic_breaks_and_code_blocks(self):
        md = "---\n\n```python\nprint('hello')\n```\n\n***"
        sections = _extract_sections(md)
        assert sections == []

    def test_heading_with_no_map_attribute(self):
        md = "# Title\n\nSome content."
        sections = _extract_sections(md)
        assert len(sections) == 1
        assert sections[0]["title"] == "Title"
        assert sections[0]["line_start"] is not None

    def test_single_heading(self):
        md = "# Hello\n\nWorld"
        sections = _extract_sections(md)
        assert len(sections) == 1
        assert sections[0]["title"] == "Hello"
        assert sections[0]["level"] == 1
        assert sections[0]["slug"] == "hello"
        assert sections[0]["path"] == "hello"

    def test_multiple_headings_with_hierarchy(self):
        md = "# A\n\n## B\n\n### C\n\n# D"
        sections = _extract_sections(md)
        assert len(sections) == 4
        assert sections[0]["path"] == "a"
        assert sections[1]["path"] == "a/b"
        assert sections[2]["path"] == "a/b/c"
        assert sections[3]["path"] == "d"

    def test_malformed_heading_no_title(self):
        md = "# \n\nContent after empty heading."
        sections = _extract_sections(md)
        assert sections == []


class TestRebuildReportDataclass:
    def test_default_values(self):
        r = RebuildReport()
        assert r.docs_processed == 0
        assert r.docs_skipped_missing == 0
        assert r.docs_empty_sections == 0
        assert r.headings_no_map == 0
        assert r.verbose == []

    def test_increment_fields(self):
        r = RebuildReport()
        r.docs_processed += 1
        r.docs_skipped_missing += 2
        r.docs_empty_sections += 1
        r.headings_no_map += 1
        r.verbose.append("test message")
        assert r.docs_processed == 1
        assert r.docs_skipped_missing == 2
        assert r.docs_empty_sections == 1
        assert r.headings_no_map == 1
        assert r.verbose == ["test message"]


MISSING_MODULE = "sldb_sections_missing_models"
_MISSING_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Note(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\n## What\\n\\n⸢rev•what⸥\\n"
    title: str = Field(description="Title.")
    what: str = Field(description="What.")
'''


def test_missing_documents_log_one_summary_warning(tmp_path, monkeypatch, caplog):
    """Five tracked documents whose files are gone: one warning that says 5, not five lines."""
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    (tmp_path / f"{MISSING_MODULE}.py").write_text(_MISSING_MODELS, encoding="utf-8")
    sys.path.insert(0, str(tmp_path))
    try:
        root = tmp_path / "world"
        root.mkdir()
        sp = api.init_store(root).store_path
        api.add_model(sp, f"{MISSING_MODULE}:Note", str(tmp_path))
        for i in range(5):
            api.create_document(sp, "Note", root / "notes" / f"n{i}.md", {"title": f"n{i}", "what": "W."}, f"n{i}", str(tmp_path))
            (root / "notes" / f"n{i}.md").unlink()
        shutil.rmtree(cache_dir(sp), ignore_errors=True)
        shutil.rmtree(tmp_path / "cache", ignore_errors=True)
        caplog.clear()
        with caplog.at_level(logging.WARNING, logger="sldb.store.section_sync"):
            report = rebuild_sections_indexes(sp, root, None, str(tmp_path))
        warnings = [r.getMessage() for r in caplog.records if r.name == "sldb.store.section_sync" and r.levelno == logging.WARNING]
        assert warnings == ["Sections rebuild: 5 documents missing on disk (Note: 5); e.g. notes/n0.md, notes/n1.md, notes/n2.md"]
        assert report.docs_skipped_missing == 5 and len(report.verbose) == 5
        assert sorted(report.missing_paths) == [f"notes/n{i}.md" for i in range(5)]
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MISSING_MODULE, None)
