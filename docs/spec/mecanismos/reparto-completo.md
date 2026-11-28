# Reparto de todo sldb en módulos

Fecha: 2026-11-27. Estado: **clasificación automática con Jev, sin revisar**. No se movió
código.

Los 950 archivos de los 32 ejes de sldb (45710 líneas; no incluye `cli/`, que no tiene eje),
clasificados uno por uno contra los módulos de [`modulos.md`](modulos.md): los ocho del kernel,
con su frontera, y las librerías. Mismo método que en [`reparto-cruce.md`](reparto-cruce.md).
Datos en `reparto-completo.json`. "Seguro" es confianza de 0,7 o más y ajuste de 0,6 o más.

## Cuánto es kernel

El kernel son 219 archivos y 11203 líneas: el 23% de los archivos y el 25% de las líneas.

| Módulo del kernel | Archivos | Líneas | Seguros |
|---|---|---|---|
| Puertos | 11 | 656 | 3 |
| Grafo | 108 | 5019 | 58 |
| Consulta | 38 | 2246 | 27 |
| Árboles | 19 | 1034 | 5 |
| Anclaje | 26 | 1321 | 12 |
| Proyección | 13 | 709 | 0 |
| Sostén | 1 | 120 | 0 |
| Acción | 3 | 98 | 0 |

## Las librerías

| Librería | Archivos | Líneas | Seguros |
|---|---|---|---|
| Notaciones y vistas | 193 | 7565 | 118 |
| Documentos con modelo | 85 | 4635 | 35 |
| Administración del store | 59 | 3656 | 31 |
| Código a documentos | 35 | 2032 | 15 |
| Grafo de proyecto | 40 | 1891 | 27 |
| Reglas, estados y política | 26 | 1469 | 14 |
| Código de un modelo | 23 | 1381 | 15 |
| Modelos (registro, esquema) | 32 | 1373 | 15 |
| Caras | 38 | 1363 | 8 |
| Relaciones declaradas | 23 | 1266 | 11 |
| Lotes y transacciones | 20 | 1252 | 15 |
| Varios stores y migración | 19 | 1194 | 16 |
| Base de los modelos (qué es un documento tipado) | 21 | 1004 | 8 |
| Similitud | 15 | 962 | 8 |
| Semántica | 20 | 951 | 14 |
| Análisis del grafo | 18 | 914 | 12 |
| Lo que se hace con git | 12 | 643 | 12 |
| Enlaces en el texto | 12 | 432 | 9 |
| Errores y hallazgos compartidos | 30 | 378 | 20 |
| Fachadas | 10 | 146 | 4 |

En total, 512 archivos seguros (54%) y 184 dudosos (19%).

## Qué tan módulo es cada eje de hoy

Para cada eje, a qué módulo va la mayoría de sus archivos y qué parte del eje es. Un eje con
porcentaje alto ya es casi un módulo; uno con porcentaje bajo es una mezcla.

