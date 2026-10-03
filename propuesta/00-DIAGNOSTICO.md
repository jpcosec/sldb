# Diagnóstico

Cuatro agentes sin contexto previo recorrieron las siete funciones. Cada uno vio
solo el marco (`BUNDLE.md`), sus archivos de evidencia y el código. Ninguno vio
el trabajo de los otros ni esta síntesis.

Los informes crudos están en `diag-s1-s2.md`, `diag-s3-s3s.md`, `diag-s4-s5.md` y
`diag-a-salud.md`.

---

## El resultado

| | función | veredicto |
|---|---|---|
| **S1** | ejecución | **AUSENTE** |
| **S2** | coordinación | presente sin mecanismo |
| **S3** | regulación | presente sin mecanismo |
| **S3\*** | auditoría | presente sin mecanismo |
| **S4** | anticipación | presente sin mecanismo |
| **S5** | clausura | presente sin mecanismo |
| **A** | corte | presente sin mecanismo |

Una función ausente. Seis presentes y ninguna bloqueada.

**Lo que eso significa**: el sistema no está mal construido. Está sostenido por
atención humana en los siete frentes a la vez. Funciona —1.207 pruebas pasan—
porque alguien recuerda cómo funciona.

---

## El hallazgo central

La modularización no falta. **Sobra, y no sirve.**

| | |
|---|---|
| archivos | 586 |
| archivo más grande | 138 líneas |
| archivos de ≤15 líneas | 90 |
| paquetes que se pueden usar solos | **0** |

586 archivos, ninguno grande, y **cero partes separables**. La fragmentación en
archivos diminutos se tomó por modularidad; pero un módulo no se define por el
tamaño de su archivo, sino por lo que se puede quitar sin que el resto se caiga.

La medición que lo demuestra:

```
$ python3 -c "import sldb.core.renderer"   # la capa 0, el conversor de texto
carga: core, models, runtime, store
módulos: 103
```

El renderizador —la pieza que el proyecto anuncia como su producto— **arrastra el
motor de almacenamiento completo**. No se puede usar el conversor sin cargar la
base de datos.

### Y la causa es una línea

```python
# src/sldb/core/exceptions/sldb_store_error.py:2
from sldb.store.exceptions import StoreError
```

Una excepción de la capa 0 hereda de una de la capa 2. `core/exceptions/__init__`
la reexporta, así que **cualquier** import del núcleo trae el almacén entero.

Medido quitándola:

| | antes | después |
|---|---|---|
| paquetes cargados | core, models, runtime, **store** | core, models, runtime |
| módulos | 103 | **57** |
| tiempo de import | 149 ms | **131 ms** |

Una línea. 46 módulos. Eso es S1.

---

## Lo que cada función reveló

### S2 · coordinación — 5 ciclos, cada uno con una sola arista culpable

| ciclo | ida | vuelta | arista minoritaria |
|---|---|---|---|
| api ↔ store | 195 | **1** | `store/edge_index/model_contribution.py#L41` |
| cli ↔ selfdoc | 14 | **1** | `selfdoc/python_relation_registry.py#L7` |
| core ↔ store | 8 | **1** | `core/exceptions/sldb_store_error.py#L2` |
| runtime ↔ core | 4 | **1** | `core/renderer_engine/python_expr.py#L5` |
| models ↔ runtime | 1 | **1** | `models/structured_doc.py#L67` |

La asimetría es la buena noticia: 195 contra 1 no es un diseño fusionado, es un
accidente. Cinco líneas sostienen cinco ciclos.

Además, **91 imports escritos dentro de funciones**. Un import diferido es casi
siempre alguien esquivando un ciclo a mano. Uno de ellos lo dice:

> `# imported late so sldb.store never loads sldb.api at import time`

Ese comentario es la única documentación de una decisión de arquitectura.

**Nada rechaza un ciclo nuevo.** El integrador corre pruebas y construcción; no
mira dependencias.

### S3 · regulación — 3 de 22 reglas tienen mecanismo

`standards.md` enuncia 22 reglas. Tres están verificadas por una prueba. Las
otras 19 dependen de que alguien se acuerde.

Y la sección «Toolchain Configuration» dice:

> *The project uses the following tools for enforcement: **ruff**, **mypy**,
> **docstring-coverage**.*

Ninguna de las tres está instalada, ni declarada en las dependencias, ni en el
integrador continuo. El documento afirma tener un mecanismo que no existe.

Es el antipatrón **estándares sin mecanismo** en su forma literal: las reglas
están escritas, son correctas, y nada las aplica.

### S3\* · auditoría — el inventario envejeció

Hay un canal propio real: `selfdoc check` corre en el integrador y bloquea. Pero
cubre solo los hechos del analizador de la interfaz.

Lo que no cubre:

- **La especificación de arquitectura declara 7 nodos. Hay 11 paquetes.** De sus
  17 nombres, 16 ya no corresponden al sistema. Nada lo detecta.
- **72 afirmaciones falsas en 73 documentos**, medidas por una puerta nueva
  (`tools/check_claims.py`): 22 rutas inexistentes, 20 módulos inexistentes, 14
  comandos inexistentes, 16 subcomandos inexistentes.
- `docs/requests/sldb-ontology-feature-request.md` documenta `sldb ontology` <!-- gone --> en 8
  invocaciones. El comando nunca se construyó <!-- gone -->. Es indistinguible de
  documentación real.
- `src/nldb/` aparece citado: el nombre que el proyecto tenía antes. <!-- gone -->

Esto es **existencia como prueba**: los documentos existen, y su existencia se
toma por evidencia de que la función está cubierta.

### S4 · anticipación — 336 definiciones públicas sin frontera

