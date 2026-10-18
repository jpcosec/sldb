---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: AntonIA
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-08-18T15:19:03'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-10-18T13:10:54'
---

# canonical path lint for repo-root references

_Describe the incoming message with enough evidence to triage._

Propuesta para SLDB: agregar un lint/regla de validación de referencias canónicas en artefactos de conocimiento. Reglas sugeridas: (1) permitir solo paths canónicos desde raíz del repo, por ejemplo source_docs/, projects/, software/, docs/, desk/; (2) rechazar rutas frágiles relativas como ../, ../../, ../../../ cuando se usan como referencias de conocimiento; (3) rechazar prefijos legacy como Lab_Chile-Teva/ y otros_proyectos/ en referencias canónicas; (4) validar que la ruta canónica referenciada exista. Caso motivador: reorganización taxonómica de AntonIA donde necesitamos paths estables e idempotentes para README, project.yaml, software.yaml, atoms, docs y provenance textual.

## Resolución

Resuelto (2026-10-18, sldb-04). `sldb lint [target] [--repo-root R] [--format text|json|yaml]` (src/sldb/cli/commands/lint.py) es el lint de paths canónicos de referencias a la raíz del repo, con `lint_path` y `lint_text`.
