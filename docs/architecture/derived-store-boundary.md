# Qué del store se versiona y qué se regenera

Estado (2026-11-04): implementado. Decisión del dueño (2026-10-29): el pasado del árbol del
store se pregunta a git, y eso exige que los shards de `core/` estén versionados. El store se
parte físicamente en dos directorios hermanos: `.sldb/` (operacional, versionado entero) y
`.sldb_cache/` (regenerable, ignorado), y sldb declara la caché en el `.gitignore` de la raíz
para que la separación sea correcta por construcción. Reemplaza la frontera del 2026-10-19,
que ignoraba `.sldb/core/` y `.sldb/runtime/` con declaración; la medición de entonces (2.816
archivos bajo `.sldb/`, 66dac43b tocando 5.045 por un hash) sigue siendo el costo asumido:
un cambio de un campo derivado reescribe muchos shards, y ese ruido es lo que git versiona.

## 1. El layout

```
<raíz>/                      el directorio padre de .sldb/ (precisión 11 de la tarea)
  .gitignore                 contiene la línea `.sldb_cache/`
  .sldb/                     versionado entero
    store.yaml               la declaración (modelos, links, predicados, generadores, include, policy)
    core/
      store_index.yaml       raíz del árbol Merkle (store_hash) y registro de modelos
      models/<Model>.yaml    nodo de cada modelo (model_hash, contract_hash, roster)
      documents/<Model>/<doc>.yaml   una hoja por documento (source_hash, content_hash)
  .sldb_cache/               ignorado; `sldb stores build` lo regenera
    edges.yaml, edges/       índice de aristas (el shard del store, uno por modelo, uno por documento)
    sections/<Model>/<doc>.yaml      secciones de cada documento
    semantic/<Model>/<doc>.yaml      contribución semántica de cada documento
    semantic_dag.yaml        padres y equivalencias declaradas de los tags
    graphs/                  grafos generados (`selfdoc python-sync` escribe python-source.graph.json)
    corpus/                  índice del corpus del servidor
    locks/store.lock         lock del store
```

`src/sldb/store/layout.py` resuelve las rutas: `cache_dir(store)` es `store.parent / ".sldb_cache"`,
hermano del directorio del store cualquiera sea su nombre (un store abierto como
`kb/.sldb_custom` cachea en `kb/.sldb_cache`); `runtime_dir` es el mismo directorio bajo el
nombre que siempre usaron los escritores de índices derivados. Nada de `.sldb/` se escribe en
una lectura: las cachés de proceso (payloads extraídos, modelos construidos) viven en
`$XDG_CACHE_HOME/sldb` (`sldb.store.user_cache`), fuera del repo.

La clave `sections_index` del índice de cada modelo conserva su forma vieja
(`.sldb/runtime/sections/<Model>.yaml`): es una clave, no un archivo, y `SectionsIndexIO` lee
de ella el store y el nombre del modelo. Cambiarla reescribiría `core/` de todos los stores sin
ganar nada.

## 2. Qué es fuente, qué es índice y qué es caché

**Fuente:** los Markdown escritos o editados por personas y agentes (`docs/`, `desk/`, `ledger/`,
`sldb/relation_types/`, `knowledge/commands/`, `knowledge/surfaces/`), el código y los modelos
Python, y `.sldb/store.yaml`, que declara qué modelos se registran, qué stores se enlazan, qué
predicados existen, qué generadores corren, qué archivo se trackea con qué modelo y la policy
de hallazgos.

**Índice versionado (`.sldb/core/`):** se deriva de la fuente y `stores build` lo reconstruye,
pero se versiona porque su historia es la historia del árbol: `git log` sobre un shard de
`documents/` dice quién movió el hash de ese documento y cuándo, y `sldb docs history <doc>`
lo lee de ahí. Es lo que antes pedía el journal ([journal-authority.md](journal-authority.md)).

**Caché (`.sldb_cache/`):** se deriva del índice y de la fuente, no guarda nada que no se pueda
recomputar y no se versiona. Borrarla entera y correr `sldb stores build` (o `edges rebuild`)
la trae de vuelta; `tests/store/test_runtime_wiped.py` lo prueba.

