# Versionado y colaboración en sldb serve

Investigación previa al protocolo de edición concurrente (modelo ProseMirror collab):
una autoridad central que acepta/rebasa según versión. Este documento responde con
evidencia del código actual; no implementa el protocolo.

## 0. Estado del transporte hoy (2026-09-21, rama main)

- Lectura: `GET /health /schema /graph /document?id= /document/ir?id= /edges/* /graph/* /models /lint /kgdb/snapshot`.
- Escritura (todos bajo `SAVE_LOCK`, optimistic-lock por payload): `POST /save` (single + batch),
  `POST /docs/create|track|untrack`.
- `/save` usa control optimista por `expected`: el cliente manda el payload que cree que hay
  (`save_plan.update_target`: `existing.payload != expected -> 409`). Detecta el conflicto pero
  no lo resuelve: el segundo cliente debe recargar y rehacer su edición.

## 1. Qué hay hoy (inventario con evidencia)

### Hashes del store (`src/sldb/store/hashing.py`, `store/ops.py`, `store/documents_hash.py`)

| hash | firma | donde vive | cuando rota |
|---|---|---|---|
| `hash_a` | root de todo el store: SHA-256 de `[{name, hash_b}]` ordenado (`hash_models_layer`) | store index | cualquier write en cualquier modelo |
| `hash_b` | por modelo: SHA-256 de `[{name, hash_c, hash_d}]` ordenado (`hash_document_entries`, order-independent) | models index | cualquier write de cualquier doc del modelo |
| `hash_c` | contenido: SHA-256 del texto markdown (`hash_text`) | documento shard | cualquier reescritura del archivo |
| `hash_d` | campos: SHA-256 del JSON del payload extraído, claves ordenadas (`hash_payload`/`hash_fields`) | documento shard | solo cuando cambian los campos |

`hash_d` es **función pura del payload**: `hash_payload(codec.extract(model, markdown))`.
Dos prints del mismo payload → mismo `hash_d`; un cambio de campo lo rota siempre. Se calcula en
`ops.track_document` y en `payload_save_steps.write_rendered_document`, y el journal registra
`hash_d_before`/`hash_d_after` en cada write (`payload_save._save_and_record`).

### Journal (`src/sldb/store/journal/*`, `src/sldb/api/journal.py`)

- Append-only, un YAML por write en `.sldb/runtime/journal/` (`append_entry`, bajo `journal_lock`).
- Cada entrada (`JournalEntry`): `operation`, `address` (`Model:doc`), `field`, `previous_value`,
  `new_value`, `hash_c_before/after`, `hash_d_before/after`, `hash_a_before/after`, `actor`,
  `timestamp`, y cadena por `previous_hash -> entry_hash` (SHA-256 de todos los campos).
- Lectura: `read_entries` (newest-first, filtros `limit/since/address`). Verificación:
  `verify_chain` camina la cadena y reporta dónde rompe (`entry_hash mismatch` /
  `previous_hash mismatch`). **No hay nada más**: no hay replay, no hay checkpoints, no hay
  inversión, no hay expurgo, y `SLDB_JOURNAL_OFF=1` puede desactivar el append por completo.

### Pasos de una escritura (`payload_save_steps.py` + `payload_save.py`)

`save_document_payload`: render (`render_checked`: render + roundtrip obligatorio) →
`write_rendered_document` (escribe `.md`, recalcula `hash_c`/`hash_d` al shard) →
`save_document_indexes` (bajo `store_lock`: shard, `hash_b`, semantic/sections/edges rebuild,
`cascade_hash_a`) → `record(...)` al journal con todo el before/after.

`payload_diff.changed_paths`/`field_label` ya nombran los campos cambiados entre dos payloads
(eso alimenta `entry.field` del journal). `payload_path_writing` ya tiene `deep_get/deep_set/deep_delete`.

## 2. Respuestas con evidencia

### (a) ¿Existe un «número de versión por documento» que sirva como «la versión que el cliente tiene»?

**No existe ningún contador ni versión entera por documento.** No hay campo version en
`DocumentEntry`, ni en `RuntimeDocument`, ni en el documento shard.

**El token que cumple el rol sin inventar nada es `hash_d`** (la firma de los campos):

- Es una función pura del payload → dos clientes con el mismo payload tienen la misma versión;
  el `expected` de hoy (comparación de payloads) coincide exactamente con comparar `hash_d`.
- Ya vive en el documento shard, ya rota en cada write, ya está _before/after_ en el journal.
- El cliente no necesita calcularlo: el servidor lo expone y el cliente lo devuelve tal cual.
- `hash_c` también sirve (firma del contenido) pero es más débil: depende del markdown como bytea,
  no de los campos; un re-render con otro template lo rota sin cambio semántico. `hash_d` es la
  firma semántica y la que alinea con la semántica actual de `/save`.

### (b) ¿El journal permite INVERTIR una escritura o solo auditarla?

**Hoy solo audita.** Evidencia:

- `verify_chain` solo valida la cadena; `read_entries` solo lista. No existe
  función de replay ni de `apply` inverso.
- Para `save_document_payload` la entrada **sí** trae `previous_value` (el payload completo
  anterior) y `hash_d_before`; un single-step undo es *posible a mano* (re-save de
  `previous_value`), pero nada lo ejecuta.
- Para `create_document`/`track_document_file`/`untrack_document` **no alcanza**: `create` y
  `track` no registran payload previo, `untrack` registra solo hashes before (el contenido del
  shard borrado no está en el journal; solo sobrevive el `.md` en disco).
- El journal es opcional (`SLDB_JOURNAL_OFF=1`): no puede ser fuente de verdad del estado.

