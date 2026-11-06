# Alcance y estado de partida

## Estado de partida verificado (2026-11-06)

- **En `spec2viz` (`/home/jp/proyectos/SLDB_1/spec2viz/spec2viz/`)**:
  - `sldb_models.py` (433 líneas): define `SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, `ViewDoc` como subclases de `sldb.api.StructuredNLDoc`.
  - `palette.py` (205 líneas) + `palettes/default.yml`: define `PaletteSpec`, `ThemeColor`, `IconSet`, `KindStyle`, `resolve_color`, `contrast`, `luminance`, `check_palette` (WCAG 1.4.11 >= 3:1 y AA >= 4.5:1) y `load_palette`.
  - `notation.py` (387 líneas) + `notations/*.yml` (8 archivos YAML): define `NotationSpec`, `GlyphSpec`, `LinkSpec`, `MarkerSpec`, `SHAPES`, `TERMINALS`, `DRAW_KINDS`, `LINE_KINDS`, `LAYOUT_KINDS`, `DEFAULT_NOTATIONS`, `KNOWN_RELATIONS`, `check_notation_style` y `load_notation`.
  - `styling.py` (89 líneas): define `resolve_style` (precedencia glifo > `style.kinds` del spec > paleta) y `resolve_line_color`.
  - `notation_view.py` (329 líneas): define `resolve_view(store, spec_ref)`, `resolve_documents(store, notation_ref, doc_refs, ...)`, `ViewError`, `flatten`, `lookup`, `render_template`, `render_keyword`, `fragments_of`, `fragment_kind`.
  - `sldb_sync.py` (886 líneas): `PaletteSync`, `NotationSync` y `SpecSync` que escriben `PaletteDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `SpecDoc`, `SpecNodeDoc` y `RelationDoc` usando `sldb.api`.
- **En `sldb` (`/home/jp/proyectos/SLDB_1/sldb/src/sldb/`)**:
  - `models/`: contiene `StructuredNLDoc`, `RelationDoc`, `RelationTypeDoc`, `SurfaceDoc`, `CliCommandDoc`, `PythonSymbolDoc`, `AnchorDoc`, `CodeAnchorDoc`. No contiene los modelos de vocabulario visual ni `ViewDoc`.
  - `api/segments/`: `build_document_segments.py`, `composition_piece.py`, `composition_spec.py`, `field_segment.py`, `segment_nodes.py`. `CompositionSpec` ya declara `ref: Literal["document", "field"] = "document"`, pero `StructuredNLDoc.compose_field` solo resuelve rutas de archivos (`ref == "document"`). No hay enriquecimiento de segmentos para diagramas (`SpecDoc`/`ViewDoc`) ni tablas estructuradas en `FieldSegment`.
  - `api/model_create/`: `create_model.py`, `field_decl.py`, `model_source.py`, `model_check.py`. Solo acepta `name`, `fields`, `template`, `base`, `target_package`. No genera `__containment__`, `__references__`, `__compositions__`, `__semantics__` ni `__authority__`.
  - `api/model_drafts/`: `field_drafts.py`, `template_drafts.py`, `draft_contract.py`, `draft_validation.py`, `backfill.py`. Solo edita fields y `__template__`; `validate_template_contract` solo verifica que los marcadores del template existan en `model_fields`. `cli/serve/models_routes.py` expone `/models`, `/models/detail`, `/models/fields-add`, `/models/fields-remove`, `/models/template-edit`, `/models/validate` y `/models/promote` (sin pasar `backfill` ni exponer `/models/create` ni `/models/metadata-edit`). `describe_model` (`ModelDescription`) no devuelve `containment`, `references`, `compositions`, `template` ni `has_draft`.

## Coordina con planes hermanos

| Nodo | Relación con `grafo-operable` (P1) y `generalizar-desde-deskops` (P2) |
|---|---|
| SV01 | Independiente. Registra los modelos de vocabulario visual y `ViewDoc` en `sldb.models.notation_models` y mantiene el alias compatible `spec2viz.sldb_models:*` en `resolve_model_ref`. `ViewDoc` conserva los campos de proyección de grafo (`nodes`, `relations`, `direction`, `notation`, `layout`) y admite opcionalmente `params` y `sections` para converger sin conflicto con `GD25`. |
| SV02 | Consume `SV01`. Coordina con `GO04` (si la proyección de payload está presente en el índice de aristas, `evaluate_projection_view` puede leer de ella; si no, cae a `load_runtime_documents`) y con `GD25` (las rutas de proyección de grafo viven bajo `/notations/*` y `/views/projection*`, dejando `/views/<name>` libre para las vistas tabulares/compuestas de `GD25`). |
| SV03 | Consume `SV02` (para adjuntar `resolved_view` en segmentos de diagrama/vista) y resuelve la tarea diferida del drawer `task-atom-como-field-tipado-composicion-por-field`. |
| SV04 | Independiente de `SV01`–`SV03`. Coordina con `GO04` (la firma de contrato de `GO04` ya incluye `fields`, `references`, `containment`, `compositions`; al promover un draft con cambios en esos atributos en `SV04`, `reindex_model` actualiza el contrato y los índices). |

## Orden de ejecución

1. **En paralelo (sin dependencias entre sí)**:
   - `SV01`: Modelos de vocabulario visual (`SpecDoc`, `SpecNodeDoc`, `NotationDoc`, `GlyphDoc`, `LinkDoc`, `PaletteDoc`, `ViewDoc`), paletas y notaciones builtin en `sldb`.
   - `SV04`: Declaración y edición draft de `__containment__`, `__references__`, `__compositions__` y `__semantics__` en `create_model`, `model_drafts`, CLI y `sldb serve`.
2. **Tras `SV01`**:
   - `SV02`: Resolvedor `resolve_view`, `resolve_documents`, `evaluate_projection_view` y `NotationSync`/`PaletteSync` en `sldb.api.notations`, CLI (`sldb notations`) y `sldb serve` (`/notations/*`, `/views/projection*`).
3. **Tras `SV02`**:
   - `SV03`: Transclusión de campos (`ref: "field"`) y segmentos ricos de diagramas/vistas y tablas en `/document/segments`.
