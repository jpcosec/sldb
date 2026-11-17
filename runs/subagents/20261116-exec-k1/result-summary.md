# Executor deskops-e-7f02ec7518c9 — sldb.api.code.code_facts + write_anchor público (C1, C2, C5)

## Cambios
- `src/sldb/api/code/__init__.py` (nuevo, paquete autorizado por el Scope): docstring con el contrato completo y `__all__ = ["code_facts"]`.
- `src/sldb/api/code/code_facts.py` (nuevo): `code_facts(root, paths=None)` → `{"facts", "skipped"}`. Reusa `sldb.code.scan.scan_file` con un único `Ids` en orden de ruta, así que los ids son los de `scan_tree`. `_has_grammar` (la extensión está en `GRAMMARS` y `available`) decide qué va a skipped. `_require_anchor` lanza RuntimeError si un fact sale sin span o sin source_hash, y no rellena nada.
- `src/sldb/api/code/requested_files.py` (nuevo): `requested_files` normaliza y deduplica las rutas y expande los directorios con `find_files`, más `_without_runtime`, que agrega los archivos con extensión de fuente cuya gramática no está instalada para que entren a skipped. `checked_path` lanza ValueError si la ruta es absoluta, está fuera de root o no existe, y lo hace antes de escanear. Para el walk reusa `_SKIP` de `sldb.code.files` y no duplica la lista.
- `src/sldb/api/anchors/__init__.py`: importa `write_anchor` (de `anchor_docs`), lo agrega a `__all__` y lo nombra en el docstring.
- `tests/api/test_anchors.py`: el import de `write_anchor` pasa a `sldb.api.anchors`. Cinco tests nuevos (9 casos) con un árbol `.py`/`.tsx`/`.sql`, un `.md`, un `.py` roto y un `node_modules`. Cubren igualdad con `scan_tree`, el orden, span y source_hash, has_error, archivos y directorios, rutas repetidas, los ValueError sin escaneo, skipped y los RuntimeError.
- `CHANGELOG.md`: entrada en 0.1.13.
- `contracts/layers.toml` (**desvío, fuera de la lista de archivos**): agregué `api/code` a los `paths` del eje `anclaje` y extendí su `does`. Sin eso, la puerta "ejes" de `check.sh --fast` falla por los dos archivos nuevos (`archivo sin eje`). Es consecuencia directa del paquete nuevo que pide el Scope.

## Decisiones del coordinador aplicadas (y choques)
1. Directorios: se expanden con find_files. Hecho.
2. ValueError con la ruta antes de escanear. La decisión dice primero que una ruta "repetida lanza ValueError" y después que "se acepta una sola vez, sin error". Apliqué lo segundo, que es explícito: deduplico después de normalizar (`src/x.py`, `./src/x.py` y `src/../src/x.py` cuentan una vez).
3. Un archivo con errores de parseo da sus facts (`has_error`) y no va a skipped. Hecho y testeado.
4. RuntimeError sin relleno. Hecho, testeado con un reader falso, y los readers reales de .py, .tsx y .sql cumplen.
5. "El orden de scan_tree (por ruta y luego por posición)": `scan_tree` en realidad ordena por **id**, no por ruta. Seguí la semántica del paréntesis (ruta en el orden de find_files, luego el orden del reader en cada archivo), con los mismos ids y el mismo conjunto de facts que scan_tree. El test lo verifica: `sorted(facts, key=id) == scan_tree(root)`.
6. y 7. Sin commit y sin aviso a IR. Done When pide "CHANGELOG y commit; aviso a IR": el commit y el aviso quedan para el coordinador.
- Extra: una ruta explícita cuya extensión no tiene gramática (p. ej. `README.md`) va a skipped en vez de parsearse como Python (grammar_of cae a Python por defecto).

## Done When
- Validation: los 3 pytest pasan (rc 0). `check.sh --fast` da rc=1 **solo** por la puerta "identidad": `archivo versionado sin clasificar en la raíz: AGENTS.md`. Es preexistente: AGENTS.md entró en 7dbb6bc9, `contracts/identity.toml` no está modificado y ni ese archivo ni esa puerta los toca esta tarea. Las puertas núcleo, capas, ejes y superficie pasan.
- `from sldb.api.code import code_facts` y `from sldb.api.anchors import write_anchor` funcionan (verificado. Además, sobre `src/sldb/code` salen 85 facts, todos con span y source_hash, y skipped vacío).
- Cada fact con span y source_hash no vacíos: garantizado por `_require_anchor` y testeado.

## Comandos (salida completa en validation.log)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py`: rc 0 (22 passed)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py`: rc 0 (14 passed)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py`: rc 0 (1193 passed)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast`: rc 1 (identidad: AGENTS.md, preexistente)
- No corrí la suite completa ni `sldb stores build --check`: delegados al integrador.

## Archivos tocados
- src/sldb/api/code/__init__.py (nuevo)
- src/sldb/api/code/code_facts.py (nuevo)
- src/sldb/api/code/requested_files.py (nuevo)
- src/sldb/api/anchors/__init__.py
- tests/api/test_anchors.py
- CHANGELOG.md
- contracts/layers.toml (desvío, ver arriba)
- runs/subagents/20261116-exec-k1/{validation.log,result-summary.md}
