"""Retract an authored edge."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from sldb.mcp.changes.base import _Change


class RetractEdge(_Change):
    """Retract an authored edge: delete its `RelationDoc`."""

    action: Literal["retract_edge"]
    name: str = Field(description="The RelationDoc's name.")
