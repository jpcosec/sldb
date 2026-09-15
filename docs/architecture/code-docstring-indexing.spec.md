# Python Docstring Indexing Contract

This specification records the agreed target behavior for code self-documentation: SLDB indexes declarations in source docstrings, the Python AST supplies structural evidence, KGDB owns persisted relationships, and spec2viz renders graph projections. It is a contract for implementation, not a claim that the current scanner already supports it.

Status: the source-fact adapter is implemented for lexical containment, imports, and annotation references, and `python-sync` materializes the corresponding SLDB documents and a regenerable KGDB snapshot. Strict metadata validation, inherited tags, legacy-ID migration, typed relation registration, and spec2viz projection remain pending. Consumers may use the published store facts through their own normal interfaces; no consumer-specific vocabulary belongs in this adapter. Continue through the [handoff](code-docstring-indexing-handoff.md) and [active task](../../desk/tasks/task-build-code-self-documentation.md).

## 1. Ownership

| Information | Source of truth | Consumer |
|---|---|---|
| Stable identity, local classification, local tags | Leading docstring frontmatter | SLDB code adapter and indexes |
| Purpose and behavioral explanation | Docstring body and code | Generated reference |
| Stored representation and source format | Model semantics | SLDB semantic index and every consumer |
| Declaration kind, location, lexical containment, resolvable dependencies | Python AST | Source-fact adapter |
| Effective tags and their inheritance provenance | Local declarations plus lexical context | SLDB indexes and KGDB ingestion |
| Persisted structural and reviewed semantic relationships | KGDB | Pron graph queries and spec2viz projections |
| Diagram layout and presentation | spec2viz specification | Renderer |

No `edges`, `contains`, dependency lists, or graph copies belong in docstring frontmatter. Source extraction can emit relationship facts without becoming a second graph store. Hand-authored semantic relationships belong in KGDB when they cannot be established from source evidence.

Every tracked record is physically rendered as Markdown, so `representation.markdown` is a base semantic tag. This does not mean every record describes a Markdown source: the base source tag is `source.document.markdown`, while the Python adapter replaces it with `source.code.python`. Consumers filter these semantic tags instead of inferring format from a folder, filename, or model name.

## 2. Docstring profile

Use the same YAML frontmatter idiom as SLDB documents, at the start of the docstring returned by `ast.get_docstring(node, clean=True)`:

```python
"""---
id: example.module.Record
kind: core
tags: [type:code.symbol]

---
Represent the facts collected from one source declaration.

Describe responsibilities, inputs, outputs, and important limits here.
"""
```

The initial profile has exactly three allowed keys:

- `id`: required nonempty string, unique within the selected store; explicit identity survives a move or rename until intentionally changed.
- `kind`: optional nonempty string, using the same classification as the corresponding spec2viz component node. Existing SLDB diagrams use `core`, `interface`, and `boundary`; spec2viz accepts other strings, but an annotator must not invent a competing vocabulary without review.
- `tags`: optional list, default empty; each value validates as the existing `KnowledgeTag` (`namespace:value`, e.g. `topic:selfdoc`). Duplicate values normalize to one value.

This is a new code-adapter profile, not an assertion that every existing SLDB model accepts these keys. `kind` in this profile is semantic classification; the existing `PythonSymbol.kind` / `PythonSymbolDoc.kind` is an AST node kind such as `ClassDef`. An implementation must retain both without overwriting one with the other.

Only an opening line exactly `---` starts metadata; a later `---` in prose is ordinary content. Require a closing delimiter, safe YAML loading, a mapping, unique keys, correct types, and no unknown keys. Malformed metadata or duplicate IDs must produce source-located diagnostics before any writes; never silently discard invalid declarations. An empty body is a documentation gap, not permission to fabricate an explanation.

The blank line before the closing delimiter in the pilots is valid YAML and a temporary rendering precaution: the current materializer embeds raw docstrings as Markdown, where `tags: ...` immediately followed by `---` becomes a setext heading. That compact form currently fails its round-trip check. Both forms must be accepted by the future adapter; whitespace is not a semantic requirement. Literal source content needs a safe rendering boundary rather than relying on author formatting.

Ordinary docstrings without frontmatter remain valid scan inputs. Keep their text and structural facts; report absent declared identity/classification separately. A qualified source reference may serve as a provisional identity, but must not be presented as stable across renames. Parse source statically: do not import or execute the target modules.

