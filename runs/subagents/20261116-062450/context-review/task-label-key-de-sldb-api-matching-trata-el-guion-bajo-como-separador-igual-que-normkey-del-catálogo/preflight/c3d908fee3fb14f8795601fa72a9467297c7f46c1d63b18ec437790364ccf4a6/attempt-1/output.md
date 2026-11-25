## REFORMULACION
Propósito: corregir `label_key` para que trate `_` como separador y coincida con `normKey` en los casos definidos. Resultado: `label_key("post_published") == "post published"`, tests nuevos y entrada en `CHANGELOG.md`. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: cambiar solo el regex de `label_key` a `re.sub(r"[\W_]+", " ", texto)`, conservando minúsculas, colapso de espacios y `strip`; no tocar `normalize_key`, `_title_aliases`, la plantilla JS del catálogo, el emparejamiento difuso ni la otra tarea citada. Es un nodo ejecutable, no un agregado.

## AMBIGUEDADES
1. “si las únicas diferencias son "_" convertido en espacio, se actualiza el golden”: no define cómo comparar ni actualizar goldens, ni cuáles; obligaría a inventar el procedimiento.
2. “con el estilo de las entradas vecinas”: criterio editorial subjetivo; obligaría a inferir formato y redacción.
3. “El commit lo hace el coordinador con deskops closeout commit” frente a “commit con esos archivos”: no aclara si el ejecutor debe commitear; obligaría a elegir.
4. “runs/subagents/<run-dir>/result-summary.md”: placeholder sin valor; obligaría a inventar el directorio de ejecución.
5. “deskops message send --to <repo>”: no nombra el repo destinatario; obligaría a inventar el aviso.

## DRY-RUN
Lecturas: `src/sldb/api/matching/atom_keys.py`, usos de `label_key` con `grep`, `tests/matching/test_matching_explicit.py`, `CHANGELOG.md` y goldens de `tests/matching/`. Cambios previstos: sustituir el regex; añadir el test de `"post_published"` y el parametrizado con los cuatro pares exactos; añadir una línea al changelog. Dependencias: localizar por nombre de función, no por línea; `TMPDIR=/dev/shm`; fixtures existentes; repo en HEAD esperado. Validaciones futuras: ejecutar `pytest -q tests/matching/`; comprobar los cuatro pares; revisar diffs de goldens y actualizar solo si la única diferencia es `_` convertido en espacio; si hay otra diferencia, detenerse y anotar el diff; generar informe y aviso. Sin ejecutar nada.

## FUTURO
El coordinador hará el commit/closeout y no habrá push del ejecutor. Un humano decidirá si aparece un diff de golden no permitido. El repo IR conserva la plantilla JS y el destinatario del aviso o su registro se resuelven fuera de este nodo.
