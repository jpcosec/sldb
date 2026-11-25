# ADR: One Command Taxonomy, Served By FastMCP

- Status: Accepted; kept in the drawer, not started
- Date: 2026-11-25
- Decision Maker: the owner
- Related repos: `sldb`, `IR` (specIR), `graph_ui`

## Context

SLDB grew four faces that were never planned together. Measured on 2026-11-25:

| Face | Size | Notes |
|---|---|---|
| `sldb.api` | 192 public names | |
| CLI | about 20 groups | the top-level help does not name `serve`, `notations`, `semantic`, `rules` or `lint` |
| `sldb serve` | about 30 routes, 45 files, 2,510 lines | hand-written on `http.server`; no extensions, no undo |
| `sldb mcp` | 15 tools, about 1,500 lines | `MCPServer` from the `mcp` SDK 2.2; stdio only |

Names differ between faces and each covers a different subset. A consumer that needs something
from two faces (specIR needed an HTTP extension that only the MCP face had) asks for it twice.

The owner's diagnosis: there is no command taxonomy. And four reasons to adopt the `fastmcp`
package rather than keep `MCPServer`: not maintaining that code, code mode, an interface agents
already know, and one declarative place for every face.

## Decision

1. **A taxonomy first**: one table of operations, each with a noun, a verb, whether it reads or
   writes, and its permission level. It reconciles the four faces and marks duplicates, gaps and
   renames. The owner approves it.
2. **One FastMCP server** declares each operation once.
3. **Interfaces become clients** of that server, and `sldb serve` is retired.
4. **The CLI** is aligned with the taxonomy.

An extension (specIR's) is a server mounted into SLDB's, not a separate mechanism.

## What FastMCP gives and does not

Read in its documentation on 2026-11-25 (version 4.2.6):

- It depends on the same `mcp` SDK v2 SLDB already uses, with a migration guide from `MCPServer`.
- Code mode exists since 3.1 and is marked experimental: a transform that shows the client three
  tools (search, get schema, execute), where the code can only call tools, under the same
  permissions.
- Composition: one server mounted into another under a namespace.
- It does **not** generate REST routes from tools. A web interface either speaks MCP over HTTP
  (CORS is documented) or routes are hand-written next to the tools.
- Its generated CLI is a flat client script, one subcommand per tool. It does not produce grouped
  commands such as `sldb docs create`.
- Per-tool authorization is skipped over stdio. SLDB's permission levels 0, 1 and 2 have to be
  rebuilt by hiding tools by tag.

So "one declarative place" holds for MCP, code mode and HTTP clients. The human CLI needs its own
decision when step 4 is reached.

## Consequences

- The request for `sldb serve --extension` is void.
- What moves from pron ([pron Is Archived](pron-is-archived.md)) lands as operations of the
  taxonomy.
- The editor contract ([Surface Is An Editor Contract](surface-is-an-editor-contract.md)) binds
  components to operations, so it depends on step 1.
- The 30 routes have no equivalent in 15 tools. Extraction, render, lint, AST, similarity and
  notations are missing from the MCP face. The old routes stay until both interfaces migrate.

## Not verified

- Whether `SurfaceDoc` and `sldb selfdoc` can hold and check the taxonomy.
