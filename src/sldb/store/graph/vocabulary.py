"""A downstream-defined graph vocabulary token, validated for the portable format."""

from typing import Annotated

from pydantic import Field

VocabularyTerm = Annotated[
    str,
    Field(
        min_length=1,
        pattern=r"^[A-Za-z][A-Za-z0-9_.:-]*$",
        description="A downstream-defined graph vocabulary token.",
    ),
]
