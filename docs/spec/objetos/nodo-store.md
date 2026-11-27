---
clase: objeto
tipo: nodo
nombre: store
estado: borrador
---

# Store

## Qué es

El store es la base: el contenedor de todos los demás nodos. Reúne los modelos registrados,
los documentos que siguen a esos modelos, el DAG semántico de tags, los enlaces a otros stores
y la declaración (`store.yaml`) que dice cómo se arma todo. Hay un store por proyecto, en
`.sldb/`. Es la raíz del espacio de direcciones: todo lo demás se nombra bajo él.

## Cómo se nombra

Hoy:

- Nodo del grafo: `sldb://store` para el store local (`src/sldb/store/edge_index/node_ids.py:12`).
  Un store enlazado aparece como `sldb://store/<alias>`
  (`src/sldb/store/edge_index/store_contribution.py:23`, `federation.py:33-34`).
- En la CLI se nombra por ruta: `--store <ruta de .sldb>` (`src/sldb/cli/parsers/stores.py:30`)
  o por alias de enlace en referencias `alias:Modelo:nombre`.
- Catálogo global: `~/.sldb` registra los stores del equipo
  (`src/sldb/api/stores/store_skeleton.py:32-47`).

Con la gramática propuesta (borrador): `[store:]st/...`. El prefijo `store:` es el namespace
bajo el que viven los dos espacios. La gramática no define una dirección para el store mismo
(sin verificar: solo se leyó `docs/architecture/one-address-grammar-two-spaces.md`, decisión 2).

## Dónde se guarda

- `.sldb/store.yaml`: la declaración, que es la fuente y va en git
  (`src/sldb/api/stores/store_declaration.py:1-8`). Lleva `links`, `models`, `predicates`,
  `include`, `policy` y otras claves (`store_declaration.py:28-45`).
- `.sldb/core/`: índices derivados (`store_index.yaml`, índices de modelo, shards de
  documentos); se versionan pero se recalculan (`src/sldb/store/layout.py:15-33`).
- `.sldb_cache/`: caché, no se versiona (`layout.py:19`).

## Los cuatro verbos

| Verbo | Hoy | Evidencia | Qué significa (propuesta) |
|---|---|---|---|
| Crear | `stores init`; escribe un store vacío y lo registra en el catálogo global | `src/sldb/cli/commands/store_init.py:10-33`, `src/sldb/api/stores/init_store.py:15-27` | **Sin confirmar:** crear un store nuevo en un proyecto, con su `store.yaml` y sus índices vacíos. |
| Leer | `stores list` (solo los enlaces); `stores declare` (imprime la declaración que implica el índice); `stores check` (salud, no contenido) | `src/sldb/cli/commands/stores.py:61-70`, `src/sldb/cli/commands/stores_build.py:26-33`, `src/sldb/api/stores/store_check.py:30` | **Sin confirmar:** devolver sus atributos (declaración, política, enlaces, hashes raíz), no solo la lista de enlaces. |
| Cambiar | No existe un comando que cambie el store como nodo. Se edita `store.yaml` a mano y `stores build` rehace lo derivado; `stores declare --write` reescribe `store.yaml` desde el índice | `src/sldb/cli/parsers/stores.py:86-91`, `src/sldb/cli/commands/stores_build.py:29-31`. Buscado en `src/sldb/cli/parsers/stores.py` y `src/sldb/cli/commands/store.py:15-24` | **Sin confirmar:** cambiar la declaración (política, predicados, includes) por una operación, y que el resto se derive. |
| Borrar | No existe un comando de borrado. El único camino que elimina un store es `stores init --force`, que hace `shutil.rmtree` y lo crea vacío otra vez | `src/sldb/api/stores/init_store.py:41-46` (buscado además en `src/sldb/api/stores/`: ningún `delete_store`) | **Sin confirmar:** adentro no se borra: borrar un store es declarar que se borró, y la red queda con ese hecho. Lo que sí se puede hacer es dejar de usar su carpeta o sacarlo del catálogo global, que es afuera (corregido 2026-11-27 con los fundamentos). |

`stores add` y `stores remove` no crean ni borran un store: crean y borran el enlace a otro
store (`src/sldb/cli/commands/store_add.py:12-21`). Ese enlace es una arista `links_to`.

## Aristas que le llegan y que salen

- `has_model`: store → modelo. La crea el índice al registrar un modelo; si el modelo es
  heredado, lleva `origin_store` (`store_contribution.py:33-37`).
