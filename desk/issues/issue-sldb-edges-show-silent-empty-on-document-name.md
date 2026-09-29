---
id: issue-sldb-edges-show-silent-empty-on-document-name
status: open
tags:
- system:sldb
- topic:cli
- topic:graph
- topic:bug
related_tasks:
- desk/tasks/task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico.md
- desk/tasks/task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges.md
---

# SLDB: `edges show` returns `[]` silently when given a document name

## Problem

`edges show` accepts a positional `node` documented as "Export id `Model:name`, or a node id `sldb://<kind>/...`". When an operator passes a bare document name instead, the command prints `[]` and exits `0`.

Reproduced against this repo's store:

```bash
python -m sldb edges show pill-008-sldb-cli-document-contract --store .sldb
# []
# rc=0
```

This is indistinguishable from "this node exists and has no edges". An operator debugging a missing edge gets a false negative, and any automation reading the exit code treats malformed input as success.

## Why this is a bug, not friction

The empty result is a *correct-looking* answer to an *invalid* input. The command has enough information to know the string is neither an export id (`Model:name`, requires a colon) nor a node id (`sldb://` prefix), so it can reject it instead of resolving to nothing.

## ⚠ Do not fix this file — it is scheduled for deletion

`src/sldb/cli/commands/edges.py` is **explicitly on the delete list** of `task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico`:

> "Borrar edge_sync.py, edge_rebuild.py, [...] **cli/commands/edges.py**, cli/parsers/edges.py, cli/serve/edges_routes.py, y podar api/__init__.py."

`docs/architecture/edges-retirement-plan.md:220` (step 5) confirms the whole `edges` command group goes: parser, dispatcher, help texts, and the `/edges*` serve branch.

That retirement is a 4-task chain, all `draft`, all at `execution-ready`:

1. `task-cerrar-los-gaps-g1-g5-que-bloquean-el-retiro-de-runtime-edges`
2. `task-dar-fuente-propia-al-grafo-store-graph-deja-de-leer-runtime-edges`
3. `task-comando-de-porte-sldb-stores-migrate-legacy-edges-y-error-de-migracion`
4. `task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico`

Relevant: **G4 in the gaps task names `sldb edges check` as having no equivalent in the new layer**, so selector validation is a live design question for the replacement surface, not just this command.

### What to do instead

Carry the requirement forward, do not patch the doomed file. The replacement graph surface must not repeat the silent-empty behaviour. If the retirement chain stalls and `edges show` survives, revisit this as a real fix.

## What's needed

- Validate the `node` argument shape before resolution.
- On an unparseable selector: error with the two accepted forms and a non-zero exit.
- On a well-formed selector that resolves to no known node: distinguish "unknown node" from "node with zero edges". These are different facts and should not share output.
- Keep `[]` reserved for the genuine case: known node, no edges.

## Files to read first

- `src/sldb/cli/commands/edges.py` — the `show` handler and how `node` is resolved
- `src/sldb/cli/graph_ops/` — node id resolution
- `.sldb/runtime/edges/` — shard layout, to confirm what "known node" means at lookup time

## Design considerations

- **Should a bare name be accepted as sugar?** Resolving `<name>` against tracked documents is plausible, but ambiguous across models. If accepted, it must error on ambiguity rather than pick one.
- **Exit codes**: invalid input and unknown node should not both be `0`.
- `--local` and `--relation` filters legitimately narrow results to empty; that path stays `[]` with `rc=0`.

## Task list

- [ ] **First**: confirm the edges retirement chain is still going ahead; if so, do not touch `cli/commands/edges.py`
- [ ] Add "selector validation: reject unparseable input, separate unknown-node from zero-edges" as an acceptance requirement on the replacement graph surface
- [ ] Check whether G4 (`sldb edges check` has no equivalent) already covers this in `task-cerrar-los-gaps-g1-g5-...`
- [ ] Only if retirement is abandoned: validate the selector in the existing handler, separate the two empty cases, add tests
- [ ] Update `docs/user-manual.md` §13, which currently records this as friction

## Pills

- `desk/pills/pill-009-cli-error-and-serialization-failure-mode.md` — user-input failures must become actionable diagnostics, not silent empty output
- `desk/pills/pill-007-sldb-text-layer-vs-kgdb-graph-layer.md` — document names live in the text layer, node ids in the graph layer
