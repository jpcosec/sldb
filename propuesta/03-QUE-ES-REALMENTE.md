# No es una biblioteca de Markdown

La identidad que declaré en `02` dice «convierte Markdown estructurado en objetos
validados y de vuelta». Eso describe **una** de sus superficies, y la confunde con
el sistema.

La pregunta que lo revela: si un símbolo de Python —una clase, una función— se
puede representar y operar acá, entonces Markdown no es el dominio. Es un
formato de entrada.

Y la respuesta está medida en el propio repositorio.

---

## La evidencia

### 1. El árbol sintáctico es abstracto, y Markdown es una implementación

```python
# src/sldb/core/node.py
@dataclass
class SLDBNode:
    """A unified node structure that abstracts away the specific AST library."""
```

```python
# src/sldb/core/ast/base_ast_handler.py
class BaseASTHandler(ABC):
    """Abstract base class for parsing content into a unified SLDBNode tree."""
```

`MarkdownASTHandler` es la única implementación concreta hoy. La abstracción
existía antes de que hubiera una segunda, lo cual significa que la separación fue
deliberada y no un accidente de refactorización.

### 2. La representación intermedia separa significado de superficie

En `core/ir/` hay dos tipos de nodo, y la diferencia entre ellos es la tesis del
sistema:

| | campos | qué es |
|---|---|---|
| `MeaningNode` | `kind`, `name`, `model`, `field_path`, `value`, `span` | lo que el documento **significa** |
| `SurfaceNode` | `kind`, `text`, `span` | *«Original reversible text content»* |

`DocumentIR` contiene ambos a la vez, más un `GraphView` con nodos y aristas
tipadas.

**Esa es la arquitectura de un compilador, no de un conversor de formato.** Un
conversor transforma A en B. Esto mantiene el significado y la superficie como dos
proyecciones del mismo objeto, ancladas por rango de líneas, de modo que se puede
operar sobre el significado y reconstruir la superficie exacta.

### 3. Ya hay tres fuentes, y dos no son Markdown

| procedencia | documentos | de dónde sale |
|---|---|---|
| `python-ast:` | **1.279** | `ast.parse()` sobre archivos `.py` |
| `parser:` | **89** | introspección de `argparse` |
| Markdown | el resto | `MarkdownASTHandler` |

Y hay un cuarto adaptador ya escrito:

```python
# src/sldb/selfdoc/click_scanner.py
"""Introspect an assembled click Group into `CommandRecord` facts...
The same typed facts the argparse `ParserScanner` produces, so a click
CLI can feed the same materialize path."""
```

«La misma ruta de materialización» desde dos bibliotecas de interfaz distintas.
Eso solo tiene sentido si el núcleo no sabe de formatos.

**1.368 de los 1.551 documentos del almacén no vienen de Markdown.** Vienen de
árboles sintácticos de código.

### 4. La propia taxonomía del sistema lo dice

```
sldb://semantic_tag/source
sldb://semantic_tag/source.code
sldb://semantic_tag/source.code.python
sldb://semantic_tag/source.document
sldb://semantic_tag/source.document.markdown
sldb://semantic_tag/representation
sldb://semantic_tag/representation.markdown
```

`source.code` y `source.document` son **ramas paralelas**. Markdown aparece como
`source.document.markdown` y como `representation.markdown`: una fuente entre
otras, y una representación entre otras.

El sistema ya se clasificó a sí mismo correctamente. El README no.

### 5. Los nodos más centrales del grafo son hermanos

```
$ sldb graph central
  representation.markdown      0.0650
  source.code.python           0.0570
  type.knowledge.code_symbol   0.0570
```

Markdown y Python son los dos nodos de los que más cuelga el grafo, con pesos
casi idénticos. Si esto fuera una biblioteca de Markdown, el segundo no existiría.

---

## Qué es, entonces

No es un conversor de formato. Es un **sistema de representación anclada y
operable**, con cuatro propiedades que ningún conversor tiene:

### Anclaje verificable

Cada documento derivado lleva la huella de su origen:

```yaml
source_path: sldb/cli/commands/ast.py
source_span: '38:58'
source_sha256: 788802abd123bf678...
provenance: python-ast:python:sldb...:ASTCLI; contract-sha256:0f5c4ef4...
```

Dos huellas distintas: una del **código fuente** y otra del **contrato** que lo
describe. Si el código cambia, el documento queda detectablemente rancio; si el
contrato cambia, también. Eso no es documentación: es una proyección con
verificación de integridad.

### Direccionabilidad por campo

```
$ sldb fields show docs/python-sldb-...-astcli/source_span
{ "value": "38:58" }
```

Un campo de un símbolo de Python, consultado por dirección. No un archivo, no una
sección: **un campo**.

### Operaciones de grafo sobre la misma estructura

```
get · list · query · neighborhood · path · cycles · order
components · central · similar · snapshot
```

Las mismas once operaciones sirven para documentos de prosa y para símbolos de
código, porque para el núcleo son el mismo tipo de objeto.

