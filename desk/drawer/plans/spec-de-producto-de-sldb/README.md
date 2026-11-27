# Spec de producto de sldb

Fecha: 2026-11-26. Repo dueño: sldb. Estado: **borrador 0, esqueleto**. JP dijo el 2026-11-26 que
hay que volver al spec antes de seguir con la taxonomía, los ADR y los planes, y que ese spec es
un documento que no existía. Este es su primer esqueleto: junta lo que JP ya fijó y deja a la
vista lo que falta. No autoriza ejecutar nada.

Cada punto dice de quién es: **JP** (con fecha) o **lectura** (del agente, sin confirmar).

Qué tiene que decir un spec de producto de sldb y no dice ningún documento de hoy: qué
operaciones hay sobre qué objetos. Los `.spec.yaml` del repo describen cómo está construido
sldb y se ponen al día con este (lectura).

## 0. Forma del spec (JP, 2026-11-26)

El spec no es un solo documento: son muchos documentos chicos en el store, enlazados, y una wiki
que se genera de ellos. Este archivo queda como portada mientras tanto.

Clases de página con que se parte ("está bien para partir", JP): objeto, operación, mecanismo,
plugin, decisión y abierto. Los anillos y los ejes no son páginas: son vistas sobre las
operaciones.

JP pidió mirar specIR para ordenarlo. Leído el 2026-11-26 (`IR` en `53343b8`); specIR ya tiene
un modelo para describir un sistema de software, con reglas que revisan que las capas calcen:

| Clase del spec | Pieza de specIR que existe | Qué da |
|---|---|---|
| Operación | `DomainOperationDoc`: "una capacidad del dominio, independiente de cómo se invoca (UI, CLI, job, agente)" | la operación separada de sus caras |
| Cara de una operación | `ApiOperationDoc` y `HandlerDoc`, con `handled_by` y `executes`; reglas `api-operation-is-handled` y `handler-executes-a-domain-operation` | "toda cara tiene su operación" ya es una regla escrita |
| Para quién y cómo se prueba | `CapabilityDoc` con `audience`, `accepted_by` hacia un test; regla `capability-has-an-acceptance-test` | cada página atada a su test |
| Objeto | `DomainEntityDoc`, con `persisted_in` | la cosa y dónde se guarda |
| Reglas y estados de lo descrito | `PolicyDoc` con `governed_by`; `StateDoc` con `transitions` | |
| Orden del repo | `PieceDoc` (un paquete) con `depends_on` | los anillos como regla sobre dependencias |
| De quién es cada afirmación | `origen` (observado, derivado, inferido, declarado) y `verificacion` en cada nodo y arista | lo que aquí se anota a mano como "JP" o "lectura" |
| Lo que hay hoy en el código | extractores (`extract/python_cli.py`, `routes.py`, `sql.py`) | poblar "lo observado" desde el código en vez de una tabla a mano |

Lo que specIR no tiene: el anillo de una operación, una clase para mecanismo, las páginas de
decisión y de abierto, y la proyección a wiki. Sin verificar: que los extractores corran sobre
sldb. Un cruce a resolver: `StateDoc` y `transitions` de specIR describen los estados de un
sistema modelado; la máquina de estados genérica del punto 6 es de sldb.

## 1. Qué es sldb

- Lo que el repo ya declara (`contracts/identity.toml`, README): un sistema para representar
  cualquier cosa con estructura derivable de forma determinista (documentos, código, interfaces
  de programa) como documentos direccionables, consultables, anclados a su origen y reversibles
  a su superficie. El núcleo no distingue Markdown de código.
- sldb no guarda las fuentes: guarda lo que sigue de ellas (qué marcó, sus hashes, sus anclajes
  y sus relaciones). Un documento puede seguirse entero, a medias o en un par de campos; por eso
  compara hashes y no archivos (JP, 2026-11-27).
- Corrección: hasta el 2026-11-27 este punto decía "un grafo de documentos Markdown". Estaba mal
  y varias preguntas mal hechas a JP salieron de ahí.
- **Lo genérico de una base va en sldb; deskops, specIR y todo lo demás son plugins** (JP,
  2026-11-26). Un mecanismo que cualquier store puede usar es de sldb. Un plugin declara su
  contenido encima.

## 2. Los objetos

Nodos: store, modelo, campo de modelo, tipo de relación, documento, sección, tag, ancla. Un valor
dentro de un documento no es un nodo: es el documento más una ruta.

Aristas: las estructurales (salen de crear o borrar nodos, no se escriben) y las escritas
(`links_to`, `semantic_parent`, `semantic_equivalent`, `tagged_as`, `references`, `contains`,
`composes` y los tipos autorados).

Detalle y estado actual en `../ejes-y-anillos-de-operaciones/README.md`.

## 3. Cómo se nombra una cosa

- Dos espacios de direcciones, estructural y semántico, bajo el namespace del store e
  independientes de dónde vive la cosa en disco (JP, 2026-11-25).
- Un modelo se califica con el store dueño, y una arista puede terminar en una sección o en un
  valor (JP, confirmado el 2026-11-26).
- La gramática concreta es borrador: `../direccion-unica-estructural-y-semantica/`.

## 4. Las operaciones

- Todo tipo de nodo y todo tipo de arista admite crear, leer, cambiar y borrar (JP, 2026-11-25 y
  26).
- Hay operaciones de otro nivel, sobre el store entero (JP).
- Enlazar dos nodos es crear una arista (lectura; JP pidió las aristas dentro del eje).
- Hay una sola lógica de navegación: una dirección, seguir aristas, filtrar con el lenguaje único
  de predicados (JP).
