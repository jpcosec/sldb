"""One entry of `EdgeIndex.problems`, structured: kind, declaring document and the text."""

from __future__ import annotations

import re

from pydantic import BaseModel, Field

from sldb.store.edge_index.node_ids import RELATION_MODEL

ENDPOINT_NOT_A_NODE = "endpoint-not-a-node"
# The one shape `resolve._authored` gives an entry of `EdgeIndex.problems`.
_ENDPOINT_PROBLEM = re.compile(r"^relation '(?P<doc>.*?)': (?:source|target) '.*' is not a tracked document$")


class EdgeProblem(BaseModel):
    """One entry of `EdgeIndex.problems`, structured: a consumer reads the fields instead of
    parsing the text."""

    kind: str = Field(description="What went wrong; `endpoint-not-a-node` for an authored edge whose end is not a node.")
    document: str = Field(description="Export id of the document that declared the edge (`RelationDoc:<name>`); empty if the text names none.")
    detail: str = Field(description="The same text as the matching entry of `problems`.")


def edge_problem(text: str) -> EdgeProblem:
    """The structured form of one `problems` entry."""
    match = _ENDPOINT_PROBLEM.match(text)
    return EdgeProblem(kind=ENDPOINT_NOT_A_NODE, document=f"{RELATION_MODEL}:{match['doc']}" if match else "", detail=text)
