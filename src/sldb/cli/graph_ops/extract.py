import re
from sldb.core.ast import AST_Handler
from sldb.cli.section_record_cls import SectionRecord
from .utils import _slugify

def extract_sections(markdown: str) -> list[SectionRecord]:
    nodes = AST_Handler().split_nodes(markdown)
    sections: list[SectionRecord] = []
    stack: list[SectionRecord] = []
    for node in nodes:
        _process_node(node, stack, sections)
    _extend_section_spans(sections, len(markdown.splitlines()))
    return sections

def _process_node(node, stack, sections):
    if not re.fullmatch(r"h[1-6]", node.tag or ""): return
    title = (node.find_leaf_text() or node.content or "").strip()
    if not title: return
    _build_section(node, title, stack, sections)

def _build_section(node, title, stack, sections):
    level = int(node.tag[1])
    while stack and stack[-1].level >= level: stack.pop()
    slug = _unique_slug(_slugify(title), stack, sections)
    path = _build_path(stack, slug)
    _finalize_section(node, title, slug, level, path, stack, sections)

def _build_path(stack, slug):
    parent = "/".join(item.slug for item in stack)
    return f"{parent}/{slug}" if parent else slug


def _unique_slug(slug: str, stack: list[SectionRecord], sections: list[SectionRecord]) -> str:
    parent = "/".join(item.slug for item in stack)
    candidate, number = slug, 2
    while _build_path(stack, candidate) in {section.path for section in sections}:
        candidate = f"{slug}-{number}"
        number += 1
    return candidate

def _finalize_section(node, title, slug, level, path, stack, sections):
    start = node.map[0] + 1 if node.map else None
    end = node.map[1] + 1 if node.map else None
    section = SectionRecord(
        title=title, slug=slug, level=level,
        path=path, line_start=start, line_end=end,
    )
    sections.append(section)
    stack.append(section)


def _extend_section_spans(sections: list[SectionRecord], last_line: int) -> None:
    for index, section in enumerate(sections):
        next_start = _next_boundary(sections[index + 1 :], section.level)
        section.line_end = (next_start - 1) if next_start is not None else last_line


def _next_boundary(sections: list[SectionRecord], level: int) -> int | None:
    return next((item.line_start for item in sections if item.level <= level and item.line_start is not None), None)
