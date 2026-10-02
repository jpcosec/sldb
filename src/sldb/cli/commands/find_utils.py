"""Compatibility bridge: `RuntimeDocProxy` now lives in `sldb.api.records`."""

from sldb.api.records.runtime_doc_proxy import RuntimeDocProxy  # noqa: F401

__all__ = ["RuntimeDocProxy"]
