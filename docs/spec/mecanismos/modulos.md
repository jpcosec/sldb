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

Lo de afuera no es del kernel; la interfaz con lo de afuera sí (JP, 2026-11-27). git, el motor
de base de datos, tree-sitter y el disco son piezas ajenas. Lo que el kernel tiene es la forma
de hablarles.

| Módulo | Con qué habla afuera | En sldb hoy | En kimun hoy | Qué falta |
|---|---|---|---|---|
| Datos: el grafo tipado | el motor de base de datos | bloque almacén y grafo: archivos YAML, índice de aristas, networkx | `kernel.db`, `kernel.datalog` (Datalog propio), `host.datalevin` (opcional) | En sldb no hay motor. En kimun conviven tres modelos de datos. |
| Consultas y reglas | el mismo motor | lenguaje de predicados dentro del eje grafo; motor de campos en consulta | Datalog con reglas recursivas | Un solo lenguaje. Hoy hay dos en sldb y tres en kimun. |
| Árboles: leer una fuente por su estructura | tree-sitter | Markdown en superficie (markdown-it); código en codigo (tree-sitter y `ast`); datos repartidos | pod de tree-sitter; árbol propio de Markdown | Un solo árbol para todos los tipos de fuente. |
| Anclaje: huella y detección de cambio | git y el disco | anclaje, huellas de código, hashing, detección de rancidez | estados de ancla; anclas de Markdown y de Clojure; cambio por git | Está repartido en tres o cuatro lugares en cada repo. |
| Interfaz con git | git | repartida en op_almacen y op_documentos | `host.git`, puntero de commit | En sldb no existe como pieza: está mezclada con las operaciones. |

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
