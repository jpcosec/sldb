"""Compatibility bridge: `SectionRecord` now lives in `sldb.api.records`."""

from sldb.api.records.section_record import SectionRecord  # noqa: F401

__all__ = ["SectionRecord"]
