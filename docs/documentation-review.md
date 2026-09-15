# Documentation Review and Remaining Gaps

Reviewed on 2026-09-13 against this working tree, including pre-existing local code changes. This is a findings register, not a claim that the entire documentation corpus or every runtime behavior has been audited. The focus is operational accuracy and missing contracts, rather than adding another manual.

## Field Ownership and Section Spans

**High priority — reproduced runtime defect.** `cli/graph_ops/map_fields.py` compares marker line numbers in the template with heading line numbers in the rendered document. Lists, frontmatter, and multiline fields change their relative positions. This can assign a field to the wrong section.

Reproduction with the bundled `SLDBGuide`: create a document from `guide.data.yaml`, then run `ast show docs/guide`. `how_it_works` is assigned to `sldb-example-guide/why-structured-reversible-documents-help`; `model_rules` is assigned to `sldb-example-guide/how-it-works`. Both disagree with their headings in the document. The same incorrect ownership reaches `sections fields`.

The example also emits unknown-marker warnings for mapping fields and literal marker examples. Nested mapping fields such as `frontmatter.example` have null ownership. Existing ownership tests pass but do not establish correctness for this variable-length example.

**Contract gap:** section `line_start`/`line_end` originate from the heading token in `cli/graph_ops/extract.py`. They do not bound the entire section body. `sections show` also has two JSON shapes: persisted entries expose top-level line fields, whereas the IR fallback nests them under `span`.

Resolved on 2026-09-14: field ownership is now determined against the template's heading order and projected to the rendered document's corresponding heading order. It is therefore independent of expansion length. A template/rendered heading-count mismatch is reported and yields no speculative ownership. Section `line_start` is the heading line and `line_end` is the last body line before the next heading at the same-or-higher level (or the document end). Persisted indexes and the IR use this same inclusive span. Regression coverage includes expanded lists and nested section spans. Repeated equal headings still need a stable, non-positional address design; the current hierarchical slug path is not sufficient for that case.

## FAQ and Explore Do Not Use the Store

**Medium priority — reproduced anchoring defect.** `FAQCLI.run` opens `Path(args.faq_path)`. Its parser defaults to `docs/faq.md` and has no `--store` option. It never calls the store resolver. The existence of a project store therefore cannot anchor this command.

`explore` and `docs explore` similarly pass working-directory-relative `docs` and `src` paths to filesystem searches. Despite the `docs explore` help mentioning tracked documents, the handler does not load the store's document inventory.

Reproduction from a directory without `docs/faq.md`: `sldb faq` exits with `No such file or directory: 'docs/faq.md'`. This is also reproducible from a subdirectory of this repository, where a store-backed command could discover the ancestor store.

Current workaround: pass an absolute `--faq-path`, or absolute `--docs-root`/`--code-root`. These options select files directly; they do not provide store integration. `pyproject.toml` does not bundle the repository FAQ as package data.

Resolved for project stores on 2026-09-14: `faq` accepts `--store` and anchors a relative `--faq-path` to the selected project root. `explore` and `docs explore` accept `--store` and anchor relative roots likewise; absolute paths retain their direct-file behavior. Package-help and installed-wheel assets remain a separate packaging decision.

## Ancestor Discovery and the Global Store Registry

Follow-up inspection on 2026-09-13 confirms that `store/resolver.py:find_local_store` already walks the current directory and its ancestors, returning the nearest valid `.sldb`. From this repository's `src/sldb` directory it resolves the repository store correctly. Resolver and linked-structural tests: 6 passed.

The missing behavior is broader context consistency and registry maintenance:

- FAQ and explore bypass discovery, as described above. Some model imports and explicit relative path arguments also remain cwd-dependent.
- Discovery returns one store; it does not return a chain of ancestor registries. `_resolve_store_arg` checks aliases only in the nearest local store, not in enclosing stores or a separate global catalog. Federated model lookup checks destination and local registries, likewise without a full ancestor chain.
- `stores init` creates only the selected store. `stores add` adds a one-way reference to the selected registry. Neither automatically registers the store in `~/.sldb` or its enclosing store.
- Actual local state: `/home/jp/.sldb/core/store_index.yaml` has zero store references. A scan of `/home/jp/proyectos/hum-ecosystem/tools` found 12 project stores, excluding `.tmp`; none is referenced by the global store. This is a scoped scan, not a census of the entire machine. This repository's store also has zero outgoing store references.
- `load_runtime_documents(..., include_linked=True)` loads the selected store and its direct links only. `--global`/`gse` therefore do not imply a scan of `~/.sldb`, all descendant stores, or transitive federation.
- Because discovery walks through the home directory, `~/.sldb` itself can be returned as an ancestor store. In that case the separate global-fallback policy in `store_context.py` is bypassed. A unified contract must account for this case.

