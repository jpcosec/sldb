# Manual de Usuario y Especificación de Interfaz: SLDB Workbench

Este documento formaliza la experiencia de usuario, los flujos operativos y las reglas de diseño de la **UI Unificada de SLDB** (*Mindmup + Wiki + Spec2Viz + Model Studio*), basada en las vistas minimalistas de papel cálido (`#FAF9F6`) e ingeniería serena desarrolladas en Stitch y respaldadas por los contratos de `sldb`, `spec2viz` y `deskops`.

---

## 1. Filosofía de Diseño: "Mundo de Papel con Fierros Ocultables"

El problema histórico de las interfaces sobre SLDB era la sobrecarga cognitiva: mostrar puertos, hashes SHA-256, botones de estado REST y cajas de consola directamente en el área de lectura.

La UI unificada resuelve esto mediante tres principios:
1. **Estética Calmada y Monocromática**: Fondo papel cálido (`#FAF9F6`), panel izquierdo en piedra suave (`#F4F3EF`), tinta negra `#1A1A1A` y gris técnico `#73726E`. Sin luces de neón ni códigos de colores tipo semáforo.
2. **Conmutador de Lente Tridimensional**:
   - `Lectura`: Vista de prosa pura editorial (como en *iA Writer* o un libro).
   - `[ Estructura / Fierros ]`: Muestra los metadatos de SLDB en el gutter izquierdo (`field: ...`, `transclude: ...`, `spec2viz: ...`), los enlaces de origen y los diagramas incrustados.
   - `Esquema`: Abre el estudio de clases, contratos y plantillas reversibles del modelo activo.
3. **Acoplamiento Bidireccional Topología ↔ Prosa**:
   - Hacer clic en un nodo del árbol espacial a la izquierda enfoca el documento o la sección en la Wiki a la derecha.
   - Pasar el cursor sobre un bloque transcluido en la Wiki ilumina el nodo de origen en el árbol.

---

## 2. Marco: dónde viven estas vistas dentro de la UI de deskops

El producto es la UI de deskops. Las cuatro vistas de este manual son **superficies de documento**, no la aplicación: se abren desde el cascarón de deskops y vuelven a él.

1. **El cascarón** son las cinco vistas del contrato `deskops view` (`board`, `task`, `drawer`, `inbox`, `agents`; ver `deskops/docs/deskops-ui.md`). En `UIs/graph_ui` ya existen las pantallas de drawer e inbox (UI05) y de agentes y corridas (UI06).
2. **La entrada es el Board.** Una tarjeta del Board abre la vista `task` (gates, evidencia de closeout, próximas acciones). Desde ahí, el documento de la tarea, sus pills y sus átomos aterrizan en el **Workbench** con la lente `Lectura` activa. Un `ref` a un diagrama abre el **Inspector**; un `ref` a una fuente abre **Extracción y Anclaje**; la pestaña `Esquema` abre el **Studio** del modelo activo.
3. **Dos proveedores de datos, sin cálculo en la UI.** `sldb` entrega documentos, segmentos, grafo, notaciones y contratos de modelo (`/document`, `/document/segments`, `/notations/*`, `/models/*`). `deskops` entrega el estado de workflow (`deskops view task`, `deskops next`). Lo que una ficha muestra sobre una tarea (por ejemplo `2/2 gates ok` en el Inspector) sale de `deskops view`, nunca se recalcula leyendo el store.
4. **Aceptación sobre el desk real.** Los mocks usan el dominio `levira`. Cada vista se acepta renderizando documentos del desk real (una `TaskDoc` con un pill transcluido, un `SpecDoc` del catálogo de arquitectura) y se cronometra sobre ese desk antes de cerrarse. Un store de prueba no vale como evidencia.

---

## 3. Toda escritura es una operación con nombre

Ningún control de la UI escribe archivos. Cada acción que muta invoca exactamente una operación nombrada del CLI o del servidor del repo dueño, y la UI lo hace visible.

