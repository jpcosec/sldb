# No: los niveles no son las unidades

La conclusión que propones es la natural, y tiene un error de categoría que vale
la pena nombrar porque es el error más común al aplicar este modelo.

**Los seis niveles son orden de dependencia. Las unidades viables son otra cosa.**

---

## La diferencia

| | qué responde | qué produce |
|---|---|---|
| **niveles** | ¿quién puede importar a quién? | ausencia de ciclos |
| **unidades viables** | ¿qué se puede sostener por separado? | partes que sobreviven solas |

Una unidad viable tiene que absorber su propia variedad: cuando algo cambia
dentro de ella, se repara dentro de ella. Un nivel no tiene por qué.

La prueba no es «¿está abajo en el grafo?». Es: **¿tiene esta pieza sus propias
siete funciones?**

---

## La prueba, aplicada

Para cada candidato pregunto si tiene ejecución, coordinación, regulación,
auditoría, anticipación, clausura y corte **propias**. Una unidad a la que le
falta una función no es una unidad: es una parte de otra cosa.

Salida de `python tools/check_axes.py --units`, con las cifras medidas en
aristas de import:

| unidad | ejes | arch. | necesita | la necesitan | ¿unidad? |
|---|---|---|---|---|---|
| **núcleo** | 7 | 80 | **2** | 28 | sí — indivisible |
| **persistencia** | 9 | 106 | 15 | 30 | sí |
| **grafo** | 1 | 33 | 4 | 2 | sí |
| **adaptadores** | 1 | 22 | 3 | **0** | sí — extraíble hoy |
| **recuperación** | 1 | 19 | 4 | **0** | sí — extraíble hoy |
| operación | 4 | 158 | **39** | 9 | **no** — fachada |
| enlaces | 1 | 7 | 2 | 0 | no — demasiado chico |

El núcleo es el dato más limpio: **necesita 2 aristas de fuera y 28 entran en
él**. Es lo que define al sistema y lo que menos depende de nada.

**Cinco unidades, no seis niveles.** Y no coinciden: el núcleo es el nivel 4,
`persistencia` el 3, `grafo` vive dentro del nudo del nivel 1, y dos de las cinco
están en el nivel 0 junto a `enlaces`, que no es unidad.

El contrato las declara en `contracts/layers.toml`, sección `[[unit]]`, y
`tools/check_axes.py` verifica que las cifras correspondan al código.

---

## Por qué «operación» no es una unidad

Es el caso instructivo. Tiene 258 archivos y 11 ejes: por tamaño parece la unidad
más obvia. Pero:

**Necesita 39 aristas de fuera y solo 9 entran.** Es un consumidor neto. Una
unidad viable produce algo que otros usan; esto consume cuatro veces más de lo que
aporta.

**Es un nudo de 11, no un grupo.** Sus 26 aristas de peso ≤2 lo mantienen fundido.
Si se extrajera tal cual, se extraería el nudo entero — y un nudo no es una
unidad, es una parte que no se dejó dividir.

**Partirla es la decisión, no extraerla.** Ignorando las aristas débiles quedan 3
nudos, el mayor de 4. Eso sugiere que ahí dentro hay tres unidades, no una.

---

## El hallazgo que esto destapa

Al buscar las funciones de cada candidato encontré algo que el diagnóstico no
había visto: **`core` no tiene pruebas propias**.

```
$ for d in core store api selfdoc links models runtime; do ... done
core          0 tests
store        38 tests
api          21 tests
selfdoc       6 tests
```

Y la estructura de `tests/` tiene **3 carpetas para 24 ejes**, con 26 archivos
sueltos en la raíz.

Revisando qué eje ejercita cada prueba:

| | |
|---|---|
| ejes con prueba directa | 22 de 24 |
| **ejes sin prueba directa** | **`representacion`, `bitacora`** |

`representacion` es el eje que declaré *la* idea del sistema —`MeaningNode` +
`SurfaceNode`— y es uno de los dos que ninguna prueba toca directamente.

**Eso es S3\* ausente a nivel de eje.** El sistema tiene 1.208 pruebas y su
auditoría no está organizada por capacidades: está organizada por los tres
paquetes grandes. Una unidad no puede ser viable si su verificación vive fuera de
ella.

---

## La respuesta a tu pregunta

**No hay que reflejar los cinco niveles.** Hay que hacer otra cosa, en este orden:

### 1. Cortar los alfileres, no reorganizar carpetas

6 aristas de peso 1 cierran el nudo del núcleo. 26 de peso ≤2 cierran el de
operación. Mientras existan, cualquier organización de carpetas es cosmética:
el acoplamiento no está en la estructura de directorios, está en 32 imports.

Ya hay precedente medido: en la Fase 0 una arista de peso 1 costaba 46 módulos.

### 2. Darle a cada unidad candidata sus siete funciones

Cinco pasan la prueba: **núcleo** (indivisible), **persistencia**, **grafo**,
**adaptadores** y **recuperación**. Para cada una:

