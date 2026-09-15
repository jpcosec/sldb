# Handoff: Continue Source Docstring Annotations

Continue the [docstring indexing specification](code-docstring-indexing.spec.md) in a small annotation-only batch. The specification is the authority; the two [PythonSymbol pilot declarations](../../src/sldb/selfdoc/python_symbol.py) demonstrate its syntax. The source-fact adapter now writes a regenerable KGDB graph, but strict docstring metadata interpretation and tag inheritance are not implemented. Do not report annotations as complete semantic classification.

## Assignment for the next agent

Read the spec completely, `standards.md`, [the active task](../../desk/tasks/task-build-code-self-documentation.md), and [the execution pill](../../desk/pills/pill-015-self-documentation-boundaries.md). Preserve unrelated working-tree changes; this checkout already contains extensive unfinished work. Do not reset, stage everything, commit, bump versions, or mark the overarching task done as part of this handoff.

The following batch-2 assignment is complete; do not repeat it. The next annotation assignment is the batch-3 proposal at the end of this handoff. Each batch annotates at most four declarations and requires reading consumers before describing behavior.

| Source | Declarations / proposed stable IDs | Evidence to read |
|---|---|---|
| `src/sldb/selfdoc/planned_document.py` | `sldb.selfdoc.planned_document`; `sldb.selfdoc.planned_document.PlannedDocument` | `selfdoc/materialize.py`, `selfdoc/python_materialize.py`, `cli/selfdoc_write.py` |
| `src/sldb/selfdoc/report.py` | `sldb.selfdoc.report`; `sldb.selfdoc.report.DocumentationReport` | `cli/selfdoc_inspect.py`, `cli/commands/selfdoc.py` |

Use module context tags `system:sldb`, `workspace:knowledge`, `topic:selfdoc`, and local class tag `type:code.symbol`, matching the pilots. Use `kind: core` only after confirming the data-contract responsibility from those consumers. Do not repeat inherited context on classes. Leave properties and methods for another batch; their source bodies still provide AST evidence without extra annotations.

The prose must explain what each declaration actually does, its input/output role, and relevant limits. `PlannedDocument` carries a validated payload and a before-image; it is not a filesystem transaction. `DocumentationReport.ok` currently ignores `semantic_gaps`; it does not certify semantic completeness. Record ambiguity here instead of inventing ownership or architecture. If a classification cannot be grounded, omit optional `kind` and record the reason.

Only edit these docstrings and the handoff/task progress notes, plus generated references/indexes resulting from the documented sync. Do not implement the adapter, rewrite business logic, annotate the whole tree, edit sibling KGDB/spec2viz repositories, or manually fill hundreds of generated `Purpose` / `Architecture` sections. Never add `edges` or `contains` to frontmatter.

Copy the pilot's blank line **before** the closing `---`. This is a temporary compatibility precaution, not a metadata requirement: without it, raw Markdown rendering treats the preceding YAML line as a setext heading and the materializer rejects the round trip. Safe literal rendering remains a separate implementation fix; do not relax the round-trip guard to bypass it.

## What exists versus what remains

The pilot delivery created the behavior spec first, then annotated one module and its class. `PythonSymbol` fields and executable behavior are unchanged. The current materializer can preserve the class's complete docstring as text; that is not metadata interpretation.

| Area | Current implementation / gap | Follow-up, outside the annotation batch |
|---|---|---|
| Frontmatter | Source-fact graph reads leading YAML opportunistically; generated symbol docs still retain raw docstrings | Typed profile, strict diagnostics, separate prose and metadata |
| Literal rendering | Compact frontmatter becomes a Markdown setext heading; `docstring` extracts as `---` and later fields shift | Safe literal-content representation; regression cases for compact frontmatter, headings, and fences |
| Context | Source graph emits module/symbol nodes and lexical containment; generated symbol inventory remains class/function-oriented | Package identity, selective inherited tags and provenance |
| Identity | Scan ID is qualified; materializer constructs a different normalized document ID | Explicit declared-ID mapping with collision checks and reviewed legacy migration |
| Existing scan config | `--source-root src --package sldb` yields `sldb.sldb.*` module names here | Fix configuration/identity together in a separate migration; preserve it for this batch |
| Relationships | Source graph emits `contains`, `imports`, and resolvable annotation `references` through KGDB; semantic export v1 remains unchanged | Registered typed relation vocabulary, re-exports/star imports/shadowing/type-checking resolution, spec2viz projection |
| Architecture | Optional spec path/hash only; no symbol-to-node association | KGDB identity-backed projection to the existing spec2viz component schema |
| Explanations | Generated `purpose`/`architecture` placeholders are preserved, not derived from prose | Source-owned extraction with explicit conflict handling for existing authored text |
| Check exit status | Python and CLI checks both return nonzero on `ok: false` | Keep regression coverage while adding report categories |
| Rename/removal | Candidates now require exactly one fact match, but still compare file hashes and assume default symbol paths | Complete-source and nondefault-output coverage; reviewed rename migration |

