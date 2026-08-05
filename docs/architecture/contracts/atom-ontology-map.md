# Atom Ontology Map

## Purpose and governing sources

This contract maps the current `desk/atoms/` ontology: its typing axes, relation semantics, domain groupings, and the most structurally central atoms.

Governing sources:
- `also_core.md`
- `core_README.md`
- `desk/atoms/tag-namespaces.yaml`
- `docs/architecture/tag-domain-map.md`
- `docs/architecture/spec2viz/target-components.yml`
- `docs/architecture/spec2viz/target-runtime.yml`
- `docs/architecture/spec2viz/target-store-graph.yml`

## In-scope

- ontology axes for atoms
- relation semantics
- domain grouping of the current atom set
- foundational and cross-cutting hub atoms

## Explicit non-goals

- no runtime implementation claims
- no code parity claims
- no attempt to replace atoms with this map
- no rewriting of atom truth beyond classification

## Ontology axes

Each atom is typed along four orthogonal axes.

1. **Layer**
   - placement in the architecture stack
   - current layers: `core`, `shared`, `shell`, `store`, `runtime`
2. **Domain leaf**
   - exactly one `domain:*` leaf tag
   - primary ontology partition
3. **5WH1+ type**
   - the question shape the atom answers: `what`, `how`, `why`, `where`, `when`
4. **Graph relations**
   - typed links to neighboring atoms: `depends_on`, `supports`, `constrains`, `implements_with`

## Current ontology size

- total atoms = 201
- total domain leaves in active use = 48

### Layer distribution
- `core` = 55
- `runtime` = 1
- `shared` = 54
- `shell` = 64
- `store` = 27

### 5WH1+ distribution
- `how` = 57
- `what` = 92
- `when` = 14
- `where` = 20
- `why` = 18

## Relation semantics

- `depends_on` = prerequisite concept; the source atom needs the target atom to be coherent.
- `supports` = enabling or downstream contribution; the source atom strengthens or helps realize the target atom.
- `constrains` = limiting rule; the source atom narrows what the target atom is allowed to do or mean.
- `implements_with` = explicit implementation substrate; the source atom names the lower-level mechanism used to realize the target atom.

## Foundational hub atoms

These atoms receive the most incoming links and act as ontology spines.

### Highest incoming `depends_on`
- `[projection](../../../../desk/atoms/projection.md)` = 16
- `[canonical-ast](../../../../desk/atoms/canonical-ast.md)` = 15
- `[cli-workflow-surface](../../../../desk/atoms/cli-workflow-surface.md)` = 13
- `[node](../../../../desk/atoms/node.md)` = 11
- `[graph-store](../../../../desk/atoms/graph-store.md)` = 9
- `[node-hash](../../../../desk/atoms/node-hash.md)` = 9
- `[store-infrastructure](../../../../desk/atoms/store-infrastructure.md)` = 9
- `[canonical-identity](../../../../desk/atoms/canonical-identity.md)` = 8
- `[capability-model](../../../../desk/atoms/capability-model.md)` = 8
- `[revision](../../../../desk/atoms/revision.md)` = 8
- `[provenance-record](../../../../desk/atoms/provenance-record.md)` = 7
- `[transaction](../../../../desk/atoms/transaction.md)` = 7

### Highest incoming `supports`
- `[projection](../../../../desk/atoms/projection.md)` = 15
- `[search-projection](../../../../desk/atoms/search-projection.md)` = 12
- `[query-engine](../../../../desk/atoms/query-engine.md)` = 11
- `[structurednldoc-contract](../../../../desk/atoms/structurednldoc-contract.md)` = 11
- `[document-materializer](../../../../desk/atoms/document-materializer.md)` = 10
- `[graph-store](../../../../desk/atoms/graph-store.md)` = 10
- `[stable-selector](../../../../desk/atoms/stable-selector.md)` = 10
- `[create-vs-track-vs-update](../../../../desk/atoms/create-vs-track-vs-update.md)` = 9
- `[hook-runtime](../../../../desk/atoms/hook-runtime.md)` = 9
- `[how-to-get-data-out-of-sldb](../../../../desk/atoms/how-to-get-data-out-of-sldb.md)` = 9
- `[semantic-vs-physical-search](../../../../desk/atoms/semantic-vs-physical-search.md)` = 9
- `[store-integrity-checks](../../../../desk/atoms/store-integrity-checks.md)` = 9

