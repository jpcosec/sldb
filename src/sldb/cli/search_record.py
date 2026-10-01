"""Compatibility bridge: `SearchRecord` now lives in `sldb.api.records`."""

from sldb.api.records.search_record import SearchRecord  # noqa: F401

__all__ = ["SearchRecord"]