Proposed contract for review, not implemented here: explicit store selection chooses the active target; otherwise the nearest enclosing store does. All project-relative operations use its project root. Alias lookup searches that store, enclosing registries, then the global registry, with nearer names taking precedence. The global registry catalogs known descendant stores and is reconciled during explicit store lifecycle/discovery operations; it is not inferred to be complete just because the directory exists.

Needed decisions and checks: whether each parent catalogs direct children or all descendants; how existing stores are discovered and stale paths repaired; identity and name collisions; whether global queries traverse the catalog or recursive links; deduplication and cycle handling. Ancestor discovery selects context, while catalog maintenance establishes discoverability; implementing only the former cannot provide the latter.

Implemented on 2026-09-14: the nearest non-global ancestor store is the default project context; `~/.sldb` is a fallback rather than an accidental ancestor project. Alias resolution now searches local/ancestor registries and then the global registry, with nearer entries winning. `stores init` explicitly creates or updates the global catalog for stores beneath the user home directory. Federated document loading traverses explicit links transitively, deduplicates canonical paths, and terminates cycles. Reads do not scan or mutate the filesystem. `stores reconcile --path <subtree>` now reports discovered, missing, and stale catalog paths; `--apply` replaces the catalog with the explicitly discovered subtree.

## Structural CLI Coverage

The old `get_block`, `get_section`, `get_owner_section`, and `find_blocks` names were design sketches, not implemented public functions. Their usable counterparts are now listed in [AST queries](ast_query_primitives.md).

The existing CLI exposes `document.ir.surface`, `structure`, `nodes`, and `context_index`. External JSON traversal can inspect blocks. Native `fields` and `sections` commands cover typed values and indexed section metadata. There is no native general-purpose block predicate language, stable block address, or command that returns a section's complete body AST by heading.

Needed: define stable versus positional identifiers, heading collisions, complete-body selection, and which parser attributes survive the surface projection. These are gaps to evaluate, not promises to add hardcoded functions.

## Composition

**Corrected documentation:** the summary formatting key is `template`, not `line_template`. The current [composition reference](composition_modes.md) distinguishes model-driven rendering from `![[...]]` transclusion.

Remaining limits: model-driven child paths resolve from the working directory; invalid/missing children may disappear silently; generated summaries do not support edits propagated to source documents. Section-only and query-driven composition remain historical proposals. Needed: document and test path anchoring, skipped-child diagnostics, cycles, and depth behavior across both mechanisms.

## Self-Documentation from the Codebase

Implementation follow-up: `selfdoc scan|sync|check` now tracks the parser-derived CLI reference, and `selfdoc python-scan|python-sync|python-check` tracks static Python symbols; see [the operational reference](self-documentation.md). Python records carry qualified identities, spans, signatures, docstrings, imports, source hashes, conservative rename candidates, and an optional hash-pinned spec2viz reference. The generated `python-ast.yml` view validates and renders as Mermaid. This does not infer semantic architecture: the current `semantic_gaps` metric is the explicit authored-review queue. See [the active task](../desk/tasks/task-build-code-self-documentation.md).

Delivery evidence: 85 command/surface documents synchronized; authored fields preserved in all 78 pre-existing records; check succeeds from the repository root and a subdirectory. The full suite passes 492 tests, including clean-code checks after splitting the knowledge models while preserving public imports. The three follow-up tasks and their context pill are tracked and routed by the board. Local store reindex processed 238 documents with no missing files; global registry behavior remains unchanged.

Follow-up on 2026-09-13: the intended direction is for this repository to document itself through derived, tracked records. Maintaining handwritten command inventories should not be the primary update mechanism.

Existing building blocks:

- `cli/commands/explore_code.py` already uses Python `ast.parse` and `ast.get_docstring` for module/class/function search. It returns search hits, not a persistent symbol inventory or dependency graph.
- `models/knowledge_surface.py` defines `CliCommandDoc` and `SurfaceDoc`; `knowledge/` already contains corresponding records. No connected parser-to-document synchronization entry point was found in this checkout.
- Introspection of `build_parser()` extracted 59 leaf commands with non-suppressed command help, including argument names, required flags, defaults, choices, and help text, without executing handlers. Hidden commands need an explicit inclusion policy. Argparse adapters can recover the assembled command tree even when definitions use helper functions and loops.
- `core/ingest/scanner.py` exposes `scan_codebase` and `scan_python_sources`, but the Python adapter delegates to `wiki_compiler` and uses external `kgdb`/`ontology` contracts. These dependencies are not declared in this package. `ingest_raw_sources` is a separate Markdown-only loop. These pieces are not an operational standalone Python ingestion CLI.
- The installed `spec2viz diagram generate` scans Python AST into component specs. Running it against `src --package sldb` generated 462 nodes and 1,104 edges; validation and Mermaid rendering succeeded. Its current generator extracts modules, top-level classes, and `ImportFrom` relationships. It skips `__init__.py`, does not resolve relative imports correctly, and does not infer domain intent, full call behavior, or architecture boundaries. Treat this output as structural evidence to refine, not a complete semantic architecture model.

