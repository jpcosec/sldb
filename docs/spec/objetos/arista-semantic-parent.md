---
clase: objeto
tipo: arista
nombre: semantic_parent
estado: borrador
---

# `semantic_parent`

## Qué es

Arista de un tag a su padre en el DAG semántico: "este tag es una clase de aquel". Hace que
preguntar por el padre alcance a los hijos (`se.type.knowledge` alcanza a
`type.knowledge.spec`; `model_tag("Q")` en reglas, igual). Hay dos clases: la implícita, que el
nombre con puntos ya dice, y la declarada a mano, que no sigue el nombre. Muchos a muchos: un
tag puede tener varios padres (`src/sldb/models/builtin_relation_types.py:21`).

## Cómo se nombra

Hoy no tiene dirección propia. Es el par (hijo, padre) con ids `sldb://semantic_tag/<tag>`
(`src/sldb/store/edge_index/node_ids.py:38-40`), en dirección hijo a padre
(`src/sldb/store/semantic_dag_graph.py:18-23`). Los comandos reciben los dos tags como texto:
`sldb semantic parent add <tag> <parent>` (`src/sldb/cli/parsers/semantic.py:23-28`).

Con la gramática propuesta (borrador): `se/<hijo>` y `se/<padre>` nombran los extremos.
**Sin confirmar:** cómo se escribe la arista misma.

## Dónde se guarda

- Implícita: no se escribe. `sync_semantic_dag` la deriva del nombre al reconstruir
  (`src/sldb/store/semantic_dag_sync.py:22-26`, `_prefix_edges` en `semantic_tags.py:60`).
- Declarada con `semantic parent add`: se escribe SOLO en `.sldb_cache/semantic_dag.yaml`
  (`src/sldb/store/semantic_parents.py:19-29` llama a `save_semantic_dag`;
  `src/sldb/store/io/semantic_dag.py:38-43` la escribe en `semantic_dag_path`;
  `src/sldb/store/layout.py:48-49` lo resuelve a `runtime_dir`, que es `.sldb_cache`
  según `layout.py:30-31` y `44-45`).
- `.sldb_cache/` está en `.gitignore:21`. `git check-ignore -v` confirma que
  `.sldb_cache/semantic_dag.yaml` queda ignorado.

**Hallazgo verificado en el código (no probé borrando la caché):** el padre declarado a mano
no se versiona y se pierde si se borra `.sldb_cache/` o se clona de nuevo. Razón: al reconstruir,
`sync_semantic_dag` parte de `load_semantic_dag`, que sin archivo devuelve un DAG vacío
(`src/sldb/store/io/semantic_dag.py:30-32`), y solo agrega los tags nuevos con sus prefijos
(`semantic_dag_sync.py:12-19`). Ninguna otra fuente guarda los padres: `.sldb/store.yaml`,
`.sldb/core/` y los shards de documentos no los tienen (busqué `semantic_parent` y
`semantic_dag` en `src/sldb/store/` y en `.sldb/store.yaml`). Además, el nodo se rechaza si
ningún documento o modelo lleva el padre (`semantic_parents.py:23,52-54`). Lo mismo anotó
deskops en `desk/inbox/20261124-023754-suggestion-semantica-del-store-padres-declarados-solo-en-el-cache-namespace-sin-padre-y-migracion-de-tags-en-bloque.md`.
`docs/architecture/derived-store-boundary.md:27` lista el archivo como caché regenerable, lo que
hoy es falso para los padres declarados.

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | `sldb semantic parent add <tag> <parent>`. Rechaza tag o padre desconocido, auto-padre y ciclo; devuelve "Nothing to change." si ya estaba | `src/sldb/cli/commands/semantic.py:23-28`, `src/sldb/api/semantic/dag_writes.py:19-27`, `src/sldb/store/semantic_parents.py:19-29,52-61` | Crear declara la arista y la guarda donde git la versiona. **Sin confirmar.** |
| Leer | `sldb semantic show <tag>`: padres, hijos, ancestros, descendientes. Lee el DAG de la caché. También `sldb graph cycles --relation semantic_parent` | `src/sldb/api/semantic/dag_reads.py:13-30`, `src/sldb/cli/commands/help_texts_graph.py:27` | Leer sigue igual, desde la fuente versionada. **Sin confirmar.** |
| Cambiar | no existe. Busqué en `src/sldb/cli/commands/semantic.py` y `src/sldb/api/semantic/`. Cambiar el padre es `remove` más `add` | `src/sldb/cli/parsers/semantic.py:23-28` | **Sin confirmar:** la arista no tiene atributos; cambiar es mover el extremo padre. |
| Borrar | `sldb semantic parent remove <tag> <parent>`. Rechaza quitar el padre que da el nombre; "Nothing to change." si no estaba declarado | `src/sldb/cli/commands/semantic.py:23-28`, `src/sldb/store/semantic_parents.py:32-42,64-65` | Borrar quita solo la declarada; la implícita se cambia renombrando el tag. **Sin confirmar.** |

## Aristas que le llegan y que salen

Es una arista entre dos `semantic_tag`. La crean `sync_semantic_dag` (implícitas) y
`semantic parent add` (declaradas). Después `refresh_store_edges` la pone en el índice de
aristas al instante (`src/sldb/api/semantic/dag_writes.py:57-63`,
`src/sldb/store/edge_index/store_contribution.py:26-27`). Los comandos `semantic parent` no
registran `--actor`: no hay procedencia (`dag_writes.py:23-24`).

## Qué lo mantiene correcto

- Rechazo de ciclo al escribir (`semantic_parents.py:57-61`).
- `sldb edges check` busca ciclos en `semantic_parent` (`src/sldb/store/edge_index/acyclic.py:13`).
- No hay hash ni procedencia del DAG.

## Abierto

- Dónde se guarda el padre declarado para que se versione (por ejemplo en `.sldb/core`, el
  mismo lugar que un shard de documento, o en `store.yaml`).
- Si `ns:valor` tiene como padre implícito su namespace, o si `parent add` puede crear el padre
  que nadie lleva todavía.
- Qué hace borrar una arista implícita (hoy se rechaza).

## Cómo se absorbe en la lógica de kimun

Lectura del agente, sin confirmar, salvo lo marcado (JP). Ver
`../decisiones/el-kernel-sigue-la-logica-de-kimun.md`.

Es una relación tipada (herencia) entre nodos de significado.

## Fuentes

`desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`, `docs/architecture/tags.md`,
`docs/architecture/derived-store-boundary.md`, `src/sldb/store/semantic_parents.py`,
`src/sldb/store/semantic_dag_sync.py`, `src/sldb/store/io/semantic_dag.py`,
`src/sldb/store/layout.py`, `src/sldb/api/semantic/`, `src/sldb/cli/commands/semantic.py`,
`src/sldb/cli/parsers/semantic.py`, `src/sldb/store/edge_index/`, `.gitignore`.
