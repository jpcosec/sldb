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

Hoy el id es descriptivo y editable: `atom-mepu-architecture-file-based-no-sap-connection`.

Dos problemas: describe el contenido, así que cuando el hecho cambia el id miente;
y si se corrige, rompe todo documento que lo citaba.

**Propuesta:** el id es matrícula, no nombre. Opaco, inmutable, invisible para el
usuario. El título es lo que se lee.

**Costo:** el YAML del documento deja de ser legible a ojo. Se compensa mostrando
títulos en la interfaz, pero es un cambio real.

**Decisión pendiente.**

## 11. Fases

| # | Entrega | Criterio de aceptación | Depende de |
|---|---|---|---|
| 1 | Vista Atom read-only | abre un atom real de la KB con origen, relaciones y usos | — |
| 2 | Vista Atom editable | el cambio llega al `.md`; round-trip verificado | — |
| 3 | Conflictos | dos pestañas → la segunda recibe 409 y lo muestra | — |
| 4 | Compositor, modo lista | arrastrar reordena y reescribe la composición | — |
| 5 | Lector | anclar un tramo crea un atom con provenance | — |
| 6 | Compositor, modo consulta | una sección se llena por tag | **H2** |
| 7 | Edit-through desde la página | editar un bloque compuesto baja al atom | **H1** |
| 8 | Bandeja | promover un borrador a atom ubicado | 1, 4 |
| 9 | Salud | divergencias, aislados, ciclos | — |

Las fases 1-5 y 9 **no requieren tocar SLDB**. Se pueden hacer hoy.

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
