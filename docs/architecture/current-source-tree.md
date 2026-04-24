# Current Source Tree

## Repository Distribution

```text
src/
├── sldb/
│   ├── __init__.py
│   ├── __main__.py
│   ├── ast_handler.py
│   ├── cli.py
│   ├── config.py
│   ├── data_extractor.py
│   ├── node_handler.py
│   ├── renderer.py
│   ├── structuredNLDoc.py
│   ├── template_extractor.py
│   ├── validation.py
│   ├── store/
│   │   ├── __init__.py
│   │   ├── diagnostics.py
│   │   ├── hashing.py
│   │   ├── io.py
│   │   ├── models.py
│   │   └── resolver.py
│   └── templates/
│       ├── __init__.py
│       ├── sldb.md
│       └── example_bundle/
│           ├── __init__.py
│           ├── README.md
│           ├── guide.data.yaml
│           ├── guide.input.md
│           └── guide_model.py
└── nldb/
    ├── __init__.py
    └── __main__.py
```

## Module Roles

- `src/sldb/structuredNLDoc.py`: base model contract and field-description enforcement
- `src/sldb/validation.py`: extract/render/roundtrip helpers used by the CLI and store hashing
- `src/sldb/cli.py`: top-level command parser and execution flow
- `src/sldb/ast_handler.py`, `src/sldb/template_extractor.py`, `src/sldb/data_extractor.py`, `src/sldb/renderer.py`: core Markdown processing pipeline
- `src/sldb/store/`: YAML-backed store layer for indexes, hashing, diagnostics, and store lookup
- `src/sldb/templates/`: bundled skill/template assets and example bundle
- `src/nldb/`: rename shim that tells users to use `sldb`

## Test Distribution

```text
tests/
├── test_standalone.py
└── store/
    ├── __init__.py
    ├── test_cli_store.py
    ├── test_diagnostics.py
    ├── test_hashing.py
    ├── test_models_io.py
    └── test_resolver.py
```
