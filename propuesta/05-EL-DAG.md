# El DAG

Pediste el dibujo. Primero el dato incómodo: **no es un DAG**.

```
$ networkx.is_directed_acyclic_graph(G)
False
1787 ciclos entre ejes
```

Hay un DAG, pero solo aparece **después de condensar los nudos**. Eso no es un
detalle de presentación: es la estructura real, y dibujarlo como un árbol limpio
sería dibujar otro sistema.

---

## El dibujo

```
                           ┌──────────┐
                           │ errores  │ 17          nivel 5 · nadie debajo
                           └────▲─────┘
                                │
     ╔══════════════════════════╧═══════════════════════════╗
     ║  N Ú C L E O   ·   nudo de 5 ejes   ·  61 archivos    ║  nivel 4
     ║                                                       ║
     ║   superficie ──9──▶ representacion ◀──7── render      ║
     ║       │ ▲                  │                 │ ▲      ║
     ║       3 └────────1─────────┘                 5 │      ║
     ║       ▼                                        │      ║
     ║     render ───────────1───────────▶ contrato   │      ║
     ║       │ 1                              │ 1    │      ║
     ║       ▼                                ▼       │      ║
     ║     runtime ◀──────────1─────────── runtime ───┘      ║
     ║        └──────1──▶ superficie                         ║
     ╚═══════════════════════▲═══════════════════════════════╝
                             │
                 ┌───────────┴────────────┐
                 │                        │
          ┌──────▼──────┐          ┌──────▼──────┐
          │ persistencia│ 34       │   codec     │ 2      nivel 3
          └──────▲──────┘          └─────────────┘
                 │
        ┌────────┼─────────┐
        │                  │
┌───────▼──────┐   ┌───────▼──────────┐
│  migracion   │ 3 │ identidad_y_hash │ 2                nivel 2
└───────▲──────┘   └───────▲──────────┘
        │                  │
        └────────┬─────────┘
                 │
  ╔══════════════╧════════════════════════════════════════════╗
  ║  O P E R A C I Ó N   ·  nudo de 11 ejes  ·  258 archivos  ║  nivel 1
  ║                                                           ║
  ║   op_almacen 46 ──┐                                       ║
  ║   op_documentos 45├─36/30/27──▶ (persistencia)            ║
  ║   op_modelos 45 ──┘                                       ║
  ║                                                           ║
  ║   op_aristas 22 ──19──▶ grafo 33 ──2──▶ indice 25         ║
  ║        └──18──────────────────────────────▲               ║
  ║                                                           ║
  ║   consulta 11 ◀──5── federacion 5    cache 6              ║
  ║   bitacora 10        semantica 10    enlaces*             ║
  ╚═══════════════════════════════════════════════════════════╝
                 ▲              ▲              ▲
                 │              │              │
        ┌────────┴───┐  ┌───────┴──────┐  ┌────┴─────┐
        │adaptadores │  │ recuperacion │  │ enlaces  │       nivel 0
        │     22     │  │      19      │  │    7     │
        └────────────┘  └──────────────┘  └──────────┘
         ast·argparse      puerto           nadie
            ·click        Embedder        depende
                                          de ellos
```

`*` `enlaces` aparece dos veces porque es nivel 0 y nada lo necesita; lo dibujé
dentro del nudo por cercanía temática y fuera por su lugar real.

---

## Cómo leerlo

**Nivel 0 = no depende de nadie.** Son hojas: `adaptadores`, `recuperacion`,
`enlaces`. Las tres se podrían extraer hoy.

**Nivel 5 = nadie depende de él hacia abajo.** `errores` es la base: todos lo
nombran y él no nombra a nadie.

**Las flechas apuntan hacia lo que se necesita.** El número es la cantidad de
imports.

---

## Los dos nudos

### El nudo del núcleo — 5 ejes, 61 archivos

`superficie` · `representacion` · `render` · `contrato` · `runtime`

Once aristas internas, y las que lo cierran pesan **1**:

