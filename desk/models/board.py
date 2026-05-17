from pydantic import Field

from sldb import StructuredNLDoc


class BoardDoc(StructuredNLDoc):
    __semantics__ = {"type": ["workflow", "board"], "workspace": ["desk"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥
Scope: ⸢rev•scope⸥

## Purpose

⸢rev•purpose⸥

## Tasks

- ⸢rev,list•tasks⸥

## Pills

- ⸢rev,list•pills⸥

## Rituals

- ⸢rev,list•rituals⸥

## Notes

⸢rev•notes⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    title: str = Field(description="Board title for one active routing surface.")
    id: str = Field(description="Stable board identifier.")
    scope: str = Field(description="What area or workspace this board routes.")
    purpose: str = Field(description="Why this board exists and what it indexes.")
    tasks: list[str] = Field(
        default_factory=list,
        description="Active task document references routed by this board.",
    )
    pills: list[str] = Field(
        default_factory=list,
        description="Active pill document references routed by this board.",
    )
    rituals: list[str] = Field(
        default_factory=list,
        description="Ritual document references relevant to this board.",
    )
    notes: str = Field(
        default="No additional notes.",
        description="Short operational notes about the current routed set.",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'system:sldb' or 'workspace:desk'.",
    )