The first body paragraph supplies the generated purpose verbatim after whitespace normalization. The remaining body supplies the detailed explanation; source facts and declared context supply architectural placement. A missing role or ambiguous explanation is reported for review, not guessed from a filename. Do not require a second manually authored copy of this information in every generated Markdown record.

## 3. Lexical context and tag inheritance

Index package/module docstrings as well as classes, functions, async functions, methods, and nested declarations. A package's `__init__.py` supplies its package context; it must not create two competing identities for the same package. Modules without docstrings still supply structural context. Declarations inside conditional/try blocks retain their nearest lexical declaration owner, with conditional evidence where applicable.

Inheritance follows the lexical package → module → class/function → nested declaration chain within the selected store and source root. Do not inherit through imports, calls, Python base classes, sibling modules, or a parent store. Only ancestor contexts included in the selected scan participate; absence must not trigger an unbounded filesystem search.

| Namespace or field | Rule |
|---|---|
| `system:*`, `workspace:*` | Nearest declaration wins, independently per namespace. More than one distinct local value in either namespace is an error. |
| `topic:*` | Union of ancestor and local values, deduplicated. |
| Other tags, including `type:*` | Local only in this initial profile. |
| `id`, semantic `kind`, body | Local only; never copied from a parent. |

Keep `local_tags` and `effective_tags` distinct in the adapter contract. Every inherited value retains the ancestor identity and source location that supplied it. Never write derived tags back into descendant docstrings. Removing an ancestor declaration or changing a context tag must remove obsolete derived values on the next successful reconciliation.

Retain colon notation in tag payloads. The existing model `__semantics__` flattener's dotted paths are a separate representation; this specification does not authorize silently converting colon tags into dotted names or claiming that dotted semantic-parent edges already implement lexical inheritance.

## 4. Structural relationships and KGDB

Containment is inferred from lexical ownership, not manually annotated. A module owns its top-level class; that class owns its methods. Imports and inheritance provide additional syntactic evidence, but not every reference resolves statically.

- Produce one immediate-parent containment fact per contained declaration; transitive containment is a query, not redundant authored data. A separate `defines` relation, if required by a consumer, must be a documented projection of those facts rather than an independently maintained list.
- Resolve dependencies using import bindings, aliases, relative import level, and lexical scope. Preserve unresolved/external references as diagnostics or explicit unresolved facts; do not create a supposedly resolved local edge by matching a short name.
- Emit inheritance or call-target edges only when the target can be resolved under documented static rules. Dynamic dispatch, decorators, conditional imports, and reflection must not be reported as certain runtime behavior. An import does not automatically imply a business-level `uses` relationship.
- Each derived fact carries source path, source span, containing-file hash, extraction version, and resolution status. File hashes establish source freshness, not individual-symbol equivalence or a complete runtime call graph.

Bind relation names and endpoint constraints through KGDB's existing `RelationTypeDoc` registry. The store registers `contains` (`python_module|python_symbol → python_symbol`), `imports`, and `references` (`python_module|python_symbol → python_module|python_symbol|python_external`), all directed and many-to-many. The adapter loads those tracked records and validates every emitted endpoint before publication. KGDB currently ships structural types such as `has_document` and model-only `extends`; do not misuse those for Python code endpoints. Register or reuse an appropriate code relation type in the KGDB integration slice, then use that exact name everywhere. Do not add a private SLDB edge enum.

Persist through the supported KGDB ingestion boundary. Reconciliation replaces only facts owned by this extractor, in its store/source-root scope, after a successful scan. It is idempotent; failed/partial scans must not remove existing facts. Preserve manually reviewed relationships and other producers' edges. Disappearing endpoints and conflicts must be surfaced for review rather than deleting authored knowledge silently.

Explicit source IDs, current generated Markdown document IDs, and KGDB node IDs are different address spaces. Maintain an explicit mapping from `(store identity, declared source id)` to the tracked SLDB export address and then to its KGDB address. Reuse KGDB's store-qualified addressing, not machine-local absolute paths or a second global-ID convention. Never silently rename existing tracked documents to match new source IDs.

