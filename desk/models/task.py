from pydantic import Field

from sldb import StructuredNLDoc


class TaskDoc(StructuredNLDoc):
    __semantics__ = {"type": ["workflow", "task"], "workspace": ["desk"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥
Status: ⸢rev•status⸥

## Goal

⸢rev•goal⸥

## Scope

⸢rev•scope⸥

## References

- ⸢rev,list•references⸥

## Dependencies

- ⸢rev,list•depends_on⸥

## Pills

- ⸢rev,list•pills⸥

## Files

- ⸢rev,list•files⸥

## Implementation Path

⸢rev•implementation_path⸥

## Validation

- ⸢rev,list•validation⸥

## Done When

⸢rev•done_when⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    title: str = Field(description="Short action-oriented task title.")
    id: str = Field(description="Stable task identifier.")
    status: str = Field(description="Current task state, typically active or blocked.")
    goal: str = Field(description="Concrete intended result for the task.")
    scope: str = Field(description="What is in and out of scope for the task.")
    references: list[str] = Field(
        default_factory=list,
        description="Relevant references such as files, docs, commits, or commands.",
    )
    depends_on: list[str] = Field(
        default_factory=list,
        description="Task identifiers that must complete first.",
    )
    pills: list[str] = Field(
        default_factory=list,
        description="Pill identifiers required for safe execution of the task.",
    )
    files: list[str] = Field(
        default_factory=list,
        description="Files or paths expected to change during the task.",
    )
    implementation_path: str = Field(
        description="Suggested implementation path for completing the task."
    )
    validation: list[str] = Field(
        default_factory=list,
        description="Tests, checks, or commands required before closure.",
    )
    done_when: str = Field(description="Observable completion rule for the task.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'system:sldb' or 'language:python'.",
    )
