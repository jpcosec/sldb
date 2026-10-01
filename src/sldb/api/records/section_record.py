from __future__ import annotations
from dataclasses import dataclass

@dataclass
class SectionRecord:
    title: str
    slug: str
    level: int
    path: str
    line_start: int | None
    line_end: int | None