The current `sldb_kgdb_semantic_export` v1 excludes source-code edges and raw bodies. The implemented source adapter therefore writes a separate regenerable KGDB GraphSnapshot through `kgdb ingest`, by default `.kgdb/python-source.graph.json`; it does not mutate v1. Its `contains`, `imports`, and `references` edge tokens are source-fact projection vocabulary with `origin: python_ast`, not authored `RelationDoc` edges. The JSON artifact is a producer detail behind SLDB's publishing boundary, not a second source of truth. A later typed-relation integration must register/validate the vocabulary without altering this provenance boundary.

### 4.1. Import bindings and reference sites

An import introduces a name in a lexical scope; it does not define the imported declaration there. Extract one typed binding fact per imported name, not a single module-name string for the whole statement. This is AST-derived adapter data, never another docstring frontmatter key.

| Binding fact | Required meaning |
|---|---|
| Importer and scope | Source module and lexical owner of the import statement |
| Syntax | `Import` or `ImportFrom`, source module spelling, relative level, imported name, explicit alias if present |
| Local binding | The name introduced in that scope, separate from the requested module/symbol |
| Resolution | Canonical target reference when proven, otherwise explicit external/unresolved/ambiguous status; preserve the requested reference even without a target |
| Evidence | Source span, containing-file hash, extractor version, and conditional/type-checking context when present |

For `import a.b`, the local binding is `a`; for `import a.b as c`, it is `c`. For `from .argument import ArgumentRecord as AR`, retain module `argument`, relative level `1`, imported name `ArgumentRecord`, and local binding `AR`. Resolve relative imports against the importer's package, not its working directory. A binding to a proven local re-export must follow its explicit provenance chain or remain unresolved; never guess the definition from the imported name alone.

Star imports cannot be expanded into invented local names. Dynamic imports are not ordinary `Import`/`ImportFrom` bindings and must not be reported as resolved without a separately documented rule. Imports under conditions, inside functions, or under `TYPE_CHECKING` retain that context; their presence does not prove execution. Do not import target modules to resolve them.

Extract reference sites separately from imports. A reference fact identifies its lexical owner, source expression and span, context (such as a type annotation or call), and resolved binding/target when proven. Name rebinding or shadowing must be accounted for; uncertain resolution remains explicit. A syntactic annotation reference does not establish a runtime call, instantiation, containment, or business-level dependency. Importing alone does not establish use or intentional public re-export, and imported declarations do not inherit the importer's tags.

### 4.2. Acceptance example: imported field types

In `src/sldb/selfdoc/command.py`, `from .argument import ArgumentRecord` and `arguments: list[ArgumentRecord]` provide different evidence:

| Fact | Expected owner / target |
|---|---|
| Definition / containment | Module `sldb.selfdoc.argument` owns its `ArgumentRecord` declaration |
| Import binding | Scope `sldb.selfdoc.command` binds `ArgumentRecord` to `sldb.selfdoc.argument.ArgumentRecord` |
| Annotation reference | Field site `CommandRecord.arguments` references that binding in `list[ArgumentRecord]` |

The analogous `ExclusiveGroup` target is `sldb.selfdoc.constraint.ExclusiveGroup`. Neither imported class is nested in `CommandRecord` or defined by `command.py`. These qualified names identify expected source targets; they do not assign new declared frontmatter IDs to unannotated classes. A field reference site can be addressed by its owning declaration and source span without requiring a separate field docstring or graph node.

The integration must bind these distinct meanings through registered KGDB relation types and retain import/reference evidence. Do not substitute containment for importation or collapse an annotation reference into a generic `uses` edge. spec2viz consumes the resulting KGDB projection through section 5; it does not perform a second semantic interpretation.

Acceptance cases must include these two concrete imports, aliases, `import a.b` versus `import a.b as c`, multi-name statements, relative imports, nested scopes, shadowing, conditionals/`TYPE_CHECKING`, unused imports, unresolved/external targets, re-export chains, and star imports. Removing a reference while retaining its import removes only the reference fact. No case may introduce false containment or imported-tag inheritance.

The legacy `PythonScanner` still stores a simplified import string in generated Markdown records. The separate source-fact adapter now preserves imported names, aliases, lexical owners, relative levels, spans, hashes, local/external targets, and annotation references in KGDB. Its current resolution is lexical and static: it does not follow re-export chains, infer star imports, prove runtime calls, or fully model shadowing/type-checking conditions. Those cases remain explicit follow-up work rather than invented edges.

### 4.3 Consumer boundary

