from pydantic import Field

from sldb import StructuredNLDoc


class RitualDoc(StructuredNLDoc):
    __semantics__ = {"type": ["workflow", "ritual"], "workspace": ["desk"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥

## Purpose

⸢rev•purpose⸥

## Trigger

⸢rev•trigger⸥

## Preconditions

- ⸢rev,list•preconditions⸥

## Steps

1. ⸢rev,list•steps⸥

## Validation

- ⸢rev,list•validation⸥

## Failure Modes

- ⸢rev,list•failure_modes⸥

## Completion

⸢rev•completion⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    title: str = Field(description="Short ritual title.")
    id: str = Field(description="Stable ritual identifier.")
    purpose: str = Field(description="Why the ritual exists.")
    trigger: str = Field(description="When the ritual should be started.")
    preconditions: list[str] = Field(
        default_factory=list,
        description="Conditions that must hold before running the ritual.",
    )
    steps: list[str] = Field(
        default_factory=list,
        description="Ordered steps to execute as part of the ritual.",
    )
    validation: list[str] = Field(
        default_factory=list,
        description="Checks that confirm the ritual was performed correctly.",
    )
    failure_modes: list[str] = Field(
        default_factory=list,
        description="Common mistakes, drifts, or anti-patterns to avoid.",
    )
    completion: str = Field(
        description="What indicates that the ritual has been completed."
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'layer:workflow' or 'system:sldb'.",
    )
