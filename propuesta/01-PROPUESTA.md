# Propuesta

El diagnóstico (`00-DIAGNOSTICO.md`) encontró una función ausente y seis
sostenidas por atención humana. Esta propuesta convierte cada una en algo que
rechaza.

**Ordenada por lo que desbloquea, no por esfuerzo.** Cada fase termina con una
puerta que corre sola, y el criterio de terminado es que la puerta rechace algo
que antes pasaba.

---

## Principio de orden

No se repara lo que no se puede verificar. Así que cada fase sigue el mismo
patrón, en este orden:

1. **la puerta primero**, en estado de aviso
2. **el contrato** que la puerta consulta, en un archivo legible
3. **la reparación**, hasta que la puerta pase
4. **la puerta en estado de rechazo**, y en el integrador

Construir la puerta antes de la reparación parece al revés, pero es lo único que
distingue «arreglado» de «arreglado hasta que alguien lo rompa de nuevo».

---

## Fase 0 · La línea que cuesta 46 módulos

**Resuelve: S1 (ausente)**

Una línea impide que el núcleo exista por separado.

```python
# src/sldb/core/exceptions/sldb_store_error.py:2
from sldb.store.exceptions import StoreError      # capa 0 → capa 2
```

### Qué se hace

Invertir la herencia: la clase base baja al núcleo, el almacén la extiende.
Las excepciones de un sistema pertenecen a su capa más baja, porque todas las de
arriba necesitan nombrarlas.

### Cómo se verifica

```bash
python3 -c "
import sys; before=set(sys.modules)
import sldb.core.renderer
assert not any(m.startswith('sldb.store') for m in sys.modules), 'el núcleo arrastra el almacén'
print('núcleo limpio:', len([m for m in sys.modules if m.startswith('sldb')]), 'módulos')"
```

Ya medido: **103 → 57 módulos**, 149 ms → 131 ms.

### Hecho

Aplicada. `StoreError` se movió a `core/exceptions/store_error.py`; el almacén la
reexporta.

| | antes | después |
|---|---|---|
| módulos al importar el núcleo | 103 | **58** |
| paquetes arrastrados | core, models, runtime, **store** | core, models, runtime |
| ciclos entre paquetes | 11 | **5** |
| aristas entre paquetes | 30 | 29 |
| pruebas | 1.207 pasan | **1.208 pasan** |

La puerta que lo sostiene está en `tools/check.sh` y rechaza la reaparición de la
fuga. La entrada R2 salió de `contracts/layers.toml`.

**Costo: una clase movida.** Eliminó seis de los once ciclos, porque el ciclo
core↔store participaba en casi todos.

---

## Fase 1 · Las cuatro aristas restantes

**Resuelve: S2**

Cada ciclo tiene una sola arista culpable. Ya están identificadas con archivo y
línea en `contracts/layers.toml`, con su reparación descrita.

| id | arista | asimetría | reparación |
|---|---|---|---|
| R4 | store → api | 1 vs 195 | bajar `describe_field` a una capa que ambos vean |
| R5 | selfdoc → cli | 1 vs 14 | subir `resolve_model_ref` a operaciones |
| R1 | core → runtime | 1 vs 4 | pasar el permiso como argumento, no consultarlo |
| R3 | models → runtime | 1 vs 1 | inyectar la extracción |

R2 (core → store) ya no está en la lista: la Fase 0 la reparó, y con ella cayeron
seis de los once ciclos. Quedan **5**.

### La puerta ya existe

`tools/check_layers.py`, construida y probada. Lee el orden de
`contracts/layers.toml` y rechaza:

- un import que cierra un ciclo **no contado**
- un import que sube de capa sin excepción declarada
- un paquete sin capa asignada
- **una excepción vencida**: si la reparación se hizo y nadie borró la entrada

Verificada inyectando una violación:

```
ERROR  ciclo no contado: cli → api → core → cli (aristas sin autorizar: core→cli)
```

### El mecanismo que hace que la deuda se pague

Las 5 excepciones están en `[allow].upward`. La puerta **pasa hoy** con ellas y
**rechazaría** un sexto ciclo. Borrar una entrada es el criterio de terminado de
su reparación, y la puerta avisa si una entrada ya no corresponde a nada.

Así la deuda queda contada en vez de escondida, y no se puede olvidar: mientras
la lista tenga entradas, la puerta imprime que el orden de capas es aspiracional.