The adapter publishes store-owned facts, not a conversational language or a consumer-specific graph view. `PythonSymbolDoc` documents are ordinary tracked SLDB records; the KGDB snapshot carries the derived structural facts and their AST provenance. Consumers—including Pron, spec2viz, an agent, or another UI—must consume those published records and relations through their normal SLDB/KGDB integration boundary. They must not depend on private artifact paths, add adapter-specific model names to their own runtime, or re-derive AST meaning from source.

`python-check` is the authority for source-to-publication freshness: it reports `kgdb_stale` when the persisted snapshot no longer represents the selected source root. The facts are static as of the last successful `python-sync`; they certify lexical containment, import bindings, and resolvable annotation references only, not runtime calls, re-export chains, star imports, or shadow-resolved names (section 4.1).

A consumer may add its own display aliases or query syntax only as ordinary consumer configuration over registered store identities and relation types. Such configuration is not part of the Python adapter and must not change or duplicate the KGDB facts.

## 5. spec2viz is a projection, not another semantic mapper

Use the existing component schema: `nodes[id].label`, `nodes[id].kind`, `nodes[id].contains`, and `edges[].from`, `to`, `relation`, `label`. `contains` in a generated diagram is a projection of KGDB containment; it is not source frontmatter. Adapter output must validate with `spec2viz diagram validate`.

Resolve projected node IDs from the explicit identity mapping. Labels come from source names or authored display text; `kind` comes from local classification; relation names come from KGDB relation types. Translate KGDB's `source_id`, `target_id`, and `relation_type` to the corresponding spec2viz fields without reclassifying their meaning. Projection filtering must not leave dangling `contains` entries or edge endpoints.

The current AST generator's `module_*` / `class_*` IDs and curated diagram IDs such as `CLICommands` are not automatically equivalent to declared source IDs. Linking code to a curated architectural group requires an explicit KGDB association, not fuzzy matching or another list in docstrings. Do not insert arbitrary metadata into component nodes: the current schema ignores unknown fields.

A reference to a spec file plus its hash establishes which artifact was referenced. It does not prove symbol-to-node membership, semantic review, or that the diagram is current against source.

## 6. Two pilot declarations and expected interpretation

The [module and class docstrings](../../src/sldb/selfdoc/python_symbol.py) are the pilot fixtures. After the adapter is implemented, they must yield:

| Declaration | Declared ID | Semantic kind | Local tags | Effective tags |
|---|---|---|---|---|
| Module | `sldb.selfdoc.python_symbol` | `core` | `system:sldb`, `workspace:knowledge`, `topic:selfdoc` | Same as local tags |
| Class | `sldb.selfdoc.python_symbol.PythonSymbol` | `core` | `type:code.symbol` | `system:sldb`, `workspace:knowledge`, `topic:selfdoc`, `type:code.symbol` |

The AST supplies one immediate module → class containment fact. The class's AST kind remains `ClassDef`. The three inherited class tags cite the module as their origin; the class's ID, semantic kind, and `type:code.symbol` are local. Its base `BaseModel` is external to the selected SLDB source tree and must not be guessed to be a local class. No graph relation appears in either frontmatter block.

These expected results are normative fixtures, not current CLI output. Today the scanner returns the class docstring as text, does not emit the module record, and does not calculate inherited tags or consume the declared ID.

## 7. Acceptance and migration

Implementation is complete only after checks cover metadata parsing/diagnostics; ordinary docstrings; lexical scope including packages and nested/conditional definitions; inherited tag origin, override, removal, and store isolation; separate AST/semantic kinds; ID collisions and explicit legacy mappings; resolvable and unresolved dependencies; KGDB relation-type validation and producer-scoped reconciliation; and a validated spec2viz projection using the same identities and relation names.

Generated references must round-trip through SLDB, keep generated source facts distinct from authored graph knowledge, and synchronize idempotently. Existing authored `purpose`, `architecture`, and tags must not be silently overwritten: when migrating to source-owned prose, report differences and require an explicit reconciliation decision. A source docstring containing headings or fences must survive materialization without becoming an accidental document section.

Report missing declarations, missing explanation, unresolved mapping, and stale source separately. The current `semantic_gaps` counter only detects empty authored placeholders; it cannot establish that a source docstring lacks meaning or measure compliance with this contract.

This delivery intentionally leaves implementation and broad annotation pending. The next annotation pass should work in small reviewed batches, document only evidence-backed responsibilities, and record ambiguities instead of inventing architecture.
