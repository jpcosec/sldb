## REFORMULACION

Encargo ejecutable de código: fijar el contrato de `sldb docs create -o <ruta relativa>` para que la ruta de salida se resuelva contra el directorio actual del proceso (cwd), no contra la raíz del store, y el archivo se escriba ahí. Resultado esperado: ajuste en el comando `docs create` localizado en `src/sldb/cli/` y un test nuevo `tests/test_docs_create_output_path.py` que use un store temporal con cwd en un subdirectorio y verifique que `-o sub.md` crea `<cwd>/sub.md`. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: solo el comando `docs create` y su test; quedan fuera render y fields. Cierre: que pase el test indicado en Validation.

## AMBIGUEDADES

1. «sldb docs create -o resuelve la ruta contra el cwd (o avisa)» (título) frente a Goal: «resuelve la ruta contra el directorio actual del proceso (no contra la raiz del store) y escribe ahi». El “o avisa” no aparece en el Goal; obligaría a inventar cuándo avisar (¿rutas absolutas?, ¿fuera del store?) y con qué mensaje/salida.
2. «store temporal, cwd = un subdirectorio del proyecto»: no aclara si el subdirectorio pertenece al repo del proyecto o al store temporal. Obligaría a inventar la topología del test y si el cwd queda dentro o fuera del store, precisamente lo que el contrato discrimina.
3. «Encontrar docs create en src/sldb/cli/ (grep -rn 'def.*create' …)» y «docs create -o»: no consta que el flag `-o` exista ni su comportamiento por defecto. Obligaría a inventar interfaz CLI (nombre del flag, salida sin `-o`, tratamiento de rutas absolutas).
4. `summary: ''`: metadato vacío; obligaría a inventar un resumen (impacto menor, no altera la ejecución).

## DRY-RUN

Lecturas previstas: TaskDoc, `src/sldb/cli/` (grep del comando `docs create`), tests existentes de docs. Cambios previstos: nuevo `tests/test_docs_create_output_path.py` (store temporal, cwd en subdirectorio, `-o sub.md`, aserción de ubicación) y ajuste de resolución de ruta en `docs create`. Dependencias: venv `/mnt/ssd/proyectos/SLDB_1/.venv`, pytest, `TMPDIR=/mnt/ssd/tmp/sldb1`. Validación futura: ejecutar únicamente el comando de pytest indicado. Nada ejecutado.

## FUTURO

Un humano decide si existe variante “avisa” y sus condiciones; otro nodo o el mismo ejecutor define el comportamiento sin `-o` y con rutas absolutas; las tareas de render/fields quedan para otros nodos.