### Reversibilidad

El `SurfaceNode` guarda el texto original reversible. Se puede extraer a
estructura, operar, y volver al texto exacto. Eso es lo que hace que la
representación sea un lugar donde *trabajar*, y no solo un volcado para leer.

---

## La identidad, corregida

| | |
|---|---|
| **lo que declaré en `02`** | una biblioteca que convierte Markdown estructurado en objetos validados y de vuelta |
| **lo que es** | un sistema para representar cualquier cosa con estructura derivable de forma determinista —documentos, código, interfaces— como documentos direccionables, consultables, anclados a su origen y reversibles a su superficie |

Markdown es la superficie **autorada**: la que un humano escribe. Los árboles
sintácticos de código son la superficie **derivada**: la que una máquina extrae.
El núcleo no distingue, y esa indistinción es el producto.

### Por qué importa la corrección

No es un detalle de redacción. Cambia tres cosas:

**Lo que el sistema promete.** «Biblioteca de Markdown» promete conversión.
«Representación anclada» promete que la estructura se mantiene verdadera respecto
de su origen, y eso es una promesa mucho más fuerte y más difícil.

**Qué es `selfdoc`.** Con la identidad anterior parecía un accesorio: la
biblioteca documentándose. Con la correcta es **la prueba del caso difícil**:
representar código —que no es Markdown, que cambia solo, y donde la deriva es
detectable— es el escenario donde el anclaje tiene que funcionar. `selfdoc` no es
el repositorio mirándose el ombligo: es el segundo dominio que demuestra que el
núcleo es genérico.

**Dónde está la frontera del producto.** En `02` clasifiqué los seis modelos de
`selfdoc` como «autoaplicación», fuera del producto. Esa clasificación ahora se
ve incompleta:

| modelo | ¿es específico de este repositorio? |
|---|---|
| `PythonSymbolDoc` | **no** — describe cualquier símbolo de Python |
| `CliCommandDoc` | **no** — describe cualquier interfaz de argparse o click |
| `SurfaceDoc` | **no** — describe cualquier agrupación de comandos |
| `KnowledgeTag`, `AnchorDoc`, `KnowledgeSurface` | vocabulario, también genérico |

**Ninguno nombra este repositorio.** Son adaptadores de dominio: Python, interfaz
de línea de comandos. Lo específico es el *contenido* del almacén (`.sldb/`,
`knowledge/`), no los modelos.

Eso significa que `selfdoc` es **producto**, no autoaplicación. Es el segundo
adaptador de superficie del sistema, igual que `MarkdownASTHandler` es el
primero.

---

## Qué revisar de lo anterior

Esto no invalida el diagnóstico —los 5 ciclos, las 19 reglas sin mecanismo, las 72
afirmaciones falsas siguen siendo ciertas— pero corrige dos cosas:

| | estado |
|---|---|
| `contracts/identity.toml` | **reescrito** con la identidad correcta |
| la frontera producto / autoaplicación | **corregida**: `selfdoc` y sus 10 modelos son producto |
| `tools/check_identity.py` | **rehecho**: verifica rutas, no modelos |

### La puerta se quedó vacía, y eso fue el hallazgo

Al reclasificar `selfdoc` como producto, la lista de «modelos de autoaplicación»
quedó vacía. La puerta siguió imprimiendo `PASS` — **porque su bucle de
verificación ya no iteraba sobre nada**.

Una puerta vacía es peor que ninguna: afirma una garantía que no está midiendo.
La regla correcta no era sobre modelos sino sobre **rutas**: un paquete genérico
que menciona `knowledge/` o `desk/` dejó de ser genérico.

Con esa regla aparecieron **dos cruces reales**:

| dónde | nombra | qué pasa |
|---|---|---|
| `src/sldb/cli/commands/lint.py#L8` | `desk/` | `ALLOWED_PREFIXES` incrusta cuatro convenciones de este repositorio |
| `src/sldb/cli/selfdoc_inspect.py#L53` | `knowledge/` | detecta renombres contra la carpeta de salida local |

Y tres falsos positivos que obligaron a afinar el detector: `desk/` citado dentro
de docstrings. Citar una ruta de ejemplo en documentación no cruza una frontera;
reportarlo como violación es la forma más rápida de enseñar a ignorar la puerta.

Los dos cruces están contados en `contracts/identity.toml` con su reparación.
Mientras existan, «el producto es genérico» es **aspiracional**.

Y abre una pregunta que el diagnóstico no hizo, porque la identidad equivocada la
ocultaba:

> **Si el núcleo acepta cualquier árbol sintáctico, ¿por qué hay una sola
> implementación concreta de `BaseASTHandler` después de 317 commits?**

La abstracción existe, está probada por dos adaptadores de interfaz y uno de
Python, y nunca se ejercitó con una segunda superficie de documento. Eso es una
capacidad declarada y no verificada — y por la regla de variedad, una capacidad
sin segundo caso es una hipótesis, no una propiedad.
