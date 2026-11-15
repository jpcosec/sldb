"""The typed changes an agent proposes, and the proposal that carries them to `apply`.

A change is a typed argument, never text the server interprets: one of the actions below,
with the model and name of the document it touches. A proposal is the batch in the form of
`sldb.api.apply_batch` (an ephemeral batch, nothing kept between steps) with the
`expected_source_hash` guard the server filled in for every document it touches, and a seal
over that batch so `apply` runs exactly what was proposed."""

from sldb.mcp.changes.assert_edge import AssertEdge
from sldb.mcp.changes.batch_change import BatchChange
from sldb.mcp.changes.create_document import CreateDocument
from sldb.mcp.changes.delete_document import DeleteDocument
from sldb.mcp.changes.proposal import Proposal
from sldb.mcp.changes.retract_edge import RetractEdge
from sldb.mcp.changes.sealer import Sealer
from sldb.mcp.changes.typed import EDGE_MODEL, Change, edge_payload, level_of, model_of
from sldb.mcp.changes.update_document import UpdateDocument

__all__ = ["EDGE_MODEL", "AssertEdge", "BatchChange", "Change", "CreateDocument", "DeleteDocument", "Proposal", "RetractEdge", "Sealer", "UpdateDocument", "edge_payload", "level_of", "model_of"]
