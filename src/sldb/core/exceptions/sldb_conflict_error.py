from typing import Any

from .sldb_store_error import SLDBStoreError


class ConflictError(SLDBStoreError):
    """An optimistic guard failed: `ref` is not in the state the caller said it expected.

    `expected` and `actual` are what was compared: two source hashes, two payloads, or two
    sha256 digests of a plain file (`actual` is None when the file does not exist).
    """

    def __init__(self, ref: str, expected: Any, actual: Any) -> None:
        super().__init__(f"{ref} changed in the store: expected {expected!r}, found {actual!r}.")
        self.ref, self.expected, self.actual = ref, expected, actual
