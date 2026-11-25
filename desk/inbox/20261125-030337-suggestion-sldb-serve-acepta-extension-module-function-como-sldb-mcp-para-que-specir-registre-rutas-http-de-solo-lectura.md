---
sldb:
  by: agent
  at: '2026-11-25T06:05:50Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T03:03:37'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-25T03:05:22'
# why the note was acknowledged; empty when no reason was given
ack_reason: 'tarea: sldb serve acepta --extension con rutas GET bajo /ext/<nombre>/'
# conversation thread/message the note came from, e.g. #hilo/1234
---

# sldb serve acepta --extension MODULE:FUNCTION como sldb mcp, para que specIR registre rutas HTTP de solo lectura

_Describe the incoming message with enough evidence to triage._

Decision D8 de JP (2026-11-25, plan graph_ui de IR: desk/drawer/plans/graph-ui-diccionario-de-componentes/PROPUESTA-UI.md). La UI nueva de specIR (IR/ui, React TSX) lee por HTTP desde sldb serve. Pedido: que sldb serve acepte --extension MODULE:FUNCTION (repetible), igual que sldb mcp (build_server(..., extensions=...) en src/sldb/mcp/server.py), y que la funcion reciba un registrador con el que la extension agrega rutas HTTP de solo lectura (GET) bajo un prefijo propio, p. ej. /ext/specir/... (impacto, reglas, controles), con acceso al store servido. sldb no importa specir: la extension se carga por nombre. Sin escritura por esta via. Bloquea U6 (grafo por capas) y U7 en IR. Respuesta esperada: tarea en sldb o nota de vuelta a IR.
