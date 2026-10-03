from .sldb_error import SLDBError
from .store_error import StoreError

class SLDBStoreError(SLDBError, StoreError):
    """Raised when there is an issue with the SLDB store or indexes."""
    pass
