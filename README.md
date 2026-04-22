# SLDB (Structured Language Database)

A structurally aware Markdown extraction and template mapping library based on `mdast` principles. SLDB allows you to treat Markdown files as a structured persistence layer, mapping them directly to Pydantic models.

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

The package now ships with a small `sldb` command.

The CLI is model-first: it operates on a `StructuredNLDoc` reference in the form `package.module:ModelName`. If the model lives in your current project rather than the installed `sldb` package, pass `--pythonpath /path/to/project`.

Every `StructuredNLDoc` field must define a non-empty Pydantic `description`. Treat those descriptions as part of the model contract: they act as cues for humans reading the schema and for LLMs generating or editing documents around it.

Extract data from a Markdown document using a model:

```bash
sldb extract myapp.docs:RecipeDoc document.md output.json
```

Render Markdown from YAML/JSON data using a model:

```bash
sldb render myapp.docs:RecipeDoc data.yaml rendered.md
```

The CLI uses positional file arguments so it can be scripted more easily:

- `extract <model-ref> <input-markdown> <output-json-or-yaml>`
- `render <model-ref> <input-data> <output-markdown>`

Use `-` as the output path to write to stdout.

The generated example bundle and CLI help both show the preferred field pattern:

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

The four hashes form a Merkle chain. `sldb store check` walks the chain and reports fractures without modifying anything:

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
sldb store init

# 2. Register a model contract
sldb model add myapp.models:Book

# 3a. Create a new document from data and track it
sldb doc add --model Book -o docs/my-book.md '{"title": "My Book"}'
# or from a YAML/JSON file
sldb doc add --model Book -o docs/my-book.md data.yaml

# 3b. Or track an existing document (validates idempotency first)
sldb doc track docs/existing.md --model Book

# 4. Check integrity
sldb store check

# 5. Update a tracked document with new data
sldb doc update my-book --model Book '{"title": "Updated Title"}'

# 6. After editing a model's Pydantic contract, re-index it
sldb model update Book

# 7. Full store reindex (after bulk changes)
sldb store update
```

### Federation

Stores can reference each other. The local store always wins on name collisions.

```bash
# Link a shared ontology store
sldb store add ~/.sldb/shared-ontology --name shared
```

### Relationship semantics

Model relationships (`inherits`, `has_many`) are **not** stored in the index — they are derived at query time from the Python class hierarchy and field types. The YAML index stores only physical pointers; the Pydantic class is the single source of truth for schema and semantics.

### CLI reference

| Command | Description |
|---------|-------------|
| `sldb store init [--path .]` | Initialize a `.sldb/` store |
| `sldb store add <path>` | Link a federated store |
| `sldb store check [--format text\|json\|yaml]` | Run integrity diagnostics |
| `sldb store update` | Recompute all hashes from current file states |
| `sldb model add <model-ref>` | Register a model contract |
| `sldb model update <name>` | Re-index a model after contract changes |
| `sldb doc add --model <name> -o <path> <payload>` | Create and track a new document |
| `sldb doc track <path> --model <name>` | Validate and track an existing document |
| `sldb doc update <name> --model <name> <payload>` | Re-render a tracked document with new data |

## License

MIT
