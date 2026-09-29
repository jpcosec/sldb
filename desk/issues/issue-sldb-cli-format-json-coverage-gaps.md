---
id: issue-sldb-cli-format-json-coverage-gaps
status: open
tags:
- system:sldb
- topic:cli
- topic:serialization
- topic:bug
related_tasks:
- desk/tasks/task-retirar-cli-graph-y-cli-graph-old-copias-fosiles-de-un-refactor-interrumpido.md
---

# SLDB: `--format json` is advertised globally but rejected by several subcommands

## Problem

`--format {json,yaml,text}` reads as a general CLI capability, but three subcommands reject it at the argparse level with a top-level usage dump.

Reproduced against this repo's store:

```bash
python -m sldb models show PillDoc --store .sldb --format json
# usage: sldb [-h] {extract,render,validate,init,...}
# sldb: error: unrecognized arguments: --format json

python -m sldb models template show PillDoc --store .sldb --format json
# same failure

python -m sldb docs update --help | grep -c format
# 0
```

Two separate defects:

1. **Missing capability** — these commands have no machine-readable output, so integrators are pushed to `sldb.api`.
2. **Misleading error** — the failure prints the *root* parser usage, not the subcommand's. It tells the operator nothing about which command rejected the flag or what that command does accept.

## Why this is a bug, not friction

A flag that exists on most subcommands and silently does not exist on others is an inconsistent contract. The error surface makes it worse: the usage dump points at the wrong parser level, so the operator cannot tell whether they mistyped the flag, the command, or both.

Confirmed working for comparison: `ast show --format json` emits clean JSON on stdout with no leading warnings.

## Relationship to tracked work

No tracked task owns `--format` coverage; this is genuinely unclaimed. Two adjacent efforts matter:

- `task-retirar-cli-graph-y-cli-graph-old-copias-fosiles-de-un-refactor-interrumpido` (`draft`) prunes fossil CLI copies. Auditing `--format` across subcommands should happen **after** that, so the matrix is not written against modules about to be deleted.
- The `edges` command group is on the delete list of `task-borrar-la-capa-runtime-edges-y-podar-el-surface-publico`. Exclude it from the audit.

The three affected commands (`models show`, `models template show`, `docs update`) are not in any retirement scope, so fixing them is safe now.

## What's needed

- Add `--format {json,yaml,text}` to `models show`, `models template show`, and `docs update`, or explicitly document them as text-only.
- Fix the error surface so rejecting an unknown flag prints the *subcommand's* usage.
- Audit every subcommand for `--format` presence and record the intended matrix, so the gap is a decision rather than an accident.

## Files to read first

- `src/sldb/cli/parser.py` — where `--format` is attached, and why it is per-subparser
- `src/sldb/cli/parsers/` — subparser definitions for `models` and `docs`
- `src/sldb/cli/commands/models_template.py` — `show` handler, currently prints a raw literal
- `src/sldb/cli/commands/models_validate.py:65` — existing precedent: progress lines go to stderr so `--format json/yaml` keeps stdout parseable

## Design considerations

- **`models template show` returns a raw template literal.** JSON output should wrap it (`{"model": ..., "template": ...}`) rather than emit a bare quoted string.
- **`docs update` is a mutation.** Its JSON form should report what changed, not just succeed silently.
- **stdout purity**: follow the `models_validate.py:65` precedent — human progress lines to stderr whenever a machine format is requested.
- Prefer a shared `--format` definition over repeating it per subparser; the current duplication is what let the gap appear.

## Task list

- [ ] Inventory `--format` support across all subcommands; **exclude** the `edges` group and any module in a retirement task's delete list
- [ ] Sequence the full audit after `task-retirar-cli-graph-y-cli-graph-old-...` so the matrix is not written against doomed modules
- [ ] Make unknown-flag errors print subcommand usage instead of root usage
- [ ] Add `--format` to `models show`, `models template show`, `docs update` (or document as text-only)
- [ ] Route human-readable progress to stderr under machine formats
- [ ] Tests asserting stdout parses cleanly for every command claiming `--format json`
- [ ] Update `docs/user-manual.md` §13, which currently records this as friction

## Pills

- `desk/pills/pill-008-sldb-cli-document-contract.md` — CLI output must present document-model state faithfully, not invent presentation-layer semantics
- `desk/pills/pill-009-cli-error-and-serialization-failure-mode.md` — machine-readable outputs stay intact; errors stay actionable
