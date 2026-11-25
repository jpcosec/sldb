## REFORMULACION

Encargo (task.code, repo sldb): modificar `refuse_lossy_overwrite` (`src/sldb/api/documents/lossy_overwrite.py:18`) para que no rechace una escritura cuando cada encabezado no declarado perdido tenga su contenido presente en el texto renderizado nuevo (en un campo o como párrafo), rechazando aún si se pierde contenido. Resultado: cambio de comportamiento, dos tests (acepta/rechaza) y CHANGELOG. Límites: solo ese módulo, su test y CHANGELOG; fuera la política `structural_noise` y otros guards; commit desde el worktree de dispatch con trailer `Task-Id`.

## AMBIGUEDADES

1. «presente en el texto renderizado nuevo: en el valor de algún campo o como párrafo»: no define comparación (subcadena, tokens, mayúsculas, normalización de ambos lados) ni límites del «texto bajo el encabezado». Obligaría a inventar semántica de matching.
2. «Un test cubre los dos casos»: no enumera cuáles; se presume aceptar/rechazar. Obligaría a inferirlos.
3. «los tests de lossy existentes pasan» frente a Validation, que solo lista `tests/api`: no indica ruta ni si basta esa suite. Obligaría a decidir el alcance de regresión.
4. «La puerta 'identidad' de check.sh --fast en rojo por workbench_demo es la excepción autorizada»: Validation no menciona `check.sh`; no queda claro si debe ejecutarse e ignorarse esa puerta. Obligaría a inventar el protocolo de gates.
5. «commit desde el worktree que dispatch te da»: sin ruta, rama ni SHA base. Obligaría a inventar ubicación.
6. «un documento con un '## Tags'»: no nombra fixture ni documento concreto. Obligaría a inventar el caso de prueba.
7. Scope incluye CHANGELOG, pero Implementation Path y Validation lo omiten. Obligaría a decidir si es entregable exigible.

## DRY-RUN

Lecturas: `lossy_overwrite.py`, test de lossy (`grep -rln lossy tests/`), tests de `tests/api`, CHANGELOG. Cambios previstos: tests p1/p2, comparación normalizada en el guard, entrada de CHANGELOG. Dependencias: worktree de dispatch, git, pytest con xdist. Validaciones futuras: test dirigido de lossy y `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider -n 4 tests/api`; eventualmente `check.sh --fast`. Nada ejecutado.

## FUTURO

Dispatch aporta worktree y Task-Id; un humano confirma la excepción f055723d y si `check.sh` corre; closeout/deskops actualiza Board y cierra la tarea.