### Nota sobre el núcleo

`core`, `models` y `runtime` quedaron declarados en la **misma capa** porque están
mutuamente entrelazados. Eso no resuelve nada: lo nombra. Mientras esa capa tenga
tres paquetes interdependientes, ninguno se extrae solo. Partirla es trabajo con
diseño propio, no una excepción que se tacha.

### Terminado cuando

`[allow].upward` está vacío y la puerta sigue pasando.

---

## Fase 2 · Las 19 reglas que nadie aplica

**Resuelve: S3**

`standards.md` enuncia 22 reglas. Tres tienen prueba. Y declara tres herramientas
«for enforcement» que no están instaladas.

### El paso que no se puede saltar

Antes de instalar nada: **clasificar las 22 reglas** por si son mecanizables.

| grupo | ejemplos | qué se hace |
|---|---|---|
| **mecanizables ya** | tipos, docstrings, `except` desnudo, `raise from` | configurar la herramienta |
| **mecanizables con trabajo** | una clase por archivo, propósito único | prueba estructural propia |
| **no mecanizables** | «refactorizar primero el árbol sintáctico», «el código es la verdad» | **marcar aspiracional en el propio documento** |

El tercer grupo es el importante. Una regla de proceso que depende de juicio no
se puede bloquear, y seguir enunciándola junto a las otras hace que todas
parezcan igual de firmes. Se queda, marcada.

### La reparación que no es instalar un linter

Instalar `ruff` y `mypy` cubre el primer grupo. Pero el defecto no era que
faltara la herramienta: era que **el documento afirmaba tener un mecanismo que no
existía**. Así que la reparación incluye que `standards.md` diga, por cada regla,
qué la bloquea — y que eso sea verificable.

### Terminado cuando

- cada regla declara su mecanismo o se marca aspiracional
- lo declarado existe y corre en el integrador
- una prueba verifica que no haya reglas sin clasificar

---

## Fase 3 · Los documentos que mienten

**Resuelve: S3\***

**72 afirmaciones falsas** en 73 documentos.

### La puerta ya existe

`tools/check_claims.py`, construida y probada. Extrae de cada documento lo
comprobable y lo comprueba contra el código:

| comprueba | falsas hoy |
|---|---|
| rutas de archivo citadas | 22 |
| módulos citados | 20 |
| comandos invocados | 14 |
| subcomandos invocados | 16 |

Pregunta al analizador de la interfaz por su estructura real en vez de raspar el
texto de ayuda, porque un detector que falla en silencio marca como falsas
afirmaciones que eran verdaderas. Construirla costó tres rondas de corregir mis
propios falsos positivos: la primera versión reportaba 130 «errores», de los que
58 eran defectos del detector.

### Las tres clases de documento falso

| clase | ejemplo | qué se hace |
|---|---|---|
| **referencia envejecida** | `src/nldb/`, el nombre anterior del proyecto | corregir | <!-- gone -->
| **función documentada que no existe** | `sldb ontology`, 8 invocaciones | mover a una carpeta de propuestas, marcada | <!-- gone -->
| **inventario desincronizado** | la especificación declara 7 nodos, hay 11 paquetes | **derivar del código, no escribir a mano** |

El tercero es el que importa. Un inventario escrito a mano envejece en silencio
y conserva su autoridad mientras miente. Si se puede derivar, se deriva.

### Cifras verificables en los documentos

Para las cifras que no se pueden derivar, un marcador:

```markdown
<!-- verify: 587 = find src -name '*.py' | wc -l -->
```

La puerta ejecuta el comando y compara. Una cifra que ya no es cierta falla.

### Terminado cuando

La puerta reporta 0 falsas y corre en el integrador.

---

## Fase 4 · Qué es estable y qué no

**Resuelve: S4**

336 definiciones públicas en un paquete no son una superficie diseñada.

### Qué se hace

1. **Marcar la frontera.** Qué es estable, qué experimental, qué interno. Sin
   esto nadie puede saber en qué apoyarse, y todo cambio es potencialmente
   incompatible.
2. **Una puerta de superficie.** Captura el conjunto de nombres públicos; si un
   cambio lo altera sin registrarlo en el historial de cambios, rechaza. Es la
   misma idea que la puerta de capas: el contrato en un archivo, la verificación
   contra él.
