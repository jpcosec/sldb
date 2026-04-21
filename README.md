# SLDB (Structured Language Database)

A structurally aware Markdown extraction and template mapping library based on `mdast` principles. SLDB allows you to treat Markdown files as a structured persistence layer, mapping them directly to Pydantic models.

## Features

- **Structural Synchronicity:** Bi-directional mapping between Markdown and Pydantic.
- **AST-Powered:** Uses `markdown-it-py` for robust structural analysis instead of fragile regex.
- **Stateful Sequential Extraction:** Robustly handles multiple identical blocks via cursor mapping.
- **Rich GFM Support:** Native handlers for Lists, Tables, YAML Metadata, and standard text blocks.
- **Marker-Based Templates:** Define extraction logic directly in Pydantic models using `__template__`.

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

## License

MIT
