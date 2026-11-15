"""The read operations of the MCP server, as plain functions over `sldb.api`.

Nothing here writes, keeps an edge index, traverses the graph or parses a predicate:
neighbours come from `edges_from`/`edges_to`, the multi-hop neighbourhood from
`sldb.api.graph.collect_neighborhood_by_direction`, predicates from `select_documents`."""

from sldb.mcp.read.tools import ReadTools

__all__ = ["ReadTools"]
