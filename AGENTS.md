# AGENTS.md

Instrucciones para agentes que trabajan en este repositorio. El contrato de trabajo del desk
está en `desk/`; lo de acá es lo que un agente necesita para no detenerse.

## Merge de .sldb

Dos ramas que tocaron documentos distintos chocan igual en los índices derivados que siguen
versionados en `.sldb/`: `.sldb/core/store_index.yaml` (`store_hash`) y
`.sldb/core/models/<Modelo>.yaml` (`roster_hash`, `model_hash`, `documents_count`), y en las
listas `include` de `.sldb/store.yaml`. Los shards de `.sldb/core/documents/<Modelo>/` se
mezclan limpios (un archivo por documento) y `.sldb_cache/` no se versiona. Tres comandos:

- `sldb stores merge-driver --install`: una vez por clon. Escribe en `.gitattributes` las
  líneas `merge=sldb` de `.sldb/core/store_index.yaml`, `.sldb/core/models/*.yaml` y
  `.sldb/store.yaml`, y en `.git/config` `merge.sldb.driver = sldb stores merge-driver %O %A %B %P`
  y `merge.sldb.name`. Es idempotente. Git ejecuta el `sldb` del `PATH`: tiene que ser una
  versión que conozca `stores merge-driver`.
- `sldb stores merge-driver %O %A %B %P`: lo llama git, no se corre a mano. Un índice derivado
  conserva la versión de la rama actual (el `store_index.yaml` suma además los modelos, links y
  predicados que solo registró la otra rama); `.sldb/store.yaml` une los `include` de las dos
  ramas por modelo sin repetir rutas (y los links, modelos y predicados por nombre); cualquier
  otro archivo sale con 1 y queda como conflicto normal.
- `sldb stores rebuild-index`: después de cada merge o rebase que tocó `.sldb/`. Recalcula
  todos los hashes de los dos niveles desde los shards de `.sldb/core/documents/` y el contrato
  de cada modelo (roster, contrato, nodo del modelo, `store_hash`) y cuenta de nuevo los
  documentos. Si git dejó marcadores `<<<<<<<` en esos índices o en `.sldb/store.yaml` (un merge
  sin el driver), los repara uniendo los dos lados; un índice que no parsea y no tiene
  marcadores se toma de `HEAD`.

Procedimiento: `sldb stores merge-driver --install` (una vez), `git merge <rama>`,
`sldb stores rebuild-index`, `sldb stores check`, `git add .sldb && git commit`. Sin el driver,
cualquier comando que lea un índice con marcadores falla con
`<ruta> is a derived index that git could not merge: run `sldb stores rebuild-index` (and `sldb stores merge-driver --install` once per clone)`;
se corre ese comando y se sigue igual. Un conflicto en un shard de documento (las dos ramas
cambiaron el mismo documento) es real: se resuelve el Markdown y se corre `sldb stores update`.

Un store por repositorio: `sldb stores init` avisa (`alert: branch '<rama>' already has a store
at .sldb/`) cuando otra rama local ya tiene uno; en ese caso se mergea esa rama en vez de crear
un segundo store.
