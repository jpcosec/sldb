# Ejes y anillos de las operaciones de sldb

Fecha: 2026-11-26. Repo dueño: sldb. Estado: **registro de una revisión en curso con JP**. No es
una decisión cerrada ni un plan de ejecución. Cada parte dice de quién es: lo que fijó JP, lo
que es lectura del agente que JP dio por buena, y lo que es lectura del agente sin confirmar.

## De dónde sale

El 2026-11-25 se quiso pasar la CLI y `sldb serve` a fastmcp
(`docs/architecture/one-command-taxonomy-served-by-fastmcp.md`). Eso topó con que los grupos de
la CLI están mal armados. JP pidió no decidir los grupos todavía: primero entender el modelo y
ortogonalizar, y de ahí sale solo cómo ordenar. Regla de JP para esta etapa: no se ejecuta
nada; sí se documenta y se crean y mejoran tareas.

## El modelo, en lo que importa acá

El store es un grafo. Medido en el store de sldb el 2026-11-25: 39.125 nodos y 222.233 aristas.

| Familia | Tipos de nodo |
|---|---|
| Contenedor | store |
| Esquema | modelo, campo de modelo, tipo de relación |
| Contenido | documento, sección |
| Vocabulario | tag, ancla |

Un valor dentro de un documento no es un nodo: es el documento más una ruta en sus campos.

Las aristas son de dos clases. Las estructurales (`has_model`, `has_field`, `has_document`,
`has_section`) salen de crear o borrar nodos y no se escriben. Las demás las escribe alguien:
`links_to` entre stores, `semantic_parent` y `semantic_equivalent` entre tags, `tagged_as`,
`references`, `contains`, `composes` y los tipos autorados (`implements` y otros).

Hay dos formas de nombrar una cosa, las dos bajo el namespace del store e independientes de
dónde vive en disco (JP, 2026-11-25): estructural y semántica. La gramática propuesta está en
`../direccion-unica-estructural-y-semantica/` y es borrador.

## Los ejes (JP, 2026-11-25 y 26)

1. **Todo tipo de nodo y todo tipo de arista admite crear, leer, cambiar y borrar.**
2. **Hay operaciones de otro nivel**, sobre el store entero: levantar, poner al día lo derivado,
   revisar la salud, migrar.
3. **Enlazar dos nodos** era un caso especial en la primera formulación. Con las aristas dentro
   del eje 1 es crear una arista, y el tipo de relación decide dónde se guarda. (Lectura del
   agente; JP fue quien pidió agregar las aristas al eje 1.)
4. **Hay una sola lógica de navegación**: partir de una dirección, seguir aristas y filtrar con
   el lenguaje único de predicados (`docs/architecture/rules-language.md`).

### Cómo está hoy contra el eje 1

Nodos:

| Nodo | Crear | Leer | Cambiar | Borrar |
|---|---|---|---|---|
| Store | `stores init` | `stores list`, `declare` | — | — |
| Modelo | `models create`, `add` | `models list`, `show` | borrador (`fields`, `template`, `metadata`) | `models remove` |
| Campo de modelo | `models fields add` | `fields show models/…` | — | `models fields remove` |
| Documento | `docs create`, `track` | `docs show`, `list`, `exists` | `docs update`, `replace`, `move` | `docs delete`, `untrack` |
| Valor en un documento | `fields create` | `fields show` | `fields update`, `append`, `clean` | `fields remove` |
| Sección | — | `sections show` | — | — |
| Tag | implícito | `semantic show`, `tags tree` | — | — |
| Tipo de relación, ancla | como documento | como documento | como documento | como documento |

Aristas:

| Arista | Crear | Leer | Cambiar | Borrar |
|---|---|---|---|---|
| Autorada (`references`, `implements`, …) | `RelationDoc`, campo de referencia, `assert_edge` (MCP) | `edges show`, `referrers`, `graph neighborhood` | `edges rewrite` | `retract_edge` (MCP), borrar el `RelationDoc` |
| `links_to` | `stores add` | `stores list` | — | `stores remove` |
| `semantic_parent` | `semantic parent add` | `semantic show` | — | `semantic parent remove` |
| `semantic_equivalent` | `semantic equivalent add` | `semantic show` | — | — |
| `tagged_as` | poner el tag en el documento | `tags`, `find` | — | quitar el tag |
| `composes`, `contains` | atributo del modelo | `edges show` | — | atributo del modelo |
| Estructurales | no se escriben | navegación | — | — |

Lo que se ve:

- Faltan celdas: borrar un store; cambiar un campo de modelo; crear, cambiar y borrar una
  sección; crear y borrar un tag; borrar una equivalencia semántica.
- El mismo verbo tiene varios nombres: crear es `init`, `create`, `add`, `track` y `record`.
- Quien llama tiene que saber por qué puerta se escribe cada cosa (el Markdown, el código
  Python del modelo, `store.yaml`, la caché del DAG semántico).
- Falta definir qué significa cada verbo en un nodo derivado, por ejemplo si borrar un tag lo
  quita de todo lo que lo lleva.

### Cómo está hoy contra el eje 4

Más de doce entradas hacen lo mismo con otra sintaxis: `legacy ls/get/glob`, `find`, `explore`,
`docs select`, `fields query`, `sections find`, `graph neighborhood/path/query`,
`semantic show`, `tags tree`, `edges show`, `edges referrers` y `ast show`.

## Los anillos (lectura del agente; JP la dio por buena el 2026-11-26)

Anillos concéntricos. Cada uno usa solo los de adentro.

