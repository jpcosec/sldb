## REFORMULACION

**Propósito**: ampliar `StoreDeclaration` con `folders` y `seeds` y añadir `sldb.api.scaffold_store(store, *, declaration=None, apply=False, template_root=None)` idempotente (reporte `created/rewritten/present/conflicts`); mover `build_store` a `sldb.api`, encadenando `apply_declaration` y luego scaffold; CLI `stores scaffold [--apply]` y sección `scaffold` en `stores build`; doc y CHANGELOG.

**Resultado**: el "Done When" del TaskDoc (carpetas, semilla text if_missing, file managed, document con track, segunda corrida todo `present`, `pkg:` resuelto, `declaration=` sin tocar store.yaml, clave desconocida falla, golden de build intacto).

**Repo**: sldb, worktree aparte en robocop2, base `6b80df36` de main; superficie en `files`/OUTPUT_SCOPE.

**Límites**: sin nombres deskops en `src/sldb/` (regla 4); salidas CLI/serve existentes sin cambio (regla 5); semillas de deskops las declara CC36; no cambia la forma de store.yaml; tests por archivo, suite completa al supervisor. Es un nodo ejecutable (`task.code`), no un agregado.

## AMBIGUEDADES

1. "folders (lista de rutas relativas a la raíz)" frente a q4 "template_root=None = el directorio de store.yaml": no se fija si "la raíz" es la del proyecto o `.sldb/`; obligaría a inventar la base de `folders` y del `path` de cada seed.
2. "lo reporta como rewritten (con apply) o como pendiente (sin apply)" frente a q8 "siempre el objeto {created, rewritten, present, conflicts}": no existe lista para "pendiente"; obligaría a inventar dónde cae un `managed` divergente sin `--apply`.
3. "build_store pasa … a sldb.api.build_store(store, *, apply)" y "stores build incluye el reporte de scaffold": no dice con qué `apply` llama build, ni cómo se obtiene `root` al perder ese parámetro; obligaría a inventar si build escribe o solo reporta.
4. "text (literal)": sin encoding ni salto de línea final declarados; obligaría a inventar los bytes exactos que compara `managed`.

## DRY-RUN

**Lecturas**: `store_declaration.py`, `stores_build.py`, `apply_declaration`, `store/io/rollback.py`, `track_document_file.py`, `document_render.render_model_template`, `api/__init__.py`, `cli/parsers/stores.py`, `cli/commands/stores.py`, tests nombrados, CHANGELOG.

**Cambios previstos**: `Seed`/`folders`/`seeds` con `extra="forbid"`; `scaffold_store.py` y `api/build_store.py` nuevos; parser y comando `scaffold`; sección `scaffold` en build; reexports; tests; `docs/architecture/store-declaration.md`; CHANGELOG.

**Dependencias**: `sldb.api.transaction` presente o no en main (GD24, se decide al implementar), `importlib.resources`, golden de `stores build`, `test_clean_code_rules`.

**Validaciones futuras**: los tres `pytest` del TaskDoc, `grep` contra `6b80df36`, `stores scaffold` dos corridas, `fetch`/`rebase` con CHANGELOG y `__init__.py` tomados de main. Nada ejecutado.

## FUTURO

GD24 cierra o no (lo decide el ejecutor mirando main); CC36 declara las semillas de deskops; el supervisor corre la suite completa e integra; el dueño/supervisor promueve con `deskops add task --from-drawer`; deskops recibe la nota de cierre; la revisión en frío decide los hallazgos.
