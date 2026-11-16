---
sldb:
  by: agent
  at: '2026-11-16T08:22:02Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T18:20:13'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:21:46'
---

# sldb mcp: gancho público de comprobaciones de dominio antes de propose_changes

_Describe the incoming message with enough evidence to triage._

IR03b (IR main 3acb087) monta specir.mcp_extension:register sobre sldb mcp. specIR necesita una regla de dominio antes de proponer cambios (claims_verified, IR05 D2-E: un agente no escribe verificacion: verificado por el MCP). Hoy la extensión quita propose_changes/apply_changes y los vuelve a registrar desde WriteTools con la comprobación, e importa sldb.mcp (changes, paging, registry, write), que no es parte de sldb.api. Pedido: un gancho público en build_server/extension para registrar validadores de lote (fn(batch, ctx) -> findings) que corran antes de propose_changes y apply_changes, y que el contrato de extensión quede en sldb.api o documentado como superficie estable.
