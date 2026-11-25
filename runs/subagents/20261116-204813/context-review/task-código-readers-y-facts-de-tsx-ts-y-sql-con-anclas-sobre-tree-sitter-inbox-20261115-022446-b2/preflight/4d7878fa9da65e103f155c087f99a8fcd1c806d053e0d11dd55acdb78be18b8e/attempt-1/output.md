REFORMULACION
Nodo ejecutable (task.code). Propósito: ampliar `sldb.code` para leer `.ts/.tsx/.js/.jsx` con un reader único sobre `tree-sitter-typescript` (extra code), publicando hechos equivalentes a Python y anclas `code:<ruta>::<qualified_name>`. Resultado: nuevo `lang_ts.py`; runtime y scan por extensión; `parse_code_ref` y `recorded_with` actualizados; fixtures y pruebas de anclas intact/changed/lost/reconnected; salida `.py` sin cambios; lock actualizado; CHANGELOG y commit. Repo: `/mnt/ssd/proyectos/SLDB_1`, paquete `src/sldb/code`, modelos/anclas y tests indicados. Límites: SQL queda para la tarea hermana; no mapear a dominio (specIR); no tocar fuera de `sldb.code` salvo `code_ref.py`/`record_anchor.py`; no duplicar maquinaria Python.

AMBIGUEDADES
1. Título y fichero incluyen SQL, pero Goal/Scope dicen “SQL lo hace la tarea hermana” y “Fuera de alcance: SQL”; obligaría a inventar si SQL entra.
2. “kind hook: misma forma que component, con nombre que empieza por use…”: no aclara si exige JSX en el cuerpo; obligaría a inventar el criterio.
3. “kind function: … const con arrow function del nivel superior”: no cubre `let` ni function expression; obligaría a inventar si crean hecho.
4. “cuyo final está en la línea inmediatamente anterior a la declaración, o a su export” y “sin los delimitadores ni los asteriscos de cada línea”: no fija comentario entre `export` y declaración ni trim/sangría; obligaría a inventar.
5. “recorded_with) informa la gramática del archivo”: no fija valor ni formato; obligaría a inventar cadena y compatibilidad.
6. “NORMALIZATION no cambia…”: no define NORMALIZATION; obligaría a inventar qué se compara.

DRY-RUN
Leería `pyproject.toml`, `uv.lock`, `runtime.py`, `scan.py`, `ids.py`, `code_ref.py`, `record_anchor.py`, tests/fixtures y API de tree-sitter-typescript. Cambiaría dependencia, `lang_ts.py`, dispatch runtime/scan/find_files, extensiones en code_ref/record_anchor, fixtures, tests y CHANGELOG. Correría `uv lock` sin `--frozen`; después las validaciones `--frozen` listadas. Depende de gramática instalada, lock nuevo y salida `.py` idéntica. Validaciones futuras: anclas, treesitter, fingerprints, agreement, component spec, clean code y `check.sh --fast`. Sin ejecutar.

FUTURO
El coordinador decide cómo commitear `uv.lock` con cambios ajenos. IR recibe el aviso y hace el mapeo de dominio. La tarea hermana SQL consume estos readers/anclas. Humano/coordinador acepta CHANGELOG y commit.
