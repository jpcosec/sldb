---
id: task-build-code-self-documentation
status: active
summary: ''
tags:
- system:sldb
- workspace:desk
- topic:selfdoc
current_node: ''
history:
- '2026-10-18 tanda 1 (sldb-04): selfdoc python-check y python-sync vuelven a correr.
  Una propiedad con setter (o un @overload) era dos símbolos con un mismo id de documento
  (31a3a5d634). python-sync ya no depende de un kgdb externo: escribe el grafo con
  sldb.store.graph, y --kgdb-command y --kgdb-output se quitaron (ab78747c). Siguiente
  tanda: con la configuración documentada (--source-root src --package sldb), el inventario
  está desactualizado (1502 símbolos faltan, 980 cambiaron, 299 sobran); un python-sync
  lo pone al día. La migración de ids sldb.sldb.* a sldb.* queda como tanda propia,
  porque cambia todas las identidades generadas.'
- '2026-10-18 tanda 2 (sldb-04): inventario de símbolos al día con python-sync (4d1126b2):
  2482 símbolos, 1502 nuevos, 980 actualizados y 299 obsoletos quitados, ninguno con
  contenido escrito a mano. stores check pasó de 25 s a 43 s y quedó como task-stores-check-escala-mal-con-el-inventario-de-símbolos-python
  (1bd2cfc2).'
- '2026-10-18 tanda 3 (sldb-04): migración de ids sldb.sldb.* a sldb.* en un commit
  propio (97c98036): git mv de los 2482 documentos, prune de los nombres viejos y
  python-sync sin --package. python-check en ok y ningún id ni nodo con sldb.sldb.
  Siguiente: el resto del handoff (parsear la metadata de los docstrings y validar
  su frontmatter, herencia de tags, re-exports y shadowing, tipos de relación registrados,
  proyección a spec2viz, federación de símbolos).'
- '2026-10-18 tandas A, B y C (sldb-04). A, c815d18c: la metadata de los docstrings
  se lee estricta y los errores y los ids duplicados salen como path:line en metadata_errors;
  python-sync no escribe nada mientras haya alguno. B, 23ed7359: herencia léxica de
  tags (system/workspace del más cercano, topic como unión, el resto local) con su
  origen en el grafo; el piloto del spec da su tabla. C, 774f3d4f: los imports siguen
  las cadenas de re-export hasta la definición (490 en sldb, con via), y se corrige
  el import relativo en un __init__. El inventario quedó al día en 70d64121.'
- '2026-10-18 tanda D (sldb-04): la proyección a spec2viz la implementa spec2viz en
  from-graph (label desde ast.name o ast.module, kind desde semantics.kind o la clase
  AST, --module-prefix sin nodos ni aristas colgando, relaciones tal cual), según
  la nota en su desk. La validación es ''spec2viz diagram validate''. Pendiente: confirmar
  con su commit que la salida valida.'
references:
- docs/documentation-review.md
- docs/architecture/code-docstring-indexing.spec.md
- docs/architecture/code-docstring-indexing-handoff.md
depends_on: []
pills:
- desk/pills/pill-015-self-documentation-boundaries.md
files: []
task_type: ''
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Build code-derived self-documentation

## Rationale

_Explain why this task exists or the business driver behind it._

SLDB should document its own executable interfaces using tracked records derived from code. Handwritten inventories have drifted from the parser and source tree.

## Goal

_Describe the concrete result this task must produce._

Provide repeatable scan, materialization, tracking, and freshness checks for code documentation.

## Scope

_State what is in scope and what is out of scope._

First slice: argparse CLI inventory to CliCommandDoc and SurfaceDoc, preserving authored explanations and detecting removed commands without deleting them. Later slices: Python symbols/docstrings, source hashes and rename handling, spec2viz architecture views. Domain semantics remain declared or reviewed.

## Implementation Path

_Outline the expected implementation route or affected surface._

Add a typed parser adapter and selfdoc scan/sync/check commands, anchor outputs to the selected store, reuse the existing document models and tracking operations, and apply the workflow to this repository.

CLI slice implemented: selfdoc scan/sync/check, typed argument and group facts, contract fingerprints, preserved author fields, obsolete-command reporting, and tracked command/surface records. The repository materialized 89 CLI records and preserved author fields in existing documents. `selfdoc python-scan|python-sync|python-check` provides and tracks a static AST inventory with qualified IDs, source hashes/spans, signatures, docstrings, imports, conservative rename candidates, and an optional hash-pinned spec2viz reference; generated facts preserve authored purpose, architecture, and tags. Semantic grouping and review workflows remain active work.

The next slice is specified in `docs/architecture/code-docstring-indexing.spec.md`, with pilot module/class docstrings in `src/sldb/selfdoc/python_symbol.py`. The contract reuses SLDB metadata and spec2viz classification, derives structure and selected contextual tags from the AST, and keeps graph persistence in KGDB. Parsing this metadata and migrating legacy generated identities remain pending; the pilot is not an implemented semantic pipeline. The continuation handoff separates small annotation batches from adapter implementation and records known limitations in rename/check reporting.

Batch 2 (2026-09-14): annotated the four declarations in `selfdoc/planned_document.py` and `selfdoc/report.py` following the pilot frontmatter format. Fixture validation, the 305-test focused suite, `python-sync` (`ok: true`, 4 written, no findings) and `python-check` (`ok: true`, zero written) all passed; results and the next batch are recorded in the handoff. Docstring metadata interpretation remains unimplemented.

Batch-2 review corrected inaccurate rename-uniqueness and exit-status claims in source documentation, plus the handoff's imported-versus-nested class mistake. Spec sections 4.1–4.2 now separate import bindings from definition/containment and annotation references, with concrete `command.py` acceptance cases. Import extraction/resolution and the known runtime reporting fixes remain pending; the next annotation batch is explicitly bounded in the handoff.

Follow-up implementation (2026-09-14): Python checks now propagate a non-current report as exit status 1, and rename candidates require exactly one matching candidate. `python-sync` writes a producer-scoped KGDB source graph at `.kgdb/python-source.graph.json`; `python-check` treats its absence or stale AST/source evidence as drift. The graph carries AST containment, import bindings, and resolved annotation-reference edges with spans/hashes, so graph-aware tools can inspect code context without re-deriving it from docstrings. Strict frontmatter validation, tag inheritance, re-export/shadowing resolution, typed relation registration, and spec2viz projection remain active work.

## Validation

_List the checks required before this task can close._

- Verify parser defaults, required options, mutually exclusive groups, nested commands, and hidden-command policy.
- Verify preservation of authored sections, freshness detection, missing tracking, removal reporting, and no writes during check.
- Verify repeated sync is a no-op and queries reach generated records.
- Extend coverage to Python symbols and architecture integration in subsequent slices.

## Done When

_Name the observable condition that makes the task complete._

CLI and Python source inventories, provenance and incremental synchronization are implemented and tested. The first CLI slice alone does not close this task.
