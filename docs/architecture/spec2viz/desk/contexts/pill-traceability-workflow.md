---
id: pill-traceability-workflow
tags:
- workspace:desk
---

# Pill: Traceability Workflow

- Cambiar arquitectura: actualizar spec yml → regenerar HTML → validador verde → commit.
- Añadir spec: crear yml conforme al schema contract → registrar en `manifest.yml` → declarar `views:` → crear vistas o aceptar coverage warning.
- Añadir vista: entrada en `../../vistas/vistas.yml` + fuente `.mmd` (+ `.puml` opcional con header) → regenerar → simetría `specs:`/`views:`.
- Cambiar un diagrama: editar solo el `.mmd` fuente → regenerar → commit (drift check lo exige).
- El validador (`scripts/validate_spec_traceability.py`) es la gate: 0 errores; warnings son backlog visible, no fallos.
- Atoms de este desk (`atom-reference-edge`, `specyaml-nexus`, `diagram-as-projection`, `traceability-symmetry`, `generated-artifact-drift`, `coverage-warning`) gobiernan estas reglas.
