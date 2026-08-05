---
id: pill-specyaml-traceability
tags:
- workspace:desk
---

# Pill: SpecYAML Traceability

- Specyaml (`docs/architecture/spec2viz/*.yml`) es el nexo machine-readable entre `desk/atoms/` y los diagramas.
- Atoms gobernantes de la capa: viven en el desk propio de spec2viz (`docs/architecture/spec2viz/desk/atoms/`): `atom-reference-edge`, `specyaml-nexus`, `diagram-as-projection`, `traceability-symmetry`, `generated-artifact-drift`, `coverage-warning`.
- Esquemas gobernantes:
  - `docs/architecture/contracts/specyaml-schema-contract.md` (forma de los YAML)
  - `docs/architecture/contracts/diagram-traceability-contract.md` (vistas, puml, HTML generado)
- Edge spec→atoms: campo `atoms:` por nodo; los ids deben existir en `desk/atoms/`.
- Edge spec→vistas: campo `views:` por spec ↔ campo `specs:` en `docs/architecture/vistas/vistas.yml` (simetría obligatoria).
- `docs/architecture/spec2viz/manifest.yml` es el índice único de specs, registry, tooling.
- El HTML de vistas es GENERADO (`scripts/generate_vistas_html.py`); nunca editarlo a mano.
- Todo task que toque `spec2viz/`, `vistas/` o `core-diagrams/` debe cerrar con `scripts/validate_spec_traceability.py` en verde (warnings permitidos, errores no).
