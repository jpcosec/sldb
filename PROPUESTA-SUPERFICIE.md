# Propuesta: superficie de conocimiento sobre SLDB

Estado: borrador para revisión.
Fecha: 2026-09-28.
Reemplaza a `sldb/docs/requests/anchoring-surface-proposal.md`, escrito antes de
entender que `WikiPageDoc` ya es un modelo SLDB.

---

## 1. El problema

En cualquier proyecto, lo que se sabe está desparramado: correos, actas, PDFs, la
cabeza de dos personas.

Alguien escribe un documento para ordenarlo. Y pasa esto:

- la misma cosa queda escrita en tres documentos distintos
- cambia un dato, se actualiza en uno, y los otros dos quedan mintiendo
- nadie sabe de dónde salió lo que dice ahí
- a los seis meses nadie confía en el documento

Hoy la wiki MEPU es un build de una sola vía: `spec.yml + atoms → HTML`. Para
cambiar una palabra hay que editar un `.md` suelto, correr el build y refrescar.
Para saber de dónde salió un párrafo, hay que grepear.

## 2. La idea

**Separar los hechos de los documentos.**

Cada hecho se escribe una sola vez, en su propia ficha: una idea, un dato, una
decisión. Un documento no es un texto: es una **lista de qué fichas mostrar y en
qué orden**.

Hoy tenés cinco documentos con el mismo párrafo copiado cinco veces. Con esto
tenés una ficha que aparece en cinco documentos. La arreglás una vez y se arregló
en todas partes, porque no hay copias.

Eso es el medio del recorrido. El ciclo completo —de texto crudo a modelo— está
en §16.

## 3. Lo que SLDB ya resuelve

Esto no se construye desde cero. SLDB ya es el motor.

Un `StructuredNLDoc` declara un contrato —campos tipados, `__template__`,
`__containment__`, `__references__`— y de ese contrato se derivan tres
representaciones equivalentes: el documento Markdown, el índice del store y el
grafo. Ninguna es sustrato de otra.

| Pieza | Estado |
|---|---|
| Documentos tipados con round-trip verificado | existe |
| Direccionamiento `st.` / `se.` | existe |
| Grafo con networkx: centralidad, caminos, ciclos, vecindad, similitud | existe |
| Predicados: aristas con tipo declarado y validable | existe |
| DAG semántico de tags | existe |
| Diagnóstico de divergencia (`stores check`) | existe |
| Journal con cadena de hashes verificable | existe |
| `WikiPageDoc` como modelo SLDB con `__compositions__` | existe |

**Editar un atom y que la página compuesta se actualice: ya funciona.** Verificado
end-to-end: `compose_field` lee el archivo hijo en cada render, así que el padre
nunca guarda una copia del texto compuesto.

## 4. Lo que falta

Tres huecos, todos dentro de SLDB. Ninguno requiere construir un motor paralelo.

### H1 · Procedencia por fragmento en el IR

Para editar un bloque compuesto y que el cambio baje al atom, hace falta saber de
qué documento vino cada pedazo de texto.

No se trata de "extraer la composición" —eso sí es imposible, la composición
proyecta con pérdida—. Se trata de **registrar el mapa** y después editar el hijo
por dirección, que ya funciona.

`MeaningNode` y `SurfaceNode` **ya tienen `SourceSpan`**. Faltan cuatro piezas:

1. `compose_field` (`structured_doc.py:43`) tiene el path del hijo y su payload, y
   los descarta al devolver un string
2. no se registran los rangos de línea del fragmento expandido en el padre
3. el IR no tiene dónde guardarlo (haría falta `provenance` en `MeaningNode`)
4. el builder recibe el payload ya aplanado y nunca ve el modelo

Dificultad: media. Es plomería, no diseño.

### H2 · Composición por query

Hoy `__compositions__` exige `source_field`: una lista explícita de rutas. No se
puede decir "todos los hechos con tag `constraint:*`".

La maquinaria pesada ya está: `search()` con `search_in="semantic"`, índice
on-disk, DAG de tags. Faltan dos cosas: que el modelo conozca su `store_path`, y
un modo `query` en el spec.

Dificultad: baja-media.

Costo a decidir: el resultado deja de ser determinista respecto al documento. Hoy
el YAML lista ids y el documento dice exactamente qué contiene. Con query, el
contenido depende del estado del store.

### H3 · Identidad estable de sección

