# Model Authoring and Draft Evolution

This document specifies the declarative model authoring and contract evolution in SLDB (`StructuredNLDoc`).

## 1. Declarative Model Attributes

Every `StructuredNLDoc` subclass may declare:

- `__authority__`: String representing document authority (`source_raw`, `authored`, `theorem`, `generated`, `cache`). Defaults to `"generated"`.
- `__semantics__`: Dictionary defining semantic dimensions (e.g., `{"representation": ["markdown"], "source": ["document", "markdown"]}`).
- `__containment__`: Mapping of `field_name -> list[target_model_names]`, establishing visual containment relations in the knowledge graph.
- `__references__`: List of field names holding document identifiers that represent non-containment graph references.
- `__compositions__`: Mapping of `comp_name -> spec_dict` where `spec_dict` defines `source_field`, `model`, `template`, and `separator`. Each composition must be rendered via a non-reversible `⸢render•<comp_name>⸥` marker in `__template__`.

## 2. Programmatic Creation (`sldb.api.create_model`)

`create_model` generates a `StructuredNLDoc` class module, validates it via roundtrip check, registers it in the store index, and creates its model and document indexes.

Parameters:
- `name`: Model class name (CamelCase identifier).
- `fields`: Field declarations (`[{name, type, description, required?, default?, enum?}]`).
- `template`: Optional markdown template. When omitted, `default_template` generates headings and slots for every field plus `⸢render•<name>⸥` for each composition.
- `containment`: Optional mapping `dict[str, list[str]]`.
- `references`: Optional list `list[str]`.
- `compositions`: Optional mapping `dict[str, dict]`.
- `semantics`: Optional mapping `dict[str, list[str]]`.
- `authority`: Optional authority string.

Validation rules:
- Every field named in `containment` or `references` must exist among the model's declared (or inherited) fields.
- Every `compositions[k].source_field` must exist among the declared (or inherited) fields.
- Every composition key must have its corresponding `⸢render•<comp_name>⸥` marker present in `__template__`.
Violations raise `SLDBModelError`.

## 3. Inspection (`sldb.api.describe_model` & `GET /models/detail`)

`describe_model` returns a `ModelDescription` containing:
- `name`, `model_ref`, `path`, `version`, `canonical`, `family`, `semantics`, `base_models`, `fields`, `documents`.
- `containment`: Dictionary of containment targets.
- `references`: List of reference fields.
- `compositions`: Dictionary of composition specifications.
- `semantics_map`: Declared `__semantics__` dictionary.
- `authority`: Declared `__authority__`.
- `template`: Model's active markdown template.
- `has_draft`: Boolean indicating whether a `.draft.py` (`.py.temp`) exists.
- `draft_path`: Path string to the draft file if present, otherwise `None`.

## 4. Draft Metadata Editing (`sldb.api.edit_model_metadata`)

Pending changes to model metadata are written to the draft sibling file (`<module>.py.temp`) using AST rewriting (`metadata_literals.py`), leaving the active model source completely untouched until promotion.

- `edit_model_metadata(store, model_name, *, containment=None, references=None, compositions=None, semantics=None, authority=None, pythonpath=None) -> ModelDraft`:
  - Inserts or replaces `__containment__`, `__references__`, `__compositions__`, `__semantics__`, `__authority__` via AST manipulation.
  - Synchronizes `⸢render•<name>⸥` sections in `__template__` when compositions are added or removed.

## 5. Contract Validation & Backfill Promotion

- `validate_model_draft(store, model_name, pythonpath)` verifies that:
  - Reversible template markers reference valid declared fields.
  - `__references__`, `__containment__`, and `__compositions__` only reference declared fields.
  - Every composition has a `⸢render•<name>⸥` marker in `__template__`.
  - Violations raise actionable `SLDBModelEditError`.

- `promote_model_draft(store, model_name, pythonpath, backfill=False)`:
  - Validates the draft.
  - With `backfill=True`, updates documents that need re-rendering under new defaults, template changes, or composition changes.
  - Atomically replaces the active model file with the draft.
  - Removes the draft file.
  - Reindexes the model, bumps contract version, and triggers derived rebuilds for semantic, section, and edge indexes.

## 6. CLI & HTTP Surface

CLI:
- `sldb models metadata edit <model> [--containment ...] [--references ...] [--compositions ...] [--semantics ...] [--authority ...]`: Creates or updates a metadata draft.
- `sldb models validate <model> --promote --backfill`: Validates, promotes the draft, and backfills tracked documents.
- `sldb models create <name> --template <tpl> --fields <spec> [--containment ...] [--references ...] [--compositions ...] [--semantics ...] [--authority ...]`.

HTTP Serve (`sldb serve`):
- `POST /models/create`: Generates and registers a new model.
- `GET /models/detail?model=<name>`: Returns complete model description including metadata and draft status.
- `POST /models/metadata-edit`: Updates draft metadata.
- `POST /models/promote`: Accepts `{"model": "<name>", "backfill": true}` to promote with document backfill and index rebuilds.
