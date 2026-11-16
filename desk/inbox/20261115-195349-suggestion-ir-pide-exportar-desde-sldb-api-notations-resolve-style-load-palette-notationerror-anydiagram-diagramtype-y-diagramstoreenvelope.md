---
sldb:
  by: agent
  at: '2026-11-16T08:23:01Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T19:53:49'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:22:46'
---

# IR pide exportar desde sldb.api.notations resolve_style, load_palette, NotationError, AnyDiagram, DiagramType y DiagramStoreEnvelope

_Describe the incoming message with enough evidence to triage._

IR12 (renderers, linter y JSON Schema de la capa visual de specIR, migrados de spec2viz) necesita de sldb seis nombres que sldb.api no exporta: resolve_style y load_palette (sldb.notations; los renderers mermaid y de clases colorean con la precedencia de estilo de sldb y escriben el texto con la tinta de la paleta builtin default), NotationError (sldb.notations; raíz de ParseError y ValidationError, la capturan los comandos render, validate y lint), y AnyDiagram, DiagramType y DiagramStoreEnvelope (sldb.models.notation.diagram_specs; el export de JSON Schema de specs y de catálogos). specIR solo importa sldb.api; hasta que sldb los reexporte desde sldb.api.notations, specIR los toma en dos módulos acotados por tests/test_imports.py: src/specir/visual/notation_style.py (sldb.notations) y src/specir/visual/spec_models.py (diagram_specs, el mismo del pedido de IR11 por los modelos de spec de D3). Cuando estén exportados, solo cambian esos imports y se quitan las excepciones. No bloquea IR12.
