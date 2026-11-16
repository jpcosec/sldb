---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: mepu
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-14T01:57:06'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:30:49'
---

# Un conflicto de git en los índices derivados de .sldb no se resuelve con un comando

_Describe the incoming message with enough evidence to triage._

Escrita a mano desde mepu (14-11) por pedido de JP: `deskops message send --to sldb` no funciona desde robocop porque el registro tiene rutas de otra máquina (ver la nota del registro no portable).

Visto en cada rebase de una rama de código de mepu sobre `dev`.

- **Diseño.** `.sldb/core/store_index.yaml` (`store_hash`) y `.sldb/core/models/<Modelo>.yaml` (`roster_hash`, `documents_count`, nodo del modelo) son los niveles del Merkle derivados de los shards de `documents/`:
  - `documents_hash._hash_b`: hash de `(nombre, hash_c, hash_d)` de los shards del modelo.
  - `hashing.hash_model_layer`: `hash(contract_hash, roster_hash)`.
  - `ops.cascade_store_hash`: sha256 de `[{nombre, hash del nodo}]`.
- **Efecto.** Cualquier escritura reescribe esas líneas. Dos ramas que tocan documentos distintos siempre chocan en `store_hash`, aunque los shards se mezclen limpios.
- **Hueco 1.** `sldb stores update` no tolera el conflicto en sus propios derivados. Con marcadores en `store_index.yaml` falla al leer el YAML (`could not find expected ':'`) y no recalcula. Reproducido en un worktree desechable de mepu: se meten marcadores alrededor de `store_hash:` y se corre `sldb stores update --store .sldb`.
- **Hueco 2.** `sldb stores build` necesita `.sldb/store.yaml`. Un store sin declarar (mepu) no puede usarlo.
- **Resultado.** El operador elige a mano una versión del derivado (`git checkout --ours`) antes de correr `stores update`, que es editar `.sldb` a mano.
- **Propuesta.**
  - (a) `stores update` recalcula los derivados aunque estén en conflicto o no se puedan leer; son reconstruibles desde los shards.
  - (b) Un merge driver de git, que sldb instala en `.gitattributes` para `store_index.yaml` y `models/*.yaml`, y que llama a lo mismo, para que un merge no deje conflicto.
  - (c) O no versionar los derivados y recalcularlos al leer.
