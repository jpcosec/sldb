"""Compatibility bridge: payload path helpers now live in `sldb.api.documents` (also exported by `sldb.api`)."""
from sldb.api.documents.payload_path_reading import _get_part, _split_path, deep_get, ensure_list  # noqa: F401
from sldb.api.documents.payload_path_writing import (  # noqa: F401
    _deep_set_dict,
    _deep_set_leaf,
    _deep_set_traverse,
    _delete_leaf,
    deep_delete,
    deep_set,
)
