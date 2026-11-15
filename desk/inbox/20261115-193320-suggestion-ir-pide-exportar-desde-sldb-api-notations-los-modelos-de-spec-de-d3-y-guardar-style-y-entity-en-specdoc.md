---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T19:33:20'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# IR pide exportar desde sldb.api.notations los modelos de spec de D3 y guardar style y entity en SpecDoc

_Describe the incoming message with enough evidence to triage._

IR11 (specIR, compiladores y proyecciones de spec2viz) consume los modelos de spec de D3. sldb.api.notations exporta load_spec y validate_spec pero no las clases: ClassDiagram, SequenceDiagram, StateDiagram, ComponentDiagram, ActivityDiagram, DeploymentDiagram, MatrixDiagram, ReflectionDiagram, BaseDiagram, EnforcementArtifact y EnforcementFact solo se alcanzan en sldb.models.notation.diagram_specs. specIR solo debe importar sldb.api; mientras tanto un único módulo de specIR (src/specir/visual/spec_models.py) las importa de sldb.models.notation.diagram_specs, con una excepción acotada en tests/test_imports.py. Pedido 1: reexportarlas desde sldb.api.notations (o sldb.api) para quitar esa excepción. Pedido 2 (SpecSync, D1): el SpecDoc no guarda el style del spec (style.kinds) ni los campos de data que no son elementos (data.entity de un spec de estado), así que la IR de un SpecDoc resuelto con resolve_view pierde style_kinds y entity frente a la IR de su YAML; specIR lo declara como SPEC_DOC_GAPS en src/specir/visual/projections.py. Guardarlos en el SpecDoc permitiría quitar esa diferencia.
