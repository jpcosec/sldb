---
status: open
priority: p2
assigned_to: sldb-team
created: 2026-04-22
labels:
  - feature-request
  - ontology
  - semantics
  - cross-repo
---

# Feature Request: Semantic Field Mapping and Ontology Registry

## Context

We use SLDB across multiple repositories (wikipu, analyzer, docs, etc.). Each repo has documents that semantically overlap (READMEs, concepts, ADRs) but with different field names and structures.

**Example: README as ConceptDoc**

```
wikipu/README.md    → ConceptDoc → {title, abstract, purpose}
analyzer/README.md  → ConceptDoc → {title, overview, setup, api}
```

Same document type, same name, **different fields**. `sldb doc track` fails. Sync is meaningless without field mapping.

## Current State

Field descriptions exist but are prose-only:

```python
abstract: str = Field(description="One-paragraph summary of the concept")
```

Humans read this. Machines cannot infer that `overview` in analyzer maps to `abstract` in wikipu.

## Proposal: Semantic Field Metadata

Extend `Field()` to accept semantic metadata that machines can read.

### Option A: Structured Metadata in Field

```python
from typing import Annotated
from pydantic import Field, BaseModel

class Semantic(BaseModel):
    concept: str = Field(description="Semantic role of this field")
    aliases: list[str] = Field(default=[], description="Alternative field names across repos")
    canonical_model: str | None = Field(default=None, description="Model:field that is canonical")
    synonym_of: str | None = Field(default=None, description="Fully-qualified field this maps to")
    ignores: bool = Field(default=False, description="Skip this field in cross-repo sync")

class ConceptDoc(StructuredNLDoc):
    title: str = Field(
        description="Title of the concept",
        metadata=Semantic(concept="name:ConceptDoc.title")
    )
    abstract: str = Field(
        description="One-paragraph summary of the concept",
        metadata=Semantic(
            concept="what-it-is",
            aliases=["overview", "synopsis"],
            canonical_model="wikipu:ConceptDoc.abstract",
            synonym_of="analyzer:ConceptDoc.overview"
        )
    )
    definition: str = Field(
        description="Formal definition of the concept",
        metadata=Semantic(concept="what-it-truly-is", type="formal")
    )
```

### Option B: Semantic Aliases in Field

```python
class ConceptDoc(StructuredNLDoc):
    abstract: str = Field(
        description="One-paragraph summary of the concept",
        semantics="concept:what-it-is",
        alias_of=["overview", "synopsis"],
        canonical="wikipu:ConceptDoc.abstract"
    )
```

Simpler but less flexible.

### Option C: Dedicated Ontology Registry

```yaml
# .sldb/ontology.yaml
models:
  ConceptDoc:
    version: "2.1.0"
    canonical: wikipu
    field_definitions:
      abstract:
        meaning: "What this thing IS"
        type: string
        aliases:
          analyzer: overview
          docs: synopsis
```

Models stay clean. Ontology is external but versioned.

## Feature: `sldb model diff`

```bash
sldb model diff wikipu:ConceptDoc analyzer:ConceptDoc
```

```yaml
model: ConceptDoc
canonical: wikipu:ConceptDoc (v2.1.0)

differing_fields:
  abstract:
    wikipu: abstract (canonical)
    analyzer: overview (alias → abstract)
    compatible: true
  definition:
    wikipu: exists
    analyzer: missing
    compatible: true
  setup:
    wikipu: missing
    analyzer: exists
    compatible: true
  api:
    wikipu: missing
    analyzer: exists
    compatible: true

summary:
  compatible: true
  field_map: 2 fields mapped
  orphan_analyzer: 2 fields
```

## Feature: `sldb ontology`

```bash
sldb ontology init          # create .sldb/ontology.yaml
sldb ontology register    # register model field meanings
sldb ontology map repo    # declare mappings to another repo
sldb ontology check      # validate compatibility
sldb ontology tree       # show field hierarchy as tree
```

### `sldb ontology tree`

```bash
$ sldb ontology tree wikipu:ConceptDoc

ConceptDoc (v2.1.0)
├── title (concept: name:ConceptDoc.title)
├── abstract (concept: what-it-is, alias: overview, synopsis)
├── definition (concept: what-it-truly-is, type: formal)
├── examples (concept: instances-of: ConceptDoc)
└── related_concepts (concept: links-to: ConceptDoc)
```

## Feature: `sldb sync --semantic`

```bash
$ sldb sync analyzer/ --semantic

Syncing ConceptDoc...

abstract:
  wikipu: abstract (canonical) ←→ analyzer: overview (mapped)
  sync: yes (semantically equivalent)

definition:
  wikipu: exists
  analyzer: missing
  sync: no (no mapping defined)

setup:
  wikipu: missing
  analyzer: exists
  sync: skipped (orphan in analyzer)

✓ Sync complete: 1 field synced, 2 skipped
```

## Feature: `sldb model validate --cross-repo`

```bash
$ sldb model validate analyzer:ConceptDoc --cross-repo wikipu:ConceptDoc

Checking: analyzer:ConceptDoc
Canonical: wikipu:ConceptDoc (v2.1.0)

✓ abstract: alias mapped (overview → abstract)
✓ definition: canonical (no alias needed)
⚠ setup: orphan field (not in canonical model)
⚠ api: orphan field (not in canonical model)

Compatible: true
Warnings: 2 orphan fields
```

## Technical Considerations

### 1. Metadata Propagation

When a model is registered, metadata should be:
- Extracted and stored in `.sldb/models/<Model>.yaml`
- Included in hash computation

### 2. Hash Cascade Extension

```
doc_hash = hash(content + field_metadata_hash)
model_hash = hash(contract + field_metadata_hash + doc_hashes)
store_hash = hash(model_hashes)
```

### 3. Versioning

```yaml
# .sldb/ontology.yaml
version: "1.0"
canonical_models:
  wikipu:ConceptDoc: "2.1.0"
```

### 4. Fallback Behavior

If metadata is missing:
- `model diff` warns but still works
- `sync --semantic` falls back to field-name match
- `ontology tree` shows metadata-only fields separately

## Use Cases

### 1. Multi-Repo Documentation

Same concept (README, ADR) exists in multiple repos with different structure. Sync is possible because field semantics are declared.

### 2. Model Evolution

Canonical model changes. Extensions see:
- Which fields are new
- Which fields are removed
- Which fields are aliased

### 3. Semantic Search

```bash
sldb search "what-it-is" --field-semantics
# Finds: ConceptDoc.abstract, ADRDoc.context, ReferenceDoc.signature
```

## Alternatives Considered

| Alternative | Pros | Cons |
|---|---|---|
| Field description parsing | No schema change | Fragile, requires conventions |
| External ontology file | Clean models | Extra file to maintain |
| This proposal | Self-documenting, machine-readable | More complex Field definition |

## Priority

1. **Field metadata in Field()** (Option A or B)
2. **sldb model diff --semantic**
3. **sldb ontology tree**
4. **sldb sync --semantic**
5. **sldb ontology init/register/map/check**

## Questions for the Team

1. Is Option A (structured Semantic model) acceptable, or is Option B (flat fields) preferred?
2. Should metadata be required or optional? (We suggest optional with warnings.)
3. How should inheritance work? (Canonical + extensions model.)
4. Should we version field metadata separately from model contract?

---

Submitted by: wikipu team
Date: 2026-04-22
