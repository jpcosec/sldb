"""Compatibility bridge: record filtering now lives in `sldb.api.records`.

`FindFilters` is the former name of `RecordFilters`, kept for existing importers.
"""

from sldb.api.records.record_filters import RecordFilters
from sldb.api.records.record_filters import RecordFilters as FindFilters  # noqa: F401

__all__ = ["FindFilters", "RecordFilters"]
