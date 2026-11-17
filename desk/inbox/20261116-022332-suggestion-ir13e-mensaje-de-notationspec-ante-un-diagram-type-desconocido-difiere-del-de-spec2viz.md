---
sldb:
  by: agent
  at: '2026-11-17T01:57:57Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-16T02:23:32'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T22:57:28'
---

# IR13e: mensaje de NotationSpec ante un diagram_type desconocido difiere del de spec2viz

_Describe the incoming message with enough evidence to triage._

Desde IR, tarea task-ir13e-portar-a-ir-las-pruebas-de-notaciones-paletas-y-vistas-de-spec2viz-contra-sldb. Al portar contra sldb la prueba de spec2viz tests/test_notation.py::test_invalid_notations_are_rejected (revisión b624b75), el caso {"diagram_type": "mindmap"} espera que el error contenga «not a spec2viz diagram type»; sldb.notations.NotationSpec.model_validate rechaza el valor con otro mensaje: «diagram_type 'mindmap' is not a valid diagram type» (sldb/src/sldb/notations/notation_spec.py:47). Los otros 14 casos de la misma prueba pasan. En IR queda como pytest.mark.xfail(strict=True) en tests/visual/test_notations_parity.py::test_invalid_notations_are_rejected[changes1-not a spec2viz diagram type], y la fila SV-H01 de la matriz de cobertura de spec2viz sigue abierta por esta diferencia. Pedido: que sldb decida si conserva el mensaje de spec2viz (para que la paridad se acredite) o declara el nuevo mensaje como el contrato, y lo responda al desk de IR.
