# Notaciones, Vocabularios Visuales y Vistas de Proyección en SLDB

## 1. Contexto y Justificación

Históricamente, los modelos de especificación visual de diagramas y proyección (`SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, `ViewDoc`) y el motor de carga y validación de notaciones y paletas residían en la biblioteca `spec2viz`.

Esta separación causaba una dependencia circular y obligatoria hacia `spec2viz` en el ecosistema (por ejemplo, `graph_ui` o stores que alojan diagramas y vistas portables). Si `spec2viz` no estaba instalado en el entorno donde se ejecutaba `sldb` o un store se servía remotamente vía `sldb serve`, las operaciones sobre diagramas o la carga de modelos registrados degradaban o requerían adaptadores ad-hoc.

La absorción en `sldb` (iniciada en el nodo SV01 del plan `absorber-spec2viz-y-modelos-ui`) centraliza en `sldb` el vocabulario visual, las paletas, las 8 notaciones builtin y la capacidad de resolver referencias legacy sin depender de `spec2viz`.

---

## 2. Modelos de Vocabulario Visual (`sldb.models.notation_models`)

Los 7 modelos son subclases de `StructuredNLDoc` (`sldb.models.structured_nl_doc.StructuredNLDoc`) y se reexportan tanto en `sldb.models` como en `sldb.api`:

1. **`SpecDoc`**: Representa una especificación de diagrama completa como documento del almacén. Sus elementos hijos se vinculan mediante referencias hacia `SpecNodeDoc`, y apunta opcionalmente a una `NotationDoc`.
2. **`SpecNodeDoc`**: Elemento individual de un diagrama (nodo, componente, estado, clase, participante, actor). Declara contención (`__containment__ = {"contains": ["SpecNodeDoc"]}`) y referencias (`spec`, `refs`, `atom_refs`).
3. **`NotationDoc`**: Define una notación visual (tipo de diagrama, nivel `types`/`instances`/`both`, layout, marcadores, lista de `GlyphDoc` y `LinkDoc`, y paleta opcional).
4. **`GlyphDoc`**: Mapeo declarativo de un modelo del store (con predicado `where` opcional) a una forma visual primitiva (`shape`), compartimentos, etiquetas (`label`, `keyword`, `label_style`), y estilo (`kind`, `fill`, `stroke`, `icon`).
5. **`LinkDoc`**: Mapeo de una relación del store (arista o modelo reificado) a su representación gráfica (`line`, terminales `source_end` / `target_end`, rótulos y color).
6. **`PaletteDoc`**: Definición de paleta de colores (`backgrounds` e `ink` por tema claro/oscuro), catálogo de iconos y tokens de estilo semánticos por `kind`.
7. **`ViewDoc`**: Vista de proyección declarativa y portable sobre el grafo del almacén (`nodes`, `relations`, `direction`, `notation`, `layout`).

### Convergencia con GD25 en `ViewDoc` (SV-D3)
`ViewDoc` conserva los campos de proyección de grafo y añade soporte para vistas compuestas mediante dos campos opcionales:
- `params: dict = Field(default_factory=dict, description="Parametros opcionales de vista compuesta (GD25).")`
- `sections: list = Field(default_factory=list, description="Secciones opcionales de vista compuesta (GD25).")`

Ambos campos cuentan con validadores para inicializar `dict` y `list` respectivamente cuando se omiten en documentos existentes, preservando total compatibilidad hacia atrás en extracción y renderizado de plantillas.

---

## 3. Resolución y Retrocompatibilidad de Referencias (SV-D2)

Para garantizar compatibilidad inmediata con almacenes creados previamente cuyas configuraciones `.sldb/store.yaml` o `.sldb/core/store_index.yaml` registran modelos bajo el prefijo legacy:

```python
from sldb.api import resolve_model_ref

model = resolve_model_ref("spec2viz.sldb_models:NotationDoc")
# Retorna sldb.models.notation_models.NotationDoc
```

En `sldb.api.model_registry.model_reference`, cualquier referencia que utilice el módulo `spec2viz.sldb_models` se redirige transparentemente al módulo canónico `sldb.models.notation_models`.

---

## 4. Motor de Notaciones y Paletas (`sldb.notations`)

El submódulo `sldb.notations` expone:

- **Paletas (`palette.py`)**:
  - `PaletteSpec`, `ThemeColor`, `IconSet`, `KindStyle`.
  - Carga y validación semántica (`check_palette`) con verificación estricta de contraste WCAG:
    - Contraste gráfico WCAG 1.4.11 $\ge 3:1$ entre trazo y fondo por tema.
    - Contraste de texto WCAG 2.2 AA $\ge 4.5:1$ entre tinta y relleno por tema.
  - Resolución de colores (`resolve_color`) admitiendo tokens de paleta, pares `{light, dark}` o hex `#rrggbb`.
  - Paleta builtin `default` en `sldb/notations/palettes/default.yml`.

- **Notaciones (`notation.py`)**:
  - `NotationSpec`, `GlyphSpec`, `LinkSpec`, `MarkerSpec`.
  - Validación de formas primitivas (`SHAPES`), terminales (`TERMINALS`), tipos de diagrama (`DiagramType`) y relaciones esperadas por tipo (`KNOWN_RELATIONS`).
  - Las 8 notaciones builtin incluidas en `sldb/notations/builtin/`:
    - `uml-class.yml` (class)
    - `statechart.yml` (state)
    - `component.yml` (component)
    - `deployment.yml` (deployment)
    - `uml-sequence.yml` (sequence)
    - `activity.yml` (activity)
    - `component-view-matrix.yml` (component_view_matrix)
    - `reflection.yml` (reflection)

- **Resolución de Estilo (`styling.py`)**:
  - `resolve_style(glyph, kind, spec_kinds, palette)`: Resuelve propiedades visuales (`fill`, `stroke`, `icon`) aplicando la precedencia estricta:
    $$\text{Glifo de la notación} > \text{Spec kinds} > \text{Paleta de la notación}$$
  - `resolve_line_color(link, palette)`: Resuelve el color de línea en función de la paleta.

---

## 5. Resolvedor de Vistas y Vistas de Proyección (`sldb.api.notations`)

A partir de SV02, `sldb.api` provee los intérpretes canónicos del contrato de notación y de vistas proyectivas sin depender de librerías externas:

### 5.1 Resolvedor de Vistas (`notation_view.py`)
- `resolve_view(store, spec_ref, pythonpath=None)`:
  - Lee el `SpecDoc` del store, valida su coincidencia con `NotationDoc.diagram_type` y resuelve los nodos, aristas y leyendas.
  - Retorna `{spec, title, diagram_type, notation, palette, level, layout, nodes, links, fragments, skipped, legend}`.
- `resolve_documents(store, notation_ref, doc_refs, *, relation_refs=None, spec_style=None, pythonpath=None)`:
  - Aplica la notación a cualquier conjunto de documentos del store sin requerir un `SpecDoc`.
  - Casado de glifos por modelo + evaluación de predicado `where` sobre el payload aplanado (`flatten()`).
  - Extracción de compartimentos con rutas punto (`data.attributes`, `data.methods`).
  - Interpolación de plantillas `{campo}` y estereotipos `keyword` (`«{kind}»`) sin dejar variables huérfanas.
  - Detección y agrupamiento de fragmentos UML consecutivos (`fragments_of()`) por operador `data.group`.
  - Generación de leyenda completa (`glyphs`, `links`, `kinds`).

### 5.2 Vistas de Proyección (`projection_view.py`)
- `evaluate_projection_view(store, view_or_ref, pythonpath=None)`:
  - Evalúa la consulta de nodos (`[{model, where}]`) y aristas (`RelationFilter(relations, direction)`) sobre el grafo del almacén.
  - Si la vista especifica una `notation`, invoca `resolve_documents` y adjunta estilo para nodos (`styled_nodes`), aristas (`edge_styles`), `ink` de paleta por tema y `legend`.
- `list_projection_views(store, pythonpath=None)`:
  - Lista todos los `ViewDoc` registrados en el almacén.
- `save_projection_view(store, name, view, pythonpath=None, actor=None)`:
  - Guarda o actualiza un `ViewDoc` en el almacén bajo `sldb/views/<name>.md`.

### 5.3 Sincronización al Almacén (`notation_sync.py`)
- `sync_palette(store, name_or_path="default")`:
  - Escribe el `PaletteDoc` correspondiente en `sldb/palettes/` y registra modelos si hiciera falta.
- `sync_notation(store, name_or_path)`:
  - Escribe `NotationDoc`, `GlyphDoc`, `LinkDoc` y sus `RelationTypeDoc` asociados en `sldb/notations/<name>/`, además de su paleta vinculada.

---

## 6. Superficie CLI y HTTP Serve

### 6.1 CLI (`sldb notations`)
Disponible con envelope JSON (`sldb --envelope notations ...`):
- `sldb notations list [--views]`: Lista las notaciones y paletas builtin y registradas en el store (o las vistas proyectivas si se indica `--views`).
- `sldb notations sync [--notation <name|path>] [--palette <name|path>]`: Sincroniza notaciones o paletas en el store.
- `sldb notations view <spec> [--projection]`: Resuelve la vista de un `SpecDoc` o evalúa una proyección (`--projection`).
- `sldb notations resolve --notation <notation> --docs <Model:name ...>`: Resuelve un conjunto arbitrario de documentos bajo una notación.

### 6.2 HTTP Serve (`sldb serve`)
- `GET /notations`: Lista notaciones y paletas builtin y del store.
- `GET /notations/view?spec=<spec_ref>`: Resuelve un `SpecDoc`.
- `POST /notations/resolve`: Resuelve un conjunto de documentos `{notation, docs, [relations], [style]}`.
- `GET /views/projection`: Lista los `ViewDoc` del store.
- `GET /views/projection/evaluate?view=<ref>`: Evalúa una vista proyectiva por referencia.
- `POST /views/projection/evaluate`: Evalúa una vista proyectiva pasada en el body JSON.
- `POST /views/projection/save`: Guarda un `ViewDoc` `{name, view}`.
