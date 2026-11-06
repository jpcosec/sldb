"""Code anchors (docs/architecture/code-anchoring.md): record what a symbol looks like, check
every anchor of a store against the code now, reconnect what moved by name. Document anchors
(anchoring.md §6): `check_doc_anchors` reports the ones whose target moved or is gone.

`record_anchor` reads one symbol; `check_anchors` only reads unless asked to `record` the
reconnections (owner's decision 3). States are `sldb.models.anchor_state.AnchorState`.
"""

from sldb.api.anchors.check_anchors import check_anchors
from sldb.api.anchors.check_doc_anchors import check_doc_anchors
from sldb.api.anchors.record_anchor import record_anchor

__all__ = ["check_anchors", "check_doc_anchors", "record_anchor"]
