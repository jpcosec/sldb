# nlDB (Natural Language Database Engine)

A structurally aware Markdown extraction and template mapping library based on `mdast` principles. nlDB allows you to treat Markdown files as a structured persistence layer, mapping them directly to Pydantic models.

## Features

- **Structural Synchronicity:** Bi-directional mapping between Markdown and Pydantic.
- **AST-Powered:** Uses `markdown-it-py` for robust structural analysis instead of fragile regex.
- **Stateful Sequential Extraction:** Robustly handles multiple identical blocks via cursor mapping.
- **Rich GFM Support:** Native handlers for Lists, Tables, YAML Metadata, and standard text blocks.
- **Marker-Based Templates:** Define extraction logic directly in Pydantic models using `__template__`.

## Installation

```bash
pip install nldb
```

## CLI

The package now ships with a small `nldb` command.

The CLI is model-first: it operates on a `StructuredNLDoc` reference in the form `package.module:ModelName`. If the model lives in your current project rather than the installed `nldb` package, pass `--pythonpath /path/to/project`.

Extract data from a Markdown document using a model:

```bash
nldb extract myapp.docs:RecipeDoc document.md output.json
```

Render Markdown from YAML/JSON data using a model:

```bash
nldb render myapp.docs:RecipeDoc data.yaml rendered.md
```

The CLI uses positional file arguments so it can be scripted more easily:

- `extract <model-ref> <input-markdown> <output-json-or-yaml>`
- `render <model-ref> <input-data> <output-markdown>`

Use `-` as the output path to write to stdout.

Validate model idempotency against a sample Markdown document:

```bash
nldb validate myapp.docs:RecipeDoc --input document.md
```

Or validate from a sample payload instead:

```bash
nldb validate myapp.docs:RecipeDoc --data data.yaml --format json
```

Load a model from another project directory:

```bash
nldb validate myapp.docs:RecipeDoc --input document.md --pythonpath /path/to/project
```

Bootstrap a repo-local skill file for models/tools:

```bash
nldb init .
```

This writes `.skills/nldb/SKILL.md` from a bundled template with a short explanation of what nlDB is, when to use it, and the available commands.

Generate a working example project bundle:

```bash
nldb example .
```

This creates `./nldb_example` with a sample model, sample Markdown input, and sample YAML data so you can try `extract`, `render`, and `validate` against a known-good reference.

## Basic Usage

```python
from nldb import StructuredNLDoc, DataExtractor, AST_Handler, TemplateExtractor

class MyModel(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\n\n⸢rev•content⸥"
    title: str
    content: str

# Parsing
ast = AST_Handler()
tpl = TemplateExtractor()
data = DataExtractor()

recipes = tpl.extract_nodes(ast.split_nodes(MyModel.__template__))
payload = data.extract_values(ast.split_nodes("# Hello\n\nWorld"), recipes)

model = MyModel(**payload)
print(model.title) # "Hello"
```

## Testing

```bash
pytest
```

The standalone test suite includes an idempotency roundtrip check, and the CLI now exposes `validate` for template validation workflows.

## License

MIT
