"""Self-describing knowledge models for turning a program into a knowledge entity.

These models let any app that uses `knowledge` document its own CLI surfaces and
commands as tracked SLDB documents. The structure is designed so that a command's
`--help` text can be populated from the document (and vice versa), making each app
a self-aware knowledge entity over sldb+kgdb.

Model tree:
- SurfaceDoc: one CLI surface / subsystem (README-equivalent for a command group).
- CliCommandDoc: one leaf command (populates and mirrors argparse --help).
"""

from __future__ import annotations

from typing import Annotated

from pydantic import Field

from sldb import StructuredNLDoc

KnowledgeTag = Annotated[
    str,
    Field(
        pattern=r"^[a-z][a-z0-9_]*:[a-z][a-z0-9_.-]*$",
        description="Namespaced semantic tag in the form namespace:value.",
    ),
]


class SurfaceDoc(StructuredNLDoc):
    """A CLI surface / subsystem: the README-equivalent for a command group."""

    __semantics__ = {
        "type": ["knowledge", "surface"],
        "workspace": ["knowledge", "surfaces"],
    }
    __template__ = """---
id: ⸢rev•id⸥
system: ⸢rev•system⸥
surface: ⸢rev•surface⸥
tags: ⸢rev•tags⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢render•surface⸥

## Purpose

⸢rev•purpose⸥

## How It Works

⸢rev•how_it_works⸥

## Commands

⸢rev•commands⸥
""".strip()

    id: str = Field(
        description="Stable id, conventionally 'surface-<system>-<surface>'."
    )
    system: str = Field(
        description="System/tool that owns this surface (e.g. sldb, kgdb)."
    )
    surface: str = Field(
        description="Surface/command-group name as exposed by the CLI (e.g. stores, docs)."
    )
    purpose: str = Field(
        description="Why this surface exists and what capability it groups."
    )
    how_it_works: str = Field(
        description="How the surface operates and how its commands relate."
    )
    commands: str = Field(
        description="Newline list of leaf command names in this surface."
    )
    tags: list[KnowledgeTag] = Field(
        default_factory=list,
        description="Namespaced semantic tags for retrieval and grouping.",
    )
    provenance: str | None = Field(
        default=None,
        description="Path to the code that implements this surface (parser + handlers).",
    )


class CliCommandDoc(StructuredNLDoc):
    """A single leaf CLI command as a self-describing knowledge entity.

    The document is the single source of truth for the command's help: `synopsis`
    maps to the one-line argparse help, `purpose`/`how_it_works` back the long
    description, and `arguments` mirrors the argparse options so `--help` can be
    populated from the document.
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
            "Newline list of arguments, one per line as "
            "'<name> | required|optional | <help>', mirroring argparse."
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
        description="Path to the code that implements this command (parser + handler).",
    )


class AnchorDoc(StructuredNLDoc):
    """Binds a grammar symbol to a semantic motive and a resolvable referent.

    Implements the knowledge core anchor contract: kind partitions what the
    symbol can refer to, ref is a typed string with a kind-specific scheme,
    and motive keeps the grammar legible and auditable.
    """

    __semantics__ = {
        "type": ["knowledge", "anchor"],
        "workspace": ["knowledge", "anchors"],
    }
    __template__ = """---
id: ⸢rev•id⸥
symbol: ⸢rev•symbol⸥
kind: ⸢rev•kind⸥
ref: ⸢rev•ref⸥
tags: ⸢rev•tags⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢render•symbol⸥

## Motive

⸢rev•motive⸥
""".strip()

    id: str = Field(
        description="Stable id, conventionally 'anchor-<symbol>'."
    )
    symbol: str = Field(
        description="The grammar symbol this anchor defines (e.g. user, check, preferences)."
    )
    kind: str = Field(
        pattern=r"^(model|doc|relation|operation|projection|expr)$",
        description="What class of referent the symbol names: model | doc | relation | operation | projection | expr (a derived relation: an s-expression template with _ holes).",
    )
    ref: str = Field(
        pattern=r"^(model:[A-Za-z_][A-Za-z0-9_]*|doc:[a-z0-9-]+|edge:[a-z_]+(:(in|out))?|op:[a-z_]+|fields:[a-z_,]+|view:[a-z_]+|expr:[(].+[)])$",
        description="Typed referent: model:<Name> | doc:<name> | edge:<rel>[:dir] | op:<fn> | fields:<f1,f2> | view:<name> | expr:(<s-expression with _ holes>).",
    )
    motive: str = Field(
        description="Natural-language meaning of the symbol: what it refers to and why, legible to humans."
    )
    tags: list[KnowledgeTag] = Field(
        default_factory=list,
        description="Namespaced semantic tags for retrieval and grouping.",
    )
    provenance: str | None = Field(
        default=None,
        description="Source of this anchor definition (spec section or code path).",
    )
