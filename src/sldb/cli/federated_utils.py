"""Compatibility bridge: federated model lookup now lives in `sldb.api.model_registry`."""
from sldb.api.model_registry.federated_lookup import (  # noqa: F401
    _build_federated_entry,
    _find_federated_model,
    _get_linked_store_candidate,
    _load_remote_entry,
    _model_registry_stores,
    _resolve_linked_store,
)
from sldb.api.model_registry.federated_registration import (  # noqa: F401
    _append_federated_entry,
    _do_ensure_federated_model,
    _ensure_federated_model_entry,
    _get_rel_model_path,
    _save_federated_indexes,
)
