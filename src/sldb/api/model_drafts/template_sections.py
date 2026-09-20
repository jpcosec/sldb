"""The `## Title` template section `add_model_field` appends (and `remove_model_field` drops).

A field only round-trips when its marker is in `__template__`, so a field edit must also
edit the template. These helpers build the section and pick the marker that matches the
field's annotation: a scalar `rev`, a `rev,list` bullet, a `rev,dict` YAML block, or a
`rev,table` for `list[dict]`.
"""

from __future__ import annotations

import re


def marker_kind(field_type: str) -> str:
    """Which reversible marker a field's annotation needs: rev, list, dict or table."""
    t = field_type.strip().replace(" ", "")
    if t.startswith("list[") and t.endswith("]"):
        return "table" if t[5:-1].startswith("dict") else "list"
    if t.startswith("dict"):
        return "dict"
    return "rev"


def section_for_field(field_name: str, field_type: str, optional: bool = False) -> str:
    """The `## Title` section a field renders from, with its marker.

    A field with a default is optional in the document, so it gets the `optrev` marker
    family; a missing section then falls back to the default instead of failing to parse.
    """
    title = field_name.replace("_", " ").capitalize()
    prefix = "optrev" if optional else "rev"
    return f"## {title}\n\n{_body(field_name, prefix, marker_kind(field_type))}"


def append_section(template: str, section: str) -> str:
    """The template with `section` appended, separated by a blank line."""
    return section if not template else template.rstrip("\n") + "\n\n" + section


def remove_field_section(template: str, field_name: str) -> str:
    """The template without the field's section (heading + marker, up to the next heading)."""
    lines = template.split("\n")
    marker_line = next((i for i, line in enumerate(lines) if _has_marker(line, field_name)), None)
    if marker_line is None:
        return template
    heading = _heading_before(lines, marker_line)
    if heading is None:
        del lines[marker_line]
        return "\n".join(lines).rstrip("\n")
    del lines[heading : _next_heading(lines, marker_line)]
    return "\n".join(lines).rstrip("\n")


def _body(field_name: str, prefix: str, kind: str) -> str:
    if kind == "list":
        return f"- ⸢{prefix},list•{field_name}⸥"
    if kind == "dict":
        return f"```yaml\n⸢{prefix},dict•{field_name}⸥\n```"
    if kind == "table":
        return f"⸢{prefix},table•{field_name}⸥"
    return f"⸢{prefix}•{field_name}⸥"


def _has_marker(line: str, field_name: str) -> bool:
    return re.search(r"⸢[^⸥]*•" + re.escape(field_name) + r"⸥", line) is not None


def _heading_before(lines: list[str], start: int) -> int | None:
    for i in range(start, -1, -1):
        if re.match(r"#{1,6} ", lines[i].lstrip()):
            return i
    return None


def _next_heading(lines: list[str], start: int) -> int:
    for i in range(start + 1, len(lines)):
        if re.match(r"#{1,6} ", lines[i].lstrip()):
            return i
    return len(lines)
