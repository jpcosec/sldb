# SLDB Store: Index Architecture and Dependency Graph

## Overview

The SLDB store system introduces a pointer database layer (`.sldb/`) that tracks the relationship between model contracts (Python classes) and their instantiated documents (`.md` files) without duplicating any semantic information already present in the code.

The store does not move or own files — it maps identities to physical paths. The graph lives in `.sldb/`.

---

## 1. Physical Layout and Scope

`.sldb/` is a pure pointer database. It contains only YAML index files. Actual `.md` documents and Python model classes may reside anywhere in the project tree.

Two scopes are supported:

- **Global store** (`~/.sldb/`): consolidates foundational models and federated stores shared across projects.
- **Local store** (`./.sldb/`): routes models for the current project. Wins on any name collision with the global store at runtime.

The local store can reference the global store as a federated dependency. Resolution always prefers local.

---

## 2. Index Topology (The DAG)

The ecosystem state is structured as a DAG through a three-level cascade of YAML index files. Each level has a single responsibility: routing, inventory, or document-level integrity.

### Level 1 — `store_index.yaml`

The master router. Knows nothing about physical documents.

```yaml
stores:
  - name: shared-ontology
    path: ~/.sldb/

models:
  - name: Book
    path: src/models/book.py
    models_index: .sldb/models/book.yaml
  - name: Dictionary
    path: src/models/dictionary.py
    models_index: .sldb/models/dictionary.yaml

hash_a: <combined hash of models layer state>
```

`hash_a` is computed over the combined state of all `models_index` entries. A change to any model contract or inventory propagates up and invalidates this hash.

### Level 2 — `models_index.yaml` (one per model)

Manages the document inventory for a single model contract. Does **not** record relationships — those are derived at runtime from the Pydantic class.

```yaml
name: Dictionary
path: src/models/dictionary.py
documents_index: .sldb/documents/dictionary.yaml

hash_b: <combined hash of document inventory>
```

`hash_b` is computed over the set of document pointers in the associated `documents_index`. Changes when instances are added or removed.

### Level 3 — `documents_index.yaml` (one per model)

Manages integrity at the individual document level. Separates raw text identity from structured data identity.

```yaml
documents:
  - name: dictionary-en
    path: content/dictionaries/english.md
    hash_c: <hash of raw .md text>
    hash_d: <hash of extracted Pydantic field values>
```

Both hashes are computed from the same file:
- **`hash_c`**: computed over the full raw text of the `.md` file.
- **`hash_d`**: computed over the extracted field values in their typed Pydantic form.

---

## 3. Relationship Semantics

Relationships (`inherits`, `has_many`) exist in the Python class definitions and are **not** stored in the index. The YAML layer is a pointer store only — the Pydantic class is the single source of truth for schema, relationships, and field semantics.

When a query system is implemented (out of scope for this spec), it will derive the DAG topology at query time by inspecting class inheritance and field types.

**Directionality rules (for future query resolution):**
- `inherits`: child declares toward parent.
- `has_many`: container declares ownership of contained models/documents.

---

## 4. Integrity Audit (Hash Cascade)

The four hashes form a Merkle-like cascade. Each hash covers only its own level. A change at any level is detectable without re-analyzing the entire project.

### Document-level diagnostics (`hash_c` / `hash_d`)

| Condition | Diagnosis | Action required |
|-----------|-----------|-----------------|
| `hash_c` changed, `hash_d` stable | Benign volatile mutation (e.g. rendered date, formatting) | None |
| `hash_d` changed | Structured field values were manually edited | Operator decision |
| Path missing, hash matches elsewhere | Document was moved | Operator reconciliation |

### Model-level diagnostics (`hash_b`)

| Condition | Diagnosis | Action required |
|-----------|-----------|-----------------|
| `hash_b` changed | Inventory altered — instances added or removed | Operator review |

### Store-level diagnostics (`hash_a`)

| Condition | Diagnosis | Action required |
|-----------|-----------|-----------------|
| `hash_a` invalidated | Model contract changed (Pydantic fields or `__template__`) | Sub-graph halted until operator intervenes |

---

## 5. Operational Model

SLDB is **diagnostics-only**. It identifies the location and nature of each fracture in the hash cascade and reports it. It never auto-repairs.

Reconciliation actions (re-index, purge orphan, update path) are issued via explicit CLI commands. The operator decides what to do with the information.

---

## 6. Out of Scope (This Spec)

- Query system for traversing the graph by relationship type
- CLI commands for reconciliation (`sldb store repair`, `sldb store reindex`, etc.)
- Conflict resolution policy when global and local stores share model names across different schemas
