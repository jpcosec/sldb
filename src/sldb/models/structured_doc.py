from typing import TypeVar

from pydantic import BaseModel


class StructuredNLDoc(BaseModel):
    __template__: str = ""

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs):
        super().__pydantic_init_subclass__(**kwargs)
        if cls is StructuredNLDoc:
            return

        missing_descriptions = sorted(
            field_name
            for field_name, field_info in cls.model_fields.items()
            if not field_info.description or not field_info.description.strip()
        )
        if missing_descriptions:
            formatted_fields = ", ".join(missing_descriptions)
            raise TypeError(
                f"{cls.__name__} fields must define a non-empty description: {formatted_fields}"
            )


M = TypeVar("M", bound="StructuredNLDoc")
