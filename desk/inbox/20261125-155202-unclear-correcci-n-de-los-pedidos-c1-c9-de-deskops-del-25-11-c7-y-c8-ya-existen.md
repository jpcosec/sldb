---
# unclear | suggestion
kind: unclear
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-25T15:52:02'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
# why the note was acknowledged; empty when no reason was given
ack_reason: ''
# conversation thread/message the note came from, e.g. #hilo/1234
---

# Corrección de los pedidos C1-C9 de deskops del 25-11: C7 y C8 ya existen

_Describe the incoming message with enough evidence to triage._

Corrección de deskops (diagnóstico del 25-11, deskops/desk/drawer/plans/deskops-plugin-de-sldb/diagnostico.md). Los pedidos C1-C9 se mandaron sin verificar contra sldb. C7 (resolver un store por nombre) ya existe: sldb.store.catalog.catalog_store y store_links; deskops/identity.py no los usa; solo faltaría reexportar catalog_store en sldb.api y darle CLI. C8 (store corresponde al árbol) ya existe: sldb stores build --check, que el CI de deskops ya corre; solo faltaría un instalador del hook de pre-commit. C1: las aristas ya se leen de stores enlazados (edges_holding include_linked=True por defecto; deskops pasa include_linked=False en lifecycle.py:318-343); falta solo la parte de reglas (rules_of y RuleGraph.domain filtran por self.local). C5 existe en MCP (--extension), falta en el CLI. C6 y C9 existen en parte (detección como RuleDoc on_check y edges rewrite; docs create --model con payload y describe_model_fields; faltan flags por campo y default/pattern en FieldDescription). Faltan de verdad C2, C3 y C4. Se pueden cerrar C7 y C8 como mal uso de deskops.
