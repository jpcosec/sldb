---
status: open
priority: p1
assigned_to: sldb-team
created: 2026-04-22
labels:
  - feature-request
  - knowledge-graph
  - integration
  - reasoning
  - federation
---

# Feature Request: sldb ↔ Knowledge Graph Integration

## Context

We have two systems with complementary strengths:

**sldb:**
- Self-describing templates (`__template__`)
- Roundtrip validation (idempotency guarantee)
- Hash cascade (Merkle-style integrity)
- Federation (cross-repo stores)

**wiki_compiler (knowledge graph):**
- Graph traversal (50+ node types)
- Facets (compliance, git, source, semantics)
- OWL reasoning (implicit relationships)
- Energy audit (systemic health)
- Context routing (relevant docs for task)

Together they can do things neither can do alone.

## Clarification: Relationship with kg_db

**IMPORTANT:** This request and `extract-kg_db-from-wikipu.md` are **complementary, not contradictory**.

| Library | Scope |
|---|---|
| **sldb + graph/ (minimal)** | Edges between documents, cross-repo links, basic traversal |
| **kg_db (full)** | OWL reasoning, energy audit, context routing, cleansing |

**sldb gets MINIMAL graph capabilities. kg_db does FULL reasoning.**

### Division of Labor

```
sldb (minimal graph)
├── .sldb/documents/    ← documents
├── .sldb/models/      ← contracts
└── .sldb/graph/       ← edges + links ONLY
                         ← NO OWL
                         ← NO energy
                         ← NO context

kg_db (full reasoning)
├── knowledge_graph.json
├── graph/             ← full operations
├── reasoning/         ← OWL + SHACL
├── energy/           ← audit
├── context/          ← routing
└── cleansing/        ← proposals
```

### What sldb DOES NOT Get

This request does NOT add to sldb:
- OWL reasoner
- Energy audit
- Context routing
- Cleansing proposals
- Full graph operations

These belong to kg_db.

## What sldb Gets (Minimal Graph)

### 1. Graph Traversal for Cross-Doc Relationships

### 1. Graph Traversal for Cross-Doc Relationships

**Current in wiki_compiler:** `src/wiki_compiler/query_executor.py`

Documents are nodes in a directed graph with typed edges:

```python
class Edge(BaseModel):
    target_id: str
    relation_type: Literal[
        "contains",
        "depends_on",
        "reads_from",
        "writes_to",
        "documents",
        "transcludes",
        "extends",
        "implements",
    ]
```

**What sldb needs:**

```python
# In .sldb/documents/<Doc>.yaml
relationships:
  - target: analyzer:ConceptDoc.foo.md
    relation: extends
  - target: wikipu:ADRDoc.bar.md
    relation: documents
  - target: self:Chapter.1.md
    relation: contains
```

**Reference implementation:**
- `src/wiki_compiler/contracts.py:Edge` — typed edge model
- `src/wiki_compiler/graph_utils.py:add_knowledge_node()` — add edges to graph
- `src/wiki_compiler/query_language.py` — query DSL for graph traversal

**Command:**

```bash
sldb doc link --from foo.md --to bar.md --relation documents
sldb doc links foo.md --relation documents
# Returns: bar.md

sldb doc tree --from foo.md --depth 2
# Shows full relationship tree
```

---

### 2. Facets: Multi-Dimensional Doc Metadata

**Current in wiki_compiler:** `src/wiki_compiler/contracts.py:KnowledgeNode`

Every node has optional facets:

```python
class KnowledgeNode(BaseModel):
    identity: SystemIdentity
    edges: list[Edge]
    semantics: SemanticFacet | None    # What does this do?
    ast: ASTFacet | None          # Code structure
    io_ports: list[IOFacet]      # Input/output
    compliance: ComplianceFacet | None  # Implementation status
    adr: ADRFacet | None          # Architecture decision
    test_map: TestMapFacet | None    # Testing strategy
    git: GitFacet | None          # Git metadata
    source: SourceFacet | None       # Provenance
```

**What sldb needs:**

