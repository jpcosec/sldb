---
sldb:
  by: agent
  at: '2026-11-16T08:25:41Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: spec2viz
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T00:47:23'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:25:25'
---

# sldb notations from-graph: elegir campo para label, kind/estilo y agrupación (heredado de spec2viz)

_Describe the incoming message with enough evidence to triage._

Origen: drawer de spec2viz, task-from-graph-etiqueta-y-estilo-desde-campos-del-documento (Governance, DAG de repos, 2026-10-21). spec2viz diagram from-graph pasó a sldb notations from-graph --store/--snapshot (fila SV-K10 de IR/docs/spec2viz/correspondencia-cli.md; código en sldb/src/sldb/cli/commands/notations_from_graph.py) y conserva la limitación: el label del nodo es el id del documento (p. ej. repo-chatbot-infra) y el kind es el modelo (RepositoryDoc). Pedido: opciones para elegir el campo del label (name/title), el campo que da kind o estilo (status o un tag como system:<id>) y, opcional, un campo de agrupación (contains por tag), para colorear los repos por sistema o estado sin editar el spec generado. Repro: sldb notations from-graph --store .sldb --models RepositoryDoc --relations depends_on sobre un store con RepositoryDoc. En spec2viz se bota (el repo se retira).