| función | qué significa acá |
|---|---|
| ejecución | ya la tiene — es lo que hace |
| coordinación | sus ejes internos no deben ciclar |
| regulación | reglas propias, verificadas |
| **auditoría** | **pruebas suyas, en su carpeta** ← lo que falta |
| anticipación | superficie pública declarada |
| clausura | qué le pertenece y qué no |
| corte | una puerta que rechace sin discusión |

Faltan **dos en las cinco**: la auditoría (`tests/` no está organizado por
unidad) y la regulación (las tres reglas mecanizadas recorren `src/` entero).

La puerta lo imprime como deuda:

```
deuda  función `auditoria` ausente en 5 de 5 unidades
deuda  función `regulacion` ausente en 5 de 5 unidades
```

### 3. Recién entonces separar

Y la separación que sale no son los niveles: son cuatro unidades, de las cuales
dos (`adaptadores`, `recuperacion`) son extraíbles hoy porque **nadie depende de
ellas**.

---

## La recursión, que es lo que falta para que sea un VSM

Acá está lo que tu pregunta apunta y el mapa de ejes no cubre.

Un sistema viable es **recursivo**: cada unidad viable contiene unidades viables,
y cada una tiene las siete funciones en su propio nivel. El mapa de 24 ejes es
plano — describe capacidades, no niveles de recursión.

Para que esto sea un sistema viable por derecho propio:

```
R0   sldb                       las 7 funciones del conjunto
      │
R1   ├── nucleo          80    indivisible: 7 ejes en un nudo
     ├── persistencia   106
     ├── grafo           33
     ├── adaptadores     22    extraíble hoy
     │    ├── python-ast       ¿7 funciones?
     │    └── argparse        ¿7 funciones?
     └── recuperacion    19    extraíble hoy
```

Y la pregunta que decide cada nivel es siempre la misma: **si esto cambia, ¿se
repara aquí dentro?**

Hoy la respuesta en R1 es «no» para las cuatro, por la misma razón: su auditoría
está afuera. Por eso la reorganización de carpetas no es el primer paso — sería
mover piezas sin darles lo que les falta.

### La prueba de que R1 existe

Un criterio verificable, no una opinión: **`tests/<unidad>/` debe poder correr
sola y pasar**, sin cargar las otras unidades.

Hoy eso es imposible porque importar el núcleo arrastraba 103 módulos (ahora 58)
y porque las pruebas no están agrupadas por unidad. Ambas cosas son reparables, y
en ese orden.

---

## Las dos dudas, verificadas

Dije que no las había comprobado. Las comprobé.

### Ninguna unidad tiene regulación propia

Las tres reglas mecanizadas viven en `tests/test_clean_code_rules.py` y recorren
`src/` entero:

```python
SRC_DIR = Path(__file__).parent.parent / "src"
```

Una clase por archivo, diez líneas por función, ochenta por archivo — para todo
el sistema por igual. **Ninguna unidad tiene una regla que le aplique solo a
ella**, lo cual es coherente: sin unidades declaradas, no hay a qué atribuirle
una regla.

Es S3 ausente a nivel de unidad, igual que S3\* lo es.

### El nudo de operación no son tres unidades

Al cortar las aristas de peso ≤2 quedan tres nudos, y ninguno es una unidad:

| nudo | necesita | lo necesitan | qué es |
|---|---|---|---|
| `render` + `superficie` | 4 | 4 | equilibrado — parte del núcleo, no unidad aparte |
| `consulta` + `federacion` | 6 | 8 | consumidor; vive dentro de persistencia |
| `op_almacen`+`op_aristas`+`op_documentos`+`op_modelos` | **39** | 9 | **fachada** |

El tercero es el dato. Cuatro ejes, 158 archivos, y necesitan 39 aristas de fuera
mientras solo 9 entran.

**Eso no es una unidad: es una fachada.** Compone operaciones sobre lo que otras
unidades producen, y no produce nada que otras necesiten. Una fachada es
legítima —es el nivel de transporte— pero no se puede extraer como parte viable,
porque no absorbe su propia variedad: cualquier cambio en las unidades de abajo
la obliga a cambiar.

Eso deja el recuento en **cinco unidades viables**: núcleo (indivisible),
`persistencia`, `grafo`, `adaptadores` y `recuperacion`. Las dos últimas son
extraíbles hoy porque nadie depende de ellas.

---

## Lo que sigue sin verificar

- **No sé si la recursión tiene sentido por debajo de R1.** Dibujé R2 como
  pregunta, no como afirmación: exigirle siete funciones propias a `superficie`
  (18 archivos) puede ser exigirle demasiado.
- **No medí si `persistencia` absorbe su variedad.** Tiene 34 archivos y 14 ejes
  que la necesitan, pero no comprobé si un cambio en el formato de almacenamiento
  se repara dentro de ella o se propaga.