Una sección se direcciona por su path jerárquico de slugs. Títulos repetidos se
desambiguan por orden de aparición (`notas`, `notas-2`). Moverlas rompe las
direcciones; reproducido en vivo.

Ya está declarado como gap en `sldb/docs/documentation-review.md`.

**Nota:** la rama `refactor-target` tiene tres milestones sobre anchor states,
reconciliación ante drift y direccionamiento stand-off (UAX #29). Revisar antes de
diseñar nada.

## 5. Nota sobre `Corpus.rank()`

`Corpus` e `IndexProjection` existen pero **no tienen callers ni CLI**. Es código
sin cablear. Si la vista Bandeja necesita ranking por similitud, hay que conectarlo
o usar `graph similar`, que sí funciona.

---

## 6. Las vistas

Cinco vistas sobre el mismo store. No cinco apps.

### 6.1 · LECTOR — anclar sobre texto crudo

De acá nace el conocimiento: un PDF, un correo, un acta. El texto es inmutable; lo
que se construye encima son anclas.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ ◂ fuentes    RE_ Propuesta Solución MEPU.pdf          ▓▓▓▓▓░░░ 62% anclado │
├──────────────────────────────────────────┬─────────────────────────────────┤
│                                          │  SELECCIÓN                      │
│  ...el cliente manifiesta que no será    │  ┌───────────────────────────┐  │
│  posible una conexión directa a SAP.     │  │ "no será posible una      │  │
│ ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓  │  │  conexión directa a SAP"  │  │
│ ┃ La integración será vía archivos     ┃  │  └───────────────────────────┘  │
│ ┃ planos depositados en un directorio  ┃◂─┤  línea 47-48                   │
│ ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛  │                                 │
│  compartido. ⟦atom-mepu-architecture⟧    │  ╭─ convertir en hecho ───────╮ │
│                                          │  │ título                     │ │
│  El plazo de aceptación de una orden     │  │ ┌────────────────────────┐ │ │
│ ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   │  │ │MEPU: sin conexión SAP  │ │ │
│ ░es de 24 horas hábiles desde que ░░░░   │  │ └────────────────────────┘ │ │
│ ░░aparece en Mercado Público.░░░░░░░░░   │  │ tags                       │ │
│                                          │  │ [constraint:it-security ×] │ │
│  Respecto al stock, se debe cruzar       │  │ [+ agregar]                │ │
└──────────────────────────────────────────┴─────────────────────────────────┘
```

- `┏━━┓` texto ya anclado · `░░░` sin anclar · `⟦atom-…⟧` la matrícula
- La barra mide cuánto de la fuente ya es conocimiento

```
Lector
├── SourcePicker          lista de fuentes + % anclado
├── SourceText            texto inmutable
│   └── AnchorOverlay     tramos + chip + click → vista Atom
└── AnchorPanel           (al seleccionar)
    ├── SelectionQuote    cita + línea exacta → provenance
    ├── AtomDraftForm     título, tags sugeridos
    └── DuplicateWarning  similitud contra atoms existentes
```

### 6.2 · ATOM — el hecho en foco

El centro. Todos los caminos llegan acá, y es lo único que se edita de verdad.

```
┌────────────────────────────────────────────────────────────────────────────┐
│ ◂ volver                                            atom-mepu-architecture │
├────────────────────────────────────────────────────────────────────────────┤
│  MEPU architecture: file-based, no SAP connection                    ✎     │
│  ──────────────────────────────────────────────────────────────────────    │
│  La integración con SAP será vía archivos planos depositados en un         │
│  directorio compartido. No habrá conexión directa por restricción de       │
│  seguridad TI del cliente.                                           ✎     │
│                                                                            │
│  [system:lab-chile] [service:mercadopublico] [constraint:it-security]      │
│ ┌────────────────────────────────────────────────────────────────────────┐ │
│ │  ORIGEN  │  RELACIONES (3)  │  USOS (2)                                │ │
│ ├──────────┴──────────────────┴────────────────────────────────────────  │ │
│ │  RE_ Propuesta Solución MEPU.pdf · línea 47                            │ │
│ │  ┌──────────────────────────────────────────────────────────────────┐  │ │
│ │  │ ...el cliente manifiesta que no será posible una conexión        │  │ │
│ │  │ ▓La integración será vía archivos planos depositados en un▓      │  │ │
│ │  └──────────────────────────────────────────────────────────────────┘  │ │
│ │                                            [abrir en el Lector ▸]      │ │
│ └────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────┘
```

**RELACIONES** — cada arista con su motivo, porque es un documento:

```
│  ──grounded_by──▸  atom-no-sap-direct-constraint                          │
│     "restricción original del área de seguridad"                      ✎   │
│  ◂──flows_to────  atom-mepu-target-automation-scope                       │
│     "el alcance depende de esta decisión"                                 │
│  ──constrains──▸  atom-mepu-sap-finanzas-order-flow                       │
│                                                        [+ relacionar]     │
```

**USOS** — el aviso de impacto:

```
│  Este hecho aparece en 2 documentos:                                      │
│    › Visión general        → "Alcance acordado"       [ir]                │
│    › Acuerdos y decisiones → "Decisiones con cliente" [ir]                │
│  ⚠ editarlo cambia los dos.                                               │
```

```
AtomView
├── AtomHeader        título editable
├── AtomBody          contenido editable ── lo único que se edita de verdad
├── TagBar
└── Tabs
    ├── OriginTab     fuente + tramo resaltado
    ├── RelationsTab  aristas tipadas, motivo editable
    └── UsagesTab     composiciones que lo citan
```

### 6.3 · COMPOSITOR — armar un documento sin escribirlo

```
┌────────────────────────────────────────────────────────────────────────────┐
│ MEPU · Visión general                                    [previsualizar ▸] │
├───────────────────┬────────────────────────────────────────────────────────┤
│ SECCIONES         │  ## Objetivo del proyecto                              │
│                   │  ╭────────────────────────────────────────────────╮    │
│ ▸ Objetivo      2 │  │ ⠿ MEPU: alcance objetivo de automatización     │    │
│ ▸ Alcance       2 │  │   Procesar órdenes desde Mercado Público,      │ ⊗  │
│ ▸ Contexto      1 │  │   cruzarlas con stock y generar insumos SAP.   │    │
│                   │  ╰────────────────────────────────────────────────╯    │
│ [+ sección]       │  ╭────────────────────────────────────────────────╮    │
│                   │  │ ⠿ Objetivo central de la integración           │ ⊗  │
│ ─────────────     │  ╰────────────────────────────────────────────────╯    │
│ FUENTE            │              [+ agregar hecho]                         │
│                   │                                                        │
│  ◉ lista          │  ## Alcance acordado                    ⟨por consulta⟩ │
│  ○ consulta       │  ╭ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─╮     │
│                   │  ┆ tags: [constraint:*]  relacionado-con: mepu   ┆     │
│  esta sección     │  ┆ ───────────────────────────────────────────── ┆     │
│  lista hechos     │  ┆ 4 hechos, actualizado solo                    ┆     │
│  explícitos       │  ┆  · sin conexión directa a SAP                 ┆     │
│                   │  ┆  · PDFs en carpetas aceptadas/rechazadas      ┆     │
│                   │  ┆  · aceptación sólo tras entrega SAP           ┆     │
│                   │  ╰ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─╯     │
└───────────────────┴────────────────────────────────────────────────────────┘
   ⠿ arrastrar    ⊗ sacar (no borra el hecho)   ╭─╮ lista   ╭┄╮ consulta
```

La decisión de diseño que esta vista expone:

```
  ╭─────────╮  LISTA      yo elijo qué va          se queda quieto
  ╭┄┄┄┄┄┄┄┄┄╮  CONSULTA   el sistema decide        crece solo
```

`⊗` saca del documento, **no borra el hecho**. Ese matiz es el que hoy no existe y
hace que nadie borre nada por miedo.

Requiere **H2** para el modo consulta.

### 6.4 · BANDEJA — lo que anotaste sin saber dónde va

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Bandeja                                                    3 sin ubicar    │
├────────────────────────────────────────────────────────────────────────────┤
│ ╭──────────────────────────────────────────────────────────────────────╮   │
│ │ "el semáforo de vencimiento lo definieron en la reunión del 12,      │   │
│ │  quedó en 3 días pero hay que confirmarlo con Patricia"              │   │
│ │  escrito hace 2 días                                            ✎ ⊗  │   │
│ ├──────────────────────────────────────────────────────────────────────┤   │
│ │  se parece a:                                                        │   │
│ │   ▸ atom-mepu-expiry-semaphore-rule            87% ─ [es el mismo]   │   │
│ │   ▸ atom-order-lifecycle-sla-timing            41%                   │   │
│ │  iría en:                                                            │   │
│ │   ▸ Acuerdos › Reglas de negocio confirmadas   [ubicar acá]          │   │
│ │   ▸ Bloqueos › Preguntas abiertas              [ubicar acá]          │   │
│ │                        [ convertir en hecho ]  [ descartar ]         │   │
│ ╰──────────────────────────────────────────────────────────────────────╯   │
│                        [ + anotar algo ]                                   │
└────────────────────────────────────────────────────────────────────────────┘
```

Las sugerencias no son magia: **similitud** (`graph similar`) para los parecidos,
**vecindad** (`graph neighborhood`) para el destino. Análisis que ya existe.

### 6.5 · SALUD

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Salud del conocimiento                                    ⬤ 2 problemas    │
├────────────────────────────────────────────────────────────────────────────┤
│  ⬤  DIVERGENCIA                                                            │
│      › domain-cobranza-canal   texto cambió, campos no  → reformateo       │
│      › step-cobranza-respuesta campos cambiaron         → cambio real      │
│                                                        [reindexar]         │
│  ⬤  SIN ORIGEN     3 hechos sin provenance                                 │
│  ◯  AISLADOS       7 hechos sin ninguna relación                           │
│  ◯  CIRCULARES     ninguno                                                 │
└────────────────────────────────────────────────────────────────────────────┘
```

La distinción "texto cambió / campos cambiaron" sale del par
`source_hash`/`content_hash`, que `stores check` ya calcula.

---

## 7. Navegación

```
        ┌──────────┐
        │  LECTOR  │  texto crudo ──anclar──┐
        └──────────┘                        │
                                            ▼
    ┌──────────┐                      ┌──────────┐
    │ BANDEJA  │──promover───────────▸│   ATOM   │
    └──────────┘                      └──────────┘
                                            │
                                      se compone
                                            ▼
                                     ┌─────────────┐
                                     │ COMPOSITOR  │
                                     └─────────────┘
```

Todo camino llega al Atom. **Nadie edita un documento.**

## 8. Los tres verbos

| Gesto | Qué toca | Efecto |
|---|---|---|
| Corregir un dato | el **atom** | cambia en todos los documentos |
| Mover un bloque | el **documento** | el atom no se entera |
| Sacar un bloque | el **documento** | el atom sigue vivo |

## 9. Reglas que la implementación debe respetar

1. **Un bloque = un atom.** No fusionar, no partir.
2. **Editar escribe al atom**, con `content_hash` como `expected`. Si vuelve 409,
   mostrar conflicto; nunca pisar.
3. **Mover ≠ editar.** Mover reescribe la composición, no toca el atom.
4. **Solo `rev`/`optrev` son editables.** Los `render` se navegan. Sale del
   template del modelo, no de una decisión de UI.
5. **Avisar antes de editar un atom compartido** (pestaña USOS).
6. **Nunca escribir markdown.** Se escribe payload; SLDB renderiza y verifica el
   round-trip.
7. **No reimplementar** composición, resolución de referencias, índice inverso ni
   round-trip: SLDB los tiene.

## 10. Identidad del atom

Ver **§17**: el id no es un string plano sino la hoja de una ruta semántica, y la
jerarquía sale del DAG de tags en vez de repetirse en el nombre.

## 11. Fases

| # | Entrega | Criterio de aceptación | Depende de |
|---|---|---|---|
| 1 | Vista Atom read-only | abre un atom real de la KB con origen, relaciones y usos | — |
| 2 | Vista Atom editable | el cambio llega al `.md`; round-trip verificado | — |
| 3 | Conflictos | dos pestañas → la segunda recibe 409 y lo muestra | — |
| 4 | Compositor, modo lista | arrastrar reordena y reescribe la composición | — |
| 5 | Lector | anclar un tramo crea un atom con provenance | — |
| 6 | Edit-through desde la página | editar un bloque compuesto baja al atom | **H1** |
| 7 | Bandeja | promover un borrador a atom ubicado | 1, 4 |
| 8 | Salud | divergencias, aislados, ciclos | — |
| 9 | Compositor, modo consulta | una sección se llena por tag, con congelamiento | **H2** |

Las fases 1-5 y 8 **no requieren tocar SLDB**. Se pueden hacer hoy.

La composición se mantiene **determinista** en toda la primera vuelta (§18).

## 12. Dónde se monta

Decisión ya tomada (21/09): unificar bajo `sldb serve`. Tres superficies
hermanas, mismo backend:

- **graph-ui** — interfaz general basada en grafos sobre SLDB
- **spec2viz** — interfaz documental tipada en YAML sobre SLDB
- **esta** — interfaz de edición y composición sobre SLDB

Comparten launcher y configuración. No se mezclan los códigos.

## 13. Lo que esta propuesta no promete

- No resuelve H3 (identidad de sección). Lo declara y remite a `refactor-target`.
- No promete que la composición por query sea determinista; expone el costo.
- No incluye la vista Grafo: existe en graph-ui y no hay que duplicarla.
- No propone un servicio wiki nuevo. La composición vive en SLDB.
- No implementa la destilación de modelos desde anchors (§16.2): la declara como
  el tramo que falta.

## 14. Estado del prototipo actual

Rama `feat/prosemirror-surface`, worktree `hum-ecosystem-worktrees/pm-surface`.

Funciona: schema PM con vocabulario SLDB, traductor IR↔payload (33 tests),
separación frontmatter/body leída del template, `markerKind` real,
`sldb_readonly` para campos `render`, round-trip byte a byte contra
`domain-cobranza-canal` de la KB real.

No funciona: guardado sin control de concurrencia, el body markdown sigue siendo
texto plano (`ir.surface` sin usar), sin selector de store.

**Está construido sobre el objeto equivocado**: edita campos de *un* documento.
Esta propuesta lo reorienta al atom como unidad. Se rescata el schema, el
traductor y el criterio de editabilidad por template.

Detalle en `sldb-ui/docs/PM-SURFACE-PENDIENTES.md`.

---

## 15. El anchor: un tipo de documento más

### 15.1 · La corrección de encuadre

Un anchor **no es una anotación** ni un metadato sobre otra cosa. Es un
`StructuredNLDoc`, igual que un atom, con su contrato, su template, su lugar en el
store y su nodo en el grafo.

Lo mismo vale para el atom: `DomainAtom`, `RuleAtom`, `ConversationStep` son tipos
de documento, no categorías especiales del sistema. SLDB no conoce "atoms" ni
"anchors": conoce documentos gobernados por un contrato.

Esto importa para la superficie: **no hay que construir un editor de anchors y
otro de atoms**. Hay una superficie de documentos tipados, y el modelo decide qué
se ve y qué se edita.

### 15.2 · El contrato, tal como está hoy

`sldb/models/anchor_doc.py`. Existe, está registrado y resuelve contra el grafo.

~~~
---
id: ⸢rev•id⸥
symbol: ⸢rev•symbol⸥
kind: ⸢rev•kind⸥
ref: ⸢rev•ref⸥
tags: ⸢rev•tags⸥
provenance: ⸢optrev•provenance⸥
---

# ⸢render•symbol⸥

## Motive

⸢rev•motive⸥
~~~

| Campo | Qué es | Validación |
|---|---|---|
| `symbol` | el símbolo de gramática que define | libre |
| `kind` | qué clase de referente nombra | `model\|doc\|relation\|operation\|projection\|expr` |
| `ref` | el referente tipado | patrón por esquema (abajo) |
| `motive` | qué significa y por qué, en lenguaje natural | libre, obligatorio |
| `tags` | tags namespaced | `namespace:valor` |
| `provenance` | de dónde salió | opcional |

El docstring del modelo lo resume: *"Binds a grammar symbol to a semantic motive
and a resolvable referent."*

**Un anchor es una entrada de diccionario.** Dice: esta palabra, en este corpus,
significa esto, y acá está la razón.

### 15.3 · Los esquemas de `ref`

```
model:<Nombre>              un modelo
doc:<nombre>               un documento
edge:<rel>[:in|:out]       un tipo de relación, con dirección
op:<fn>                    una operación
fields:<f1,f2>             un conjunto de campos
view:<nombre>              una vista
expr:(<s-expression>)      una relación derivada, con huecos `_`
```

`anchor_targets.py` los resuelve a node ids del grafo; `ref_form.py` lee la
s-expression. Las dos piezas funcionan hoy.

Lo relevante para el ciclo: **un anchor puede apuntar a un modelo**, no solo a un
documento. Es lo que permite que la gramática hable de estructura, no solo de
contenido.

### 15.4 · El campo que sostiene todo: `motive`

Es lenguaje natural obligatorio, y no es decorativo. El docstring dice que existe
para *"keep the grammar legible and auditable"*.

Sin `motive`, un anchor es una asociación opaca —alguien decidió que esta palabra
apunta a este nodo, y no se sabe por qué—. Con `motive`, la gramática se puede
revisar, discutir y corregir.

Es la diferencia entre un índice y un diccionario.

---

## 16. El ciclo

```
  LENGUAJE NATURAL
  no organizado · sin estructura
        │
        │  anchors / refs
        ▼
  KB GRÁFICA  (atoms)
  organizado · sin estructura
        │
        │  composición   ──▶
        ◀──   indexación
        ▼
  MARKDOWN COMPUESTO  (fields de documentos)
  organizado · con estructura gobernada
        │
        │  azúcar sintáctico: anchors sobre el texto compuesto
        ▼
  TEXTO  ────────────▶  y los anchors acumulados
                         declaran un MODELO
```

| Capa | Organizado | Estructurado | Qué la habita |
|---|---|---|---|
| Lenguaje natural | ✗ | ✗ | PDFs, correos, actas |
| KB gráfica | ✓ | ✗ | atoms y sus relaciones |
| Markdown compuesto | ✓ | ✓ | documentos con contrato |

**Composición ↔ indexación es un par bidireccional**, no una flecha. Se baja
componiendo y se sube indexando. Esa es la respuesta al problema de edit-through:
no se trata de invertir el render, sino de indexar — operación que SLDB ya tiene.

### 16.1 · La espiral

El ciclo no vuelve al mismo punto. Cada vuelta deja un modelo que antes no
existía, y el texto siguiente nace más gobernado:

```
   texto sin contrato ──▶ anchors ──▶ regularidad ──▶ MODELO
                                                        │
   el próximo texto nace bajo ese contrato  ◂───────────┘
```

Los anchors que se repiten con el mismo `kind` son candidatos a campo. Suficientes
campos con posición estable son un `__template__`. Los anchors de `kind: relation`
son `__references__` / `__containment__`.

**El modelo no se escribe: se destila.** Y el `motive` de cada anchor es lo que
hace auditable la destilación — no es inferencia estadística, es una razón escrita
por alguien.

### 16.2 · Estado de cada tramo

| Tramo | Estado |
|---|---|
| Texto → anchors | contrato listo, **sin superficie** |
| Anchor → nodo del grafo | **funciona** (`anchor_targets.py`) |
| Atoms → composición | **funciona** (`__compositions__`) |
| Composición → indexación | **funciona** parcialmente; falta procedencia (H1) |
| Anchors → regularidad → modelo | **no existe** |

`core/ingest/` se retiró el 24/09 (commit `d0df139`): 9 módulos del producto
anterior, muertos e inimportables. No se perdió nada vivo, pero tampoco quedó nada
que haga esta vuelta.

---

## 17. Identidad: el id como nombre-hoja

### 17.1 · El problema real

Hoy conviven dos jerarquías que dicen lo mismo:

```
archivo:  domain/domain-cobranza-canal.md
tags:     domain:cobranza.canal
```

El prefijo `domain-cobranza-` del nombre **repite** lo que ya dicen la carpeta y el
tag. El id carga la jerarquía adentro, en vez de tomarla de su posición.

De ahí sale la contradicción aparente: si el id describe el contenido y el
contenido cambia, el id miente; pero corregirlo rompe las citas.

### 17.2 · La salida

El id no es un string plano: es **la hoja de una ruta semántica**.

| Capa | De dónde sale |
|---|---|
| Jerarquía | el DAG de tags (`domain:cobranza.canal`) |
| Hoja | el título del documento |

Si el contenido cambia, el título cambia, y la hoja cambia con él. No miente
nunca, porque lo que da identidad es la **posición en el DAG**, no el string.

SLDB ya tiene el DAG semántico y las direcciones `se.` para recorrerlo. La pieza
que falta es que la organización en disco lo refleje en vez de duplicarlo.

### 17.3 · Lo que queda abierto

Si una hoja cambia de rama —se le corrige el tag—, ¿qué pasa con las citas que la
nombraban por su ruta anterior?

Es el mismo problema que **H3**, un nivel más arriba: direccionamiento estable
frente a reubicación. Conviene resolverlos juntos, y mirar antes la rama
`refactor-target` de SLDB (anchor states, reconciliación ante drift, stand-off).

---

## 18. Composición determinista

**Decisión tomada: por ahora la composición es determinista.** Listas explícitas
de atoms; el documento dice exactamente qué contiene.

La composición por query (**H2**) queda fuera de la primera vuelta. Cuando se
incorpore, debe traer congelamiento: resolver la consulta una vez, dejarla escrita
y que no se mueva sola.

Esto cambia el orden de las fases: la fase 6 (modo consulta) pasa al final, y el
Compositor de la fase 4 arranca solo con listas.