`knowledge/symbols/` sigue siendo derivado (lo escribe `selfdoc python-sync`) y la declaración
lo lista en `derived`, con `.sldb/core/` y `.sldb_cache/` que siempre lo son para la copia de
`stores build --check`.

## 3. Los comandos

- `sldb stores init` crea `.sldb/` y agrega la línea `.sldb_cache/` al `.gitignore` de la raíz si
  ninguna línea ya la nombra (idempotente); nunca borra ni reordena otra línea.
- `sldb stores build` lee `.sldb/store.yaml`, registra modelos y links, corre los generadores,
  trackea cada `include` y reconstruye los índices y la caché. Es idempotente. En un clon limpio
  (que trae `.sldb/` entero), `stores build` seguido de `stores check` da PASS. `stores build
  --check` construye una copia de los fuentes sin `.sldb/core/`, `.sldb_cache/` ni lo declarado
  en `derived`, y falla si esa copia no pasa `stores check`, si algo trackeado no está declarado
  o si trackea distinto que el store local.
- `sldb stores check` emite dos hallazgos sobre el `.gitignore` (`src/sldb/core/finding.py`),
  evaluados con `git check-ignore --no-index` desde la raíz del repo:
  - error `stores/core_ignored` (exit 1) si git ignora `.sldb/core/` o `.sldb/store.yaml`: el
    pasado del store se lee de git, así que nada de `.sldb/` puede estar ignorado;
  - alert `stores/cache_not_ignored` (exit 0) si `.sldb_cache/` no está ignorada.
  Fuera de un work tree de git no hay policy y no hay hallazgos.
- `sldb stores migrate-layout [--store PATH] [--force]` lleva un store del layout anterior al
  actual: mueve el contenido de `.sldb/runtime/` a `.sldb_cache/` (edges, sections, semantic,
  graphs, locks), se niega si `.sldb_cache/` existe con contenido salvo `--force` (que la borra
  primero), borra `.sldb/runtime/journal/` sin archivarlo, elimina `.sldb/runtime/` y reescribe
  el `.gitignore` de la raíz: quita solo las líneas cuyo patrón, sin barras inicial ni final,
  es `.sldb/core` o `.sldb/runtime`, pone `.sldb_cache/` donde estaba la primera de ellas (al
  final si no había ninguna) y conserva las demás líneas y comentarios tal cual. Sin
  `.sldb/runtime/` no hay nada que mover y solo corrige el `.gitignore`, así que correrlo dos
  veces es inocuo. Sin `--store` descubre el store como los demás comandos `stores`.

## 4. Adoptar el layout en un repo que versionaba lo viejo

1. `sldb stores migrate-layout --store .sldb`.
2. `git add .sldb .gitignore` (entra `core/` entero, salen las líneas viejas del `.gitignore`).
3. `sldb stores check`: sin `stores/core_ignored` ni `stores/cache_not_ignored`.
4. En el CI, `stores build --check` sigue siendo la verificación; la copia que construye ya no
   necesita que `.sldb/core/` esté ignorado, porque lo excluye por sí misma.

Los cinco stores de SLDB_1 (deskops, sldb, spec2viz, pron, scion) se migran con este
procedimiento al integrar la tarea; pron construye su `.sldb/` con `make world` y sigue sin
versionarlo por decisión del coordinador (ver sección 5).

## 5. Lo que sigue bloqueando un clon limpio

- 15 modelos (48 documentos del desk) se heredan del store de deskops por el link
  `../deskops/.sldb`. Un clon solo de sldb no los resuelve: el CI necesita deskops al lado,
  con la misma ruta relativa.
- 3 modelos de pron (AnchorDoc, ProjectionDoc, MoveDoc, con documentos en `ledger/`) viven en
  el store de pron y sldb los hereda por `../pron/.sldb` (106ed3c0). pron no versiona su
  `.sldb/` y lo construye con su propio CLI (`make world`); el CI de sldb corre `make world`
  en el checkout hermano de pron antes de reconstruir el de sldb. Un generador de `store.yaml`
  solo corre subcomandos de sldb, a propósito.
