> **Active.** A 2026-09-07 note declared this repository frozen and superseded by
> `knowledge`. That is not what happened: there were 223 commits afterwards,
> including 897 file changes under `src/` and whole new subsystems (`serve`,
> `graph`, merkle hashing, document merge). The successor froze the same day and
> its evaluator moved elsewhere, so the handover never took place.
>
> What this repository is, and the boundary between the product and the
> self-application that exercises it, is declared in
> [`contracts/identity.toml`](contracts/identity.toml) and verified by
> `tools/check_identity.py`. The tag `v1-frozen` still marks the September state.

# SLDB (Structured Language Database)

Documentation checked against the working tree on 2026-09-13: see [current CLI](docs/architecture/current-cli-tree.md), [AST queries](docs/ast_query_primitives.md), and [remaining gaps](docs/documentation-review.md). This checkout declares package version `0.1.0`; historical changelog headings do not establish the version installed locally or published to a registry.

A system for representing anything with deterministically derivable structure —
documents, source code, program interfaces — as addressable, queryable documents
anchored to their origin and reversible to their surface.

Markdown is the *authored* surface: what a human writes. Code syntax trees are the
*derived* surface: what a machine extracts. The core does not distinguish between
them, and that indistinction is the product: of the 1,551 documents in this
repository's own store, 1,368 come from syntax trees rather than Markdown.

The capability map — 24 axes, five viable units, and which of them can be
extracted today — is in [`contracts/layers.toml`](contracts/layers.toml); run
`python tools/check_axes.py --units` to read it.

Within the `hum-ecosystem`, SLDB is the human-readable rendering and navigation layer over canonical `specYaml` semantics. It may author, extract, and render structured markdown, but it should not compete with `specyaml/` as the semantic source-of-truth contract.

The workflow-domain example layer now lives in the sibling `opsys` repo, not inside `sldb` itself. See `docs/workspaces.md` for the boundary between reusable SLDB infrastructure and downstream workflow-domain consumers.

## Features

- **Structural Synchronicity:** Bi-directional mapping between Markdown and Pydantic.
- **AST-Powered:** Uses `markdown-it-py` for robust structural analysis instead of fragile regex.
- **Stateful Sequential Extraction:** Robustly handles multiple identical blocks via cursor mapping.
- **Rich GFM Support:** Native handlers for Lists, Tables, YAML Metadata, and standard text blocks.
- **Marker-Based Templates:** Define extraction logic directly in Pydantic models using `__template__`.
- **Store System:** A `.sldb/` pointer database that tracks model contracts and document instances via a Merkle-style hash cascade, with integrity diagnostics and federation support.

## Installation

```bash
pip install structuredLanguageDB          # uv add structuredLanguageDB
pip install 'structuredLanguageDB[graph]'  # PageRank (scipy)
```

The PyPI name is `structuredLanguageDB`; the import and the CLI are still `sldb` (`import sldb`, `sldb --help`).

## CLI

This repository can generate and check its own tracked CLI reference:

```bash
sldb selfdoc scan
sldb selfdoc sync
sldb selfdoc check
```

See [self-documentation](docs/self-documentation.md) for store anchoring, generated/authored field ownership, and use with other argparse applications.

The package ships with a graph-first `sldb` CLI.

Run commands as `sldb ...` or `python -m sldb ...`, not `bash sldb ...`.

Start with curated help:

```bash
sldb help
sldb help find
sldb help fields
sldb help ast
sldb help docs
sldb faq
sldb faq store
sldb explore store
```

