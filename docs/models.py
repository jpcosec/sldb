from __future__ import annotations

from typing import Any

from pydantic import Field

from sldb import StructuredNLDoc


class ArchitectureNarrativeDoc(StructuredNLDoc):
    __authority__ = "authored"
    __semantics__ = {
        "type": ["documentation", "architecture"],
        "workspace": ["docs", "architecture"],
    }
    __template__ = """
# ⸢rev•title⸥

⸢rev•body⸥
""".strip()

    title: str = Field(description="Primary H1 heading for the document.")
    body: str = Field(
        description="Narrative document body after the H1, including subsections, lists, tables, and code fences."
    )


class ArchitectureDoc(ArchitectureNarrativeDoc):
    pass


class ArchitectureDiagramDoc(StructuredNLDoc):
    __authority__ = "authored"
    __semantics__ = {
        "type": ["documentation", "architecture"],
        "workspace": ["docs", "architecture"],
    }
    __template__ = """
# ⸢rev•title⸥

⸢rev•intro⸥

```mermaid
⸢rev•diagram⸥
```
""".strip()

    title: str = Field(description="Primary H1 heading for the diagram document.")
    intro: str = Field(description="Introductory paragraph before the Mermaid diagram.")
    diagram: str = Field(
        description="Mermaid diagram body without the code fence wrapper."
    )


class ArchitectureDiagramWithHighlightsDoc(StructuredNLDoc):
    __authority__ = "authored"
    __semantics__ = {
        "type": ["documentation", "architecture"],
        "workspace": ["docs", "architecture"],
    }
    __template__ = """
# ⸢rev•title⸥

⸢rev•intro⸥

```mermaid
⸢rev•diagram⸥
```

### Component Highlights

1. ⸢rev,list•highlights⸥
""".strip()

    title: str = Field(description="Primary H1 heading for the diagram document.")
    intro: str = Field(description="Introductory paragraph before the Mermaid diagram.")
    diagram: str = Field(
        description="Mermaid diagram body without the code fence wrapper."
    )
    highlights: list[str] = Field(
        description="Ordered highlight items after the diagram."
    )


class CLITreeDoc(StructuredNLDoc):
    __semantics__ = {
        "type": ["documentation", "architecture"],
        "workspace": ["docs", "architecture"],
    }
    __template__ = """
# ⸢rev•title⸥

```text
⸢rev•cli_tree⸥
```

## Command Groups

- ⸢rev,list•command_groups⸥
""".strip()

    title: str = Field(description="Primary H1 heading for the CLI tree document.")
    cli_tree: str = Field(
        description="Rendered CLI tree without the fenced code wrapper."
    )
    command_groups: list[str] = Field(
        description="Bullet list describing command group categories."
    )


class SourceTreeDoc(StructuredNLDoc):
    __semantics__ = {
        "type": ["documentation", "architecture"],
        "workspace": ["docs", "architecture"],
    }
    __template__ = """
# ⸢rev•title⸥

## Repository Distribution

```text
⸢rev•repository_distribution⸥
```

## Module Roles

⸢rev•module_roles⸥
""".strip()

    title: str = Field(description="Primary H1 heading for the source tree document.")
    repository_distribution: str = Field(
        description="Source tree snapshot without the fenced code wrapper."
    )
    module_roles: str = Field(
        description="Narrative explanation of the module roles section."
    )


class PackagingDoc(StructuredNLDoc):
    __authority__ = "authored"
    __semantics__ = {
        "type": ["documentation", "packaging"],
        "workspace": ["docs", "packaging"],
    }
    __template__ = """
# ⸢rev•title⸥

⸢rev•body⸥
""".strip()

    title: str = Field(description="Primary H1 heading for the packaging guide.")
    body: str = Field(
        description="Full packaging guide body after the H1, including checklists, sections, and code blocks."
    )


class AtomicDocumentDoc(StructuredNLDoc):
    __authority__ = "authored"
    __semantics__ = {
        "type": ["documentation", "atom"],
        "workspace": ["docs", "atoms"],
    }
    __template__ = """
# ⸢rev•title⸥

## Related Concepts

- ⸢rev,list•related_concepts⸥

## What It Is

⸢rev•what_it_is⸥

## Why It Matters

⸢rev•why_it_matters⸥

## How It Works

⸢rev•how_it_works⸥

## When It Shows Up

⸢rev•when_it_shows_up⸥

## Where It Lives

⸢rev•where_it_lives⸥

## Who Uses It

⸢rev•who_uses_it⸥
""".strip()

    title: str = Field(description="Primary H1 heading for the atomic knowledge document.")
    related_concepts: list[str] = Field(
        description="Short list of adjacent concepts that connect this atom to the wider SLDB knowledge graph."
    )
    what_it_is: str = Field(
        description="Direct definition of the concept without workflow preamble or surrounding history."
    )
    why_it_matters: str = Field(
        description="Reason this concept exists and what user or system confusion it prevents."
    )
    how_it_works: str = Field(
        description="Operational explanation of the mechanism or contract that the concept represents."
    )
    when_it_shows_up: str = Field(
        description="Concrete moments in the SLDB workflow where a user or command encounters this concept."
    )
    where_it_lives: str = Field(
        description="Physical or logical location where the concept is materialized in files, commands, or runtime structures."
    )
    who_uses_it: str = Field(
        description="Primary consumers of the concept and the practical outcome they get from it."
    )


