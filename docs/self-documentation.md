# CLI Self-Documentation

The first self-documentation slice derives CLI reference records from an assembled argparse parser and tracks them with SLDB's existing `CliCommandDoc` and `SurfaceDoc` models.

`sldb selfdoc python-scan --source-root src --package sldb` is the read-only Python inventory. `python-sync` materializes it under `knowledge/symbols/` and persists the regenerable source facts through KGDB; `python-check` reports documentation or source-graph drift without writing. They use the standard-library AST and never import scanned modules. Each record has a qualified `python:<module>:<qualname>` identity (not stable across moves or renames), source span, syntactic signature, declared docstring, module imports, and a file hash. Regeneration owns those facts and preserves authored `purpose`, `architecture`, and tags. Roles, architecture boundaries, rename equivalence, and spec2viz grouping still require declared or reviewed metadata.

The [docstring indexing contract](architecture/code-docstring-indexing.spec.md) specifies source-owned metadata and explanations, AST-derived relationships, selective tag inheritance, and KGDB-backed projections. `python-sync` now projects module/symbol containment, import bindings, and resolvable annotation references, with source span and hash evidence. These are store facts for any consumer; the adapter does not prescribe a consumer query language or read the artifact back through another runtime. It does not yet apply inherited tags or migrate the legacy document IDs.

All tracked records are rendered as Markdown, but the semantic index distinguishes their source format. Ordinary models inherit `representation.markdown` and `source.document.markdown`; `PythonSymbolDoc` has `representation.markdown` and `source.code.python`. Consumers must use those tags rather than infer source format from a path or model name.

For this repository, bind records to the current structural evidence:

```bash
sldb selfdoc python-sync --source-root src --package sldb --system sldb \
  --architecture-spec docs/architecture/spec2viz/python-ast.yml
sldb selfdoc python-check --source-root src --package sldb --system sldb \
  --architecture-spec docs/architecture/spec2viz/python-ast.yml
```

`python-sync` invokes the public `kgdb ingest --input ... --output ...` flow. Override the persistence location with `--kgdb-output path` or the KGDB executable with `--kgdb-command command`; paths are rooted at the selected store and cannot escape it. `.kgdb/` is generated local state and is ignored by Git. A missing or source-stale KGDB graph appears as `kgdb_stale` and makes `python-check` return 1, just like source-document drift.

For example, the graph distinguishes `command` **containing** `CommandRecord`, the module **importing** `ArgumentRecord`, and the field annotation **referencing** it. The projection proves containment, imports, and annotation references — not runtime calls, re-export chains, star imports, or shadowing. Consumers query the published store facts through their own supported SLDB/KGDB integration; an agent does not treat `.kgdb/` as an ad-hoc source of truth. The consumer boundary is specified in [the docstring indexing contract, section 4.3](architecture/code-docstring-indexing.spec.md).

The `architecture_spec` field stores that relative path and its SHA-256. It identifies the referenced artifact; it does not prove review, source freshness, symbol-to-node membership, or semantic roles. These commands retain this checkout's existing scan configuration: `src --package sldb` currently duplicates the `sldb` module prefix. Do not change it during annotation-only work, as that would change generated document identities.

When a source inventory no longer contains a tracked Python symbol, `python-check` reports removed records without deleting them. A rename candidate now appears only for one unique fact match; an actual rename may change its signature, docstring, or source file hash and therefore produce no candidate. Candidates remain review hints, and SLDB never rewrites a symbol ID or authored context automatically. Complete-source removal and nondefault output paths need additional coverage.

`python-check` also reports `semantic_gaps`: the count of tracked symbols whose authored `purpose` or `architecture` is still `Not documented.`. This is a placeholder metric, not evidence of missing information in source docstrings, generated semantic classification, or an integrity failure. Both Python and CLI checks now return 1 whenever JSON reports `ok: false`.

## Workflow

From this project root or any subdirectory inside its store:

