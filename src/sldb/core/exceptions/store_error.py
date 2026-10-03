class StoreError(Exception):
    """Base error for anything owned by the store layer.

    Defined in the core and not in the store because the core needs to name it:
    `SLDBStoreError` inherits from it, and `core.exceptions` re-exports that, so
    importing it from the store made every core import pull in the whole
    persistence layer — 46 extra modules to use the text converter.

    An exception hierarchy belongs to the lowest layer that mentions it.
    """
