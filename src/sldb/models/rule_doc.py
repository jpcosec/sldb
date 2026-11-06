"""The rule: a predicate a family of documents must satisfy, declared as an sldb document (GO06).

`sldb rules check` and `sldb rules explain` evaluate it (docs/architecture/rules.md). What one
RuleDoc must say on its own is checked here, by its validators: `condition` and `where` parse
in the language of docs/architecture/rules-language.md, `subject` is `model <= X` or a
top-level conjunction of them, and `severity` and `moment` are in their vocabulary. Whether
`X` names a registered model depends on the store, so the write checks it (`sldb.api.rules`).
"""

from __future__ import annotations

from typing import Literal

from pydantic import Field, field_validator

from sldb.models.structured_doc import StructuredNLDoc


class RuleDoc(StructuredNLDoc):
    """Declares one rule: which documents it is about (`subject`, narrowed by `where`), what
    must hold of each (`condition`), how much a failure weighs (`severity`), when it is
    evaluated (`moment`) and what to say when it fails (`message`)."""

    __family__ = "rule"
    __semantics__ = {"type": ["rule"], "layer": ["governance"]}
    __template__ = """---
subject: ⸢rev•subject⸥
where: ⸢rev•where⸥
condition: ⸢rev•condition⸥
severity: ⸢rev•severity⸥
moment: ⸢rev•moment⸥
message: ⸢rev•message⸥
---

# ⸢rev•title⸥
""".strip()

    title: str = Field(description="Rule title shown as the H1 heading.")
    subject: str = Field(description="The family the rule is about: `model <= X`, or a top-level conjunction of such terms (the intersection of their families).")
    where: str = Field(default="", description="Optional predicate evaluated on each member of the family first; false or incomplete means the rule does not apply to that document.")
    condition: str = Field(description="The predicate every document the rule applies to must satisfy (docs/architecture/rules-language.md).")
    severity: Literal["error", "alert"] = Field(description="Level of the finding a false condition produces; an error fails `sldb rules check`.")
    moment: Literal["on_write", "on_transition", "on_check"] = Field(description="When the rule is evaluated; `sldb rules check` without --subject runs only the on_check rules.")
    message: str = Field(default="", description="Optional text the finding starts with, before the explanation of the clause that decided it.")

    @field_validator("condition", "where")
    @classmethod
    def _parses(cls, value: str, info) -> str:
        if value or info.field_name == "condition":
            _parse(value)
        return value

    @field_validator("subject")
    @classmethod
    def _is_a_family(cls, value: str) -> str:
        if not _only_families(_parse(value).root):
            raise ValueError(f"subject must be `model <= X` or a conjunction of them, not {value!r}; other filters go in `where`")
        return value


def _parse(text: str):
    from sldb.store.graph.language.predicate_parser import parse_predicate

    return parse_predicate(text)


def _only_families(root: tuple) -> bool:
    """Whether a tree is `model <= X`, or a top-level `and` of such leaves only."""
    if root[0] == "and":
        return _only_families(root[2]) and _only_families(root[3])
    return root[0] == "leaf" and root[2] == "model"