```yaml
# .sldb/documents/foo.yaml
facets:
  compliance:
    status: implemented
    failing_standards: []
  git:
    blob_sha: abc123
    created_at_commit: def456
    last_modified: "2026-04-22"
  source:
    compiled_from: wiki-compiler
    compiled_at: "2026-04-22T14:00:00Z"
  test_map:
    test_type: unit
    coverage_percent: 85.0
```

**Reference implementation:**
- `src/wiki_compiler/contracts.py:ComplianceFacet` — implementation status
- `src/wiki_compiler/contracts.py:GitFacet` — git tracking
- `src/wiki_compiler/contracts.py:SourceFacet` — provenance
- `src/wiki_compiler/facet_injectors.py` — how facets are populated

---

### 3. OWL Reasoning: Implicit Relationships

**Current in wiki_compiler:** `src/wiki_compiler/owl_reasoner.py`

OWL ontology reasoner infers implicit relationships:

```python
from owlready2 import World, sync_reasoner

# If ConceptDoc extends Document
# And Document has a "readme" relationship
# Then ConceptDoc has a "readme" relationship (inferred)

# Run reasoner
world = World()
graph = world.get_ontology("https://wikipu.ai/")
sync_reasoner(graph)
```

**What sldb needs:**

```bash
# Model inheritance as OWL axioms
sldb model owl ConceptDoc --output concept.owl
```

```turtle
# Generated OWL:
:ConceptDoc rdfs:subClassOf :Document .
:Document rdfs:subClassOf :StructuredNLDoc .

# If query asks for all subclasses of Document:
# OWL reasoner returns: ConceptDoc, ADRDoc, ReferenceDoc, ...
```

**Reference implementation:**
- `src/wiki_compiler/owl_reasoner.py` — owlready2 integration
- `src/wiki_compiler/owl_backend/owl_reasoner.py:run_owl_reasoner()`
- `src/wiki_compiler/shacl/validator.py` — SHACL shape validation

**Command:**

```bash
sldb model subclasses ConceptDoc
# Returns: HowToDoc, ReferenceDoc, IndexDoc, ...

sldb model ancestors HowToDoc
# Returns: HowToDoc → ConceptDoc → Document → StructuredNLDoc

sldb doc infer-links foo.md
# Returns: inferred relationships from OWL reasoner
```

---

### 4. Energy Audit: Systemic Health

**Current in wiki_compiler:** `src/wiki_compiler/energy.py`

Systemic energy measures health of the entire knowledge base:

```python
class SystemicEnergy(BaseModel):
    energy_score: float
    node_count: int
    edge_count: int
    compliance_violations: int
    perturbations: int
    redundant_nodes: int
    boilerplate_ratio: float
```

**Energy breakdown:**

```python
structural_energy = redundancy_check(graph)     # Duplicate nodes
abstraction_energy = complexity_check()     # Long files, complex functions
violation_energy = compliance_violations    # Failing standards
perturbation_energy = git_drift()          # Uncommitted changes
```

**What sldb needs:**

```bash
sldb store energy --report
```

```yaml
energy_score: 42.5
model_count: 7
document_count: 156
validated_documents: 142
unvalidated_documents: 14
hash_drift: 3
orphan_documents: 2
redundant_models: 1  # Model with >10 doc instances
boilerplate_ratio: 0.23
```

**Reference implementation:**
- `src/wiki_compiler/energy.py:run_energy_audit()` — full energy calculation
- `src/wiki_compiler/energy.py:calculate_redundancy()` — Jaccard similarity
- `src/wiki_compiler/perception.py:build_status_report()` — zone status

---

### 5. Context Routing: Relevant Docs for a Task

**Current in wiki_compiler:** `src/wiki_compiler/context.py`

Given a task, retrieve relevant docs:

```python
class ContextRequest(BaseModel):
    node_ids: list[str]
    task_hint: str | None
    depth: int = 1
    include_planned: bool = False

class ContextBundle(BaseModel):
    nodes: list[KnowledgeNode]
    edges: list[Edge]
    rationale: dict[str, str]
    scores: dict[str, float]
    prose: dict[str, str]
```

**What sldb needs:**

```bash
sldb context "review architecture decision"
# Returns: relevant ADRs, their models, related concepts, ...
# Scored by relevance to task

sldb context "audit sldb store"
# Returns: store_index.yaml, models/, documents/
# Tracked in .sldb/context_cache/
```