| paquete | definiciones públicas | declara su superficie |
|---|---|---|
| store | **336** | sí |
| api | 253 | sí |
| cli | 234 | sí |
| core | 67 | **no** |
| selfdoc | 33 | **no** |
| runtime | 12 | **no** |

336 definiciones públicas no son una superficie diseñada: son todo lo que quedó
sin un guion bajo delante. Nada marca qué es estable y qué experimental, así que
quien integra no puede saber en qué apoyarse.

En la raíz hay dos planes, `TASK-sldb-serve.md` y `TASK-store-generalize.md`, sin
cierre. `sldb serve` se documenta en `docs/` y no existe como comando.

### S5 · clausura — el veredicto estaba mal planteado

**Corregido en [`02-QUE-ES-ESTE-REPO.md`](02-QUE-ES-ESTE-REPO.md).** El
diagnóstico dio «sin mecanismo» y listó directorios como intrusos, sin decir
antes qué es el sistema. Sin identidad declarada, «no pertenece» no es un
veredicto: es una impresión.

`.sldb/README.md` dice que el almacén *«is part of the repo's operating surface,
not a second codebase»*, y `desk/SPEC.md` declara su capa operativa. Estaban
escritos; no los leí antes de juzgarlos.

Lo que sigue es el hallazgo que sí se sostiene.

El README declaraba:

> *Historical freeze (2026-09-07). `sldb` v1 is superseded by `knowledge`.*

Hubo **223 commits después de esa fecha**, con 897 cambios bajo `src/` y
subsistemas nuevos completos.

**Resuelto**: no ocurrió. El sucesor se congeló el mismo día y su evaluador se
movió a otro proyecto, que está activo y no importa `sldb`. El relevo nunca tuvo
lugar, así que esto no es un proyecto cerrado con trabajo residual: es el
proyecto vigente. El README lo dice ahora y `contracts/identity.toml` lo declara.

Y los directorios versionados:

| directorio | archivos | pertenece |
|---|---|---|
| `src/sldb`, `tests`, `docs` | — | sí |
| **`knowledge/`** | **1.368** | **no — es el proyecto sucesor, dentro del repo congelado** |
| `desk/` | 149 | no — otro sistema (harness de workflow) |
| `surface/` | 140 | no — una aplicación web propia, ausente del README |
| `ledger/` | 37 | no — bitácoras de movimientos de archivos |
| `runs/` | 17 | no — salidas de subagentes |
| `kgdb/` | 14 | no — otro sistema del ecosistema |

El repositorio sucesor está dentro del repositorio al que sucede. Nada rechaza
una pieza que no pertenece.

### A · corte — señal, no interrupción

El integrador corre en cada envío. Pero **sin protección de rama**, cuando falla
el commit ya está en la rama principal.

Eso no es un corte: es un aviso posterior. La función de corte interrumpe *antes*.
Tampoco hay nada que corra antes de un commit local.

| puerta | qué rechaza | corta o avisa |
|---|---|---|
| pruebas (1.208) | regresiones de comportamiento | avisa |
| `selfdoc check` | referencia de interfaz desactualizada | **avisa, y está en rojo** |
| construcción | empaquetado roto | avisa |
| *nada* | ciclos, capas, reglas, afirmaciones falsas | — |

### La puerta que ya estaba roja

`selfdoc check` es la única puerta propia del proyecto, y **falla hoy**: 29
documentos faltantes y 11 cambiados. Verificado como preexistente, antes de
cualquier cambio de esta propuesta.

Falla dentro de `knowledge/` — el directorio que el diagnóstico de S5 identificó
como perteneciente a otro proyecto. La puerta de auditoría del sistema audita un
sistema ajeno, y lleva así el tiempo suficiente para que nadie lo note.

Esto cierra el argumento de la función de corte: no alcanza con tener una puerta.
Una puerta que avisa en lugar de interrumpir termina en rojo permanente, y el
rojo permanente es indistinguible de no tener puerta.

---

## Salud prestada

> *Si quien escribió esto se va mañana, ¿qué se degrada y en cuánto tiempo?*

| | |
|---|---|
| autores reales | **1** |
| commits | 317 |
| commits en un solo mes | **224 (71%)** |
| decisiones que viven solo en comentarios | 4 |

El conocimiento del sistema cabe en una cabeza y en seis comentarios.

**Lo que se degrada primero no es la ejecución: es la capacidad de decidir.** Las
pruebas siguen verdes y el integrador sigue corriendo. Pero alguien que «limpie»
el import tardío de `model_contribution.py#L41` restaura el ciclo, las pruebas lo
dejan pasar, y nadie puede explicar por qué esa línea importaba.

Las cuatro decisiones sin respaldo:

| decisión | dónde vive |
|---|---|
| import tardío para romper el ciclo store→api | un comentario |
| «PLAN 15 capa 5»: fragmentos por documento, con lectura heredada | dos comentarios |
| carrera de descriptores de archivo bajo concurrencia | dos comentarios |
| tolerancia a almacenes anteriores a `field_hashes` | dos comentarios |

---

## La conclusión

El sistema está **sano y prestado**.

Nada de lo que falla es un defecto de construcción: 1.207 pruebas pasan, los
archivos son chicos, las capas se nombran, los documentos abundan. Lo que falta
es que algo **rechace** cuando eso deje de ser cierto.

Siete funciones, y en las siete la respuesta a «¿qué lo bloquea?» es *alguien se
acuerda*. Eso es exactamente lo que se evapora cuando el autor deja de mirar.

El trabajo no es reescribir. Es **convertir seis mecanismos humanos en seis
puertas**, y empezar por la línea que cuesta 46 módulos.