### Highest incoming `constrains`
- `[cli-workflow-surface](../../../../desk/atoms/cli-workflow-surface.md)` = 3
- `[graph-store](../../../../desk/atoms/graph-store.md)` = 3
- `[code-linting](../../../../desk/atoms/code-linting.md)` = 2
- `[ports-and-adapters](../../../../desk/atoms/ports-and-adapters.md)` = 2
- `[projection](../../../../desk/atoms/projection.md)` = 2
- `[python-cli-orchestration-layer](../../../../desk/atoms/python-cli-orchestration-layer.md)` = 2
- `[rust-core](../../../../desk/atoms/rust-core.md)` = 2
- `[canonical-address](../../../../desk/atoms/canonical-address.md)` = 1
- `[canonical-ast](../../../../desk/atoms/canonical-ast.md)` = 1
- `[content-addressed-store](../../../../desk/atoms/content-addressed-store.md)` = 1
- `[create-vs-track-vs-update](../../../../desk/atoms/create-vs-track-vs-update.md)` = 1
- `[decision-pyo3-ffi](../../../../desk/atoms/decision-pyo3-ffi.md)` = 1

## Ontology by domain leaf

The domain leaf is the main partition of the atom space.

### `domain:architecture-boundaries` (10)

- `core`: `text-layer-vs-graph-layer`

- `shared`: `capability-model`, `effect-plan`, `kernel-api`, `lisp-metalanguage`, `ports-and-adapters`, `projection-plan`, `query-plan`, `semantic-export-boundary`, `transaction-plan`


### `domain:architecture-decisions` (12)

- `core`: `decision-blake3-hashing`, `decision-canonical-ast-over-markdown`, `decision-pyo3-ffi`, `decision-rayon-parallelism`, `decision-relation-ast-extensibility`, `decision-rowan-ast`, `decision-rust-core-with-minimal-python`

- `shared`: `decision-links-and-anchors-are-canonical`, `field-descriptions-are-required-contract`

- `store`: `decision-graph-store-over-yaml-indexes`, `decision-rusqlite-store`, `decision-search-index-library`


### `domain:architecture-integration` (3)

- `shared`: `document-source`

- `shell`: `agent-provider`, `semantic-provider`


### `domain:architecture-migration-strategy` (4)

- `shared`: `compatibility-surface`, `migration-unit`

- `shell`: `decision-v1-parity-before-scope-expansion`, `phase-1-v1-replication`


### `domain:implementation-python-cli` (2)

- `shell`: `git-orchestration-in-python`, `python-cli-orchestration-layer`


### `domain:implementation-rust-core` (2)

- `core`: `relation-ast-extensibility`, `rust-core`


### `domain:model-addressability` (7)

- `core`: `local-anchor`

- `shared`: `addressability-layer`, `canonical-address`, `derived-address`, `fragment-id`, `stable-selector`

- `shell`: `alias`


### `domain:model-anchors` (14)

- `core`: `anchor-sample`, `ast-anchor`, `ast-locator`, `dom-locator`, `page-locator`, `source-locator`, `syntax-locator`, `text-locator`

- `shared`: `document-path`, `locator-strategy`, `source-document-hash`

- `shell`: `anchor-comment`, `external-anchor`, `text-anchor`


### `domain:model-artifacts` (1)

- `shared`: `artifact`


### `domain:model-ast-core` (5)

- `core`: `canonical-ast`, `tree-spine`

