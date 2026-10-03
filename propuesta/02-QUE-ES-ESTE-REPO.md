# Qué es este repositorio

El diagnóstico de S5 dio «presente sin mecanismo» y pasó de largo. Eso fue un
error de método: S5 es la función que fija la identidad, y un diagnóstico que no
dice qué es el sistema no puede juzgar si algo le pertenece.

Peor: el veredicto trataba varios directorios como intrusos. Esa lectura era
falsa, y el propio repositorio la contradice por escrito.

---

## Lo que yo dije, y por qué estaba mal

Marqué como «no pertenece» a `knowledge/` (1.368 archivos), `desk/` (149),
`surface/` (140), `ledger/` (37), `runs/` (17), `kgdb/` (14).

El criterio fue: *el README describe una biblioteca; estos directorios no son una
biblioteca; por lo tanto sobran*.

Pero `.sldb/README.md` dice:

> *The store itself is part of the repo's operating surface, not a second
> codebase.*

Y `desk/SPEC.md`:

> *contributors need a local operational layer that records what was done, why it
> was done, what remains open.*

Están declarados. No son acumulación: son una decisión que no leí antes de
juzgarla. Confundí «no encaja en la identidad que yo inferí del README» con «no
pertenece», y eso es exactamente el error que un diagnóstico debe evitar.

---

## Lo que el repositorio es

Dos cosas, y de ahí vienen casi todas sus tensiones.

### 1. Una biblioteca

| | |
|---|---|
| nombre instalable | `sldb` |
| descripción | *structured Markdown to Pydantic and back* |
| comando | `sldb` |
| estado declarado | Alpha |

Seis paquetes genéricos, que no saben nada de este repositorio:

| paquete | archivos |
|---|---|
| `core` | 64 |
| `models` | 11 |
| `runtime` | 3 |
| `store` | 157 |
| `api` | 164 |
| `cli` | 151 |

### 2. El primer caso de uso de esa biblioteca, que es ella misma

El repositorio se describe con su propia herramienta. No es una demostración:
es la mayor instancia que existe.

| | |
|---|---|
| documentos en el almacén | **1.551** |
| símbolos de código descritos | 1.279 de 1.665 (**77%**) |
| comandos descritos | 68 |
| modelos registrados | 23 |

El aparato que lo hace posible:

| pieza | qué es |
|---|---|
| `selfdoc` (22 archivos) | deriva documentos del código y detecta deriva |
| 3 modelos (`PythonSymbolDoc`, `CliCommandDoc`, `SurfaceDoc`) | los contratos de esa derivación |
| `.sldb/` (1.551 docs) | el almacén del propio repositorio |
| `knowledge/` (1.368) | la salida: documentos derivados del código |
| `desk/` (149) | la capa operativa declarada en su propia especificación |

**Esos tres modelos solo los usa `selfdoc`.** Ninguno de los seis paquetes
genéricos los menciona. Es la frontera más nítida del repositorio y no estaba
declarada en ninguna parte.

---

## La identidad, en una frase

> **Una biblioteca que convierte Markdown estructurado en objetos validados y de
> vuelta, más la aplicación de esa biblioteca a sí misma como primer caso de uso
> y como prueba viva de que funciona a escala.**

La segunda mitad es la que faltaba. Sin ella:

- `selfdoc` parece un accesorio, y es la demostración central
- `knowledge/` parece un intruso, y es la salida del producto
- `.sldb/` parece andamiaje, y es la instancia mayor
- `desk/` parece de otro proyecto, y está en su especificación

Con ella, cada directorio tiene un lugar y la pregunta «¿esto pertenece?» se
puede responder.

---

## Lo que esa frase sí rechaza

Una identidad que no rechaza nada no es identidad. Esta rechaza:

- **una función del producto que el propio repositorio no use** — si no se puede
  autoaplicar, no entra; esa es la prueba
- **documentación escrita a mano sobre algo derivable** — existiendo `selfdoc`,
  escribir a mano lo que se deriva es duplicar la fuente
- **un modelo específico de este repositorio en los paquetes genéricos** — la
  frontera entre producto y autoaplicación
- **una capa operativa que no esté declarada en su especificación** — `desk/` lo
  está; lo que no, no

Y resuelve dos casos que dejé ambiguos:

