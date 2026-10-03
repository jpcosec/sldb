# Lo que falta diseñar

Hasta acá hay diagnóstico (`00`), plan (`01`), identidad (`02`, `03`), ejes (`04`),
grafo (`05`) y unidades (`06`). Cuatro puertas construidas.

Esto es el inventario de lo que **no** está diseñado, con lo que cada cosa
desbloquea. Empiezo por el hallazgo que cambia las prioridades.

---

## El hallazgo: hay consumidores reales

El diagnóstico trató S4 (anticipación) como un problema interno: «336
definiciones públicas sin frontera». Eso subestimaba el asunto.

**Cuatro proyectos del ecosistema ya dependen de `sldb`**, y uno de ellos importa
rutas internas profundas:

| consumidor | imports profundos | por la superficie |
|---|---|---|
| **deskops** | **101** | 11 |
| kgdb | 14 | 8 |
| spec2viz | 6 | 0 |
| hum-scrapper | 0 | 7 |
| ontology | 0 | 1 |

A dónde llegan los 101 de deskops:

```
37  runtime.validation       ← extract_model_data
15  store.io
 9  store.layout
 9  api.documents
 5  core.exceptions
 4  cli.model_utils
 4  cli.main                 ← la interfaz, importada como biblioteca
 3  store.resolver
```

### Por qué esto cambia todo

**No hay superficie pública: hay 586 archivos que son API de hecho.** Cualquier
reorganización de unidades rompe deskops, y nada lo detectaría hasta que alguien
lo ejecute.

Y peor: `cli.main` importado como biblioteca significa que la capa de transporte
—la que declaré «no debe contener lógica que un programa necesite»— contiene
lógica que un programa necesita.

**Consecuencia para el plan**: la Fase 4 (superficie pública) deja de ser cuarta.
Es la primera, porque sin ella ninguna de las otras se puede ejecutar sin romper
a cuatro proyectos.

---

## Lo que falta, por orden de lo que desbloquea

### 1 · El contrato de superficie — bloquea todo lo demás

**Qué diseñar**: qué puede importar un consumidor, y qué es interno.

Hoy la respuesta es «todo», y por eso cualquier cambio interno es potencialmente
incompatible. La evidencia la dan los propios consumidores: los 101 imports de
deskops **son** la superficie real, les guste a ambos o no.

Tres decisiones concretas:

| | |
|---|---|
| `extract_model_data` | 37 usos externos. Es superficie, viva donde viva |
| `store.io`, `store.layout` | 24 usos. ¿Superficie, o deskops está mal acoplado? |
| `cli.main` | 4 usos. Importar la interfaz como biblioteca es un defecto de ambos lados |

**La puerta**: captura el conjunto de nombres públicos; si un cambio lo altera sin
registrarlo, rechaza. Ya la describí en la Fase 4 y no la construí.

**Lo que desbloquea**: separar unidades sin romper a nadie.

### 2 · La auditoría por unidad — bloquea la viabilidad

Las cinco unidades fallan la misma prueba:

```
deuda  función `auditoria` ausente en 5 de 5 unidades
```

`tests/` tiene 3 carpetas para 24 ejes y 26 archivos sueltos. `tests/core/` <!-- gone -->
no existe, y `representacion` —la idea central del sistema— no tiene prueba directa.

**Qué diseñar**: `tests/<unidad>/`, con el criterio de que **corra sola y pase**
sin cargar las otras unidades.

Eso es verificable y hoy es imposible: las pruebas no están agrupadas por unidad.

**Lo que desbloquea**: que una unidad sea viable. Sin verificación propia, una
unidad no absorbe su variedad — cualquier cambio en ella se verifica desde afuera.

### 3 · La regulación por unidad — bloquea la gobernanza

```
deuda  función `regulacion` ausente en 5 de 5 unidades
```

Las tres reglas mecanizadas recorren `src/` entero. Es coherente —sin unidades
declaradas no hay a qué atribuirle una regla— pero ahora las unidades existen en
el contrato.

**Qué diseñar**: qué regla aplica a qué unidad. Ejemplos del propio mapa:

