## REFORMULACION

El encargo (GD26, plan generalizar-desde-deskops rev3, hijo de PG2) es implementar en el repo sldb —worktree robocop2, base 6b80df36— el scaffold declarativo de store: ampliar `StoreDeclaration` con `folders` y `seeds` (modos `if_missing`/`managed`; fuentes `text`, `file` con `pkg:`, `document` con `track`), crear `sldb.api.scaffold_store` idempotente con `ScaffoldReport {created, rewritten, present, conflicts}`, mover `build_store` a `sldb.api` ejecutando `apply_declaration` y luego `scaffold_store`, añadir CLI `stores scaffold [--apply]` y sección scaffold en `stores build`, con tests, doc y CHANGELOG. Límites: ningún nombre deskops en `src/sldb/` salvo fixtures; no cambiar el formato de `store.yaml` ni salidas CLI/serve existentes (aditivo); no inventar la API de grafo-operable.

## AMBIGUEDADES

1. Firma de `scaffold_store`: cita «scaffold_store(store, *, declaration=None, apply=False, template_root)» frente a «scaffold_store(store, *, declaration=None, apply=False) → ScaffoldReport». ¿`template_root` es obligatorio, opcional o solo prosa? Obliga a inventar firma y default.
2. Semántica de `folders`: cita «folders (lista de rutas relativas a la raíz)» sin modo. ¿Qué hace si existe, si es archivo, si es `managed`? Obliga a inventar.
3. Detección de GD24: cita «si GD24 ya cerró; si no, por archivo con rollback_on_error». No indica cómo comprobarlo. Obliga a inventar el mecanismo.
4. «trackear»: cita «un document con track se trackea con el modelo y nombre declarados». No nombra API de tracking. Obliga a inventar la llamada.
5. Sección scaffold vacía: cita «más la sección scaffold vacía». No define forma (lista vacía u objeto con ceros). Obliga a inventar el shape del golden.
6. `pkg:`: cita «pkg:modulo/ruta». No aclara `importlib.resources`, paquete instalado o relativo. Obliga a inventar.
7. Clave desconocida: cita «falla al cargar nombrando la clave». No da tipo de excepción ni mensaje. Obliga a inventar.

## DRY-RUN

Un ejecutor futuro leería `store_declaration.py:20`, `document_render.py:31`, `stores_build.py:35`, parsers/commands de stores, `api/__init__.py`, `rollback.py`, tests y CHANGELOG. Crearía `scaffold_store.py` y `build_store.py`; ampliaría `store_declaration.py`; tocaría `api/__init__.py`, CLI, tres tests, doc y CHANGELOG. Dependencias: GD24 (opcional, fallback `rollback_on_error`), `render_model_template`, `transaction`. Validaría con los tres `pytest`, grep de nombres deskops contra 6b80df36, CLI JSON, segunda corrida idempotente y nota a deskops. Sin ejecutar.

## FUTURO

CC36 declara las semillas deskops; GD24 puede o no haber cerrado; el supervisor corre la suite completa y decide las revisiones en frío; deskops recibe la nota de cierre; un humano dispone hallazgos como correcciones del TaskDoc.