`semantic_gaps` counts placeholder fields only; it is not a test of docstring quality. A pinned architecture spec hash proves neither review nor graph connectivity. Annotation-only changes are not expected to reduce that counter. Do not hide it with manually copied prose.

## Validation and synchronization

Use Python 3.13 from `.venv` for the existing generated inventory. Repository style tests cap effective file length at 80 lines, including docstring lines; keep annotations concise and do not refactor working code merely to add prose.

1. Parse edited files with `ast.parse`. Extract each module/class docstring with `ast.get_docstring(clean=True)`, split its leading delimiters, and validate its YAML mapping and `tags` against `sldb.models.knowledge_tag.KnowledgeTag`. Check exact IDs against the pilot and this batch; no `edges` or `contains` keys. This is fixture validation, not proof that a production parser exists.
2. Run the existing focused suite:

```bash
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/selfdoc tests/test_clean_code_rules.py
```

3. Synchronize once, retaining the current options and generated IDs. From the repository root:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/jp/proyectos/hum-ecosystem/tools/deskops \
  .venv/bin/python -m sldb selfdoc python-sync --store .sldb \
  --source-root src --package sldb --system sldb --output knowledge \
  --architecture-spec docs/architecture/spec2viz/python-ast.yml
```

The sibling `deskops` path lets the existing store load its registered desk models; adapt the absolute path if the checkout moves. Do not add external stores to resolve an import problem. Module docstrings affect the containing-file hash and therefore generated records from that file, although they are not indexed as module records yet.

4. Repeat the same invocation with `python-check` instead of `python-sync`. Inspect JSON `ok`, `missing`, `changed`, `untracked`, `stale_indexes`, `removed`, and `renamed`; exit status alone is unreliable. Preserve pre-existing findings and report them. No need to regenerate the full spec2viz AST artifact for docstring-only changes.
5. After editing tracked narrative/task notes, run `sldb stores update --store .sldb --pythonpath .` and `sldb stores check --store .sldb --pythonpath .` through the same `.venv` and `PYTHONPATH` environment. Review the diff: only intended annotations and their derived files should be newly changed by this batch. Do not confuse pre-existing modifications with your work.

Do not add redundant docstring-only test files. The later implementation slice needs the behavioral cases in spec section 7, especially YAML failures, lexical inheritance, ID migration, and preservation of authored KGDB facts.

## Implementation entry points for a separate agent

SLDB: `selfdoc/python_scanner.py`, `selfdoc/python_symbol.py`, `selfdoc/python_materialize.py`, `models/python_symbol_doc.py`, `models/knowledge_tag.py`, `store/semantic_tags.py`, `store/export.py`, and `cli/selfdoc_inspect.py` (all under `src/sldb`).

KGDB contracts: sibling `kgdb/src/kgdb/models/relation_doc.py`, `relation_type_doc.py`, and `builtin.py`. Python containment is not a currently shipped builtin; reuse the registry mechanism, not model-only `extends` for code classes.

spec2viz: run `spec2viz diagram schema --type component`. The local sibling source is `spec2viz/spec2viz/models/component.py`; existing curated examples are in `docs/architecture/spec2viz/`. Preserve node/edge meanings through an adapter; do not create a parallel semantic taxonomy or match curated nodes by fuzzy labels.

## Delivery checkpoint

Pilot validation on 2026-09-14:

- IDs: `sldb.selfdoc.python_symbol` and `sldb.selfdoc.python_symbol.PythonSymbol`. Both leading YAML mappings and local tags validated against the existing tag type; AST parsing succeeded.
- Both narrative documents passed `ArchitectureNarrativeDoc` extraction/render/extraction checks. The pilot class passed the production `plan_python_documents` round-trip guard with the blank-line precaution described above.
- Focused suite: 305 passed; two warnings about existing pytest configuration/parametrization.
- First compact-frontmatter sync attempt was rejected during planning, before writes. This reproduced the literal-rendering gap above; it was not bypassed by disabling validation.
- Final `python-sync`: JSON `ok: true`, 1,233 documents, one written (the pilot class reference), no missing/changed/untracked/stale/removed/renamed findings.
- Subsequent `python-check`: JSON `ok: true`, zero written, same empty findings. `semantic_gaps: 1233` remains expected under the current placeholder-only logic.

The next agent should append its four annotated IDs, commands/results, unresolved questions, and a next bounded batch. Completion of an annotation batch does not close the active self-documentation task or imply the spec is implemented.

## Batch 2 delivery checkpoint (2026-09-14)

Annotated the four assigned declarations; the two files now follow the pilot format with the blank line before the closing `---`.

- IDs: `sldb.selfdoc.planned_document`, `sldb.selfdoc.planned_document.PlannedDocument`, `sldb.selfdoc.report`, `sldb.selfdoc.report.DocumentationReport`.
- `kind: core` confirmed for all four from the consumer evidence: `PlannedDocument` is the typed data contract `materialize.py` / `python_materialize.py` produce and `selfdoc_write.py` / `selfdoc_inspect.py` consume; `DocumentationReport` is the typed findings contract those consumers fill and `cli/commands/selfdoc.py` prints as JSON. Recorded ambiguity: `DocumentationReport` also doubles as the CLI's stdout JSON surface, so a reviewer could argue `interface`; kept `core` because the command, not the model, is the user-facing surface.
- Prose limits recorded: `PlannedDocument` is a planning record, not a filesystem transaction (the write path re-verifies before-images in `write_documents`); `DocumentationReport.ok` ignores `semantic_gaps`. Review clarified that it means no checked findings were populated, not a guarantee of complete detection or semantic correctness.

Fixture validation: `ast.parse` plus `ast.get_docstring(clean=True)` on both files; each leading YAML mapping parsed, keys limited to `id`/`kind`/`tags`, no `edges`/`contains`, all four IDs matched this handoff, and every tag validated against `KnowledgeTag`.

- Focused suite: `PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q tests/selfdoc tests/test_clean_code_rules.py` → 305 passed, the same two pre-existing pytest configuration/parametrization warnings.
- `python-sync` (same options and environment as the pilot): JSON `ok: true`, 1,233 documents, `written: 4`, empty `missing`/`changed`/`untracked`/`stale_indexes`/`removed`/`renamed`. Four writes, not two: annotating the module docstrings changed each file's `source_sha256`, so the class references plus the generated `model_name` and `ok` property references were refreshed. `semantic_gaps: 1233` unchanged, as expected under placeholder-only logic.
- `python-check` (identical invocation): JSON `ok: true`, zero written, all findings empty.
- After editing this handoff and the task progress note: `sldb stores update` and `sldb stores check` through the same `.venv` and `PYTHONPATH`; store integrity passed with no new unintended changes.

No adapter implementation was started; annotations are source text plus generated reference refreshes only. Unresolved questions carried forward: the compact-frontmatter rendering fix, module-record indexing, the `--source-root src --package sldb` identity migration, and the scanner's module/package record gap all remain outside annotation batches.

### Review corrections before batch 3

The batch-2 YAML and freshness checks passed, but the prose incorrectly promised one-to-one rename matches and universal command-exit gating by `ok`. `DocumentationReport` and the misleading `rename_candidates` helper docstring now describe the actual behavior: ambiguous rename matches can depend on plan order, and Python check/sync currently return zero independently of the JSON finding status. Their algorithms are unchanged; correcting the prose is not fixing those runtime limitations.

The import-versus-containment mistake in the next-batch instructions is corrected below. Spec sections 4.1–4.2 define typed import bindings, separate annotation-reference sites, scope/alias/resolution evidence, and acceptance cases grounded in `command.py`. The implemented source-fact graph covers direct static bindings and resolvable annotations; its deliberate limits are recorded in the specification.

Review validation: 305 focused tests passed with the same two warnings; all six existing annotated declarations passed AST/YAML/tag fixture checks; both narrative documents round-tripped through SLDB. The two import bindings and field annotation expressions in spec section 4.2 were checked against the actual AST. `python-sync` returned JSON `ok: true` with 11 references refreshed (the containing-file hashes affect all symbols in `report.py` and `selfdoc_inspect.py`); subsequent `python-check` returned `ok: true`, zero written, and empty findings. The placeholder-only `semantic_gaps` count remains 1,233.

### Source-fact implementation checkpoint (2026-09-14)

`python-sync` now writes `.kgdb/python-source.graph.json` through KGDB's public ingest command. It replaces only this generated graph and carries producer/source hashes, spans, lexical containment, import binding metadata, local/external targets, and annotation-reference evidence. `python-check` compares the expected AST projection with the saved graph and exposes `kgdb_stale`; a missing/stale graph is a nonzero check result. It does not mutate SLDB semantic export v1 or human-authored KGDB relations.

The Python exit-status and ambiguous-rename bugs are fixed. Full validation: 518 tests passed (two existing pytest warnings); a repository sync reported 1,273 documents and no findings, and the next check reported zero writes. The generated graph was queried with KGDB: `CommandRecord.arguments` has a `references` edge to `ArgumentRecord`, distinct from its module's `imports` and `contains` edges.

### Next bounded batch proposal (batch 3)

Four more declarations, same rules and consumers-first reading:

| Source | Declarations / proposed stable IDs | Evidence to read |
|---|---|---|
| `src/sldb/selfdoc/command.py` | `sldb.selfdoc.command`; `sldb.selfdoc.command.CommandRecord` | `selfdoc/materialize.py`, `selfdoc/projection.py`, `selfdoc/parser.py` |
| `src/sldb/selfdoc/parser.py` | `sldb.selfdoc.parser`; `sldb.selfdoc.parser.ParserScanner` | `cli/commands/selfdoc.py`, `cli/selfdoc_context.py`, `tests/selfdoc/test_parser.py` |

`ArgumentRecord` and `ExclusiveGroup` are imported from `argument.py` and `constraint.py`; they are not nested declarations. Leave their defining files and parser methods unchanged. Do not add import lists or edges to docstrings. Explain `CommandRecord` as a data contract and `ParserScanner` as an argparse-tree extractor, not as another record model. Keep `kind: core` only when the actual responsibility supports that classification; record ambiguity otherwise.

Before syncing, check every behavioral claim against executable statements in its producer/consumer, not merely existing docstrings or `Field` descriptions. The rename claim above demonstrates that those descriptions can themselves be wrong. AST/YAML validity and green freshness checks do not validate prose. Keep the scope to these four annotations, progress notes, and derived references/indexes; implementing sections 4.1–4.2 needs a separate implementation batch.

### Documentation-only delivery checkpoint (2026-09-14, Pron exposure)

Documentation-only pass against the Pron capability (iteration 4 closed in the Pron repo during this work; nothing under `src/`, `knowledge/`, or the store contents was modified):

- `self-documentation.md` example paragraph corrected and completed: the direct query `does CommandRecord reference` returns only the targets of the AST `references` relation (annotation references); import bindings are queried with `does ... import`. Facts are static and as of the last `python-sync`; Pron's freshness guard compares merged-graph hash against the source-fact artifact, `python-check` detects source-versus-artifact drift, and the remedy after changing source is `python-sync` (`pron refresh` alone only re-merges an already-current artifact). Agents never read `.kgdb/` artifacts.
- New spec section **4.3 "Query contract: Pron is the agent-facing surface"**: virtual read-only `PythonSymbol` (noun `python symbol(s)`), node kinds `python_symbol`/`python_module`/`python_external`, relations `contains`/`imports`/`references` plus base verb forms; four real commands with real outputs; `does ... <verb>` auxiliary rule limited to source relations; trace-as-provenance (`pron graph ...` + `kgdb edges_from/to ...`); exact-identity-first name resolution; stale-graph behavior and message; static limits (no runtime calls, re-export chains, star imports, shadowing).
- Exposure paragraph updated to the implemented iteration 4: `ProjectionDoc.source_symbols` is an explicit opt-in (`true` enables, `false` excludes, undeclared keeps previous behavior; the local `all` projection exposes it) and `source_relations` selects a subset of the three relations; source relations are read-only in every projection.
- Validation: `sldb stores update` (1,571 documents, 0 missing) and `stores check` PASS after each edit round.

Still pending (unchanged scope): federation of source symbols, curated aliases, strict metadata validation, inherited tags, legacy-ID migration, typed relation registration, spec2viz projection.
