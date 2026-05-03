# Current Source Tree

## Repository Distribution

```text
src/
├── sldb/
│   ├── __init__.py
│   ├── __main__.py
│   ├── ast_handler.py
│   ├── config.py
│   ├── data_extractor.py
│   ├── node_handler.py
│   ├── renderer.py
│   ├── structuredNLDoc.py
│   ├── template_extractor.py
│   ├── validation.py
│   ├── cli/
│   │   ├── __init__.py
│   │   └── main.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── ast.py
│   │   ├── data_extractor.py
│   │   ├── node_handler.py
│   │   ├── renderer.py
│   │   └── template_extractor.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── structured_doc.py
│   ├── runtime/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── validation.py
│   ├── store/
│   │   ├── __init__.py
│   │   ├── diagnostics.py
│   │   ├── hashing.py
│   │   ├── io.py
│   │   ├── models.py
│   │   └── resolver.py
│   ├── assets/
│   │   ├── __init__.py
│   │   └── skills/
│   │       ├── __init__.py
│   │       └── sldb.md
│   └── examples/
│       ├── __init__.py
│       └── reference_bundle/
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

- `src/sldb/core/`: core Markdown parsing, extraction, node handling, and rendering pipeline
- `src/sldb/models/structured_doc.py`: base model contract and field-description enforcement
- `src/sldb/runtime/`: config and extract/render/roundtrip helpers used by the CLI and store hashing
- `src/sldb/cli/main.py`: top-level command parser and execution flow
- `src/sldb/store/`: YAML-backed store layer for indexes, hashing, diagnostics, and store lookup
- `src/sldb/assets/skills/`: bundled skill-file assets for `sldb init`
- `src/sldb/examples/reference_bundle/`: bundled reference example for `sldb example`
- compatibility re-export modules remain at `src/sldb/*.py` for older import paths
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
