---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: AgentsKBs
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-09-16T17:05:00'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: 2026-09-23T19:30:00
---

# cached_document no firma por hash_b: un campo nuevo del modelo queda invisible para siempre

_Describe the incoming message with enough evidence to triage._

Bug de sldb: el payload de un documento es funcion de (documento, contrato del modelo),
pero el cache de nivel documento solo indexa por el documento. Si el contrato gana un campo
y el markdown no cambia, `load_runtime_documents` sigue devolviendo el payload viejo
indefinidamente: no hay forma de invalidarlo salvo tocar los .md o borrar el runtime a mano.

Asimetria entre los dos niveles de cache (`sldb/store/runtime_cache.py`):

- `cached_store` SI firma por contrato. Su docstring declara la clave como
  "hash_a, every model's hash_b, and the current operation's document leaf sweep",
  y usa `sig = signature(s_path)`.
- `cached_document` NO. Su clave es `key = (*leaf, s_name, m_name)`, donde
  `leaf = (path, hash_c[, mtime, size])`. El `hash_b` del modelo no entra.

Agravante: en `cached_document`, `disk.from_disk(...)` se consulta ANTES que el loader
(`disk.from_disk(...) or loader()`), asi que el payload viejo persistido en
`.sldb/runtime/` gana aunque el contrato haya cambiado y aunque el cache en memoria este frio.

Reproduccion con el caso real (KB knowledge_grifo, modelo ConversationStep de kb_models):

1. El modelo declara `allowed_transitions` y el markdown lo trae en el frontmatter.
2. `sldb extract kb_models.knowledge:ConversationStep <step>.md out.yaml --pythonpath ..`
   -> devuelve `allowed_transitions` completo. La extraccion directa funciona.
3. `SLDBReader(...).find("type.knowledge.step")` -> `allowed_transitions: None` en los 23 steps.
4. `.sldb/runtime/cache/extracted.json` tiene el payload con 10 claves y sin ese campo:
   fue extraido cuando el runtime resolvia los modelos contra un paquete hermano
   (`kb_agent.models.knowledge`, 11 campos) en vez del canonico (`kb_models`, 16 campos).
5. `sldb stores update` no lo corrige: reporta "0 processed" porque los .md no cambiaron.
6. `sldb stores check` dice PASS: la integridad del store no mira el contenido del payload.

Impacto aguas abajo: el exportador de flujo del runtime arma las aristas leyendo
`allowed_transitions`, asi que `GET /api/flow` devuelve `nodes: 23, edges: 0` y la UI
muestra el grafo plano, pese a que el grafo real existe (159 RelationDoc `transitions_to`
coherentes 1:1 con lo declarado en los steps). El sintoma se lee como dato faltante en la KB
cuando en realidad es un payload cacheado.

Sugerencia: incluir el `hash_b` del modelo en la clave de `cached_document` (el store ya lo
guarda por modelo, es el mismo dato que usa `signature`), y consultar `disk.from_disk` solo
cuando ese hash coincide. No lo parcheo desde AgentsKBs porque el docstring referencia
"PLAN 15 capa 6" y una "hand-edit guarantee" cuyo contexto no conozco, y porque la asimetria
entre `cached_store` y `cached_document` puede ser deliberada.

Workaround verificado del lado KB: borrar `.sldb/runtime/{cache,sections,semantic}` y
correr `sldb stores update --store .sldb --pythonpath <repo-con-kb_models>`.

## Resolution

Commit c7c5df1 "fix(store): el cache de documento firma por el hash_b del modelo (contrato), no solo por el leaf": la clave de `cached_document` en `src/sldb/store/runtime_cache.py` (y el cache en disco en `runtime_cache_disk.py`) incluye el `hash_b` del modelo, asi un contrato que gana un campo invalida el payload viejo aunque el markdown no cambie. Regresion en `tests/test_runtime_cache.py`.
