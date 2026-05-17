from pydantic import Field

from sldb import StructuredNLDoc


class StepDoc(StructuredNLDoc):
    __semantics__ = {"type": ["workflow", "step"], "workspace": ["desk"]}
    __template__ = """
# ⸢rev•title⸥

ID: ⸢rev•id⸥

## Action

⸢rev•action⸥

## Outcome

⸢rev•outcome⸥

## Tags

- ⸢rev,list•tags⸥
""".strip()

    title: str = Field(description="Short step title.")
    id: str = Field(description="Stable step identifier.")
    action: str = Field(description="What the step should do.")
    outcome: str = Field(description="What the step should produce or confirm.")
    tags: list[str] = Field(
        default_factory=list,
        description="Semantic tags placed at the end, using namespaced forms such as 'topic:testing' or 'workspace:desk'.",
    )
