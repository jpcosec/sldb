from __future__ import annotations

from pathlib import Path

import pytest

from sldb.store.semantic import RebuildReport, _extract_sections


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