class PlanDoc(StructuredNLDoc):
    __authority__ = "authored"
    __semantics__ = {
        "type": ["documentation", "plan"],
        "workspace": ["docs", "superpowers"],
    }
    __template__ = """
# ⸢rev•title⸥

⸢rev•body⸥
""".strip()

    title: str = Field(description="Primary H1 heading for the plan document.")
    body: str = Field(
        description="Full plan body after the H1, including quoted guidance, checklists, tables, and code blocks."
    )


class SpecDoc(StructuredNLDoc):
    __authority__ = "authored"
    __semantics__ = {
        "type": ["documentation", "spec"],
        "workspace": ["docs", "superpowers"],
    }
    __template__ = """
# ⸢rev•title⸥

⸢rev•body⸥
""".strip()

    title: str = Field(description="Primary H1 heading for the spec document.")
    body: str = Field(
        description="Full spec body after the H1, including sections, tables, and explanatory prose."
    )


class RequestDoc(StructuredNLDoc):
    __authority__ = "authored"
    __semantics__ = {
        "type": ["documentation", "request"],
        "workspace": ["docs", "requests"],
    }
    __template__ = """
---
⸢rev,dict•frontmatter⸥
---

# ⸢rev•title⸥

⸢rev•body⸥
""".strip()

    frontmatter: dict[str, Any] = Field(
        description="Top-level YAML frontmatter carried by the request document."
    )
    title: str = Field(description="Primary H1 heading for the request document.")
    body: str = Field(
        description="Full request body after the H1, including proposal sections, examples, tables, and code blocks."
    )


class FAQDoc(StructuredNLDoc):
    __authority__ = "authored"
    __semantics__ = {
        "type": ["documentation", "faq"],
        "workspace": ["docs", "faq"],
    }
    __template__ = """
# ⸢rev•title⸥

⸢rev•body⸥
""".strip()

    title: str = Field(description="Primary H1 heading for the FAQ document.")
    body: str = Field(
        description="Full FAQ body after the H1, including subsections, code blocks, and examples."
    )


class StoreReadmeDoc(StructuredNLDoc):
    __authority__ = "authored"
    __semantics__ = {
        "type": ["documentation", "store"],
        "workspace": ["sldb", "store"],
    }
    __template__ = """
# ⸢rev•title⸥

## Purpose

⸢rev•purpose⸥

## Layout Summary

⸢rev•layout_summary⸥

## Durable Core (`.sldb/core`)

⸢rev•core_contract⸥

## Runtime State (`.sldb/runtime`)

⸢rev•runtime_contract⸥

## Local Config (`.sldb/.config`)

⸢rev•local_config_contract⸥

## Promotion Rules

⸢rev•promotion_rules⸥

## Git Policy

⸢rev•git_policy⸥

## Command Map

⸢rev•command_map⸥

## Migration Status

⸢rev•migration_status⸥
""".strip()

    title: str = Field(description="Primary H1 heading for the store README.")
    purpose: str = Field(
        description="Why the store exists and how it should be used as the project-local SLDB workspace."
    )
    layout_summary: str = Field(
        description="Concrete overview of the intended store layout, including subtree responsibilities and examples."
    )
    core_contract: str = Field(
        description="Durable contract for what belongs under .sldb/core and what must stay out of it."
    )
    runtime_contract: str = Field(
        description="Operational contract for ephemeral runtime state under .sldb/runtime, including rebuild and cleanup expectations."
    )
    local_config_contract: str = Field(
        description="Local-machine contract for .sldb/.config, including override rules and non-shared state."
    )
    promotion_rules: str = Field(
        description="Rules for promoting drafts or generated state into durable tracked artifacts."
    )
    git_policy: str = Field(
        description="Commit and ignore policy across .sldb/core, .sldb/runtime, and .sldb/.config."
    )
    command_map: str = Field(
        description="Command-oriented guidance for common store operations and index rebuild flows."
    )
    migration_status: str = Field(
        description="Current migration posture, including transitional notes while the flat store implementation is still being refactored."
    )