| arista | peso |
|---|---|
| superficie → representacion | 9 |
| render → representacion | 7 |
| render → superficie | 5 |
| superficie → render | 3 |
| runtime → render | 3 |
| **representacion → superficie** | **1** |
| **render → runtime** | **1** |
| **render → contrato** | **1** |
| **contrato → runtime** | **1** |
| **runtime → superficie** | **1** |
| **runtime → contrato** | **1** |

Seis aristas de peso 1 sostienen el nudo entero. Las cinco pesadas van en una
sola dirección: hacia `representacion`.

**Esto es reparable.** Y es el mismo patrón de la Fase 0: una arista de peso 1
—`StoreError`— costaba 46 módulos.

### El nudo de operación — 11 ejes, 199 archivos

`op_almacen` · `op_documentos` · `op_modelos` · `op_aristas` · `grafo` ·
`indice_de_aristas` · `consulta` · `semantica` · `bitacora` · `cache` ·
`federacion`

45 aristas internas, de las cuales **26 pesan ≤2**. Medí cuánto se desarma al
ignorarlas:

| ignorando aristas de peso | resultado |
|---|---|
| ≤1 | 2 nudos, el mayor de **7** |
| ≤2 | 3 nudos, el mayor de **4** |
| ≤3 | 1 nudo de 4 |
| ≤5 | 1 nudo de 3 |
| ≤8 | 1 nudo de 2 |

**Las 26 aristas débiles convierten 11 ejes en un solo nudo.** Sin ellas queda un
núcleo irreducible de 4, que es la fusión real.

Ejemplos de las débiles:

```
cache          → consulta        1
cache          → op_aristas      1
cache          → op_documentos   1
cache          → semantica       1
semantica      → cache           1
federacion     → cache           1
```

`cache` tiene cuatro aristas de peso 1 hacia ejes que también lo usan. Un caché
que conoce a sus clientes está invertido: debería ser una hoja.

---

## Lo que el dibujo dice

**1. La identidad es un nudo, no una jerarquía.** Los cinco ejes que definen qué
es el sistema se necesitan mutuamente. No es necesariamente un defecto
—significado y superficie son dos caras de una cosa— pero significa que **no se
puede publicar `sldb-core` partido en piezas**. Va entero o no va.

**2. `persistencia` es el centro de gravedad y no es identidad.** 110 aristas
entran en él desde los ejes de operación. Es lo más usado del sistema y lo menos
definitorio.

**3. Hay tres hojas listas.** `adaptadores`, `recuperacion` y `enlaces` no
dependen de nada. `recuperacion` es la más interesante: 19 archivos, el eje mejor
diseñado, y extraíble hoy.

**4. El nudo grande se sostiene con alfileres.** 26 de sus 45 aristas internas
pesan 1 o 2, entre 258 archivos. Ninguna parece una decisión de diseño: son
conveniencias acumuladas.

**5. `errores` abajo explica R2.** El eje de excepciones está en el nivel más
profundo porque todos lo nombran. Por eso una excepción que heredaba del almacén
contaminaba el núcleo entero: estaba en la base y apuntaba hacia arriba.

---

## El DAG que sí existe

Condensando los dos nudos:

```
  errores
     ▲
  [núcleo: 5 ejes]
     ▲
  persistencia ── codec
     ▲
  migracion ── identidad_y_hash
     ▲
  [operación: 11 ejes]
     ▲
  adaptadores ── recuperacion ── enlaces
```

Seis niveles. Es un DAG legítimo, y es el que habría dibujado si no hubiera
comprobado los ciclos primero.

Vale la pena notar la diferencia: ese dibujo es **verdadero y engañoso a la vez**.
Verdadero porque el orden de dependencia existe; engañoso porque esconde que dos
de sus seis nodos son nudos de 5 y 11 ejes que no se pueden separar.

---

## Reproducirlo

```bash
python tools/check_axes.py --map        # ejes y acoplamiento
python tools/check_axes.py --dag        # niveles, nudos y aristas débiles
```
