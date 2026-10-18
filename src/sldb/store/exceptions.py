"""The errors the store raises: the one seam to sldb's exception hierarchy.

The hierarchy lives in `sldb.core.exceptions` (the lowest layer that names it: `SLDBStoreError`
is both an `SLDBError` and a `StoreError`). The store's modules import their errors from here,
never from the core directly, so a store packaged on its own replaces only this module.
"""

from sldb.core.exceptions import SLDBError, SLDBGraphCycleError, SLDBModelError, SLDBStoreError  # noqa: F401
from sldb.core.exceptions.store_error import StoreError  # noqa: F401
