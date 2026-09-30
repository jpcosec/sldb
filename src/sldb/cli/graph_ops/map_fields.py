import logging
import re
from sldb.core.contracts import MARKER_PATTERN, parse_marker
from .extract import extract_sections

logger = logging.getLogger(__name__)

def _field_template_line_map(markdown: str, known_fields: set[str] | None = None) -> dict[str, int]:
    field_lines: dict[str, int] = {}
    for line_no, line in enumerate(markdown.split("\n"), 1):
        for match in re.finditer(MARKER_PATTERN, line):
            _process_marker(match, line_no, known_fields, field_lines)
    return field_lines

def _process_marker(match, line_no, known_fields, field_lines):
    marker = parse_marker(match.group(1))
    if marker.kind not in ("rev", "optrev") or not marker.name: return
    if known_fields is not None and marker.name not in known_fields:
        logger.warning("Template marker '%s' references unknown field '%s'", match.group(0), marker.name)
    field_lines[marker.name] = line_no

def _map_fields_to_sections(template: str, sections: list, known_fields: set[str] | None = None) -> dict[str, str]:
    field_lines = _field_template_line_map(template, known_fields=known_fields)
    template_sections = extract_sections(template)
    owners = _template_field_owners(field_lines, template_sections)
    return _rendered_owner_paths(owners, template_sections, sections)


def _template_field_owners(field_lines: dict[str, int], sections: list) -> dict[str, int]:
    heading_lines = [(section.line_start, index) for index, section in enumerate(sections)]
    result: dict[str, int] = {}
    for field_path, line_no in field_lines.items():
        owner = _previous_heading(line_no, heading_lines)
        if owner is not None:
            result[field_path] = owner
    return result


def _previous_heading(line_no: int, heading_lines: list[tuple[int | None, int]]) -> int | None:
    return next((index for heading_line, index in reversed(heading_lines) if heading_line is not None and heading_line <= line_no), None)


def _rendered_owner_paths(owners: dict[str, int], template_sections: list, rendered_sections: list) -> dict[str, str]:
    """Each template section's path in the rendered document, or {} when it cannot be told.

    The counts legitimately differ: a field value can hold a whole markdown document, and
    its headings are not template sections. Refusing outright lost the ownership of every
    field in such a document (16 of this repo's 1550, 60 fields).
    """
    if not _correspond(template_sections, rendered_sections):
        logger.warning("Cannot map template fields: template has %s headings but rendered document has %s", len(template_sections), len(rendered_sections))
        return {}
    return {
        field_path: rendered_sections[section_index].path
        for field_path, section_index in owners.items()
    }


def _correspond(template_sections: list, rendered_sections: list) -> bool:
    """Whether the sections at the template's indices are the template's own sections.

    With a single template section this is provable: there is one candidate owner, so
    extra headings -- which can only come from a field value, rendered inside it -- cannot
    displace it, and the only thing left to check is that the level is the right one.

    With more sections it is not: a heading injected by a field value can take a template
    slot and the mapping would be silently wrong, which is the defect this guard exists
    for. There it keeps refusing instead of guessing.
    """
    if len(rendered_sections) < len(template_sections):
        return False
    if len(template_sections) == 1:
        return template_sections[0].level == rendered_sections[0].level
    return len(template_sections) == len(rendered_sections)
