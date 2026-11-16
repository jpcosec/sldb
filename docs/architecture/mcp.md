# `sldb mcp`: the store served to an MCP client

`sldb mcp --store <project>/.sldb [--level 0|1|2] [--actor <who>] [--extension module:function]...`
serves one store over stdio as a Model Context Protocol server. It is the server of specIR
(`specir.mcp`, IR03 reads and IR04 writes) moved here, because it knows nothing of specIR's domain: it
reads and writes a store only through `sldb.api`. A consumer mounts its own domain tools on top
(see *Extension point*) instead of copying it.

Code: `src/sldb/mcp/`. Layer: transport (`contracts/layers.toml`), beside `cli`. Optional extra
`mcp` (`pip install 'structuredLanguageDB[mcp]'`, `mcp>=2.2`); only `sldb.mcp.server`'s own
modules import the library, so sldb without the extra works and `sldb mcp` says how to install it.

## Levels

The level is the operator's (`--level`), never a tool argument, and levels are cumulative.

| level | serves |
| --- | --- |
| 0 (default) | the eleven read tools and `list_signals`, all read-only |
| 1 content | adds `propose_changes` and `apply_changes` for documents of registered models and authored edges (`RelationDoc`) |
| 2 rules as data | the same two tools may also write `RelationTypeDoc` and `RuleDoc` |

Models as Python code (level 3) are never served: no tool writes a Python module.

Read tools: `list_models`, `describe_model`, `list_relation_types`, `describe_relation_type`,
`read_document`, `select_documents`, `neighbors`, `neighborhood`, `list_views`, `resolve_view`,
`check_integrity`. Documents have the stable address `sldb://document/<export_id>`; every set is
a page `{items, total, offset, limit, truncated, next_offset}`.

## Writing: propose, then apply

`propose_changes` turns typed changes (`create`, `update`, `delete`, `assert_edge`, `retract_edge`)
into a batch for `sldb.api.apply_batch` with the `expected_source_hash` guard of every document it
touches, seals it, and answers what it would write; it writes nothing. `apply_changes` takes that
proposal back unchanged and hands it to `apply_batch`: all or nothing, or rejected with its cause
(`stale` when a guarded document changed, `rules` naming the RuleDocs that refused it). `--actor`
signs the provenance of what is written. What `sldb.api` does not offer yet (a public dry run,
edge validation before the write, the store hash as a precondition) is listed in every answer's
`pending`, with the inbox note that asks for it.

## Signals

Asking for something that does not exist, or is called differently, is not an error: it is a
signal. The answer says it does not exist or is not implemented and was registered as a signal,
and carries `suggestions` (the five names `sldb.api.matching.Matcher.rank` ranks nearest, in its
order). The closed catalog of classes: `unknown_tool`, `unknown_model`, `unknown_document`,
`unknown_field`, `unknown_relation`, `unknown_view`, `unknown_argument` and `not_implemented`.
For an unknown tool or argument nothing runs.

Each signal is one JSON line appended (`O_APPEND`) to **`<project>/.sldb_cache/signals.jsonl`**:

```json
{"at": "2026-11-15T16:15:32.896Z", "tool": "describe_model", "arguments": {"model": "Itm"}, "signal_class": "unknown_model", "suggestions": ["Item", "Stage"], "actor": null}
```

`list_signals(signal_class?, offset, limit)` reads it, paged like every set, at every level. The
log lives in the cache (`sldb.store.layout.cache_dir`), next to `.sldb_cache/rules` and
`.sldb_cache/composed`: it is derived, ignored by git, and not store state, so recording a signal
at level 0 writes no tracked document and no linked store. There is no rotation yet.

## Undo (pending)

`undo_changes` is declared and not served: `apply_batch` does not yet return the inverse batch
with guards (inbox request 20261115-123855; undo belongs to sldb). Calling it answers
`not_implemented` and is logged. When the request is resolved the tool re-applies the inverse.

## Extension point

```python
from sldb.mcp.server import build_server

def register(server, context):          # context: store_path, project_root, level, actor, log
    @server.tool()
    def my_tool(name: str, offset: int = 0, limit: int = 50) -> dict: ...

server = build_server(store, level=1, actor="agent:me", extensions=[register])
```

or `sldb mcp ... --extension my_package.tools:register` (repeatable). Every tool registered on the
server, the built-in ones and an extension's, goes through the same guard: a failure reaches the
agent with its cause, an unknown argument is a signal, and a dict answer carrying
`{"signal": {"class": ..., "name": ...}}` is logged with suggestions. Pages come from
`sldb.mcp.paging.page`; an extension reads `context.level` to refuse what the operator did not allow.

### Batch validators

An extension adds a domain rule to the write tools without re-registering them:

```python
def register(server, context):
    def claims_verified(changes, context):   # changes: the batch's list of changes
        return [{"code": "claims_verified", "level": "error", "what": "only the server verifies", "subject": c.name} for c in changes if ...]
    context.add_batch_validator(claims_verified)
```

The stable extension contract is `sldb.mcp.extension.Extension` (`extension(server, context)`),
`sldb.mcp.extension.BatchValidator` (`validator(changes, context) -> list[dict]`) and
`ServerContext.add_batch_validator(validator)`. `build_server` runs every extension before the server
answers its first call and hands the `ServerContext` to the write tools, which read
`context.batch_validators` on every call:

- `propose_changes` runs them after its level and path checks and before building the batch, over
  its typed changes (`create`/`update`/`delete`/`assert_edge`/`retract_edge`); `apply_changes` runs
  them after its level check and the seal check, over the proposal's `BatchChange`s (`id`, `action`,
  `model`, `payload`, `path`).
- Every validator runs, always. A finding is `{"code", "level", "what", "subject"}` with `level`
  `"error"` or `"alert"`.
- Any `"error"`: the answer is `{"applied": false, "rejected": "domain", "explanation": "<n> domain
  check(s) failed", "written": false, "findings": [every finding, errors and alerts]}`; nothing is
  sealed or written.
- Only alerts: the dry run of `propose_changes` and the answer of `apply_changes` gain
  `"domain_alerts": [...]`. Without findings (or without validators) the answers are as before.
