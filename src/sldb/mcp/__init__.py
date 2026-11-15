"""The MCP server of sldb: thin MCP adapters over `sldb.api`, migrated from the specIR server.

`read.ReadTools` and `write.WriteTools` hold the operations as plain functions that return
JSON-ready dicts; `server.build_server` exposes them as MCP tools over stdio (`sldb mcp`).
Nothing here keeps an edge index, traverses the graph or parses predicates: SLDB does all of
it. This package imports the `mcp` library only from `server`, so sldb without the `mcp` extra
keeps working and `sldb mcp` says how to install it."""

from sldb.mcp.read import ReadTools

__all__ = ["ReadTools"]
