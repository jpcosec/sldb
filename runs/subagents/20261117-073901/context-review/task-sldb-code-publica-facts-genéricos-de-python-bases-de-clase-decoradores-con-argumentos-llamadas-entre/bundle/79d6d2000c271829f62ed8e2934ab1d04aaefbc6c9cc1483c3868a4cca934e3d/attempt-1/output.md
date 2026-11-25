REFORMULACION
Encargo: ampliar `sldb.code` para publicar hechos sintácticos genéricos de Python sin conocer frameworks: bases de clase (relación `extends`), decoradores con args/kwargs, llamadas de cada función o método y asignaciones de módulo/clase con llamada o literal, incluida una clase anidada como `Meta`. Resultado: facts nuevos que permitan a specIR reconstruir rutas, campos, serializers y cadenas de llamadas de un proyecto Django/DRF. Repo: `SLDB_1`; superficie `src/sldb/code/` (`scan.py`, `readers.py`, `facts.py`, `fingerprints.py`, `ids.py`, módulos nuevos), `tests/selfdoc/test_treesitter_symbols.py`, fixture `tests/fixtures/treesitter/` y `CHANGELOG.md`. Límites: no interpretar Django/DRF, no resolver tipos ni imports, no TS/JS.

AMBIGUEDADES
1. «en scan_tree, scan_file y code_facts»: `code_facts` no aparece en los archivos provistos; obliga a inventar dónde vive o si debe crearse.
2. «attrs.calls con línea de cada llamada»: no aclara si la línea es absoluta del archivo o relativa a la función; obliga a inventar la convención.
3. «las llamadas que hace cada función o método a otros nombres»: no precisa si incluye llamadas dentro de `def` anidadas; obliga a inventar el alcance.
4. «una asignación (nombre = valor) es kind assignment»: no cubre la asignación anotada (`x: int = 5`); obliga a inventar si cuenta y con qué `attrs`.

DRY-RUN
Lecturas: `readers.py`, `scan.py`, `facts.py`, `fingerprints.py`, `ids.py` (confirmar `take_late`/`flush`), tests y fixture existentes, y el patch `runs/subagents/20261116-exec-k3-c1/executor-diff-c3py-c1.patch`.
Cambios previstos: módulos nuevos en `sldb.code` (regla de 80 líneas) para bases (`extends`), decoradores (`attrs.decorators`), llamadas (relación `calls` + `attrs.calls`) y asignaciones (`kind assignment`; `kind call` para sentencia-call de módulo); integrarlos en `scan_file` para `.py`; ids nuevos con `take_late` y `flush` en `scan_tree`/`scan_file`/`code_facts`; normalizar con `py_norm`; fixture Django/DRF y tests; CHANGELOG y nota de NORMALIZATION.
Dependencias: existencia real de `Ids.take_late`/`flush` y de `code_facts`; gramática Python de tree-sitter; estructura `fact`/`rels`; el patch previo.
Validaciones futuras: los siete comandos de Validation y el Done When (facts del fixture, anclas sin cambio, CHANGELOG y commit).

FUTURO
specIR interpreta los facts como Django/DRF (otro nodo). Un humano o coordinador decide la subida de NORMALIZATION y aprueba el alcance. Otra tarea cubre TS/JS. El patch de intentos previos lo produce otro ejecutor. El commit, el aviso a IR y el cierre los decide el humano/closeout.