| Eje | Archivos | Va sobre todo a | Parte | El resto va a |
|---|---|---|---|---|
| `runtime` | 1 | Base de los modelos (qué es un documento tipado) | 100% |  |
| `vistas` | 58 | Notaciones y vistas | 93% | Código a documentos 1, Relaciones declaradas 1, Documentos con modelo 1 |
| `enlaces` | 11 | Enlaces en el texto | 91% | Documentos con modelo 1 |
| `vocabulario_visual` | 131 | Notaciones y vistas | 90% | Errores y hallazgos compartidos 9, Fachadas 2, Base de los modelos (qué es un documento tipado) 1 |
| `errores` | 22 | Errores y hallazgos compartidos | 86% | Kernel: Grafo 1, Kernel: Acción 1, Fachadas 1 |
| `indice_de_aristas` | 36 | Kernel: Grafo | 83% | Relaciones declaradas 4, Kernel: Anclaje 1, Varios stores y migración 1 |
| `semantica` | 9 | Semántica | 78% | Documentos con modelo 2 |
| `reglas` | 21 | Reglas, estados y política | 76% | Semántica 5 |
| `migracion` | 4 | Varios stores y migración | 75% | Administración del store 1 |
| `persistencia` | 35 | Kernel: Grafo | 74% | Modelos (registro, esquema) 3, Lo que se hace con git 1, Lotes y transacciones 1 |
| `consulta` | 19 | Kernel: Consulta | 68% | Documentos con modelo 4, Fachadas 1, Varios stores y migración 1 |
| `vistas_compuestas` | 12 | Notaciones y vistas | 67% | Reglas, estados y política 2, Análisis del grafo 1, Varios stores y migración 1 |
| `adaptadores` | 30 | Código a documentos | 67% | Caras 4, Kernel: Árboles 2, Base de los modelos (qué es un documento tipado) 1 |
| `anclaje` | 10 | Kernel: Anclaje | 60% | Código a documentos 2, Administración del store 1, Semántica 1 |
| `mcp` | 40 | Caras | 57% | Lotes y transacciones 4, Documentos con modelo 4, Relaciones declaradas 2 |
| `op_aristas` | 73 | Grafo de proyecto | 55% | Relaciones declaradas 11, Kernel: Grafo 8, Administración del store 6 |
| `op_documentos` | 87 | Documentos con modelo | 53% | Lotes y transacciones 13, Caras 7, Kernel: Anclaje 6 |
| `lectura_de_fuentes` | 2 | Documentos con modelo | 50% | Kernel: Puertos 1 |
| `identidad_y_hash` | 2 | Documentos con modelo | 50% | Kernel: Grafo 1 |
| `federacion` | 4 | Varios stores y migración | 50% | Fachadas 1, Kernel: Grafo 1 |
| `recuperacion` | 34 | Similitud | 44% | Notaciones y vistas 6, Documentos con modelo 4, Análisis del grafo 2 |
| `superficie` | 16 | Kernel: Árboles | 44% | Kernel: Anclaje 4, Kernel: Proyección 3, Kernel: Acción 1 |
| `grafo` | 52 | Kernel: Consulta | 42% | Kernel: Grafo 16, Análisis del grafo 11, Semántica 2 |
| `op_almacen` | 97 | Administración del store | 42% | Documentos con modelo 16, Kernel: Grafo 11, Lo que se hace con git 10 |
| `op_modelos` | 55 | Código de un modelo | 42% | Modelos (registro, esquema) 22, Varios stores y migración 4, Documentos con modelo 2 |
| `render` | 15 | Kernel: Proyección | 40% | Base de los modelos (qué es un documento tipado) 4, Kernel: Árboles 2, Notaciones y vistas 2 |
| `codigo` | 26 | Código a documentos | 38% | Kernel: Puertos 6, Kernel: Árboles 6, Kernel: Grafo 2 |
| `codec` | 3 | Base de los modelos (qué es un documento tipado) | 33% | Modelos (registro, esquema) 1, Kernel: Grafo 1 |
| `bitacora` | 3 | Kernel: Grafo | 33% | Administración del store 1, Lotes y transacciones 1 |
| `contrato` | 22 | Base de los modelos (qué es un documento tipado) | 32% | Kernel: Anclaje 4, Modelos (registro, esquema) 2, Relaciones declaradas 2 |
| `representacion` | 13 | Base de los modelos (qué es un documento tipado) | 31% | Kernel: Anclaje 2, Kernel: Grafo 2, Código a documentos 1 |
| `cache` | 7 | Administración del store | 29% | Kernel: Grafo 2, Kernel: Puertos 2, Documentos con modelo 1 |

## Lo que muestra

- **El kernel es chico.** Cerca de una quinta parte del código. Lo demás es librería.
- **La librería más grande es notaciones y vistas**, con casi 7.600 líneas. Es contenido que ya
  se decidió mover a specIR.
- **Ejes que ya son un módulo** (90 % o más a un solo destino): `vistas`, `enlaces`,
  `vocabulario_visual`, y casi `errores`, `indice_de_aristas`, `semantica` y `persistencia`.
- **Ejes que son una mezcla** (menos de la mitad a un solo destino): `grafo`, `codigo`,
  `superficie`, `render`, `contrato`, `representacion`, `recuperacion`, y los ejes chicos de
  pegamento (`cache`, `codec`, `bitacora`, `identidad_y_hash`).
- **`grafo` son tres módulos**: el lenguaje de consultas (Kernel: Consulta), el almacén del grafo
  (Kernel: Grafo) y el análisis (librería).
- **`codigo` son tres cosas**: puertos hacia tree-sitter, árboles, y código a documentos.
- **Árboles y Proyección salen con poca confianza.** Los archivos que leen y escriben Markdown
  están tan atados a los modelos de documento que Jev duda entre el kernel y la base de los
  modelos. Es el mismo lugar donde el agente y Jev no coincidían. La frontera entre leer una
  fuente y leer un documento con modelo no existe en el código de hoy.
- **Sostén y Acción no existen.** Tres archivos entre los dos, y ninguno seguro.

## Límites

Los mismos de `reparto-jev.md`: Jev vio docstring, nombres públicos e imports, no el cuerpo; las
descripciones de los módulos las escribió el agente; y solo el bloque operación se cruzó con una
lectura hecha por un agente. Aquí no hay segunda opinión.
