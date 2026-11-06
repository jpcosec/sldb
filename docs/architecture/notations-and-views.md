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
