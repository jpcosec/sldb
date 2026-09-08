> **Frozen (2026-09-07).** `sldb` v1 is superseded by [`knowledge`](https://github.com/jpcosec/knowledge) (SLDB v2 kernel + models + anchored evaluator, one product). This repo receives no features; tag `v1-frozen` marks this state and `v2-seed-2026-09` the branch `refactor-target` that seeded `knowledge`. Existing installs (`iso-lab/worktrees/sldb`) keep working until milestone S6 migrates deskops.

# SLDB (Structured Language Database)

A structurally aware Markdown extraction and template mapping library based on `mdast` principles. SLDB allows you to treat Markdown files as a structured persistence layer, mapping them directly to Pydantic models.

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
pip install sldb
```

## CLI

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

The public workflow is now organized around `stores`, `models`, `docs`, `fields`, `sections`, `find`, and `ast`.
The raw address surface (`st.{Model}.doc.field`, `se.tag`, `gse.tag`) lives under `sldb legacy ls|get|glob|find`; it is the same engine spelled as addresses.

### Read and write by address, never by opening Markdown

The store is a database of addressable fields over Markdown. Every field of every tracked document has an address, and every read, filter or update goes through that address. SLDB re-renders the file; you do not edit it by hand.

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

`{Model+}` is the family form: the model and every subclass, whether or not the base is registered. `--where` takes one predicate: `has(f)`, `"x" in f`, `f ~ "regex"`, `f = "v"`, `f != "v"`, `f >= n`, `model <= Base`. The full address model, the predicate grammar and the mapping between `legacy` addresses and the `fields`/`find` surface are in [`docs/addressability_model.md`](docs/addressability_model.md).

To inspect what one store already knows, use `sldb models list --store .sldb`.

If you are new to the CLI concepts, read `docs/faq.md` after `sldb help`. The FAQ answers the first-use questions around stores, model refs, tracked doc names, semantic versus physical search, and link composition.

You can also browse those answers directly from the CLI with `sldb faq`, and log unclear points or improvement suggestions into the active project's `desk/inbox/` with `sldb inbox`.

To revisit those notes later, use `sldb inbox --list` and `sldb inbox --show <id>`.
If the project store already has `InboxNoteDoc` registered, new inbox notes auto-track into the store too.

> **Deprecation notice (v0.5):** The singular command aliases (`store`, `model`, `doc`, `ls`, `get`, `glob`, `raw-find`, `recover`, `compose`) are deprecated and will be removed in **v0.6**. Use the plural surfaces (`stores`, `models`, `docs`) or `sldb legacy ...` instead. Set `SLDB_SUPPRESS_DEPRECATION=1` or pass `-W ignore` to silence deprecation warnings in automation.

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
```

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
store_index.yaml          ← master router; owns hash_a
  └─ .sldb/models/<Name>.yaml   ← per-model inventory; owns hash_b
       └─ .sldb/documents/<Name>.yaml  ← per-document hashes
            ├─ hash_c  ← sha256 of raw .md text
            └─ hash_d  ← sha256 of extracted Pydantic field values
```

The four hashes form a Merkle chain. `sldb stores check` walks the chain and reports fractures without modifying anything:

| Observation | Meaning |
|-------------|---------|
| hash_c changed, hash_d stable | Benign text mutation (e.g. a rendered date). No action needed. |
| hash_d changed | Field values were edited manually. |
| Path missing | Document was moved or deleted. |
| hash_b changed | Document inventory altered (added/removed). |
| hash_a invalidated | Model contract changed (fields or template). |

### Caches

The hash chain is a Merkle tree, and the caches use it as one: `hash_a` says whether
anything changed, each model's `hash_b` whether that model did, each document's `hash_c`
whether that document did. A read descends only where a hash moved. One concession to
Markdown edited by hand: the leaves are also stat-ed (mtime and size, microseconds per
file, no reads), so an edit made behind sldb's back is seen before `stores update` moves
its hash. A store that is only written through sldb can set `SLDB_TRUST_CHAIN=1` and
skip that sweep.

| Cache | Where | Key |
|-------|-------|-----|
| Index cache | memory (`sldb.store.io`) | each yaml index by its file's mtime and size; loads return copies; saves that change nothing do not touch the file |
| Runtime documents | memory (`sldb.store.runtime_cache`) | the store by `hash_a` + every `hash_b` (+ the leaf stats); each extracted document by `(path, hash_c[, mtime, size], model)` |
| Extracted payloads | `.sldb/runtime/cache/extracted.json` | the payloads by the same leaf key, so a new process does not extract what it has already seen |
| Built per model | `.sldb/runtime/cache/built.json` | the semantic contribution and the sections of each model by `hash_b`; a rebuild walks only models whose documents moved |

`sldb stores update` rehashes every document's text (that is its job: to see edits made
behind sldb's back and move the chain) but recomputes field hashes only where the text
changed. A store layout that is already canonical is not rewritten when a command opens
it. The rebuilds keyed by `hash_b` do not see a hand edit until `stores update` moves
its `hash_c`; readers do, through the leaf sweep. The two cache files are derived; delete
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
```

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
| `sldb stores add <path>` | Link a federated store |
| `sldb stores check [--format text\|json\|yaml]` | Run integrity diagnostics |
| `sldb stores update [--wait] [--verbose]` | Recompute all hashes from current file states |
| `sldb models add <model-ref>` | Register a model contract |
| `sldb models update <name>` | Re-index a model after contract changes |
| `sldb docs create --model <name> -o <path> <payload>` | Create and track a new document |
| `sldb docs track <path> --model <name>` | Validate and track an existing document |
| `sldb docs update <name> <payload>` | Re-render a tracked document with new data |

Note: `stores update` now prints a rebuild summary (docs processed, missing, empty sections, unparseable headings). Pass `--wait` to block if the store is locked by another process, and `--verbose` to see individual skip details.

## License

MIT
