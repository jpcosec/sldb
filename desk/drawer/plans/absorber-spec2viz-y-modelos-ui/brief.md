# Brief: absorber spec2viz en sldb y extender la autoría de modelos para la UI unificada

Fecha: 2026-11-06. Repo dueño: sldb. Estado: plan en drawer con tareas promovidas al Board (`SV01`–`SV04`). Complementa `grafo-operable` (P1) y `generalizar-desde-deskops` (P2).

## Encargo

Que el vocabulario visual, las notaciones, las paletas y el resolvedor de vistas de `spec2viz` (`resolve_view`, `resolve_documents`), así como la transclusión rica en `/document/segments` y la declaración/edición completa de contratos de modelo (`__containment__`, `__references__`, `__compositions__`, `__semantics__`), vivan nativamente en `sldb` (`sldb.models`, `sldb.api`, CLI y `sldb serve`), sin depender de un repositorio `spec2viz` separado ni de archivos YAML intermedios para proyectar y editar el grafo desde la UI unificada.

## Por qué ahora

- `UIs/graph_ui` y los stores del ecosistema importan `spec2viz.sldb_models` (`SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, `ViewDoc`) y `spec2viz.notation_view.resolve_view` / `resolve_documents`. Si `spec2viz` no está instalado o el store se sirve por `sldb serve` en modo remoto, las vistas de notación y proyección degradan con `501` o requieren adaptadores locales fuera de `sldb`.
- El contrato de notación (`spec2viz/docs/notation-contract.md`) opera exclusivamente sobre documentos del store y `sldb.api.where_matches`: es mecánica de proyección del store de `sldb`, no de un compilador externo.
- En `/document/segments`, los documentos necesitan transcluir campos de otros documentos (`CompositionSpec.ref == "field"`, tarea diferida `task-atom-como-field-tipado-composicion-por-field`) y proyectar bloques ricos (diagramas `SpecDoc`/`ViewDoc` ya resueltos y tablas estructuradas) directamente en el árbol de segmentos que consume la UI.
- `sldb.api.create_model` y `sldb.api.model_drafts` (y sus rutas `/models/*` en `sldb serve`) hoy solo permiten declarar y editar campos escalares/listas y `__template__`. La UI unificada necesita declarar y editar también `__containment__`, `__references__`, `__compositions__` y `__semantics__`, con validación de contrato en el draft y soporte de `backfill` en `POST /models/promote`.

## Resultado esperado del plan completo

1. **Modelos y catálogos builtin de vocabulario visual en `sldb` (SV01)**: `SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc` y `ViewDoc` viven en `sldb.models.notation_models` (reexportados en `sldb.models` y `sldb.api`), junto con el validador y cargador de paletas (`default.yml`, contraste WCAG) y las 8 notaciones builtin (`uml-class`, `statechart`, `component`, `deployment`, `uml-sequence`, `activity`, `component-view-matrix`, `reflection`) en `sldb.notations`. `resolve_model_ref` resuelve `spec2viz.sldb_models:<Model>` como alias compatible hacia `sldb.models.notation_models:<Model>`.
2. **Resolvedor de vistas de notación y proyección en `sldb.api`, CLI y `sldb serve` (SV02)**: `resolve_view`, `resolve_documents` y `evaluate_projection_view` viven en `sldb.api.notations`, leen directamente del store (aprovechando la proyección del índice de aristas cuando está disponible) y se sirven en `sldb notations ...` y en `GET /notations`, `GET /notations/view`, `POST /notations/resolve` y `GET|POST /views/projection*`.
3. **Transclusión por campo y segmentos ricos de diagramas/vistas en `/document/segments` (SV03)**: `CompositionSpec.ref == "field"` resuelve campos de otros documentos del store mediante un resolver inyectado; además, los segmentos con trait/composición de diagrama o vista (`SpecDoc`/`ViewDoc`) y tabla entregan en `DocumentSegments` la proyección ya resuelta (`resolved_view` / `table_data`) lista para dibujar inline en la UI.
4. **Autoría y edición draft completa de modelos para la UI (SV04)**: `create_model`, `describe_model`, `model_drafts` y las rutas `/models/*` de `sldb serve` declaran, describen, editan en draft, validan y promueven (con `backfill`) `__containment__`, `__references__`, `__compositions__`, `__semantics__` y `__authority__`, manteniendo sincronizados `__template__`, el índice semántico y el índice de aristas.