- `links_to`: store → store enlazado. La crea `stores add` (`src/sldb/api/stores/link_store.py:20-47`) y el índice
  la emite (`store_contribution.py:25`).
- Los tags del DAG (`semantic_parent`, `semantic_equivalent`) salen del mismo shard del store
  (`store_contribution.py:26-30`), pero cuelgan de tags, no del store.
- Hacia el store no llega ninguna arista escrita por alguien.

## Qué lo mantiene correcto

- Árbol de hashes: `store_hash` sobre los hashes de modelo
  (`src/sldb/store/hashing.py:115-120`).
- `stores check` clasifica hallazgos (`src/sldb/api/stores/store_findings.py:20,37`) y
  `stores check --apply` ejecuta lo que dice la política de `store.yaml`
  (`src/sldb/cli/parsers/stores.py:34`).
- `stores update` recalcula hashes; `stores build --check` reconstruye una copia y compara
  (`src/sldb/cli/parsers/stores.py:37-42,86-92`).
- La guarda de nombre de enlace (`src/sldb/api/stores/link_store.py:62-65`) y el rechazo de enlazar un store
  consigo mismo (`link_store.py:56-59`).

## Abierto

- Borrar un store: ¿qué pasa con los documentos Markdown que seguía? ¿Quedan en disco, como
  hoy cuando se borra un modelo con `--with-documents`, o se borran también?
- ¿Un store enlazado por otro puede borrarse mientras algún modelo suyo es heredado? Hoy
  `stores remove` del enlace lo rechaza en ese caso (`src/sldb/cli/parsers/stores.py:25`).
- ¿Cambiar el store es cambiar `store.yaml` (declarado) o también sus derivados? Hoy el
  índice y la declaración pueden divergir y hay dos comandos en sentidos opuestos
  (`declare --write` y `build`).

## Desde los fundamentos

- **Qué es.** El adentro: la red de nodos y relaciones, con su borde. Es lo único que tiene
  identidad. Los archivos del proyecto quedan afuera y se tocan por anclas.
- **Principio.** 3, "Hay un adentro y un afuera", y 4 ("el sistema actúa sobre sí mismo": lo que
  declara el store es red como lo demás).
- **Qué contradice los niveles 1 y 2:**
  - "los documentos que siguen a esos modelos" y el verbo Crear ("con su `store.yaml` y sus
    índices vacíos"): trata el store como un contenedor de documentos Markdown (h) y supone
    modelos antes que documentos (c).
  - Borrar, incluida la pregunta abierta de qué pasa con los documentos: adentro no se borra;
    los archivos de afuera no dependen del store (a).
  - "`store.yaml` ... es la fuente": lo que alguien declara (política, predicados, includes)
    vive adentro, como nodos y relaciones. Un YAML aparte es la puerta de hoy, no la fuente (f).
  - "Es la raíz del espacio de direcciones": solo los nodos y relaciones tienen identidad; las
    partes sin marcar se nombran por su dirección, que no cuelga de la raíz del store (b).
  - Abierto 3 (declaración y derivados divergen): los derivados se rehacen; lo declarado no (g).
- **Qué queda igual.** Los índices y el árbol de hashes son cálculos que se pueden borrar y
  rehacer. Los enlaces entre stores (`links_to`) son relaciones. `stores check` consulta sin
  cambiar la red (principio 8).

## Cómo se absorbe en la lógica de kimun

Lectura del agente, sin confirmar, salvo lo marcado (JP). Ver
`../decisiones/el-kernel-sigue-la-logica-de-kimun.md`.

El store no es una clase de grafos en abstracto: al final es todo Clojure (JP). El grafo y lo que lo declara son formas de Clojure, que son dato y código a la vez. Cómo se persiste no está definido.

## Fuentes

- `desk/drawer/plans/ejes-y-anillos-de-operaciones/README.md`
- `desk/drawer/plans/spec-de-producto-de-sldb/README.md`
- `docs/architecture/one-address-grammar-two-spaces.md`, `docs/addressability_model.md`
- `src/sldb/cli/parsers/stores.py`, `src/sldb/cli/commands/{stores,store,store_init,store_add,stores_build}.py`
- `src/sldb/api/stores/{init_store,store_skeleton,link_store,store_declaration,store_check,store_findings}.py`
- `src/sldb/store/{layout,hashing}.py`, `src/sldb/store/edge_index/{node_ids,store_contribution,federation}.py`