1. **Una acción, una operación.** Las escrituras sobre documentos y modelos van a `sldb` (`POST /save` con `expected`, `POST /models/*`, operaciones de anclaje). Las escrituras sobre el flujo de trabajo van a `deskops` (`add`, `edit`, `bind`, `advance`, `closeout`, `message`, `promote`, `retire`). La UI no compone escrituras a partir de varias operaciones ni emula una que falte.
2. **La lente Fierros muestra la operación.** Junto a cada control editable aparece el nombre de la operación que ejecutará (por ejemplo `POST /save · expected 74285b5` o `deskops advance task <id>`), y tras ejecutarla, su resultado: hash nuevo, estado nuevo o error accionable.
3. **La procedencia la escribe la operación.** El bloque `sldb` de cada documento registra `by`, `at`, `via` y `authority` (`docs/architecture/provenance.md`). El `via` es el nombre de la operación que escribió; la UI no inventa uno propio. Así el bloque de procedencia, `.deskops.log` y lo que se ve en pantalla cuentan la misma historia.
4. **⌘K es la superficie de los verbos de deskops.** La paleta lista cada verbo con su nombre de CLI y sus argumentos, y `deskops next` decide cuáles están disponibles para la tarea activa. Un verbo que no aplica se muestra deshabilitado con la razón, no se oculta.
5. **Escribir ensucia el working tree, y se muestra.** `.sldb/core` y `desk/` están versionados: todo guardado deja cambios sin commitear hasta que alguien commitea. La cabecera muestra `N cambios sin commitear` y el commit es una operación aparte, visible como cualquier otra.
6. **Si falta una operación, se pide.** Cuando la UI necesita una escritura que ningún CLI ofrece, se anota en el inbox del repo dueño con `deskops message send --kind unclear`. No se agrega un script ni un endpoint en la UI para salvar el hueco.

---

## 4. Autoridad de escritura por modelo

Cada modelo declara `__authority__` con uno de los cinco valores de `sldb` (`source_raw`, `authored`, `theorem`, `generated`, `cache`; ver `docs/architecture/provenance.md`), y `describe_model` lo expone (SV04). La UI decide qué se puede editar, y desde dónde, leyendo ese valor y el dueño del modelo. Nunca asume que un campo visible es editable.

| Autoridad | Comportamiento en la UI |
| :--- | :--- |
| `source_raw` | Solo lectura en toda lente. Es evidencia externa: solo se **ancla** sobre ella (vista 03). Editarla rompe todos los offsets de sus átomos. |
| `authored` | Editable in situ con `POST /save` y `expected`, salvo que el modelo sea de deskops (ver abajo). |
| `theorem` | Solo lectura. Muestra `from` (el código o documento del que deriva); editar significa ir a la fuente. |
| `generated` / `cache` | Solo lectura. Muestra la operación que lo regenera. |

**Segunda dimensión: el dueño del modelo.** Los modelos de deskops (`TaskDoc`, `BoardDoc`, `PillDoc`, `InboxNoteDoc`, `AtomDoc` del desk y sus especializaciones) se escriben solo con verbos de deskops, aunque sean `authored`. Para esos campos la UI muestra `gestionado por deskops` y ofrece el verbo correspondiente (por ejemplo `deskops edit task <id> <campo>`), no un campo editable. El dueño se deduce del módulo de origen que devuelve `describe_model`: modelos bajo `sldb.models` y `deskops` son builtin; los que viven en el `pythonpath` del repo son del store local.

**Transclusiones.** Un bloque transcluido hereda la autoridad del documento hijo, no del padre. Editar `atom-04#body` desde el informe aplica las reglas de `AtomDoc`. Si ese átomo está anclado a una fuente, la edición cambia su estado de anclaje a `changed`: la UI lo muestra como alerta ruidosa en la ficha, en la lente Fierros y en el panel de cobertura de la vista 03. No es un error y no bloquea; es una desviación declarada que alguien tiene que resolver.

