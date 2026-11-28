# Reparto del bloque operación: cruce de dos clasificaciones

Fecha: 2026-11-27. Estado: sin revisar por JP. No se movió código.

El bloque operación de sldb (372 archivos en siete ejes) se repartió dos veces, por separado:

- un agente leyó cada archivo y lo asignó a un módulo: [`reparto-operacion.md`](reparto-operacion.md);
- Jev, un modelo de decisiones, clasificó 355 de ellos a partir de su docstring, sus nombres
  públicos y sus imports: [`reparto-jev.md`](reparto-jev.md).

Ninguno vio el resultado del otro. Aquí se comparan.

## Cuánto coinciden

Sobre los 314 archivos que los dos nombran uno por uno:

| | Coinciden |
|---|---|
| Todos | 225 de 314 (72 %) |
| Donde Jev estaba seguro | 162 de 187 (87 %) |
| Donde Jev no estaba seguro | 63 de 127 (50 %) |

La confianza de Jev avisa bien: donde dice estar seguro, el agente llega a lo mismo casi
siempre; donde duda, es una moneda al aire. Entonces los 162 se pueden dar por ubicados y hay
que mirar a mano el resto.

## En qué están de acuerdo

- **Operación no es un módulo.** Los dos la reparten.
- **Abrir y ubicar un store son del kernel de datos.** Sostienen 60 de los 138 imports de la
  deuda de anillos. Al abrir hay que sacarle la migración y los modelos heredados, que son de
  "varios stores".
- **Anclaje** está bien delimitado: 8 de 8.
- **Aparecen módulos que no estaban en la lista:**

| Módulo nuevo | Según el agente | Según Jev |
|---|---|---|
| Referencias o grafo de proyecto: armar un grafo de un repositorio desde sus archivos, y reescribir referencias | 50 archivos | 43 |
| Administración del store: declarar, montar, revisar, diagnosticar | 34 (diagnóstico 20, declaración y montaje 14) | 43 |
| Contratos de modelo: editar el código de un modelo, borradores | 31 | dentro de "modelos" (46) |
| Escritura por lotes y transacciones, con deshacer | 14 | dentro de "documentos" |

## Dónde no coinciden

| El agente dice | Jev dice | Archivos |
|---|---|---|
| Kernel: datos | Administración del store | 9 |
| Kernel: consultas | Documentos | 6 |
| Operaciones | Kernel: datos | 4 |
| Kernel: árboles | Documentos, caras, código a documentos | 6 |

El desacuerdo se junta en un solo lugar: **la frontera entre el kernel y las librerías**. En
"consultas" coinciden en 3 de 14 archivos, y en "árboles" en 2 de 12. El agente manda al kernel
piezas que Jev ve como parte de documentos. No es un error de ninguno: es que esa frontera no
está dicha con precisión todavía.

## Lo que encontró solo el agente

- **Validar un modelo contra su texto se parte en dos.** Lo que solo usa plantilla y texto va a
  árboles, en el kernel; lo que recibe la clase del modelo va a documentos. Es la tercera
  función de la deuda (18 imports).
- **Once archivos hay que partirlos.** Siete mezclan su lógica con una llamada propia a git.
- **La interfaz con git no existe como pieza.** Son diez llamadas sueltas repartidas.
- **Tres archivos sin ningún usuario** (`api/edges/edges_blocked.py`, `api/graph/traverse.py`,
  `api/schema/field_description.py`) y ocho que solo usa una prueba. Casi todos se reexportan en
  `sldb.api`, así que pueden ser superficie pública.

## Sin resolver

1. Dónde termina el kernel en consultas y en árboles.
2. Si la escritura por lotes es el lado de escritura del kernel de datos o una librería. Cada
   pieza llama a validación, relaciones y reglas.
3. Si diagnóstico y declaración del store son un módulo o dos.
4. Si editar el código de un modelo va aparte o con modelos.
5. Qué es `api/records`: 18 archivos que ninguno de los dos pudo ubicar con claridad.

## Segunda pasada, con el kernel de ocho módulos

Después de que JP fijó el criterio del kernel (lo que si falta, sldb deja de ser sldb; módulos
con frontera), se volvió a clasificar con Jev usando los ocho módulos de `modulos.md`, cada uno
con lo que hace y lo que no hace. Se separaron además "lotes y transacciones" y "código de un
modelo", que el agente había propuesto. Datos en `reparto-jev-2.json`.

| Destino | Archivos | Líneas |
|---|---|---|
| Documentos con modelo | 64 | 3.570 |
| Administración del store | 50 | 3.294 |
| Grafo de proyecto | 40 | 1.891 |
| Modelos | 26 | 1.035 |
| Código de un modelo | 23 | 1.381 |
| Reglas, estados y política | 22 | 1.297 |
| **Kernel: Grafo** | 21 | 998 |
| Lotes y transacciones | 14 | 908 |
| Relaciones declaradas | 13 | 626 |
| **Kernel: Anclaje** | 12 | 621 |
| Lo que se hace con git | 11 | 606 |
| Varios stores y migración | 11 | 715 |
| Notaciones y vistas | 11 | 579 |
| Semántica | 7 | 338 |
| **Kernel: Proyección, Árboles, Consulta, Sostén, Acción, Puertos** | 10 entre todos | 591 |
| Caras, fachadas y otros | 20 | 763 |

Lo que cambia con la frontera dicha:

- **El kernel dentro del bloque operación baja de 58 archivos a 43**, unas 2.200 líneas de
  17.000. Casi todo lo que hay en operación es librería.
- **Lotes y transacciones sale limpio**: 14 archivos, confianza 0,85. Es un módulo.
- **Código de un modelo también**: 23 archivos.
- **Consulta, Árboles, Proyección, Sostén y Acción casi no tienen código en este bloque.** Es
  coherente: Consulta y Árboles viven en otros ejes, y Sostén y Acción no existen. De Sostén
  aparece un solo archivo, `api/edges/referrers.py` (quién se refiere a qué), y de Acción uno,
  `api/edges/apply_effects.py`, que además solo lo usa una prueba.
- **Puertos tiene un archivo**, `store/package_version.py`. Confirma que la interfaz con lo de
  afuera no existe como pieza.

Queda sin hacer: la misma clasificación sobre los otros 25 ejes, que es donde están el resto
del kernel (árboles, grafo, consulta) y las cimas.