Needed integration, rather than another handwritten reference:

1. A source inventory with identities qualified by store, module, and symbol, plus source paths/spans, hashes, signatures, docstrings, and explicit relationships.
2. Extractor adapters for Python AST and the assembled CLI parser, producing typed records usable by SLDB models. The Python AST and SLDB's Markdown/document IR are different representations and require a defined mapping.
3. A field ownership policy for documentation generation: code owns extracted signatures/options; declared or reviewed metadata owns semantic roles and rationale. Regeneration must preserve authored explanations and avoid a circular code-to-doc-to-code authority rule.
4. A repeatable scan/materialize/track/check operation: update changed records, detect removed or renamed symbols, preserve stable IDs, and report stale documentation. SLDB's existing document hashes do not automatically establish freshness against a Python source file.
5. Spec2viz views over those identities, with code-derived relationships and explicit semantic grouping. Clean code makes extraction and review easier; it does not establish stable identity, provenance, or semantic truth by itself.

Integration defect observed in the installed spec2viz: rendering the generated component spec with `--renderer json` raises `TypeError: data must be str, not ComponentIR`. Mermaid rendering works. No spec2viz source was changed.

The proof artifacts were generated under `/tmp/sldb-selfdoc-U4AUmW/`; this inspection did not install a new self-documentation command or track those artifacts in the project store.

## Versions and Historical Plans

The declared package version is `0.1.0`; “v1” is the product generation. The old changelog contains `0.1.1`, `0.1.2`, and `0.2.0` headings, and the README previously announced v0.5/v0.6 deprecations. These do not form a consistent release inventory.

README and changelog now distinguish current metadata, historical development records, and the freeze. The v0.6 removal promise has been retired from current guidance. Target architecture and migration documents are explicitly historical.

Needed before any release: reconcile registry artifacts and Git tags with their source metadata. Registry publication was not checked in this local review. No version bump, tag, commit, or publication was performed.

## Existing Features with Incomplete Guidance

| Surface | Evidence in code | Missing or fragmented guidance |
|---|---|---|
| HTTP store server | `cli/serve/routes.py`, `tests/test_serve.py` | Request/response/error examples for `/health`, `/schema`, `/graph`, `/kgdb/snapshot`, `/save`; current knowledge record lists flags but not route contracts |
| AST/IR | `cli/graph_ops/`, `core/ir/` | Shape stability, source-span semantics, parser attributes lost in projection, ownership failure modes |
| Model drafts | `cli/commands/models_validate*.py`, existing local edits | Validate active versus draft contracts, promotion failure behavior, empty/invalid tracked-document cases |
| Source ingestion | `core/ingest/` | Supported entry point and operational status; no `ingest` command in the public parser tree |
| Store anchoring | `cli/store_context.py`, `store/resolver.py` | One command-by-command contract for store discovery, alias resolution, cwd-relative arguments, and documentation search |
| Generated command records | `knowledge/commands/`, `knowledge/surfaces/` | Real invocations and examples; descriptions often repeat parser help and do not explain behavior |
| Architecture diagrams and dependency map | `docs/architecture/spec2viz/`, `architecture_map.md` | Regeneration against current imports; exhaustive map marked historical, diagrams not revalidated in this review |
| Packaging | `pyproject.toml`, CI | Wheel smoke tests for FAQ and all examples, including Pandoc Markdown assets |

## Verification

- Installed the already-declared `linkify-it-py` dependency in the existing `.venv`; it was missing. Also installed the declared development dependency `pytest` to run checks. Dependency declarations were not changed.
- `linkify-it-py` supports automatic URL/email recognition in the `MarkdownIt("gfm-like")` parser. Explicit `[[links]]` and transclusions use `links/parser.py` instead. Without linkify installed, the GFM parser fails even for Markdown without URLs.
- Both reference and Pandoc example validations passed after restoring the dependency.
- `tests/test_composition.py`, `tests/test_field_ownership.py`, `tests/test_cli_v2.py`, and `tests/test_links.py`: 55 passed. Pytest warns that `asyncio_default_fixture_loop_scope` is unknown in this environment.
- Created an isolated temporary store, registered `SLDBGuide`, created its document, and exercised field access, AST output, and section navigation. This exposed the ownership defect above despite the passing tests.
- Reproduced FAQ cwd failure and checked the explicit-path workaround.
- Executed all four documented AST/section JSON filters, checked the composition configuration snippet, and verified local file-link destinations in the 16 changed/new Markdown documents. Documentation diffs pass whitespace checks.

Documentation changes do not constitute a full standards audit. Existing code changes belong to the working tree and were preserved. The repository's store was not reindexed as part of this review.
