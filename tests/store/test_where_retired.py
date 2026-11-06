"""GO10: the old query languages are gone from `src/` and `docs/` (rules-language.md §7).

Two greps, as the acceptance fixes them. The identifiers `where_parse` and `FieldCondition`
(substrings, prose included: they are code names) appear nowhere in `src/` or `docs/`; the
eight old operator names, as whole words, appear in no fenced block or inline code span of a
Markdown file of `docs/`. The one exception is the rows of the historical equivalence table of
`docs/architecture/rules-language.md`, under a heading that says "Histórico".
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HISTORIC_DOC = ROOT / "docs" / "architecture" / "rules-language.md"
IDENTIFIERS = re.compile(r"where_parse|FieldCondition")
OPERATORS = re.compile(r"(?<!\w)(eq|ne|gt|lt|contains|starts_with|is_null|is_not_null)(?!\w)")
INLINE = re.compile(r"(`+)(.+?)\1", re.S)
HEADING = re.compile(r"^(#{1,6})\s")


def _historic_rows(path: Path, lines: list[str]) -> set[int]:
    """Line numbers of the table rows under the "Histórico" heading (only in the one doc)."""
    if path != HISTORIC_DOC:
        return set()
    rows, level = set(), None
    for number, line in enumerate(lines, 1):
        heading = HEADING.match(line)
        if heading:
            depth = len(heading.group(1))
            if level is not None and depth <= level:
                level = None
            if re.search(r"Hist[óo]rico", line):
                level = depth
        elif level is not None and line.lstrip().startswith("|"):
            rows.add(number)
    return rows


def _code(lines: list[str]) -> list[tuple[int, str]]:
    """`(line number, code)` for every fenced line and every inline code span."""
    found, fence, paragraph = [], None, []

    def flush() -> None:
        if paragraph:
            first, text = paragraph[0][0], "\n".join(line for _, line in paragraph)
            found.extend((first + text.count("\n", 0, m.start()), m.group(2)) for m in INLINE.finditer(text))
            paragraph.clear()

    for number, line in enumerate(lines, 1):
        stripped = line.lstrip()
        if fence:
            fence = None if stripped.startswith(fence) else fence
            if fence:
                found.append((number, line))
        elif stripped.startswith(("```", "~~~")):
            flush()
            fence = stripped[:3]
        elif not stripped:
            flush()
        else:
            paragraph.append((number, line))
    flush()
    return found


def _files(*folders: str):
    for folder in folders:
        yield from (p for p in sorted((ROOT / folder).rglob("*")) if p.is_file() and "__pycache__" not in p.parts)


def test_no_old_identifier_in_src_or_docs():
    hits = []
    for path in _files("src", "docs"):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        historic = _historic_rows(path, lines)
        hits += [f"{path.relative_to(ROOT)}:{n}" for n, line in enumerate(lines, 1) if IDENTIFIERS.search(line) and n not in historic]
    assert hits == []


def test_no_old_operator_in_the_code_of_docs():
    hits = []
    for path in (p for p in _files("docs") if p.suffix == ".md"):
        lines = path.read_text(encoding="utf-8").splitlines()
        historic = _historic_rows(path, lines)
        hits += [f"{path.relative_to(ROOT)}:{n}: {m.group(1)}" for n, code in _code(lines) if n not in historic for m in OPERATORS.finditer(code)]
    assert hits == []
