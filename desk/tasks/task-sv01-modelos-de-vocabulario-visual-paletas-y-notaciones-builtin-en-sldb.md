---
id: task-sv01-modelos-de-vocabulario-visual-paletas-y-notaciones-builtin-en-sldb
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/models/notation_models.py
- src/sldb/models/__init__.py
- src/sldb/notations/__init__.py
- src/sldb/notations/palette.py
- src/sldb/notations/notation.py
- src/sldb/notations/styling.py
- src/sldb/notations/palettes/default.yml
- src/sldb/notations/builtin/activity.yml
- src/sldb/notations/builtin/component-view-matrix.yml
- src/sldb/notations/builtin/component.yml
- src/sldb/notations/builtin/deployment.yml
- src/sldb/notations/builtin/reflection.yml
- src/sldb/notations/builtin/statechart.yml
- src/sldb/notations/builtin/uml-class.yml
- src/sldb/notations/builtin/uml-sequence.yml
- src/sldb/api/model_registry/model_reference.py
- src/sldb/api/__init__.py
- docs/architecture/notations-and-views.md
- CHANGELOG.md
- tests/notations/test_notation_models_and_builtins.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# SV01: Modelos de vocabulario visual, paletas y notaciones builtin en sldb

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo SV01 del plan desk/drawer/plans/absorber-spec2viz-y-modelos-ui (dag.yaml rev 1). UIs/graph_ui y los stores del ecosistema importan spec2viz.sldb_models y las notaciones/paletas builtin de spec2viz; absorberlos en sldb elimina la dependencia hacia spec2viz para abrir, validar y servir diagramas, notaciones y vistas desde el store.

## Goal

_Describe the concrete result this task must produce._

Los siete modelos de vocabulario visual y proyeccion (SpecDoc, SpecNodeDoc, NotationDoc, GlyphDoc, LinkDoc, PaletteDoc, ViewDoc) viven en sldb.models.notation_models (reexportados en sldb.models y sldb.api); palette.py, notation.py y styling.py junto con default.yml y las 8 notaciones builtin viven en sldb.notations; resolve_model_ref traduce spec2viz.sldb_models:<Model> a sldb.models.notation_models:<Model>.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/models/notation_models.py, src/sldb/models/__init__.py, src/sldb/notations/__init__.py, src/sldb/notations/palette.py, src/sldb/notations/notation.py, src/sldb/notations/styling.py, src/sldb/notations/palettes/default.yml, src/sldb/notations/builtin/*.yml (uml-class, statechart, component, deployment, uml-sequence, activity, component-view-matrix, reflection), src/sldb/api/model_registry/model_reference.py (alias compatible spec2viz.sldb_models:*), src/sldb/api/__init__.py, docs/architecture/notations-and-views.md, CHANGELOG.md y tests/notations/test_notation_models_and_builtins.py. Fuera: el resolvedor resolve_view / resolve_documents y las rutas HTTP (SV02), y los compiladores PlantUML/Mermaid/D2 estaticos de spec2viz.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 1, SV01): (1) Crear src/sldb/models/notation_models.py con SpecDoc, SpecNodeDoc, NotationDoc, GlyphDoc, LinkDoc, PaletteDoc y ViewDoc (subclases de StructuredNLDoc con los mismos campos, templates, __semantics__, __references__, __containment__ y validadores de spec2viz/spec2viz/sldb_models.py; ViewDoc incluye ademas params y sections opcionales con default_factory=list para converger sin conflicto con GD25). Reexportarlos en sldb.models y sldb.api. (2) Crear src/sldb/notations/ con palette.py (PaletteSpec, ThemeColor, IconSet, KindStyle, resolve_color, contrast, luminance, check_palette con WCAG 1.4.11 >= 3:1 y AA >= 4.5:1, builtin_palettes, resolve_palette, load_palette, palette_ref), notation.py (GlyphSpec, LinkEndSpec, LinkSpec, MarkerSpec, NotationSpec, DEFAULT_NOTATIONS, KNOWN_RELATIONS, ANY_RELATION, DRAW_KINDS, LINE_KINDS, TERMINALS, LEVELS, SHAPES, LAYOUT_KINDS, builtin_notations, resolve_notation, load_notation, check_notation_style, notation_palette, notation_ref, glyph_ref, link_ref) y styling.py (PROPERTIES, resolve_style con precedencia glifo > style.kinds del spec > paleta, resolve_line_color), mas los YAMLs en src/sldb/notations/palettes/default.yml y src/sldb/notations/builtin/*.yml. (3) En src/sldb/api/model_registry/model_reference.py, mapear el prefijo spec2viz.sldb_models: a sldb.models.notation_models: para que cualquier store con modelos registrados desde spec2viz resuelva sin spec2viz instalado.

## Validation

_List the checks required before this task can close._

- pytest tests/notations/test_notation_models_and_builtins.py -q sin fallos ni saltados
- resolve_model_ref("spec2viz.sldb_models:NotationDoc") devuelve sldb.models.notation_models.NotationDoc
- load_palette("default") y load_notation para las 8 notaciones builtin validan sin errores

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de SV01 cumplida, tests en verde, G_SV_MODELS satisfecho en dag.yaml.
