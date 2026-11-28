# Mecanismo: de lo implementado a librerías

Clase de página: mecanismo. Fecha: 2026-11-27. Estado: **propuesta del agente, sin revisar**.
Cruza lo que hay en el código de sldb (ya con el refactor por anillos fusionado en `main`, PR
#5) con lo que hay en el código de kimun, para ver cuáles son los módulos de verdad y cuáles
pasarían a ser librerías. Sale de dos lecturas del código hechas el 2026-11-27; lo que dice de
cada repo está medido con sus herramientas o con búsquedas, no ejecutado.

Criterio de corte, de JP (kimun, sesión del 2026-11-27): en el kernel van el motor de datos
tipo Datomic, la interfaz con tree-sitter, el anclaje y el sistema de datos; sobre el kernel,
todo es plugin. Aquí "plugin" se llama librería.

## Lo que muestran los dos códigos

**sldb.** Los 32 ejes del contrato no son 32 módulos. El grafo de imports se comporta como
seis bloques:

| Bloque | Ejes que lo forman | Cómo se comporta |
|---|---|---|
| texto | superficie, representacion, render, contrato, runtime, errores | Una unidad: 36 dependencias internas y 1 hacia afuera. |
| código | codigo | Ya está separado: no depende de nadie. Lee Python, TypeScript y SQL. |
| almacén y grafo | persistencia, consulta, cache, codec, identidad_y_hash, indice_de_aristas, semantica, grafo, federacion, migracion, bitacora, lectura_de_fuentes | Casi una unidad. |
| operación | op_documentos, op_modelos, op_aristas, op_almacen, anclaje, reglas, vistas_compuestas | No es un módulo: es la capa que compone todo. 401 dependencias hacia el almacén y 163 hacia texto. |
| notación | vocabulario_visual, vistas | Casi separada. Es lo que consume specIR. |
| cimas | mcp, recuperacion, adaptadores, enlaces | Nadie las importa. Se pueden sacar hoy. |

Casi toda la deuda de anillos (138 imports) son tres funciones puestas en un anillo más alto
que quienes las usan: abrir un store (48), validar un modelo contra su texto (18) y ubicar un
store (12).

**kimun.** Los anillos se hacen cumplir por script y son cinco: kernel, host, superficie
Markdown y motor de sesión, superficie y plugins, línea de comandos. El kernel tiene un Datalog
propio; Datalevin, tree-sitter y el anclaje están fuera del kernel, en los anillos 1 y 3.

## Los módulos, lado a lado

### Kernel

Criterio (JP, 2026-11-27): kernel es todo aquello sin lo cual sldb deja de ser sldb. Y no es un
atado de cosas: son módulos con fronteras bien definidas.

Para decidir qué entra se usa la prueba de los fundamentos: un módulo es del kernel si al
quitarlo deja de cumplirse alguno de los ocho principios. Para que la frontera sea clara, cada
módulo dice qué hace, qué entrega, de qué otros módulos del kernel depende, con qué habla
afuera, y qué no hace.

| Módulo | Qué hace | Entrega | Depende de | Habla afuera con | No hace | Principio |
|---|---|---|---|---|---|---|
| **Puertos** | Es el único lugar que habla con lo que no es sldb. | Una interfaz por cada cosa de afuera. | nada | git, el motor de base de datos, tree-sitter, el disco | No decide nada. No conoce nodos ni árboles. | 3 |
| **Grafo** | Guarda nodos, relaciones y hechos, con su identidad, su autor y su origen, dentro de un store. Es solo significado. | Crear, leer, cambiar y declarar retirado. | Puertos | el motor de base de datos | No conoce fuentes ni árboles. No pone nombres. | 1, 6 |
| **Árboles** | Lee una fuente como árbol de partes y la vuelve a escribir igual. Vale para todo tipo de fuente. Un árbol es grafo: nodos unidos por relaciones de estructura (qué contiene a qué, en qué orden), y además puede llevar otro significado. | Un árbol hecho de nodos y relaciones; la dirección de cada parte; la huella de una parte. | Puertos, Grafo | tree-sitter, el disco | No conoce modelos ni documentos. | 2 |
| **Consulta** | Un solo lenguaje para preguntar y filtrar sobre el grafo. | Respuestas que dicen hasta dónde miraron. Evaluar una condición. | Grafo | el motor de base de datos | No escribe. No conoce modelos ni documentos. | 8 |
| **Anclaje** | Ata un nodo a una parte de una fuente, recuerda qué vio y nota que cambió. | Anclar, comprobar, anclar de nuevo. | Árboles, Grafo, Puertos | git, el disco | No decide qué significa el cambio ni a quién afecta. | 3 |
| **Proyección** | Saca nodos hacia afuera con reglas dichas, y escribe un cambio sobre la versión que se vio. | Proyectar; editar; decir qué conserva una proyección. | Árboles, Grafo, Anclaje | el disco | No decide si un cambio se permite. | 2 |
| **Sostén** | Baja un cambio por las relaciones que lo llevan y dice qué quedó firme, movido o suelto. | Qué depende de qué; el estado de un nodo o de una zona. | Grafo, Consulta, Anclaje | nada | No arregla nada. No decide si algo es cierto. | 7 |
| **Acción** | Hace algo cuando algo ocurre, con una condición y con autor. | Sin definir (`abiertos/hooks.md`). | Consulta, Sostén | lo que cada acción declare | Sin definir. | 4 |

Las dependencias van en un solo sentido: Puertos; Grafo; Consulta y Árboles; Anclaje;
Proyección; Sostén; Acción.

La diferencia entre Grafo y Árboles (JP, 2026-11-27): en el grafo hay solo significado; en un
árbol se mezclan el significado de la estructura y otros significados. Por eso Árboles usa a
Grafo y queda en un nivel intermedio, no al lado.

Lo que la prueba deja fuera del kernel, aunque hoy esté mezclado con él:

- **Modelos de documento.** El principio 5 dice que para entrar no se exige un tipo.
- **Reglas y máquinas de estado** como cosas declaradas. El kernel entrega evaluar una
  condición (Consulta) y hacer algo (Acción); qué reglas hay lo declara cada proyecto.
- **Lotes, transacciones y deshacer.** Son una forma de usar Proyección, no un principio.
- **Administrar un store, el grafo de proyecto, las etiquetas, varios stores, las notaciones.**

Estado en los dos códigos:

| Módulo | En sldb hoy | En kimun hoy |
|---|---|---|
| Puertos | no existe como pieza: git son diez llamadas sueltas; el disco se toca desde unas 90 piezas | `host`: hash, archivos, git, tree-sitter, Datalevin |
| Árboles | Markdown en superficie; código en codigo; datos repartidos. Dos caminos. | pod de tree-sitter y árbol propio de Markdown. Dos caminos. |
| Grafo | archivos YAML, índice de aristas, networkx | `kernel.db`; conviven tres modelos de datos |
| Consulta | dos lenguajes | tres |
| Anclaje | repartido en cuatro lugares | repartido en cuatro lugares |
| Proyección | render reversible, solo para documentos con modelo | render canónico de Markdown; recetas |
| Sostén | no existe | no existe |
| Acción | no existe | evaluación aislada de declaraciones; nada más |

### El kernel con dos criterios

Criterio de JP (2026-11-27): juntar quién importa a quién con qué no debería cambiar nunca, o
casi nunca.

El primero se mide. El segundo es una decisión: sale de los principios. Medido sobre el reparto
de [`reparto-completo.md`](reparto-completo.md):

- **Lo usan**: imports que llegan al módulo desde otros módulos.
- **Usa**: imports que salen del módulo hacia otros.
- **Inestabilidad**: usa dividido por la suma de los dos. Cerca de 0, todos dependen de él y él
  de casi nadie: es base. Cerca de 1, depende de todos y nadie de él: es punta.
- **Cambios por archivo**: commits que tocaron cada archivo desde agosto de 2026, en promedio.

| Módulo | Archivos | Lo usan | Usa | Inestabilidad | Cambios por archivo |
|---|---|---|---|---|---|
| Errores y hallazgos compartidos | 30 | 53 | 1 | 0.02 | 1.2 |
| Kernel: Puertos | 11 | 53 | 3 | 0.05 | 2.4 |
| Kernel: Grafo | 108 | 348 | 59 | 0.14 | 2.4 |
| Base de los modelos | 21 | 71 | 23 | 0.24 | 2.2 |
| Modelos (registro, esquema) | 32 | 101 | 53 | 0.34 | 2.6 |
| Semántica | 20 | 33 | 25 | 0.43 | 2.4 |
| Fachadas | 10 | 45 | 35 | 0.44 | 2.5 |
| Kernel: Consulta | 38 | 48 | 38 | 0.44 | 2.6 |
| Kernel: Acción | 3 | 5 | 4 | 0.44 | 0.7 |
| Lo que se hace con git | 12 | 9 | 9 | 0.50 | 1.4 |
| Kernel: Árboles | 19 | 29 | 30 | 0.51 | 1.5 |
| Kernel: Anclaje | 26 | 33 | 35 | 0.51 | 1.4 |
| Kernel: Proyección | 13 | 16 | 18 | 0.53 | 2.2 |
| Varios stores y migración | 19 | 40 | 48 | 0.55 | 2.6 |
| Caras | 38 | 29 | 38 | 0.57 | 1.8 |
| Relaciones declaradas | 23 | 29 | 41 | 0.59 | 1.8 |
| Análisis del grafo | 18 | 14 | 20 | 0.59 | 1.9 |
| Documentos con modelo | 85 | 114 | 200 | 0.64 | 2.6 |
| Reglas, estados y política | 26 | 30 | 71 | 0.70 | 2.4 |
| Grafo de proyecto | 40 | 10 | 25 | 0.71 | 1.3 |
| Lotes y transacciones | 20 | 19 | 52 | 0.73 | 2.4 |
| Enlaces en el texto | 12 | 3 | 10 | 0.77 | 1.8 |
| Notaciones y vistas | 193 | 29 | 104 | 0.78 | 1.2 |
| Similitud | 15 | 3 | 11 | 0.79 | 1.3 |
| Administración del store | 59 | 44 | 181 | 0.80 | 3.9 |
| Código a documentos | 35 | 10 | 47 | 0.82 | 1.6 |
| Kernel: Sostén | 1 | 2 | 10 | 0.83 | 3.0 |
| Código de un modelo | 23 | 1 | 30 | 0.97 | 2.6 |

Cruzando los dos criterios salen cuatro grupos:

| | Todos lo importan (base) | Pocos lo importan |
|---|---|---|
| **No debería cambiar** (sale de un principio) | **Kernel que ya está en su lugar**: Puertos, Grafo, y los errores y hallazgos compartidos. | **Kernel que hay que sacar o construir**: Árboles, Anclaje y Proyección están a media altura porque dependen de los modelos; Consulta también; Sostén y Acción no existen. |
| **Puede cambiar** (lo declara cada proyecto) | **El centro equivocado de hoy**: la base de los modelos y el registro de modelos. Todos dependen de ellos, y por los principios no deberían ser base. | **Librerías**: todo lo demás. |

Lo que esto corrige de la tabla de más arriba:

- **Errores y hallazgos compartidos es del kernel.** Es lo más estable del repo (0,02) y lo
  usa todo. No estaba en la lista de ocho. Es el vocabulario con que cualquier módulo dice que
  algo falló o que algo cambió.
- **Puertos y Grafo se confirman** con el número: 0,05 y 0,14.
- **El kernel de hoy no es el kernel que queremos.** En el código, el centro son los modelos de
  documento: `structured_doc`, la validación y la referencia a un modelo. Árboles, Anclaje y
  Proyección, que por principio van al centro, hoy importan tanto como los importan (0,5).
  Mover el kernel no es mover carpetas: es invertir esa dependencia, que leer una fuente deje
  de necesitar un modelo.
- **Los cambios por archivo casi no distinguen**: todo se mueve entre 1 y 4. Sirven para ver
  archivos sueltos. `store/query.py` es del kernel y cambió 17 veces: es el cargador de
  documentos mezclado con la carga desde otros stores. Un archivo del kernel que cambia mucho
  es una frontera mal puesta.
- **Administración del store y documentos con modelo son los que más cambian y los que más
  usan a otros.** Son punta, como corresponde a una librería.

Límite: estos números describen el reparto que hizo Jev, con sus dudas. Para los módulos con
pocos archivos seguros (Árboles, Proyección) el número es una pista, no una medida.

### Librerías

| Librería | En sldb hoy | En kimun hoy |
|---|---|---|
| Documentos con forma: modelos, plantillas, ida y vuelta | bloque texto | `surface.models`, render de Markdown |
| Operaciones sobre documentos, modelos y relaciones | bloque operación | `surface` (docs, fields, sections), autoría |
| Semántica: etiquetas y su jerarquía | semantica, y etiquetas dentro de reglas | `surface.semantic`, tipado |
| Reglas, estados y política de escritura | reglas, transiciones, política y puerta de escritura | no existe |
| Análisis del grafo: caminos, ciclos, centralidad | parte de grafo | `graph` |
| Enlaces y transclusión | enlaces | `surface.links` |
| Notaciones y vistas | bloque notación | no existe |
| Código a documentos | adaptadores | no existe |
| Similitud | recuperacion | no existe |
| Varios stores y migración | federacion, migracion | no existe |
| Lo que se hace con git encima de la interfaz: driver de merge, historia de un documento | repartido en op_almacen y op_documentos | cambios, puntero de commit |
| Declaraciones evaluadas y recetas | no existe | `declare`, `reading`, `generate` |

### Caras

| Cara | En sldb hoy | En kimun hoy |
|---|---|---|
| Línea de comandos | `cli/`, 223 archivos, fuera del mapa de ejes | 19 grupos de comandos |
| MCP | mcp | `surface.mcp` |
| HTTP | `cli/serve` | `surface.http` |
| REPL | no existe | `cli.repl`, `engine.session` |

## Lo que no existe en ninguno de los dos

- Máquinas de estado y condicionales como mecanismo declarado. sldb tiene transiciones sueltas.
- Hooks que ejecuten algo y anclen el resultado.
- Juntar y sintetizar. kimun reúne proposiciones con el mismo identificador; nada más.
- Certeza y propagación de un cambio por las relaciones.

## Resuelto con JP (2026-11-27)

- **git** no es del kernel; la interfaz con git sí. El mismo criterio vale para el motor de
  base de datos, tree-sitter y el disco.
- **Modelos de documento**: el corte de arriba (el árbol en el kernel, los modelos como
  librería) está bien pensando en kimun.
- **Operación** no es un módulo: es algo que pasa sobre los módulos, y por eso hoy está
  repartida. Al repartir cada trozo de código donde corresponde puede aparecer algún módulo más.
- **Lo que usan los otros repos** se conserva o se migra.

## Lo que sigue

Repartir el bloque operación de sldb: tomar cada archivo de `op_documentos`, `op_modelos`,
`op_aristas`, `op_almacen`, `anclaje`, `reglas` y `vistas_compuestas` y decir a qué módulo de
esta página pertenece. Lo que no calce en ninguno es candidato a módulo nuevo.