- Las operaciones se cargan como documentos del store, con la regla de que toda cara tenga su
  operación. El inventario de 142 operaciones de `367eff435` es el insumo (JP, 2026-11-26).

## 5. Los anillos

Cada anillo usa solo los de adentro (lectura que JP dio por buena el 2026-11-26).

| Anillo | Qué es |
|---|---|
| 0 | El grafo: crear, leer, cambiar y borrar nodos y aristas; la navegación |
| 1 | Lo que mantiene el grafo correcto |
| 2 | El store entero |
| 3 | Lo compuesto |
| afuera | Las caras (CLI, MCP, HTTP); no agregan operaciones |

Qué va en cada anillo no está cerrado.

## 5b. No perder datos

Regla de JP (2026-11-26): nunca se pierden datos salvo que se pida explícito, y todo se
explicita. Primer caso: borrar algo que tiene dependientes no borra en cascada ni se rechaza; se
borra y los dependientes quedan marcados como sin soporte. Borrar también los dependientes hay
que pedirlo.

## 6. La máquina de estados

- Es un documento declarado, con un grafo de sus estados (JP, 2026-11-26). Es de sldb, por la
  regla del punto 1.
- Hoy no existe: hay transiciones sueltas (`RelationDoc` con condición, `sets` y `terminal`) y
  `edges_holding` lee el grafo "como máquina de estados", pero ningún documento dice qué estados
  tiene una máquina, cuál es el inicial ni a qué modelo aplica.
- Lectura: un modelo dice qué máquina lo gobierna y en qué campo guarda el estado; "tomar una
  transición" es la operación de la máquina sobre un documento (verifica, aplica los efectos y
  escribe), del anillo 1.
- Toda transición pertenece a una máquina; las sueltas se migran (JP, 2026-11-26). Y es regla
  para todo lo que hoy existe fuera: lo que vive suelto afuera de un mecanismo declarado de sldb
  entra a ese mecanismo, no convive con él.

## 7. La automatización, por etapas

Etapas separadas, en este orden (JP, 2026-11-26):

1. Hooks, y el árbol.
2. Alertas.
3. Daemon. Además de avisar a una interfaz abierta, tiene que poder activar un agente.
4. Entre el daemon y el agente pueden ir jev, RAG o evaluaciones deterministas del estado.
5. Agente bibliotecario o de desk: conciliaciones y automantención de los desks.

Lectura: "el árbol" es el árbol de hashes; cada etapa funciona sin las siguientes; las etapas 1
a 3 son de sldb. El agente es de un plugin (JP lo confirmó).

Hoy existe parte de 1 y 2 a pedido: `stores check` clasifica hallazgos y la política de
`store.yaml` dice qué se hace con cada uno. No corren solas.

## 8. El motor

- El motor es dueño de todo el grafo (JP, 2026-11-26).
- Cuál motor: abierto. El criterio de JP es preparar la llegada de kimun. kimun no declara hoy
  ningún motor Datalog en sus dependencias.

## 8b. Fuentes, hooks, persistencia y motor (JP, 2026-11-27)

- sldb puede llegar a escribir código, no solo Markdown: es el caso fácil de lo que ya hace. El
  spec vale para Markdown y para código.
- No todo documento necesita modelo (kimun; sldb ya lo considera con el grafo de proyecto y la
  lectura de código). Lectura: el anillo 0 trabaja con fuentes como árbol, con o sin modelo;
  validar contra el modelo y correr reglas es anillo 1 siempre, también al escribir.
- Hooks: algo propuesto antes y nunca cumplido es que un valor hasheado puede venir de ejecutar
  algo y anclar su resultado. kimun lo nombra como ancla de evaluación (`14 §7`, motores `sci`,
  `shell:CMD`, `llm:`; no implementado allá). Sin diseñar aquí.
- Persistencia y caché hay que verlas ahora: en el corto plazo sldb tiene que poder correr sobre
  Postgres.
- Para el grafo conviene adoptar un motor externo de inmediato, sin esperar. Esto reabre P1; la
  propuesta que había (Cozo con sqlite, `desk/drawer/plans/grafo-datalog-daemon/`) es anterior
  al requisito de Postgres.

## 9. Los plugins

- deskops y specIR son plugins (JP, 2026-11-25).
- Falta un plugin de compilación de contexto, estado y "harness" o "superharness"; el agente de
  la etapa 5 es de ahí (JP, 2026-11-26). Sin especificar todavía.
- El patrón de plugins se arregla en este spec y después va a ADR (JP, 2026-11-26). Un ADR no
  lleva cosas sin probar.
- Para después: hay que crear una forma de incorporar hacia adentro, a sldb, los mecanismos que
  nacen en los plugins (JP, 2026-11-26). Va en la definición de plugin. Sin diseñar.

## 10. Lo que falta escribir

- Qué va en cada anillo.
- Qué significa cada verbo en los nodos y aristas derivados (borrar un tag, cambiar una sección).
- La máquina de estados: su modelo, cómo se ata a un modelo, qué pasa con las transiciones
  sueltas que ya existen.
- Cada etapa de la automatización: qué recibe, qué entrega y qué la dispara.
- El plugin de contexto, estado y harness.
- Un solo vocabulario para el tipo de enlace (hoy hay tres) y qué pasa con los enlaces del texto,
  que no entran al índice de aristas.
- Dónde caen evaluar, proponer/aplicar/deshacer y convertir texto sin store.
- El espacio semántico, dirección contra consulta, los tres grafos y la federación.

## 11. Lo que espera a este spec

La taxonomía de comandos (JP la revisa a fondo antes), el ADR del patrón de plugins, el orden
entre el cambio de ids y el almacén del motor, el servidor fastmcp, y el orden del repo por
anillos.
