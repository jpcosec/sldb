"""The models of the store the MCP tests serve. The module is copied into the store's project root,
so the server process imports it from there."""

from pydantic import Field
from sldb import StructuredNLDoc


class Stage(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Item(StructuredNLDoc):
    __references__ = ["depends_on"]
    __template__ = "---\nstatus: ⸢rev•status⸥\nowner: ⸢optrev•owner⸥\nstage: ⸢rev•stage⸥\ndepends_on: ⸢rev,list•depends_on⸥\n---\n\n# ⸢rev•title⸥"
    title: str = Field(description="Title.")
    status: str = Field(description="Column of the board.")
    owner: str = Field(default="", description="Who works on it.")
    stage: str = Field(description="The lifecycle node the item is at (`Stage:<name>`).")
    depends_on: list = Field(default_factory=list, description="Items this one waits for.")
