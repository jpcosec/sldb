"""SurfaceDoc document contract."""
from __future__ import annotations

from pydantic import Field
from sldb.models.structured_doc import StructuredNLDoc
from .knowledge_tag import KnowledgeTag


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
