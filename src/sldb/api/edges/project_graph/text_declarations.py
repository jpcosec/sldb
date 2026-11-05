"""References read from a document's body: YAML blocks, sections and line mentions."""

from __future__ import annotations

import re

import yaml

from sldb.api.edges.project_graph.declaration import Declaration
from sldb.api.edges.project_graph.line_mentions import LineMentions
from sldb.api.edges.project_graph.mapping_declarations import MappingDeclarations
from sldb.api.edges.project_graph.section_mentions import SectionMentions

HEADING = re.compile(r"^(#{2,6})\s+(.+?)\s*$")
YAML_BLOCK = re.compile(r"```ya?ml\s*\n(?P<body>.*?)\n```", re.MULTILINE | re.DOTALL)


def yaml_block_declarations(text: str, mapping_declarations: MappingDeclarations) -> list[Declaration]:
    """Declarations of every fenced YAML block holding one mapping, located `line:N:yaml`."""
    declarations: list[Declaration] = []
    for match in YAML_BLOCK.finditer(text):
        try:
            loaded = list(yaml.safe_load_all(match.group("body")))
        except yaml.YAMLError:
            continue  # a block that is not YAML declares nothing
        if len(loaded) == 1 and isinstance(loaded[0], dict):
            line_number = text[: match.start()].count("\n") + 1
            declarations.extend(mapping_declarations(loaded[0], f"line:{line_number}:yaml"))
    return declarations


def section_declarations(lines: list[str], rule: SectionMentions) -> list[Declaration]:
    """Mentions on the lines below a heading the rule names, located `line:N:<heading>`."""
    declarations: list[Declaration] = []
    section: str | None = None
    for number, line in enumerate(lines, start=1):
        heading = HEADING.match(line)
        if heading:
            section = re.sub(r"\s+", " ", heading.group(2).strip().lower())
        elif section in rule.headings:
            locator = f"line:{number}:{section}"
            declarations.extend(Declaration(target, rule.role, locator) for pattern in rule.patterns for target in pattern.targets(line))
    return declarations


def line_declarations(lines: list[str], rule: LineMentions) -> list[Declaration]:
    """Mentions on every line except `---` fences and skipped frontmatter fields."""
    declarations: list[Declaration] = []
    in_frontmatter = False
    for number, line in enumerate(lines, start=1):
        if line == "---" and (number == 1 or in_frontmatter):
            in_frontmatter = number == 1
        elif not (in_frontmatter and line.split(":", 1)[0] in rule.skipped_frontmatter_fields):
            locator = f"line:{number}:{rule.locator}"
            declarations.extend(Declaration(target, rule.role, locator) for pattern in rule.patterns for target in pattern.targets(line))
    return declarations
