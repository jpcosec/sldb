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

| Módulo | En sldb hoy | En kimun hoy | Qué falta |
|---|---|---|---|
| Datos: el grafo tipado y su motor | bloque almacén y grafo: archivos YAML, índice de aristas, networkx | `kernel.db`, `kernel.datalog` (Datalog propio), `host.datalevin` (opcional) | En sldb no hay motor. En kimun el motor de verdad quedó fuera del kernel y conviven tres modelos de datos. |
| Consultas y reglas | lenguaje de predicados, dentro del eje grafo; motor de campos en consulta | Datalog con reglas recursivas; el lenguaje de predicados de sldb no existe | Un solo lenguaje. Hoy hay dos en sldb y tres en kimun. |
| Árboles: leer una fuente por su estructura | Markdown en superficie (markdown-it); código en codigo (tree-sitter y `ast`); datos repartidos en 63 archivos | pod de tree-sitter (Markdown, Python, Clojure); árbol propio de Markdown; datos solo como encabezado | Un solo árbol para todos los tipos de fuente. En los dos repos Markdown y código entran por caminos distintos. |
| Anclaje: huella y detección de cambio | anclaje, huellas de código, hashing, detección de rancidez en el índice | estados de ancla en el kernel; anclas de Markdown y de Clojure; cambio por git | Está repartido en tres o cuatro lugares en cada repo. |

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
| git: historia, driver de merge | repartido en op_almacen y op_documentos | `host.git`, cambios, puntero de commit |
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

## Dudas

1. **git.** JP lo listó aparte. Aquí quedó como librería, pero el anclaje lo necesita para saber
   que un archivo cambió. Si es así, es del kernel.
2. **Documentos con forma.** JP listó "AST documento (lo que ahora en sldb son modelos)" junto
   al AST de código, los dos igual de nucleares. Aquí los modelos quedaron como librería y solo
   el árbol en el kernel. Puede que el corte correcto sea otro.
3. **Operación.** En sldb es la capa más grande (unos 17.000 líneas) y no es un módulo. No está
   claro si se reparte entre las librerías o si es una librería propia.
4. **Lo que usan los otros repos.** deskops entra a `runtime.validation` 73 veces y a
   `store.io` 18; specIR usa notaciones, código, anclas y MCP; graph_ui usa la API de
   documentos y `cli.serve`. Cualquier corte tiene que conservar eso o migrarlo.
