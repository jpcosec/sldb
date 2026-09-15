"""CliCommandDoc document contract."""
from __future__ import annotations

from pydantic import Field
from sldb.models.structured_doc import StructuredNLDoc
from .knowledge_tag import KnowledgeTag


class CliCommandDoc(StructuredNLDoc):
    """A single leaf CLI command as a self-describing knowledge entity.

    In the selfdoc workflow, the parser owns identity, synopsis, arguments, and
    provenance. Authors own purpose, how_it_works, usage examples, and tags.
    Regeneration preserves those authored fields instead of deriving semantics
    from option names. This contract does not itself populate argparse help.
    """

    __semantics__ = {
        "type": ["knowledge", "cli_command"],
        "workspace": ["knowledge", "commands"],
    }
    __template__ = """---
id: ⸢rev•id⸥
system: ⸢rev•system⸥
command_path: ⸢rev•command_path⸥
synopsis: ⸢rev•synopsis⸥
tags: ⸢rev•tags⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢render•command_path⸥

## Synopsis

⸢render•synopsis⸥

## Purpose

⸢rev•purpose⸥

## How It Works

⸢rev•how_it_works⸥

## Arguments

⸢rev•arguments⸥

## Usage

⸢rev•usage⸥
""".strip()

    id: str = Field(
        description="Stable id, conventionally 'cmd-<system>-<dashed-command-path>'."
    )
    system: str = Field(
        description="System/tool that owns this command (e.g. sldb, kgdb)."
    )
    command_path: str = Field(
        description="Full command path as invoked, space-separated (e.g. 'stores init')."
    )
    synopsis: str = Field(
        description="One-line help string; the argparse `help=` for this command."
    )
    purpose: str = Field(
        description="Why the command exists and what problem it solves."
    )
    how_it_works: str = Field(
        description="What the command does step by step and how it uses the store/graph."
    )
    arguments: str = Field(
        description=(
            "Markdown argument reference; selfdoc emits fenced JSON retaining "
            "argparse defaults, cardinality, choices, actions, and exclusive groups."
        )
    )
    usage: str = Field(
        description="Concrete example invocation(s) of the command."
    )
    tags: list[KnowledgeTag] = Field(
        default_factory=list,
        description="Namespaced semantic tags for retrieval and grouping.",
    )
    provenance: str | None = Field(
        default=None,
        description="Source reference; selfdoc stores the parser factory, command path, and contract hash.",
    )