| | veredicto |
|---|---|
| `surface/` (140 archivos, app web) | **no pertenece** — no está declarada en ninguna especificación, ni es producto ni autoaplicación |
| `sldb/relation_types/` (1 archivo en la raíz) | **no pertenece** — duplica `kgdb/relation_types/`, y un directorio con el nombre del paquete en la raíz solo genera ambigüedad |

Nótese la diferencia con mi veredicto anterior: ahora el rechazo se sostiene en
un criterio declarado, no en mi impresión de lo que un repositorio debería
contener.

---

## El congelamiento

Queda una contradicción que la identidad no resuelve, porque es una decisión y no
un hallazgo.

El README dice:

> *Historical freeze (2026-09-07). `sldb` v1 is superseded by `knowledge`.*

Hubo **223 commits después de esa fecha**. Y el README añade que el trabajo
posterior *«no establece una nueva versión ni reemplaza al proyecto sucesor»*.

Eso es coherente como intención: el repositorio está congelado **como producto** y
activo **como caso de uso**. Pero entonces conviene decirlo así, porque hoy la
palabra «freeze» aplicada a un árbol con 223 commits nuevos entrena a leer el
README como decorativo.

**Lo que hay que decidir** —no lo decido yo— es cuál de estas dos:

1. **Congelado como producto, activo como autoaplicación.** El README lo dice
   explícito, y una puerta rechaza cambios en los seis paquetes genéricos que no
   sean correcciones.
2. **Activo.** Se levanta el congelamiento y se dice qué es ahora.

Lo que no funciona es la ambigüedad actual, porque hace que `selfdoc check` lleve
semanas en rojo sin que nadie lo lea como un problema.

---

## Consecuencia para la propuesta

Esto cambia la Fase 5. No se trata de sacar directorios ajenos: se trata de
**declarar la frontera que ya existe y nadie escribió**.

| | |
|---|---|
| **antes** (equivocado) | sacar `knowledge/`, `desk/`, `ledger/`, `runs/`, `kgdb/` |
| **ahora** | declarar los tres grupos: producto, autoaplicación, ajeno |

Los tres grupos:

| grupo | contenido | regla |
|---|---|---|
| **producto** | `core`, `runtime`, `store`, `api` | genérico; no puede nombrar nada de este repositorio |
| **mezclados** | `models`, `cli` | contienen las dos cosas; deuda contada |
| **autoaplicación** | `selfdoc`, 6 modelos, `.sldb/`, `knowledge/`, `desk/`, `ledger/`, `runs/` | puede nombrar el repositorio; no puede entrar al producto |
| **ajeno** | `surface/`, `sldb/`, `kgdb/` | declarado como prestado |
| **huérfanos** | 2 planes sin cierre, 4 specs de agosto sin referencias | contados, con su acción |

La puerta (`tools/check_identity.py`) verifica: **ningún paquete del producto
nombra un modelo de autoaplicación**, ningún paquete queda sin grupo, ningún
directorio o archivo de la raíz queda sin clasificar.

---

## La puerta corrigió mi frontera

Escribí el contrato poniendo `models` y `cli` como producto. La puerta lo
rechazó con **18 violaciones**, y tenía razón.

`models/` contiene dos cosas que no se parecen:

| | usado por |
|---|---|
| `structured_doc` | core, runtime, store, api, cli — **el contrato base** |
| `relation_doc`, `relation_type_doc`, `builtin_relation_types` | api, store — producto |
| `python_symbol_doc`, `cli_command_doc`, `surface_doc`, `knowledge_surface`, `knowledge_tag`, `anchor_doc` | **solo `selfdoc`** |

Seis de los diez modelos existen únicamente para que el repositorio se describa a
sí mismo. Y `cli/` expone los comandos `selfdoc_*`.

**La frontera no corre entre paquetes: corre por dentro de dos de ellos.** Eso no
se puede verificar hasta separarlos, así que el contrato lo declara como deuda
con su reparación: mover los seis modelos a `selfdoc/models/`.

Mi primera versión del contrato era una suposición razonable y falsa. La puerta
la refutó en una corrida.

---

## Eso es lo que faltaba en S5

No un inventario de lo que sobra, sino **la regla que permite decidir**. Y la
prueba de que la regla sirve es que rechazó la primera clasificación de quien la
escribió.