- `shared`: `canonical-existence`, `canonical-identity`, `node`


### `domain:model-documents` (5)

- `core`: `non-reversible-document-family`, `reversible-document-family`

- `shared`: `document`, `revision`, `structurednldoc-contract`


### `domain:model-fields-schemas` (4)

- `shared`: `field-binding`, `field-path`, `schema-binding`, `type-contract`


### `domain:model-identity` (1)

- `core`: `identity-stability-rules`


### `domain:model-relations` (11)

- `core`: `dependency-edge`, `link-edge`, `link-reference`, `projection-edge`, `relation-ast`, `transclusion-reference`

- `shared`: `ownership-edge`, `reference-edge`

- `shell`: `derived-edge`, `semantic-edge`

- `store`: `store-edge`


### `domain:model-text-structure` (4)

- `shared`: `lead-paragraph-anchor-rule`, `shallow-title-plus-body-default`

- `shell`: `structured-text`, `text-as-graph`


### `domain:pipeline-emitters` (4)

- `core`: `document-materializer`, `emitter-compiler`, `markdown-emitter`, `renderer`


### `domain:pipeline-importers` (6)

- `core`: `canonicalizer`, `importer-translator`, `markdown-importer`, `parser`

- `shell`: `node-reconciliation`, `source-manager`


### `domain:quality-clean-code-generic` (1)

- `shell`: `code-linting`


### `domain:quality-clean-code-python` (1)

- `shell`: `python-code-linting`


### `domain:quality-clean-code-rust` (1)

- `core`: `rust-code-linting`


### `domain:quality-patterns-generic` (1)

- `shell`: `patterns`


### `domain:quality-patterns-python` (1)

- `shell`: `python-patterns`


### `domain:quality-patterns-rust` (1)

- `core`: `rust-patterns`


### `domain:quality-reliability` (4)

- `runtime`: `degraded-mode`

- `shared`: `failure-model`, `observability-surface`

- `store`: `corruption-state`


### `domain:quality-testing` (3)

- `shared`: `conformance-suite`, `golden-fixture`, `reference-behavior`


### `domain:quality-testing-generic` (1)

- `shell`: `testing`


### `domain:quality-testing-python` (1)

- `shell`: `python-testing`


### `domain:quality-testing-rust` (1)

- `core`: `rust-testing`


### `domain:runtime-adapters` (3)

- `core`: `matrix-adapter`, `prosemirror-adapter`, `tree-sitter-adapter`


### `domain:runtime-hooks` (4)

- `shared`: `hook-binding`

- `shell`: `effect-outbox`, `event-bus`, `hook-runtime`


### `domain:runtime-projections` (4)

- `core`: `projection`, `projection-spec`, `semantic-exporter`

- `shell`: `graph-projection`


### `domain:runtime-provenance` (2)

- `shared`: `provenance-record`

- `shell`: `authorship-state`


### `domain:runtime-query` (2)

- `core`: `query-engine`

- `shell`: `ast-as-the-debugging-surface`


### `domain:runtime-resolvers` (2)

- `shell`: `external-anchor-resolver`, `local-anchor-resolver`


### `domain:runtime-semantic` (7)

- `shared`: `concept-binding`, `semantic-query-hint`, `semantic-reference`, `semantic-role`, `semantic-tag`

- `shell`: `embeddings`

- `store`: `semantic-indexing`


### `domain:runtime-transactions` (2)

- `core`: `primitive-operation`, `transaction`


### `domain:security-capabilities` (1)

- `shared`: `threat-model`


### `domain:store-graph` (12)

- `core`: `ast-persistence`

- `shell`: `repository-registry`

- `store`: `backup-export`, `document-head`, `garbage-collection`, `graph-store`, `immutable-append-only-database`, `local-vs-global-store-precedence`, `retention-policy`, `store-infrastructure`, `store-recovery`, `what-a-store-is`


### `domain:store-hashing` (4)