Conclusión: el journal es **log de auditoría** (quién, qué, antes/después, encadenado y
verificable); habilita undo de un solo paso solo para saves completos, reconstruyendo
manualmente desde `previous_value`, pero no reconstruye estados arbitrarios del store.

### (c) ¿Qué falta para que `/save` acepte `{doc, base_version, changes}`?

Ya existe casi todo; faltan tres piezas pequeñas en el transporte:

1. **Leer la versión actual del doc en el handler de save**: `doc_hashes(store_path, model, doc)`
   (shard) da `hash_d` barato — de hecho hoy se podría comparar `base_version` contra el
   `payload` ya cargado por `load_runtime_documents`. Necesita: comparar
   `base_version != current_hash_d` y en ese caso responder 409 **con el doc completo actual**
   (`serialize_document` + `version`), que ya existe tras esta ronda.
2. **Aplicar `changes` como parches de campos**: el transporte puede resolver `changes`
   = lista de `{op: set|delete, path, value}` contra el payload base del cliente usando
   `deep_set`/`deep_delete`, y luego escribir con `save_document_payload` (render+roundtrip
   ya garantizado). El `field` del journal ya se deduce con `payload_diff`.
3. **Responder la versión resultante**: `hash_d_after` del shard (o del journal del write),
   para que el cliente rebase sin recargar. Hoy `/save` responde `{ok, doc}` sin versión.

Nada del motor del store cambia: sigue siendo `save_document_payload` + journal. El modo
actual `{doc, payload}` (sin `base_version`) debe seguir funcionando (compatibilidad).

## 3. Implementado en esta ronda (solo aditivo)

- `sldb.api.documents.serialize_document` (contrato compartido) ahora emite
  `"version": <hash_d del documento>` — leído del shard vía `api.journal.doc_hashes`.
  Única clave nueva; shape existente intacta.
- Como consecuencia, la versión aparece en:
  - `GET /graph` → cada documento trae `version`.
  - `POST /docs/create|track` (doc recién escrito) y `POST /docs/untrack`
    (versión capturada antes de borrar el shard; bug de orden detectado y corregido por test).
- `GET /document` / `GET /document/ir` **no** incluyen `version`: su envelope lo serializa
  `_flat()` en `src/sldb/cli/serve/document_routes.py`, archivo de otro agente en curso
  (fuera de mi alcance). El cliente del protocolo la toma de `/graph` o de la respuesta de
  los writes; pendiente de coordinar con el dueño de esa ruta.
- Tests: `tests/test_serve.py` +25 (lifecycle completo con versión, rotación de `version`
  tras un `/save`, contratos de error 400/404/409/422).

## 4. Propuesta concreta de protocolo (vuelta siguiente)

```jsonc
// Cliente -> servidor
POST /save
{ "doc": "atom-x",
  "base_version": "<hash_d que el cliente tiene>",
  "changes": [ {"op": "set", "path": "title", "value": "..."},
               {"op": "delete", "path": "obsolete" } ] }

// Servidor, si base_version == hash_d actual del doc (acepta)
200 { "ok": true, "doc": { "...": "...", "version": "<hash_d_after>" } }

// Servidor, si difiere (rebasa)
409 { "ok": false, "error": "Conflicto. Recarga sobre la versión vigente.",
      "doc": { "id": ..., "model_name": ..., "path": ..., "version": "<hash_d actual>",
               "payload": { ... }, "semantic_tags": [...] } }
```

Reglas propuestas:

- El cliente **nunca mergea solo**: ante 409 muestra el payload vigente (va en el cuerpo del
  409) y la UI decide rebasar manualmente (o re-aplicar sus cambios encima y reintentar con la
  nueva `base_version`).
- `changes` se resuelve contra el payload **base del cliente** (no contra el del servidor):
  evita dependencia de orden de llegada; el servidor valida el resultado final con el modelo.
- Tolerancia de reloj nula (no hay timestamps): el `base_version` ES el token de orden.
- Modo legacy `{doc, payload}` sin `base_version` se mantiene (equivalente a `changes=[]`
  con `expected=payload` actual).
- `hash_c` no se usa para el conflicto; queda para detectar ediciones *fuera de banda* del
  `.md` (cambio de hash_c sin cambio de hash_d) en un futuro aviso, no bloqueo.

Trabajo pendiente detectado (fuera de alcance): decidir con el dueño de `document_routes.py`
si el envelope de `/document` debe emitir `version` para que un solo endpoint alimente al
cliente; y que `/save` devuelva la versión resultante (la vuelta siguiente lo necesita).

## 5. Validación real

- `python3 -m pytest tests/test_serve.py -q` → **25 passed**.
- `python3 -m pytest tests/ -q` → **4 failed, 952 passed**; los 4 fallos son **pre-existentes**
  a esta ronda (idénticos a la baseline anterior): `selfdoc/test_preflight.py::test_invalid_existing_document_prevents_any_sync`,
  `test_clean_code_rules[sldb/selfdoc/python_relation_registry.py]`,
  `test_clean_code_rules[sldb/cli/commands/selfdoc.py]`, `test_cli_v2::test_find_supports_physical_and_semantic`.
- Clean-code gate sobre los archivos tocados: OK.
- curl real contra `AgentsKBs/knowledge_psp` (servidor propio en `:8311`, código nuevo;
  el de `:8310` corre un snapshot anterior):
  - `GET /graph` → 168 documentos, cada uno con `version` (ej.
    `atom-antonia-aplicacion -> 272e83a3…c1258ac`).
  - `GET /document?id=atom-antonia-bienvenida` → envelope `{id, model_name, path, payload, semantic_tags, ir}`
    **sin** `version` (ruta de otro agente, ver §3).