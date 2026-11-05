"""A regular expression whose matches in a document's text name graph nodes."""

from __future__ import annotations

import re
from functools import cached_property

from pydantic import BaseModel, ConfigDict, Field


class MentionPattern(BaseModel):
    """A pattern and the target id its matches name."""

    model_config = ConfigDict(frozen=True, ignored_types=(cached_property,))

    regex: str = Field(description="The pattern searched line by line.")
    target: str = Field(description="`str.format` template of the target id: `{0}` is the match, named groups by name.")

    @cached_property
    def compiled(self) -> re.Pattern[str]:
        """The compiled pattern."""
        return re.compile(self.regex)

    def targets(self, line: str) -> list[str]:
        """The target ids the matches in `line` name, in match order."""
        return [self.target.format(match.group(0), **match.groupdict()) for match in self.compiled.finditer(line)]