- `core`: `cache`, `node-hash`

- `shared`: `hash-field`

- `store`: `merkle-index`


### `domain:store-history` (4)

- `core`: `temporal-layer`

- `store`: `append-only-event-log`, `snapshots`, `transaction-log`


### `domain:store-indexes` (5)

- `core`: `search-projection`

- `store`: `dependency-index`, `derived-index`, `field-index`, `section-index`


### `domain:store-integrity` (3)

- `shared`: `tracked-document-identity`

- `shell`: `document-tracker`

- `store`: `store-integrity-checks`


### `domain:store-persistence` (2)

- `store`: `content-addressed-store`, `storage-backend`


### `domain:surfaces-cli-command-groups` (10)

- `shell`: `ast-command-group`, `cli-workflow-surface`, `docs-command-group`, `fields-command-group`, `find-command-group`, `legacy-cli-aliases`, `models-command-group`, `plural-first-cli-surface`, `sections-command-group`, `stores-command-group`


### `domain:surfaces-cli-inputs-outputs` (4)

- `shared`: `model-reference-format`

- `shell`: `cli-invocation-contract`, `how-to-get-data-out-of-sldb`, `payload-input-forms`


### `domain:surfaces-cli-onboarding` (2)

- `shell`: `faq-command-group`, `help-command-group`


### `domain:surfaces-cli-workflows` (11)

- `shared`: `semantic-search`

- `shell`: `compose-rendered-document-view`, `create-document-workflow`, `direct-mode`, `draft-first-model-edits`, `field-and-section-navigation`, `physical-search`, `recover-link-resolution`, `store-backed-mode`, `track-existing-document-workflow`, `update-tracked-document-workflow`


### `domain:surfaces-visual-inspectors` (6)

- `shell`: `highlighting-engine`, `link-editor`, `model-browser`, `template-browser`, `visual-graph-explorer`, `visual-ux-surface`


## Cross-cutting ontology bands

### 1. Canonical model band
- `canonical-ast`
- `canonical-identity`
- `node`
- `document`
- `revision`
- `ownership-edge` / `reference-edge` / `semantic-edge` / `derived-edge`

### 2. Import and reconciliation band
- `document-source`
- `parser`
- `canonicalizer`
- `source-manager`
- `identity-stability-rules`
- `node-reconciliation`

### 3. Store and history band
- `graph-store`
- `transaction-log`
- `content-addressed-store`
- `document-head`
- `store-infrastructure`
- `backup-export`
- `store-recovery`
- `garbage-collection`
- `retention-policy`

### 4. Runtime control band
- `transaction`
- `primitive-operation`
- `query-engine`
- `projection`
- `hook-runtime`
- `effect-outbox`
- `capability-model`
- `threat-model`

### 5. Behavior proof band
- `conformance-suite`
- `reference-behavior`
- `golden-fixture`
- `testing`
- `store-integrity-checks`

### 6. Boundary and host band
- `kernel-api`
- `transaction-plan`
- `query-plan`
- `projection-plan`
- `effect-plan`
- `lisp-metalanguage`
- `ports-and-adapters`
- `python-cli-orchestration-layer`
- `rust-core`

## Normalization rules for future atoms

- Keep one dominant `domain:*` leaf per atom.
- Prefer short single-purpose atoms over compound omnibus atoms.
- Use links for composition instead of large mixed-scope prose.
- Put lifecycle placement in `layer`, not in ad hoc title wording.
- Put question shape in `five_wh_one_plus`, not in tags.
- Add new ontology leaves deliberately through `tag-namespaces.yaml` when a real gap exists.

## Downstream constraints

- New atoms should attach to this ontology through an existing domain leaf or an explicitly added one.
- New operational concepts should connect to the current hub atoms instead of creating duplicate centers of authority.
- Spec2viz surfaces should continue to reflect the same ontology partitions: model, pipeline, store, runtime, boundaries, and quality/reliability bands.