**Reference implementation:**
- `src/wiki_compiler/context.py:build_context_bundle()` — context routing
- `src/wiki_compiler/query_executor.py:StructuredQuery` — structured queries
- `src/wiki_compiler/registry.py` — facet registry

---

### 6. Cleansing: Structural Optimization

**Current in wiki_compiler:** `src/wiki_compiler/cleanser.py`

Proposals to optimize the graph:

```python
class CleansingProposal(BaseModel):
    node_id: str
    operation: Literal["destroy", "relocate", "split", "merge"]
    rationale: str
    requires_human_approval: bool = True
```

**What sldb needs:**

```bash
sldb cleanse --dry-run
# Proposes:
# - merge: redundant_concept_a.md + redundant_concept_b.md
# - split: large_adr.md into context.md + decision.md + consequences.md
# - relocate: orphan_docs/ → tracked/
# - destroy: duplicate_docs/
```

**With sldb validation:**

```bash
sldb cleanse --apply --proposal merge
# sldb validate roundtrips the merged doc
# If fails: proposal rejected, fix required
# If passes: merge applied + committed
```

**Reference implementation:**
- `src/wiki_compiler/cleanser.py:detect_cleansing_candidates()`
- `src/wiki_compiler/cleanser.py:apply_proposal()`
- `src/wiki_compiler/validation.py:validate_model_input_roundtrip()` — sldb can use this directly

---

## Implementation Priorities

### Phase 1: Foundation (Take from wiki_compiler as-is)

| Feature | File | What to port |
|---|---|---|
| Typed edges | `contracts.py:Edge` | Copy to sldb |
| Facets | `contracts.py:ComplianceFacet` | Copy to sldb |
| Model registry | `registry.py` | Adapt for sldb models |

### Phase 2: Reasoning

| Feature | File | What to port |
|---|---|---|
| OWL reasoner | `owl_reasoner.py` | Port + adapt |
| SHACL shapes | `shacl/validator.py` | Port + adapt |

### Phase 3: Systemic View

| Feature | File | What to port |
|---|---|---|
| Energy audit | `energy.py` | Adapt for hash cascade |
| Context routing | `context.py` | Adapt for sldb docs |
| Cleansing | `cleanser.py` | Adapt for sldb |

---

## Specific Code References

### Edge Model (copy directly)

```
src/wiki_compiler/contracts.py:12-29
```

```python
class Edge(BaseModel):
    target_id: str
    relation_type: Literal[
        "contains", "depends_on", "reads_from",
        "writes_to", "documents", "transcludes",
        "extends", "implements",
    ] = Field(description="...")
    metadata: dict[str, Any] = Field(default_factory=dict)
```

### Facet Models (adapt)

```
src/wiki_compiler/contracts.py:145-205
```

Compliance, Git, Source, Semantic, AST, I/O, Test, ADR facets.

### OWL Reasoner (adapt)

```
src/wiki_compiler/owl_reasoner.py:32-45
src/wiki_compiler/shacl/shapes.py:40-55
```

Uses owlready2 + SHACL shapes.

### Energy Audit (adapt)

```
src/wiki_compiler/energy.py:150-250
```

Calculates structural, abstraction, violation, perturbation energy.

### Context Routing (adapt)

```
src/wiki_compiler/context.py:75-120
```

```python
def build_context_bundle(request: ContextRequest) -> ContextBundle:
    nodes = query_graph(request)
    edges = get_edges_between(nodes)
    scores = calculate_relevance(nodes, request.task_hint)
    return ContextBundle(...)
```

---

## Questions for the Team

1. **Architecture:** Should sldb embed a mini-graph, or should it delegate to wiki_compiler?
2. **OWL integration:** Port owlready2, or use a lighter reasoner?
3. **Energy:** Use hash cascade (sldb-native) vs node count (wiki-native)?
4. **Federation:** Should federation links be graph edges?
5. **Backward compatibility:** How to add without breaking existing store?

---

Submitted by: wikipu team
Date: 2026-04-22
Repo: https://github.com/jpcosec/wikipu