3. **Cerrar los dos planes de la raíz.** `TASK-sldb-serve.md` y
   `TASK-store-generalize.md`: completados, archivados o borrados. Un plan sin
   cierre en la raíz es una intención que parece compromiso. `sldb serve` se
   documenta y no existe.

### Terminado cuando

Cada paquete declara su superficie, y cambiarla sin registrarlo falla.

---

## Fase 5 · Qué pertenece

**Resuelve: S5**

Dos contradicciones de identidad:

**El congelamiento que no congeló.** ~~Hay que elegir.~~ **Resuelto**: no
ocurrió. 223 commits después de la fecha, 897 cambios bajo `src/`, subsistemas
nuevos, y un sucesor que se congeló el mismo día. El README y
`contracts/identity.toml` declaran el estado activo.

**El sucesor dentro del antecesor.** `knowledge/` son 1.368 archivos del proyecto
que, según el README, reemplaza a este. Más `desk/` (149), `surface/` (140),
`ledger/` (37), `runs/` (17), `kgdb/` (14).

### Qué se hace

Un archivo que declare, directorio por directorio, si pertenece. Y una puerta que
rechace un directorio nuevo de primer nivel sin clasificar.

No hay que mover nada necesariamente: hay que **declarar**. Un directorio prestado
y declarado es honesto; uno sin declarar hace que la identidad del sistema sea
indecidible.

### Terminado cuando

Todo directorio versionado está clasificado, y agregar uno sin clasificar falla.

---

## Fase 6 · De aviso a interrupción

**Resuelve: A**

El integrador corre en cada envío, pero sin protección de rama el commit ya está
en la rama principal cuando falla. Es un aviso posterior.

### Qué se hace

**Antes que nada: poner `selfdoc check` en verde.** Está en rojo desde hace
tiempo, dentro de `knowledge/`. Un integrador con una puerta permanentemente roja
entrena a todos a ignorarlo, y entonces las puertas nuevas tampoco se respetan.

| | |
|---|---|
| **protección de rama** | el integrador debe pasar *antes* de integrar |
| **gancho pre-commit** | las puertas rápidas corren antes de un commit local |
| **una sola entrada** | `tools/check.sh` con todas las puertas, en orden de costo |

La entrada única importa por sí misma: dos listas de comprobaciones en dos
lugares divergen, y entonces lo que decide deja de estar claro.

### Terminado cuando

Un cambio que viola cualquier puerta no entra en la rama principal sin que
alguien lo autorice explícitamente.

---

## Lo que esta propuesta no cubre

Declararlo es parte del método; un plan que no dice sus límites no es
verificable.

- **No reescribe nada.** 1.207 pruebas pasan: el comportamiento no está en
  discusión. Si una fase exige reescribir, está mal planteada.
- **No parte el núcleo.** Los tres paquetes entrelazados quedan declarados en una
  capa. Separarlos es un rediseño con su propio análisis.
- **No mide cobertura.** 1.207 pruebas verifican comportamiento; ninguna fase
  cambia eso.
- **No resuelve la salud prestada.** Las puertas convierten conocimiento tácito en
  mecanismo, lo que reduce la dependencia. Pero un solo autor sigue siendo un
  solo autor, y ninguna puerta arregla eso.
- **Las puertas no juzgan prosa.** `check_claims.py` verifica que las referencias
  apunten a algo real, no que la descripción sea buena. Eso queda para revisión
  humana y está declarado en la herramienta.

---

## Estado

| fase | resuelve | puerta | estado |
|---|---|---|---|
| 0 | S1 | puerta de núcleo aislado | **HECHA** — 103 → 58 módulos |
| 1 | S2 | `tools/check_layers.py` | **puerta lista**, 4 aristas por reparar |
| 2 | S3 | linter + pruebas estructurales | por hacer |
| 3 | S3\* | `tools/check_claims.py` | **puerta lista y probada** |
| 4 | S4 | puerta de superficie | por hacer |
| 5 | S5 | puerta de pertenencia | por hacer |
| 6 | A | protección de rama + pre-commit | por hacer |

Tres puertas existen y corren juntas desde `tools/check.sh`. Una fase está
aplicada y medida.

Las tres encontraron defectos reales mientras se construían, **incluidos defectos
en sus propios contratos**: la puerta de capas rechazó mi primera clasificación
de `selfdoc`, y la de afirmaciones reportó 130 errores de los que 58 eran míos.
Una puerta que no se equivoca sobre sí misma probablemente no está midiendo nada.
