from pydantic import Field

from sldb import StructuredNLDoc


class PillDoc(StructuredNLDoc):
    __semantics__ = {"type": ["workflow", "pill"], "workspace": ["desk"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥

## What

⸢rev•what⸥

## Why

⸢rev•why⸥

## When

⸢rev•when⸥

## Where

⸢rev•where⸥

## How

⸢rev•how⸥

## How Not

⸢rev•how_not⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    title: str = Field(
        description="Pill title, including semantic prefix when useful, such as 'ADR:' or 'Pattern:'."
    )
    id: str = Field(description="Stable pill identifier.")
    what: str = Field(description="What the pill defines or clarifies.")
    why: str = Field(
        description="Why this context matters for implementation or refactoring."
    )
    when: str = Field(description="When this pill should be applied.")
    where: str = Field(
        description="Where this pill applies, either as general scope or as references to existing code or docs."
    )
    how: str = Field(description="How to apply the guidance in practice.")
    how_not: str = Field(description="How not to apply the guidance or what to avoid.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'language:python' or 'library:pydantic'.",
    )
