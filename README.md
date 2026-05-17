# SLDB (Structured Language Database)

A structurally aware Markdown extraction and template mapping library based on `mdast` principles. SLDB allows you to treat Markdown files as a structured persistence layer, mapping them directly to Pydantic models.

Within the `wikipu-ecosystem`, SLDB is the human-readable rendering and navigation layer over canonical `specYaml` semantics. It may author, extract, and render structured markdown, but it should not compete with `specyaml/` as the semantic source-of-truth contract.

This repo's own operating system lives in `desk/` as the **opsys** workflow-domain layer — see `docs/workspaces.md` for the three-layer architecture (sldb infra / specyaml semantics / opsys workflow domain).

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

Start with curated help:

```bash
sldb help
sldb help find
sldb help fields
sldb help ast
```

The public workflow is now organized around `stores`, `models`, `docs`, `fields`, `sections`, `find`, and `ast`.
The older raw address/query surface still exists under `sldb legacy ...`, but it is no longer the primary interface.

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
```

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

See `docs/workspaces.md` for the workspace pattern behind `docs/`, `desk/`, and `desk/drawer/`.

## Structured Composition

`StructuredNLDoc` models can declare render-time compositions through `__compositions__` and expose them with `render` markers in the template.

This supports explicit expansion of referenced child documents during rendering while leaving other references untouched. In this repo, `desk/models/board.py` composes task summaries from referenced task docs, while `desk/models/ritual.py` can compose structured step details from `StepDoc` references.

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
