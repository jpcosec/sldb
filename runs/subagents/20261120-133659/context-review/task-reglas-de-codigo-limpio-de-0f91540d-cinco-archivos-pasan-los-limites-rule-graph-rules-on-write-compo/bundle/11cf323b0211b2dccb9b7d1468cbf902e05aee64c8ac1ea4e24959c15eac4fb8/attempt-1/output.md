## REFORMULACION

Nodo ejecutable (`task.refactor`), no agregado. **Propósito:** hacer pasar entero `tests/test_clean_code_rules.py` sin subir límites, partiendo cinco unidades que los exceden: `rule_graph.py` (97 > 80), `component_spec_graph.py` (90 > 80), `store_check.py` (86 > 80), `check_on_write` en `rules_on_write.py` (12 > 10) y `_diagnose_model` en `store/diagnostics.py` (11 > 10), mediante funciones auxiliares y módulos nuevos. **Resultado:** esos cinco puntos dentro de límite con el mismo comportamiento; los tests de las tareas afectadas siguen verdes sin cambiar asserts; módulo nuevo fuera de carpeta con eje declarado en `contracts/layers.toml`; commit solo de sus rutas con trailer `Task-Id` y `deskops advance`. **Repo:** `/mnt/ssd/proyectos/SLDB_1/sldb`. **Límites:** solo los cinco archivos, módulos nuevos y `layers.toml`; no cambiar comportamiento ni límites.

## AMBIGUEDADES

1. «los tests de las cuatro tareas (tests/api/test_on_write_entering.py, tests/api/test_rules.py, tests/matching/test_matching_refs.py, tests/notations/test_notations_from_graph_cli.py, tests/store/test_diagnostics.py)»: dice cuatro tareas pero enumera cinco archivos. Obliga a inventar cuántos y cuál sobra.
2. «Un módulo nuevo fuera de una carpeta con eje se declara en contracts/layers.toml»: no define «carpeta con eje» ni formato de declaración. Obliga a inventar criterio y sintaxis.
3. «moviendo código a módulos nuevos donde haga falta»: no fija granularidad ni destino del split. Obliga a inventar cuántos módulos y con qué frontera.
4. «todas las puertas en verde salvo 'identidad' por workbench_demo (excepción autorizada; decisión aparte)»: no aclara si un fallo de identidad se ignora al validar ni cómo registrarlo. Obliga a inventar el criterio de aceptación.
5. Validación lista solo `tests/test_clean_code_rules.py`, mientras «Done When» exige «los cinco archivos de tests». Obliga a decidir si los cinco son obligatorios o informativos.
6. «con el trailer Task-Id»: no da valor ni formato. Obliga a inventar el identificador exacto.

## DRY-RUN

**Lecturas:** TaskDoc, rituales, Board, cinco fuentes, cinco archivos de test, `tests/test_clean_code_rules.py`, `contracts/layers.toml`, `tools/check.sh`, `git log/status`. **Cambios previstos:** extraer funciones auxiliares y módulos hermanos, ajustar imports, declarar módulos en `layers.toml`, commit acotado por rutas. **Dependencias:** pytest, git, deskops, `check.sh`. **Validaciones futuras:** pytest de `test_clean_code_rules`; los cinco archivos; `check.sh --fast`; suite completa; commit con trailer; `deskops advance`. Sin ejecutar.

## FUTURO

Decisión humana sobre la excepción «identidad»/`workbench_demo`; el nodo `integrate` corre la suite completa; `deskops`/closeout retiran la tarea del Board; resolución del valor `Task-Id` si no consta en el documento.