| unidad | regla propia plausible |
|---|---|
| núcleo | no importa persistencia (ya es puerta) |
| grafo | no importa nada de `sldb` (hoy: 4 aristas) |
| adaptadores | no escribe; solo deriva |
| recuperación | no depende de ninguna biblioteca vectorial |

**Lo que desbloquea**: que cada unidad tenga una frontera que rechace, no solo
una descripción.

### 4 · Los 32 alfileres — bloquea la separación física

6 aristas de peso 1 cierran el nudo del núcleo. 26 de peso ≤2 el de operación.

**Qué diseñar**: nada. Están identificadas con archivo y línea. Es trabajo, no
diseño, y el precedente está medido: en la Fase 0 una arista de peso 1 costaba 46
módulos.

Lo que sí hay que decidir: **si el nudo del núcleo se parte o se declara
indivisible**. Las cinco aristas pesadas apuntan a `representacion`; las seis de
peso 1 cierran el ciclo. Partirlo es posible; que convenga es otra pregunta.

### 5 · Las 19 reglas sin mecanismo — bloquea S3

`standards.md` enuncia 22 reglas, 3 tienen prueba, y declara tres herramientas
«for enforcement» que no están instaladas.

**Qué diseñar**: la clasificación. Antes de instalar nada, decidir para cada regla
si es mecanizable, mecanizable-con-trabajo, o no mecanizable.

El tercer grupo es el importante: una regla de proceso que exige juicio **se
queda, marcada**. Enunciarla junto a las otras hace que todas parezcan igual de
firmes.

### 6 · El corte real — bloquea que lo anterior sirva

Aquí está el defecto más barato de arreglar y el más caro de ignorar:

**Las cuatro puertas que construí no corren en el integrador.**

```
$ grep -c "check.sh\|check_layers\|check_axes\|check_identity" .github/workflows/ci.yml
0
```

Existen, funcionan, encontraron defectos reales — y no gobiernan nada. Son
exactamente lo que el diagnóstico llamó «estándares sin mecanismo», un nivel más
arriba.

Y además:

| | estado |
|---|---|
| protección de rama | no hay — 28 merges de 317 commits |
| gancho pre-commit | no hay |
| CODEOWNERS | no hay |
| `selfdoc check` | **en rojo**, preexistente |

**Qué diseñar**: casi nada. Agregar `bash tools/check.sh` al integrador es una
línea. Lo que hay que decidir es el orden: poner `selfdoc check` en verde primero,
porque un integrador con una puerta permanentemente roja entrena a ignorarlo.

---

## Lo que no está en el plan y debería

Tres cosas que aparecieron al mapear y no tienen fase asignada.

### El contrato de recursión

`06` dibujó R0 → R1 y dejó R2 como pregunta. Falta decidir **si la recursión baja
más**, y el criterio no puede ser el tamaño: es si la unidad candidata absorbe su
propia variedad.

Para `adaptadores` la pregunta es concreta: ¿`python-ast` y `argparse` son dos
unidades, o dos implementaciones de una? Si mañana se agrega un adaptador de otro
lenguaje, ¿se repara dentro de `adaptadores` o hay que tocar el núcleo?

Eso es diseño, no trabajo, y no está hecho.

### Los dos lenguajes de consulta

| | operadores |
|---|---|
| `query_engine` | `=` `!=` `<=` `>=` |
| `graph/language` | `eq` `ne` `lt` `gt` `contains` `starts_with` `is_null` `is_not_null` |

Dos vocabularios para filtrar por campo, en dos unidades distintas. Si
`persistencia` y `grafo` se separan, cada una se lleva su lenguaje y la
divergencia se vuelve permanente.

**Qué diseñar**: un solo lenguaje de condiciones, y en qué unidad vive. Probable
respuesta: en el núcleo, porque ambas lo necesitan y ninguna lo posee.

### La superficie autorada única

`MarkdownASTHandler` es la única implementación de `BaseASTHandler` tras 317
commits, mientras hay tres adaptadores derivados.

**Qué decidir** —y es una decisión, no un hallazgo—: o la abstracción es para
superficies derivadas y Markdown es la única autorada **por diseño**, o falta una
segunda y la capacidad está sin verificar.

Por la regla de variedad, una capacidad sin segundo caso es hipótesis. Declararlo
cierra la pregunta sin trabajo; dejarlo abierto la deja envejeciendo.