| Anillo | Qué es | Qué entra |
|---|---|---|
| 0 | El grafo | crear, leer, cambiar y borrar nodos y aristas; la navegación |
| 1 | Lo que mantiene el grafo correcto | validar contra el modelo, reglas y transiciones, hashes y detección de mutaciones, anclas, procedencia, política, historia y deshacer, derivar y refrescar |
| 2 | El store entero | levantar, revisar la salud, migrar |
| 3 | Lo compuesto | vistas, notaciones, composición de texto, segmentos, cobertura, exportar, lectura de código, grafo de proyecto, selfdoc |
| afuera | Las caras | CLI, MCP, HTTP; no agregan operaciones |

Qué va en cada anillo no está cerrado: la tabla es la primera asignación.

Lo que esto explicaría del desorden de la CLI: sus grupos mezclan anillos (`stores` tiene `init`,
`add` y `check`) y el anillo 1 no tiene verbos propios (está repartido entre `stores check`,
`anchors check`, `edges check`, `rules check`, `tags check`, `models check`, `lint` y
`docs recover`).

## Lo implementado que no tiene lugar en la CLI (pedido por JP el 2026-11-26)

Revisado en los documentos de `docs/architecture/`, en los paquetes de `src/sldb` y en la ayuda
de los comandos. No se corrió cada comando.

### Composición

| Mecanismo | Dónde se declara | Qué produce | Comando |
|---|---|---|---|
| Transclusión `![[doc]]`, `![[doc#Sección]]` | en el texto | texto expandido | `docs compose`, `legacy compose` |
| `__compositions__` | en el modelo | aristas `composes` y piezas con su origen | ninguno propio; se ve en `serve` (`/document/segments`) |
| `__containment__` | en el modelo | aristas `contains` | ninguno propio |

Sin verificar: si `docs compose` resuelve también `__compositions__`. Por
`src/sldb/links/composer.py` solo expande `![[…]]`.

### Enlaces entre documentos

- En el texto: `[[destino]]` y `[predicado:: [[destino]]]`. Los revisan `docs recover` y `lint`,
  y los reescribe `move`. No entran al índice de aristas: solo `links`, `docs batch` y el lint
  de `serve` los leen.
- Menciones: las captura el grafo de proyecto. `edges referrers` y `rewrite` las juntan con las
  del índice.
- Hay tres vocabularios para el tipo de enlace: `predicates` del store (enlaces del texto),
  `RelationTypeDoc`, y los atributos del modelo (`__references__`, `__containment__`).
- `tools/check_axes.py --units` marca `links` como "capacidad sin superficie: lo necesitan 0".

### Hashing y mutaciones

- Árbol de hashes: `store_hash`; `model_hash` (de `roster_hash` y `contract_hash`); por
  documento `source_hash`, `content_hash` y un hash por campo. No se encontró hash por sección.
- `stores check` recorre el árbol y clasifica (`data-mutation`, `contract-mutation`,
  `contract-moved`, `roster-stale`, `rewrite-loss`, `structural-noise` y otros).
- `stores check --apply` ejecuta lo que la política de `store.yaml` responde a cada hallazgo.
- Alrededor: `stores update`, `rebuild-index`, `migrate-hashes`, los documentos marcados sucios
  y la guarda contra sobrescritura con pérdida.

### Anclajes al origen

- `AnchorDoc`: apunta a algo del store; resuelve y no guarda lo que vio.
- Ancla a código: `code:<ruta>::<nombre>` con huellas de firma, forma, docstring y cuerpo;
  `anchors record`, `anchors check [--record]`.
- Ancla a documento: `doc:Modelo:nombre@sha256:<hash>`, por `__doc_anchors__` o por el `from:`
  de la procedencia; estados intacta, cambiada, perdida.
- Segmentos: cada valor de un documento con su posición exacta en el texto original. Solo en la
  API y en `serve`.

Lectura del agente, sin confirmar: un ancla es una arista que recuerda el hash de su destino,
y entonces anclar es un modo de enlazar y no un grupo aparte.

### Otras ocho

1. Procedencia y autoridad: el bloque `sldb:` de cada documento (`by`, `at`, `via`,
   `authority`, `from`). La autoridad decide si una mutación es error o alerta.
2. Política del store: qué se hace ante cada hallazgo.
3. Selectores: `docs select` por referencia, prefijo, glob, familia de modelo y predicado.
4. Lectura de código: `sldb.code` (Python, TypeScript, SQL). La usan anclas, selfdoc y `explore`.
5. Grafo de proyecto: archivos que el store no modela (`graph project …`).
6. Cobertura y matching: `api/matching`. Sin comando de CLI visto; sale por `serve`.
7. Salidas del store: `semantic-export`, `semantic-map`, `graph snapshot save/load`.
8. Edición de texto y de ubicación: `docs replace` y `move`.

## Lo que sigue abierto

- Qué va en cada anillo, módulo por módulo.
- Dónde caen evaluar (reglas, transiciones, correr una vista), el modo de escritura (proponer,
  aplicar, deshacer), convertir texto sin store (`extract`, `render`, `validate`) y el análisis
  del grafo completo.
- Qué significa cada verbo en los nodos y aristas derivados.
- Los temas de la revisión que no se han tocado: el espacio semántico, dirección contra
  consulta, los tres grafos (aristas, proyecto, DAG semántico), federación, y qué piden los
  consumidores.
- JP propuso el 2026-11-26 usar estos mismos anillos y ejes para ordenar el repo. Planificar
  ese refactor es una tarea aparte del desk.

## Qué depende de esto

- La taxonomía de comandos y el servidor fastmcp.
- El plan `direccion-unica-estructural-y-semantica` (borrador).
- El patrón de plugins (`sala/2026-11-25-planificacion/patron-de-plugins.md`, fuera de este
  repo), en lo que toca al nombre de una operación y a la CLI.
- El orden del repo.
