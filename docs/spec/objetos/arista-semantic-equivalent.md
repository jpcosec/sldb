---
clase: objeto
tipo: arista
nombre: semantic_equivalent
estado: borrador
---

# `semantic_equivalent`

## Qué es

Arista entre dos tags que dice que significan lo mismo. Sirve sobre todo entre stores
enlazados: un tag local se declara equivalente a un tag global y `gse.<tag>` alcanza los
documentos de todos los stores cuyos tags mapean a él. Se declara como "este tag local mapea a
aquel tag global" (`.sldb/store.yaml:180-182`; muchos a muchos entre `semantic_tag` en
`src/sldb/models/builtin_relation_types.py:22`).

## Cómo se nombra

Hoy no tiene dirección propia. Es el par (local, global) con ids `sldb://semantic_tag/<tag>`
(`src/sldb/store/edge_index/node_ids.py:38-40`). Dos comandos la escriben con argumentos
distintos: `sldb semantic equivalent add <local> <global>`
(`src/sldb/cli/parsers/semantic.py:31-36`) y `sldb stores semantic-map <a> <b>`
(`src/sldb/cli/parsers/stores.py:61-65`).

Con la gramática propuesta (borrador): `se/<local>` y `<store>:se/<global>` nombran los
extremos. **Sin confirmar:** cómo se escribe la arista y el extremo de otro store.

## Dónde se guarda

Solo en `.sldb_cache/semantic_dag.yaml`, campo `equivalences`
(`src/sldb/store/models/semantic_d_a_g.py:7`), escrito por `save_semantic_dag`
(`src/sldb/store/io/semantic_dag.py:38-43`) en la ruta de `src/sldb/store/layout.py:48-49`.
Esa carpeta está en `.gitignore:21`. Es el mismo hallazgo que en `arista-semantic-parent.md`
y vale igual aquí: nada versionado la guarda ni la reconstruye. `sync_semantic_dag` solo
conserva las equivalencias que ya había en el archivo (`src/sldb/store/semantic_dag_sync.py:48-49`);
si se borra la caché, se pierden. No lo probé.

Inconsistencia: `semantic equivalent add` guarda una sola dirección
(`src/sldb/store/semantic.py:105-111`), mientras `stores semantic-map` guarda las dos
(`src/sldb/cli/commands/store_semantic_map.py:9-11,15-20`).

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | `sldb semantic equivalent add <local> <global>`. No exige que los tags existan. `sldb stores semantic-map <a> <b>` hace lo mismo en dos direcciones y sin pasar por la API ni refrescar el índice de aristas | `src/sldb/api/semantic/dag_writes.py:41-54`, `src/sldb/cli/commands/semantic.py:30-33`, `src/sldb/cli/commands/store_semantic_map.py:7-13` | Crear declara la equivalencia y la guarda donde git la versiona. **Sin confirmar.** |
| Leer | `sldb semantic show <tag>` (campo `equivalents`, solo las salientes del tag). `gse.<tag>` bajo `sldb legacy`. En reglas, `model_tag` la lee en las dos direcciones | `src/sldb/api/semantic/dag_reads.py:21`, `src/sldb/store/query_engine/global_semantic.py:25-50`, `src/sldb/store/graph/language/semantic_scope.py:4-6` | Una lectura simétrica: equivalente es lo mismo en cualquier sentido. **Sin confirmar.** |
| Cambiar | no existe. Busqué en `src/sldb/cli/parsers/semantic.py`, `stores.py` y `src/sldb/api/semantic/` | `src/sldb/cli/parsers/semantic.py:31-36` | **Sin confirmar:** sin atributos, cambiar es mover un extremo. |
| Borrar | no existe. Busqué `remove`/`delete` de equivalencias en `src/sldb/cli/`, `src/sldb/api/semantic/` y `src/sldb/store/semantic.py`: solo hay `add`. Hoy solo se borra editando el YAML de la caché | `src/sldb/cli/parsers/semantic.py:31-36`, `src/sldb/store/semantic.py:105-111` | Borrar quita la equivalencia en las dos direcciones. **Sin confirmar.** |

## Aristas que le llegan y que salen

Arista entre dos `semantic_tag`. La crean los dos comandos de arriba. El índice de aristas la
emite una vez por declaración (`src/sldb/store/edge_index/store_contribution.py:28-29`), y
`semantic_scope` la lee en los dos sentidos porque el DAG guarda una sola
(`src/sldb/store/graph/language/semantic_scope.py:4-6`,
`src/sldb/store/graph/backend/index_semantics.py:34`). `gse.` en cambio lee solo
local a global (`global_semantic.py:49-50`). El puente `gse.<tag>.se.{store}` lee el DAG del
otro store (`global_semantic.py:71-76`).

## Qué lo mantiene correcto

No hay validación al escribir: ni que los tags existan, ni que el global exista en otro store.
No hay chequeo de ciclos para esta relación (`src/sldb/store/edge_index/acyclic.py:13`
solo cubre `semantic_parent` y `extends`). No hay hash ni procedencia.

## Abierto

- Si la equivalencia es simétrica (se guardan dos aristas o una que se lee en ambos sentidos).
- Si un tag global tiene que existir en algún store, o puede ser solo un nombre.
- Dónde se guarda para que se versione y sobreviva a borrar la caché.
- Si `stores semantic-map` se unifica con `semantic equivalent add`.

## Fuentes

`desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`, `docs/addressability_model.md`,
`docs/architecture/derived-store-boundary.md`, `src/sldb/api/semantic/`,
`src/sldb/store/semantic.py`, `src/sldb/store/semantic_dag_sync.py`,
`src/sldb/store/query_engine/global_semantic.py`, `src/sldb/store/edge_index/store_contribution.py`,
`src/sldb/store/graph/language/semantic_scope.py`, `src/sldb/cli/commands/store_semantic_map.py`,
`src/sldb/cli/parsers/semantic.py`, `src/sldb/cli/parsers/stores.py`.