---

## El orden

Actualizado tras cerrar las dudas (`09-DUDAS-CERRADAS.md`):

| | qué | tipo | desbloquea |
|---|---|---|---|
| ~~**1**~~ | ~~puertas al integrador~~ | **hecho** | — |
| **2** | contrato de superficie — y **promover** lo que los consumidores ya usan | **diseño** | separar sin romper 2 consumidores |
| **3** | operación de lectura de índices | trabajo | que `store/io` vuelva a ser interno |
| **4** | `tests/<unidad>/` | trabajo | viabilidad de las 5 unidades |
| **5** | reglas por unidad | **diseño** | gobernanza de cada frontera |
| **6** | **`layout_version` en el almacén** | **diseño** | que `persistencia` absorba su variedad |
| **7** | los 32 alfileres + el corte de 4 del núcleo | trabajo | separación física |
| **8** | clasificar las 22 reglas | **diseño** | S3 |
| **9** | lenguaje de consulta único | **diseño** | separar persistencia de grafo |
| **10** | decidir el congelamiento | **decisión** | que la identidad sea decidible |
| **11** | decidir la superficie autorada | **decisión** | cerrar una hipótesis |
| **12** | reparar deskops y kgdb | trabajo | al final, como se decidió |

Cambios respecto de la primera versión:

- **el paso 1 está hecho**: `bash tools/check.sh --fast` corre en el integrador
- **se agregó el 6**: `persistencia` no absorbe cambios de formato porque no hay
  versionado. Lo destapó la duda 5 y no estaba en ninguna fase
- **se agregó el 3**: la operación de lectura que falta, que hace innecesario
  exponer `store/io`
- **el contrato de recursión salió**: la duda 4 lo resolvió. R2 existe en
  `adaptadores` y está declarado
- **«4 consumidores» → «2»**: la duda 3 midió que solo deskops y kgdb están
  acoplados; los otros tres usan la superficie estable

Cinco de doce son diseño, cuatro son trabajo, dos son decisiones tuyas, uno está
hecho.

**Lo primero es lo más barato**: una línea en el integrador convierte cuatro
puertas de adorno en gobierno. Hoy son lo que critican.

---

## Las dos dudas, verificadas

### deskops no está mal acoplado: falta una operación

Lo que importa de `store.io` y `store.layout`:

```
8  load_store_index
7  load_models_index
7  load_documents_index
6  store_exists
3  project_root
```

**Solo lee índices.** Ninguno de los cinco es un detalle de implementación: son
las cinco preguntas que cualquier consumidor le hace a un almacén —¿existe?,
¿dónde está la raíz?, ¿qué contiene?—.

Eso no es acoplamiento indebido: es una **operación de lectura que debería estar
en la superficie y no está**. El consumidor bajó a buscarla donde vivía porque no
había puerta.

Cambia el diseño del punto 2: el contrato de superficie no tiene que *prohibir*
estos imports, tiene que **promoverlos**. Cinco funciones de lectura de índice,
expuestas, y deskops deja de importar `store.io`.

El caso distinto es `cli.main` (4 usos): ahí sí hay un defecto de ambos lados.

### `enlaces` es composición de documentos

```python
from .parser import parse_links
from .resolver import resolve_document_input, resolve_link_target
from .recovery import recover_links
from .composer import compose_document
```

Siete archivos que parsean referencias entre documentos, las resuelven, las
recuperan y **componen un documento a partir de otros**. Solo lo usa la interfaz
(`cli/commands/links.py`, `cli/serve/lint_routes.py`).

Lo descarté como unidad por tamaño y era mal criterio: es una capacidad real
—composición— que está infradimensionada, no una sobra. Que `compose_document`
viva en siete archivos sin consumidores externos sugiere que la capacidad está
construida y no expuesta.

**Revisión**: `enlaces` no es «demasiado pequeño», es «capacidad sin superficie».
Mismo patrón que las cinco funciones de lectura de índice.

---

## Lo que sigo sin saber

- **No medí si romper a los consumidores importa.** Los cinco proyectos son del
  mismo autor y del mismo ecosistema; si se mueven juntos, la superficie puede ser
  más laxa de lo que supongo. Eso no lo decide un análisis.
