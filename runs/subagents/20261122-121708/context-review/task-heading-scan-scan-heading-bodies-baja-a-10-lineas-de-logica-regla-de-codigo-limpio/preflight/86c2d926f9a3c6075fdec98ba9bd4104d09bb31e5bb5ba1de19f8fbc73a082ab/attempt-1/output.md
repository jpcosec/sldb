## REFORMULACION

**Propósito:** desbloquear el integrate de sldb haciendo que `scan_heading_bodies` cumpla la regla de código limpio (máx. 10 líneas de lógica).

**Resultado:** `src/sldb/api/documents/heading_scan.py` con `scan_heading_bodies` en ≤10 líneas, extrayendo una auxiliar privada en el mismo archivo, sin cambiar comportamiento.

**Repo:** sldb (`/mnt/ssd/proyectos/SLDB_1/sldb`). **Límites:** solo ese archivo; no tocar tests ni comportamiento.

## AMBIGUEDADES

1. "partiéndola en una auxiliar privada del mismo archivo": no se fija nombre, firma ni punto de corte; obligaría a inventar el contrato de la auxiliar.
2. Validación lista dos archivos ("tests/test_clean_code_rules.py tests/api/test_lossy_overwrite_content.py") frente a "Los tres archivos de tests pasan" y p2, que añade `tests/test_extraction_segments.py`; obligaría a inventar qué conjunto es exigible.
3. "en verde salvo 'identidad' por workbench_demo (excepción f055723d)": no se define qué comprueba `identidad` ni cómo acreditar la excepción; obligaría a inventar el criterio de aceptación de p3.
4. "Task-Id: <id de esta tarea>": placeholder literal; aunque el id figure en frontmatter, obligaría a inferir el valor exacto.
5. "p1: partir scan_heading_bodies": no indica dónde cortar; obligaría a inventar el límite de extracción, solo acotado por "sin cambiar el comportamiento".

## DRY-RUN

**Lecturas:** `heading_scan.py`, `tests/test_clean_code_rules.py` (para conocer la métrica), los dos/tres tests citados y `tools/check.sh`.
**Cambios previstos:** extraer auxiliar privada y reducir el cuerpo de `scan_heading_bodies`.
**Dependencias:** worktree que entrega dispatch; excepción `f055723d`.
**Validaciones futuras:** pytest de los archivos indicados, `bash tools/check.sh --fast`, commit con `git commit -- src/sldb/api/documents/heading_scan.py` y trailer `Task-Id`.

## FUTURO

Dispatch entrega el worktree; un humano o coordinador aclara el alcance exacto de tests y la excepción `f055723d`; el nodo de integrate consume el commit resultante.