`faq` reads `docs/faq.md` relative to the current directory; it does not resolve a store. Outside this checkout, pass `--faq-path /absolute/path/to/sldb/docs/faq.md`. Likewise, `explore` uses `--docs-root` and `--code-root`, not the store root. See the [anchoring gap](docs/documentation-review.md#faq-and-explore-do-not-use-the-store).

The public workflow is now organized around `stores`, `models`, `docs`, `fields`, `sections`, `find`, and `ast`.
The raw address surface (`st.{Model}.doc.field`, `se.tag`, `gse.tag`) lives under `sldb legacy ls|get|glob|find`; it is the same engine spelled as addresses.

### Read and write by address, never by opening Markdown

The store is a database of addressable fields over Markdown. Every field of every tracked document has an address, and every read, filter or update goes through that address. SLDB re-renders the file; you do not edit it by hand.

A linked store is reached by prefix: `b:st.{Model+}.doc.field` for the store linked as `b` (`sldb stores add`), with results carrying the prefix back; see `docs/addressability_model.md`.

```bash
# one value, or a subfield: a key of a dict field, an item of a list field, a table row
sldb fields show docs/recipe/title --store .sldb --pythonpath src
sldb fields show docs/recipe/steps/0/title --store .sldb --pythonpath src
sldb legacy get 'st.{RecipeDoc}.recipe.metadata.author' --format text --store .sldb --pythonpath src

# one field across every document (and linked stores)
sldb fields query status --global --store .sldb --pythonpath src

# every document of a family where a field has a value — one command
sldb legacy find 'st.{RecipeDoc+}' --where 'status = "draft"' --store .sldb --pythonpath src
sldb find "" --in physical --type doc --where 'model <= RecipeDoc' --store .sldb --pythonpath src

# change the value; SLDB rewrites the Markdown, validates the roundtrip, updates hashes and indexes
sldb fields update docs/recipe/status '"published"' --store .sldb --pythonpath src
sldb fields append docs/recipe/tags '"dessert"' --store .sldb --pythonpath src
```

`{Model+}` is the family form: the model and every subclass, whether or not the base is registered. `--where` takes predicates joined by ` and `: `has(f)`, `nonempty(f)` (also rejects `[]` and `{}`), `"x" in f`, `f ~ "regex"`, `f = "v"`, `f != "v"`, `f >= n`, `model <= Base`; a literal may carry the backslash escapes `\"` (a quote) and `\\` (a backslash); `"v"` may be the empty string (`f = ""` is a field present and empty; `f != ""` is present and not empty; an absent field matches neither — `has(f)` asks presence). A predicate no evaluator parses is an error, not an empty result. The full address model, the predicate grammar and the mapping between `legacy` addresses and the `fields`/`find` surface are in [`docs/addressability_model.md`](docs/addressability_model.md).

To inspect what one store already knows, use `sldb models list --store .sldb`.

If you are new to the CLI concepts, read `docs/faq.md` after `sldb help`. The FAQ answers the first-use questions around stores, model refs, tracked doc names, semantic versus physical search, and link composition.

You can also browse those answers directly from the CLI with `sldb faq`, and log unclear points or improvement suggestions into the active project's `desk/inbox/` with `sldb inbox`.

To revisit those notes later, use `sldb inbox --list` and `sldb inbox --show <id>`.
If the project store already has `InboxNoteDoc` registered, new inbox notes auto-track into the store too.

> **Compatibility:** Singular aliases (`store`, `model`, `doc`, `ls`, `get`, `glob`, `raw-find`, `recover`, `compose`) are deprecated. Use plural surfaces (`stores`, `models`, `docs`) or `sldb legacy ...`. The former v0.6 removal target was a historical plan, not a confirmed release commitment for this frozen checkout. Set `SLDB_SUPPRESS_DEPRECATION=1` to suppress deprecation warnings.

The CLI is still model-first: it operates on a `StructuredNLDoc` reference in the form `package.module:ModelName`. If the model lives in your current project rather than the installed `sldb` package, pass `--pythonpath /path/to/project`.

Every `StructuredNLDoc` field must define a non-empty Pydantic `description`. Treat those descriptions as part of the model contract: they act as cues for humans reading the schema and for LLMs generating or editing documents around it.

Core authoring and runtime commands remain available:

```bash
sldb extract myapp.docs:RecipeDoc document.md output.json
sldb render myapp.docs:RecipeDoc data.yaml rendered.md
sldb validate myapp.docs:RecipeDoc --input document.md
```

Store, model, and doc lifecycle:

```bash
sldb stores init --path .
sldb models list --store .sldb
sldb models add myapp.docs:RecipeDoc --store .sldb --pythonpath src
sldb models template edit RecipeDoc --input next.template.md --store .sldb --pythonpath src
sldb models fields add RecipeDoc summary --type str --description "Short summary" --default '"Draft"' --store .sldb --pythonpath src
sldb models fields remove RecipeDoc summary --store .sldb --pythonpath src
sldb models validate RecipeDoc --store .sldb --pythonpath src
sldb models validate RecipeDoc --promote --store .sldb --pythonpath src
sldb docs create --model RecipeDoc -o docs/recipe.md data.yaml --store .sldb --pythonpath src
sldb docs track docs/existing.md --model RecipeDoc --store .sldb --pythonpath src
sldb docs untrack recipe --store .sldb --pythonpath src
sldb docs delete recipe --yes --store .sldb --pythonpath src
```

`docs untrack` drops the document from the store and **keeps** its Markdown file, so a
later `docs track` picks it up again. `docs delete` removes both the store entry and
the file, and purges the entry the extraction cache keeps for it; it asks first unless
given `--yes`.

Model template edits are draft-first: `models template edit` writes a `*.py.temp` draft beside the registered model source. The active model contract stays unchanged until `models validate --promote` succeeds, at which point the draft replaces the active template and the store reindexes the model.

Field edits use the same draft workflow. Successful promotion bumps the registered model version, and `sldb models show <Model>` exposes that version through the store AST.

Exploration and graph inspection:

```bash
sldb find docs --in physical --store .sldb --pythonpath src
sldb find type.documentation.Readme --in semantic --global --store .sldb --pythonpath src
sldb ast show docs/recipe --store .sldb --pythonpath src
sldb stores semantic-export --store .sldb --pythonpath src --format kgdb --encoding json --rebuild -o kgdb.semantic.json
```

`sldb stores semantic-export` is the SLDB-owned semantic handoff for KGDB. It exports graph-ready model, document, section, semantic tag, semantic DAG, equivalence, and store provenance data; source-file relations and workflow-specific graph edges are added downstream. See `docs/architecture/semantic-export-boundary.md` for the full boundary.

Section context and navigation:

```bash
sldb sections show docs/recipe --store .sldb --pythonpath src
sldb sections find tasks --in semantic --store .sldb --pythonpath src
sldb sections find "" --where '"Roadmap" in breadcrumbs' --store .sldb --pythonpath src
sldb sections fields docs/recipe/overview --store .sldb --pythonpath src
```

Field queries now expose the owning section:

```bash
sldb fields query title --store .sldb --pythonpath src
# Results include "owning_section": "overview"
```

Field-level CRUD and collection operations:

```bash
sldb fields show docs/recipe/title --store .sldb --pythonpath src
sldb fields update docs/recipe/title '"Updated title"' --store .sldb --pythonpath src
sldb fields append docs/recipe/tags '"dessert"' --store .sldb --pythonpath src
sldb fields clean docs/recipe/tags --dedupe --store .sldb --pythonpath src
```

Link recovery and composition work with either a tracked doc name or a file path:

```bash
sldb docs recover recipe --store .sldb --format yaml
sldb docs compose recipe --store .sldb --format yaml -o -
```

Generate a model from a template plus field spec:

```bash
sldb models create RecipeDoc --template recipe.template.md --fields recipe.fields.yaml --output myapp/models.py
```

Use `-` as an output path to write to stdout when a command supports it.

## Serving and surfaces

`sldb serve` exposes the store over HTTP so that UIs never touch Markdown directly: they read
documents, fields, segments and edges, and write by payload (`/save` with `expected`, `POST /docs`
to create). SLDB re-renders the Markdown and verifies the round-trip.

```bash
sldb serve --store .sldb --pythonpath . --port 8787 --cors
```

Routes, grouped by what a surface needs:

- read: `GET /document`, `/document/ir`, `/document/segments?id=` (literals and fields with
  character offsets, provenance per composed piece), `/graph`, `/edges[?id=Model:name]`,
  `/schema` (degrades per model, with field descriptions), `/models`, `/fields`, `/sections`,
  `/ast`, `/find`, `/render`, `/stores`, `/stores/check`
- write: `POST /save`, `POST /docs` (409 if it exists, 422 if it does not validate)
- extraction: `POST /extract`, `POST /extract/segments` (raw text + model → typed fields,
  alignment to the raw text, unmatched spans, coverage)
- similarity: `GET /corpus/rank` (documents, or `fields=1`), `GET /similar`
- diagnostics: `GET /health`, `/lint`, `/kgdb/snapshot`

The surfaces in this repo live in `surface/` (`@sldb/surface`): a generic document UI (Documento,
Composición, Extracción, Salud, Bandeja, Lector, Destilación) and `maqueta.html`, the atoms UI
(Extracción · Grafo · Compositor · Respuesta) built on `AtomDoc`, `RelationDoc`, `GrupoDoc` and
report models. Design and status: `docs/surface/PROPUESTA-SUPERFICIE.md`,
`docs/surface/OPERACIONALIZACION-VISTAS.md`, tasks in `docs/surface/tasks/`. Sibling UIs
(the `graph_ui` and `sldb-ui` repos, launched together by the `kbsurfaces` repo) are views over the
same server.

## Tracking This Repo's Docs

The project documentation workspace under `docs/` is now modelled in `docs/models.py`.

- `ArchitectureNarrativeDoc` covers `docs/architecture/*.md`
- `PackagingDoc` covers `docs/packaging instructions.md`
- `RequestDoc` covers `docs/requests/*.md`

See `docs/README.md` for the current tracking workflow, semantic query examples, and the authoring rule for generic `title + body` docs.

See `docs/workspaces.md` for the workspace pattern behind durable docs in this repo and downstream workflow-domain consumers such as the sibling `opsys` repo.

## Structured Composition

`StructuredNLDoc` models can declare render-time compositions through `__compositions__` and expose them with `render` markers in the template.

This supports explicit expansion of referenced child documents during rendering while leaving other references untouched. Downstream repos can use this to compose workflow documents, checklists, and other structured views from tracked child docs.

The generated example bundle and model generator both follow the preferred field pattern:

```python
from pydantic import Field

class RecipeDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Recipe title shown in the H1 heading.")
```

Validate model idempotency against a sample Markdown document:

```bash
sldb validate myapp.docs:RecipeDoc --input document.md
```

Or validate from a sample payload instead:

```bash
sldb validate myapp.docs:RecipeDoc --data data.yaml --format json
```

Load a model from another project directory:

```bash
sldb validate myapp.docs:RecipeDoc --input document.md --pythonpath /path/to/project
```

Bootstrap a repo-local skill file for models/tools:

```bash
sldb init .
```

This writes `.skills/sldb/SKILL.md` from a bundled template with a short explanation of what SLDB is, when to use it, and the available commands.

Generate a working example project bundle:

```bash
sldb example .
```

This creates `./sldb_example` with a sample model, sample Markdown input, and sample YAML data so you can try `extract`, `render`, and `validate` against a known-good reference.

## Basic Usage

```python
from pydantic import Field

from sldb import StructuredNLDoc, DataExtractor, AST_Handler, TemplateExtractor

class MyModel(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\n\n⸢rev•content⸥"
    title: str = Field(description="Primary document heading.")
    content: str = Field(description="Main document body content.")

# Parsing
ast = AST_Handler()
tpl = TemplateExtractor()
data = DataExtractor()

recipes = tpl.extract_nodes(ast.split_nodes(MyModel.__template__))
payload = data.extract_values(ast.split_nodes("# Hello\n\nWorld"), recipes)

model = MyModel(**payload)
print(model.title) # "Hello"
```

Every `StructuredNLDoc` field must define a non-empty Pydantic `description` so the model carries usage cues for humans and LLMs.

## Testing

```bash
pytest
```

The standalone test suite includes an idempotency roundtrip check, and the CLI now exposes `validate` for template validation workflows.

## Python Marker Safety

`py` markers are disabled by default. In safe mode, SLDB leaves `⸢py•...⸥` markers untouched instead of evaluating them.

Enable evaluation explicitly when you trust the template source:

```python
from sldb import configure

configure(python_execution_mode="unsafe")
```

You can also gate unsafe mode with a custom filter for future policy checks:

```python
from sldb import configure

configure(
    python_execution_mode="unsafe",
    python_expression_filter=lambda expression, data: expression.startswith("title."),
)
```

Set `SLDB_PYTHON_EXECUTION_MODE=unsafe` to change the default process-wide mode.

## Store System

The store is a `.sldb/` pointer database that decouples physical file locations from logical model identity. It tracks model contracts and their document instances without moving or owning any files. A global store at `~/.sldb/` can be shared across projects; a local `.sldb/` in the project root takes precedence.

### How it works

The store maintains a three-level YAML index cascade:

```
.sldb/core/store_index.yaml                  ← master router; owns store_hash
  └─ .sldb/core/models/<Name>.yaml           ← per-model node; owns model_hash
       ├─ roster_hash   ← sha256 of the document list      (the node's first child)
       ├─ contract_hash ← sha256 of field schema + template (the node's second child)
       └─ .sldb/core/documents/<Name>/*.yaml ← per-document shards
            ├─ source_hash  ← sha256 of raw .md text      (deprecated alias: hash_c)
            └─ content_hash ← sha256 of extracted fields  (deprecated alias: hash_d)
```

`model_hash` is derived: `sha256(roster_hash, contract_hash)`. Both children are persisted
next to it so a node that disagrees can be attributed to one of them — a bare "the hash moved"
cannot tell a document that was edited from a model whose contract changed under it.

Earlier stores persisted the same four values as `hash_a`..`hash_d`; the models still read
them as deprecated aliases and write only the semantic names, so versioned KBs keep
loading. Run `sldb stores migrate-hashes` to rewrite a store's `.sldb/core/` once.

The four hashes form a Merkle chain. `sldb stores check` walks the chain and reports fractures without modifying anything:

| Observation | Meaning |
|-------------|---------|
| source_hash changed, content_hash stable | Benign text mutation (e.g. a rendered date). No action needed. |
| content_hash changed | Field values were edited manually. |
| Path missing | Document was moved or deleted. |
| roster_hash changed | Document inventory altered (added/removed). |
| contract_hash changed | The model's fields or `__template__` changed. `stores update` re-extracts that model's documents even though no `.md` moved. |
| store_hash changed | A model node moved, or the set of models changed. |

A contract change is reported as its own category (`contract_mutation`) rather than as a
damaged document: the text on disk is exactly what it was, and the reader should be sent to
the model, not to the file.

### Caches

The hash chain is a Merkle tree, and the caches use it as one: `store_hash` says whether
anything changed, each model's `model_hash` whether that model did, each document's
`source_hash` whether that document did. A read descends only where a hash moved. One
concession to Markdown edited by hand: the leaves are also stat-ed (mtime and size,
microseconds per file, no reads), so an edit made behind sldb's back is seen before
`stores update` moves its hash. A store that is only written through sldb can set
`SLDB_TRUST_CHAIN=1` and skip that sweep.

| Cache | Where | Key |
|-------|-------|-----|
| Index cache | memory (`sldb.store.io`) | each yaml index by its file's mtime and size; loads return copies; saves that change nothing do not touch the file |
| Runtime documents | memory (`sldb.store.runtime_cache`) | the store by `store_hash` + every `model_hash` (+ the leaf stats); each extracted document by `(path, source_hash[, mtime, size], model)` |
| Extracted payloads | `.sldb/runtime/cache/extracted.json` | the payloads by the same leaf key, so a new process does not extract what it has already seen |
| Built per model | `.sldb/runtime/cache/built.json` | the semantic contribution and the sections of each model by `model_hash`; a rebuild walks only models whose documents moved |

`sldb stores update` rehashes every document's text (that is its job: to see edits made
behind sldb's back and move the chain) but recomputes field hashes only where the text
changed. A store layout that is already canonical is not rewritten when a command opens
it. The rebuilds keyed by `model_hash` do not see a hand edit until `stores update` moves
its `source_hash`; readers do, through the leaf sweep. The two cache files are derived; delete
them freely and add `.sldb/runtime/cache/` to `.gitignore`.

### Typical workflow

```bash
# 1. Initialize the store in your project root
sldb stores init

# 2. Register a model contract
sldb models add myapp.models:Book

# 3a. Create a new document from data and track it
sldb docs create --model Book -o docs/my-book.md '{"title": "My Book"}'
# or from a YAML/JSON file
sldb docs create --model Book -o docs/my-book.md data.yaml

# 3b. Or track an existing document (validates idempotency first)
sldb docs track docs/existing.md --model Book

# 4. Check integrity
sldb stores check

# 5. Update a tracked document with new data
sldb docs update my-book '{"title": "Updated Title"}'

# 6. After editing a model's Pydantic contract, re-index it
sldb models update Book

# 7. Full store reindex (after bulk changes)
sldb stores update
```

### Federation

Stores can reference each other. The local store always wins on name collisions.

```bash
# Link a shared ontology store
sldb stores add ~/.sldb/shared-ontology --name shared
sldb stores list            # each link with its state: ok, or [missing|not-a-store: <path>]
```

The link is recorded relative to the project root, so two repos checked out side by side keep
it on another machine. The alias must be letters, digits, `.`, `_` or `-`; `local` is reserved.

Referencing a document of a linked store does not track it here: `docs list` and the root hash
stay local. `alias:ref` reads the store linked **directly** as `alias` (links of links are not
followed); a bare ref never leaves the local store.

```bash
sldb docs show shared:my-book                 # also shared:Book/my-book or shared:<tracked path>
sldb docs exists shared:my-book --format json # from the indexes only, no model import
```

`docs exists` answers with its exit code: `0` ok, `1` missing, `2` ambiguous, `5` the alias is
not linked (`link-missing`) or its target is gone (`link-broken`). From Python:
`sldb.api.doc_status(store, "shared:my-book").status`.

Linked store aliases can be used as generic document destinations from the current project. Relative output paths are resolved against the destination store's project root:

```bash
sldb docs create --store shared --model Book -o docs/book.md data.yaml
```

Models can also be resolved from a linked store namespace and registered into the destination store as a document index when first used:

```bash
sldb docs create \
  --store target-project \
  --model deskops:InboxRequestDoc \
  -o desk/inbox/request-123.md \
  request.yaml
```

SLDB treats this as a generic stores/models/docs operation. Workflow tools such as `deskops` should own higher-level semantics like inbox routing, sender/recipient fields, request lifecycle, and assignment, and call SLDB only to resolve stores, render, validate, write, and track structured Markdown documents.

### Relationship semantics

Model relationships (`inherits`, `has_many`) are **not** stored in the index — they are derived at query time from the Python class hierarchy and field types. The YAML index stores only physical pointers; the Pydantic class is the single source of truth for schema and semantics.

### CLI reference

| Command | Description |
|---------|-------------|
| `sldb stores init [--path .]` | Initialize a `.sldb/` store |
| `sldb stores add <path> [--name alias]` | Link a federated store |
| `sldb stores list` | List links with their state |
| `sldb stores check [--format text\|json\|yaml]` | Run integrity diagnostics |
| `sldb stores update [--wait] [--verbose]` | Recompute all hashes from current file states |
| `sldb models add <model-ref>` | Register a model contract |
| `sldb models update <name>` | Re-index a model after contract changes |
| `sldb models remove <name> [--with-documents]` | Unregister a model, its documents too with the flag (its class need not import) |
| `sldb docs create --model <name> -o <path> <payload>` | Create and track a new document |
| `sldb docs track <path> --model <name>` | Validate and track an existing document |
| `sldb docs update <name> <payload>` | Re-render a tracked document with new data |
| `sldb docs exists <[alias:]ref>` | Check that a reference resolves (exit 0/1/2/5) |

Note: `stores update` now prints a rebuild summary (docs processed, missing, empty sections, unparseable headings). Pass `--wait` to block if the store is locked by another process, and `--verbose` to see individual skip details.

## License

MIT