```bash
sldb selfdoc scan
sldb selfdoc sync
sldb selfdoc check
sldb fields show docs/cmd-sldb-selfdoc-sync/arguments
```

`scan` emits a JSON inventory without running command handlers. `sync` updates generated fields, registers missing models/documents, and updates tracking hashes and section indexes. `check` compares expected fields, files, and document tracking without writing them. A repeated sync of current inputs does not rewrite the documents.

The repository CI checks the generated reference on Python 3.13, the runtime used to materialize it. The normal test matrix continues covering Python 3.10–3.13; parser presentation can differ between Python versions.

`sync` and `check` resolve the nearest ancestor store or accept `--store PATH/ALIAS`. `--output knowledge` is relative to the selected store's project root, not the current subdirectory; destinations outside that project are rejected. The global registry is not modified by this workflow.

All project-relative interfaces use the same context rule: the nearest non-global ancestor store is selected, then its project root anchors paths. A relative `faq --faq-path`, `explore --docs-root`, and `explore --code-root` follow that root; pass an absolute path to opt out. Store aliases resolve from the closest registry outward and finally from `~/.sldb`. `stores init` explicitly catalogs stores below the user home directory in that global store; ordinary reads never perform a disk-wide discovery scan.

For existing stores, reconciliation is explicit: `sldb stores reconcile --path <subtree>` reports discovered, missing, and stale catalog paths; add `--apply` to replace that catalog with the discovered subtree. It is intentionally never performed by a read/query command.

For another trusted argparse application:

```bash
sldb selfdoc scan --factory myapp.cli:build_parser --pythonpath src
sldb selfdoc sync --factory myapp.cli:build_parser --pythonpath src --system myapp
sldb selfdoc check --factory myapp.cli:build_parser --pythonpath src --system myapp
```

The factory must return `argparse.ArgumentParser`. Importing it and building the parser executes Python, so the factory must be trusted and side-effect-free. Relative `--pythonpath` resolves from the selected project root. The default factory and system identifier describe SLDB itself.

## Ownership and Freshness

| Fields | Owner during regeneration |
|---|---|
| Command identity/path, synopsis, arguments, provenance | Assembled parser |
| Surface identity, command inventory, provenance | Assembled parser |
| Purpose, how_it_works, usage examples, tags | Documentation author; preserved |

New explanations are marked `Not documented.` rather than inferred from option names. New command usage starts with argparse's usage string; existing examples remain authored. Arguments are represented as JSON inside the Markdown field, including required flags, defaults, choices, converters, cardinality, action type, and mutually exclusive groups.

The `provenance` field identifies the parser factory and command path and includes `contract-sha256`. This is a fingerprint of parser facts, not a claim that handler logic was analyzed. A handler-only change may require updating authored explanations without changing the parser contract.

Hidden commands/options are omitted by default; `--include-hidden` includes them. SLDB's `init` and `example` now carry public parser help because they are supported bootstrap commands. Alias paths are represented separately. Filename collisions are rejected before sync writes documents.

## Findings and Limits

JSON reports distinguish missing files, changed generated fields, missing tracking, stale document hashes, and removed commands. `check` exits 0 when current and 1 when findings remain. Invalid inputs fail without starting document writes. `sync` retains obsolete documents and exits 1 while removed-command findings remain; removal/untracking is a separate explicit operation.

All expected payloads are validated before writes and original file contents are checked before applying a plan. Persistence uses existing SLDB operations, not a transaction spanning all documents; an I/O failure can require rerunning sync. Custom parser defaults must have deterministic JSON representations. Automatic rename equivalence and a general call graph are follow-up work.

See [the active task](../desk/tasks/task-build-code-self-documentation.md), [tests](../tests/selfdoc/), and [remaining findings](documentation-review.md).

## Structural Architecture Evidence

The Python inventory makes source symbols trackable; [the spec2viz AST view](architecture/spec2viz/python-ast.md) adds a reproducible module/import projection. It is deliberately adjacent to, rather than a replacement for, curated semantic architecture specs.
