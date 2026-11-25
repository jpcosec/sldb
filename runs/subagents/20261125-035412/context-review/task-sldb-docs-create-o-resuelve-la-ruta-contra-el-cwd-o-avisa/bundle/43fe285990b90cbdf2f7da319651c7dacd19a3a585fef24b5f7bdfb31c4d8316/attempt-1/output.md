REFORMULACION  
Nodo ejecutable (`task.code`), no agregado. Propósito: que `sldb docs create -o <ruta relativa>` resuelva la ruta contra el cwd del proceso y escriba allí, no contra la raíz del store. Resultado: ajuste del comando y test nuevo `tests/test_docs_create_output_path.py`, con store temporal, cwd en un subdirectorio y verificación de `<cwd>/sub.md`. Repo: `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`). Límites: solo `docs create` y un test; fuera render y fields; validación centrada en el test indicado.

AMBIGUEDADES  
1. «cwd = un subdirectorio del proyecto»: no define qué es “proyecto”, qué ruta concreta usar ni cómo se descubre el store desde ahí; obligaría a inventar el layout y el fixture.  
2. «Correr solo ese test.» frente a «then the full suite when shared behavior changed»: obligaría a inventar si el cambio en la CLI exige ampliar la suite.  
3. «pills: []», «atoms: []», «files: []», «references: []» frente a «las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra»: obligaría a decidir si se ejecuta sin contexto vinculado o se bloquea por falta de él.

DRY-RUN  
Lecturas: TaskDoc, rituales execution/testing/closeout, Board, búsqueda de `docs create` en `src/sldb/cli/` y tests existentes. Cambios previstos: añadir el test nuevo y ajustar la resolución de `-o` relativa contra cwd. Dependencias: venv, `TMPDIR`, store temporal, CLI y pytest. Validaciones futuras: ejecutar el comando pytest indicado; después, closeout con árbol limpio y commit atómico. Sin ejecutar nada.

FUTURO  
El ejecutor localizará el comando, escribirá el test y aplicará el arreglo mínimo. El nodo de testing/closeout correrá las validaciones, actualizará Board/CHANGELOG y hará el commit. Un humano resolverá el layout del cwd y el alcance de la suite.
