## REFORMULACION

**Propósito:** que el `SpecDoc` sincronizado conserve las claves de `data` del spec YAML que no son elementos (p. ej. `data.entity`), además del `style` que ya guarda, y que la vista resuelta incluya ese `style`.

**Resultado:** campo `data: dict[str, Any] = Field(default_factory=dict)` en `src/sldb/models/notation/spec_doc.py` con marcador en `__template__` y render/extract reversibles; escritura en `src/sldb/api/notations/spec_sync_docs.py`; tests de round-trip en `tests/notations/test_spec_sync.py` y de `style` en la vista resuelta; línea en `CHANGELOG.md` bajo `## 0.1.13 — not released yet`.

**Repo:** SLDB_1. **Límites:** no reexportar clases, no cambiar el YAML de specs, no migrar `docs.models:SpecDoc`; commit y push son del coordinador.

## AMBIGUEDADES

1. "con un marcador de bloque YAML en la plantilla del modelo igual al que use style en spec_doc.py (copiar su forma)": `style` usa `⸢optrev•style⸥`, un escalar, no un bloque; obligaría a inventar la sintaxis de bloque.
2. "toda otra clave de data se guarda en el campo nuevo": no se enumera qué claves son "elementos" por `diagram_type` (`states`, `steps`, `participants`, `views`, `connections`…); obligaría a inventar la lista o el criterio dinámico.
3. "el resolvedor de vistas en sldb.api.notations" / "resolve_view (sldb.api.notations)": no se da firma, módulo exacto ni forma de la vista; obligaría a inventar el contrato del test.
4. "render y extract reversibles en la plantilla del modelo": no se dice cómo serializar el dict (bloque, JSON inline); obligaría a inventar el formato.
5. `tests/notations/test_spec_catalog_sync.py` figura en validación pero no en `files` ni en el bundle; obligaría a asumir que existe y pasa.
6. ¿`style` vive en la raíz del spec o dentro de `data`? Si es lo segundo, el campo nuevo lo duplicaría; no se aclara.

## DRY-RUN

**Lecturas:** nota de origen en `desk/inbox/…`, `spec_doc.py` (campo `style`, plantilla), `spec_sync_docs.py` (`upsert_spec_doc`, `spec_style_kinds`), resolvedor en `sldb.api.notations`, `tests/notations/test_spec_sync.py` (fixtures `project`, `FLOW` con `entity`).

**Cambios previstos:** campo + marcador; payload en `upsert_spec_doc`; test de round-trip y de `style`; CHANGELOG.

**Dependencias:** existencia real de `resolve_view`, helper de store de prueba, formato de marcador existente.

**Validaciones futuras:** los tres comandos listados; `git status` limpio; commit del coordinador.

## FUTURO

El coordinador ejecuta `deskops closeout commit` y el aviso al repo; un humano decide la migración de `SpecDoc` de `docs.models`; otra tarea reexporta clases en `sldb.api.notations`; si un test de `test_spec_loader.py` falla, se decide tocarlo.