**Studio.** Los modelos builtin de sldb y de deskops se muestran en solo lectura. Cambiar su contrato requiere una tarea en el repo dueño, porque altera el desk de todos. El Studio crea y promueve modelos del store local; `Validar Draft` y `Promover` muestran siempre el plan de backfill antes de aplicar.

---

## 5. Catálogo de Vistas y Pantallas

Las 4 vistas operativas están descargadas y guardadas localmente en [`docs/ui-workbench/screens/`](file:///home/jp/proyectos/SLDB_1/docs/ui-workbench/screens/):

| Vista | Archivo HTML / Captura | Propósito Principal |
| :--- | :--- | :--- |
| **01. Workbench Principal** | [`01_workbench.html`](file:///home/jp/proyectos/SLDB_1/docs/ui-workbench/screens/01_workbench.html) / [`01_workbench.png`](file:///home/jp/proyectos/SLDB_1/docs/ui-workbench/screens/01_workbench.png) | Navegación split: Árbol espacial (Mindmup) + Prosa Wiki con transclusiones vivas y diagramas embebidos. |
| **02. Inspector Spec2Viz** | [`02_spec2viz_inspector.html`](file:///home/jp/proyectos/SLDB_1/docs/ui-workbench/screens/02_spec2viz_inspector.html) / [`02_spec2viz_inspector.png`](file:///home/jp/proyectos/SLDB_1/docs/ui-workbench/screens/02_spec2viz_inspector.png) | Inspección de diagramas (`SpecDoc`) y nodos individuales (`SpecNodeDoc`), mostrando los átomos y código vinculados. |
| **03. Extracción y Anclaje** | [`03_extraccion_anchoring.html`](file:///home/jp/proyectos/SLDB_1/docs/ui-workbench/screens/03_extraccion_anchoring.html) / [`03_extraccion_anchoring.png`](file:///home/jp/proyectos/SLDB_1/docs/ui-workbench/screens/03_extraccion_anchoring.png) | Lector de texto fuente crudo (`FuenteDoc`), selección de tramos por offset y creación asistida de `AtomDoc` con chequeo de duplicados. |
| **04. Model & Notation Studio** | [`04_esquema_studio.html`](file:///home/jp/proyectos/SLDB_1/docs/ui-workbench/screens/04_esquema_studio.html) / [`04_esquema_studio.png`](file:///home/jp/proyectos/SLDB_1/docs/ui-workbench/screens/04_esquema_studio.png) | Editor interactivo de contratos de modelos (`StructuredNLDoc`), declaración de slots, plantilla `__template__` y promoción de drafts. |

---

## 6. Manual de Usuario: Flujos de Interacción

### Flujo 1: Navegar y Editar un Documento Compuesto (Workbench)
1. **Seleccionar Documento**: En el panel izquierdo, el nodo raíz (ej. `Informe Clínico Levira`) muestra sus ramificaciones hacia átomos y diagramas hijos.
2. **Edición In-Situ de Campos**:
   - Al posicionarse sobre un campo tipado (ej. `resumen`), aparece una línea vertical fina en el gutter izquierdo.
   - El usuario escribe el texto directamente.
   - Al confirmar (`Enter` o `⌘↵`), la UI envía `POST /save` a SLDB con el payload tipado y el `expected` hash. SLDB re-renderiza y garantiza que el round-trip sea 100% fiel; el cambio queda en el working tree hasta su commit (sección 3).
3. **Interacción con Bloques Transcluidos (`ref: "field"`)**:
   - Los párrafos que provienen de átomos (ej. `atom-04#body`) aparecen sangrados con un encabezado sutil: `atom-04.md → #body (AtomDoc · editable in-place) ↗`.
   - Modificar ese texto guarda la mutación directamente en el documento hijo (`atom-04.md`), reflejándose automáticamente en el documento padre sin desincronizar el store.

### Flujo 2: Navegar y Rastrear Diagramas Semánticos (Spec2Viz)
1. **Abrir un Diagrama**: Al hacer clic en un bloque de diagrama dentro del texto o seleccionarlo en el mapa, la pantalla conmuta al **Spec2Viz Inspector**.
2. **Hacer foco en una compuerta o paso**:
   - Al hacer clic en un nodo visual (ej. el rombo de decisión `< CrCl < 30 mL/min? >`), el canvas resalta la caja con un borde nítido.
   - En la barra inferior se indica la regla de notación aplicada (`GlyphDoc: activity.decision`).
3. **Inspeccionar la Wiki del Nodo (`SpecNodeDoc`)**:
   - En el panel derecho se despliega la ficha viva del nodo.
   - **Átomos Vinculados (`atom_refs`)**: Muestra los textos normativos o criterios médicos que justifican la existencia de esa compuerta en el flujo.
   - **Trazabilidad hacia Código y Tareas (`refs`)**: Permite saltar con un clic al símbolo Python (`PythonSymbolDoc: levira.rules.check_renal_clearance`) o a la tarea de Deskops (`TaskDoc`).

### Flujo 3: Extracción de Átomos sobre Texto Fuente (Anchoring)
1. **Cargar la Fuente**: Se abre un `FuenteDoc` (acta, prompt del sistema, folleto regulatorio).
2. **Seleccionar Texto Crudo**:
   - El usuario arrastra el cursor sobre cualquier frase o párrafo.
   - Se despliega automáticamente el popover de anclaje: calcula los offsets de inicio y fin (`body[640:755]`) y el rango de líneas.
   - Sugiere un slug de símbolo (ej. `atom-monitoreo-hepatico`).
3. **Prevención de Duplicados en Vivo**:
   - El sistema consulta silenciosamente `GET /corpus/rank?fields=1` en SLDB.
   - Si no hay duplicados, informa: `✓ Nuevo en el store (máx. similitud 34%)`.
   - Si detecta un fragmento similar (>75%), muestra el enlace al átomo existente para evitar fragmentación de conocimiento.
4. **Guardar Átomo**: Al presionar `[ Crear AtomDoc y Anclar ]`, SLDB registra el nuevo documento y dibuja inmediatamente la nueva rama en el árbol izquierdo.

### Flujo 4: Diseñar o Evolucionar un Modelo (`Model Studio`)
1. **Acceder a Esquema**: Desde cualquier documento, presionar la pestaña `[ Esquema ]` en la cabecera.
2. **Editar Declaración**:
   - Agregar o modificar campos en la tabla de `FieldDecl`.
   - Especificar si un campo es un valor escalar (`str`), una lista de referencias (`list[DocRef]`) o una proyección rica (`DocRef[SpecDoc]`).
   - Ajustar la plantilla `__template__` asegurando que cada campo tenga su slot `⸢rev•...⸥` o `⸢render•...⸥`.
3. **Validación y Promoción Segura**:
   - Presionar `[ Validar Draft ]`: SLDB ejecuta `validate_model_draft` contra todos los documentos existentes del store y reporta el plan de backfill.
   - Presionar `[ Promover ]`: Se aplica el cambio de contrato, se reindexa el store y se incrementa la versión del modelo sin intervención manual en terminal.

---

## 7. Atajos de Teclado y Ergonomía

- `⌘K`: Abrir paleta de comandos universal (búsqueda rápida de documentos por ID, símbolo, hash o modelo).
- `1` / `2` / `3`: Alternar entre lentes (`1`: Lectura, `2`: Estructura/Fierros, `3`: Esquema).
- `⌘↵` (en campo editable): Confirmar y guardar segmento (`POST /save`).
- `Esc`: Cancelar selección activa o cerrar popover de anclaje.
- `Tab` / `Shift+Tab`: Navegar entre campos editables consecutivos del documento.
