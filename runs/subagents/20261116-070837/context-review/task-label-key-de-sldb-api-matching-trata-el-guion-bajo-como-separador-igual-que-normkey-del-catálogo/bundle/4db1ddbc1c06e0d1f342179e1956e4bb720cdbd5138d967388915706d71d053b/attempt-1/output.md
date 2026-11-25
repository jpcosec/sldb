## REFORMULACION

Encargo del nodo: en el repo SLDB_1, modificar `label_key` de `src/sldb/api/matching/atom_keys.py` para que el guion bajo sea separador, usando exactamente `re.sub(r"[\W_]+", " ", texto)` y conservando minúsculas, colapso de espacios y `strip`. Resultado: `label_key("post_published") == "post published"` y equivalencia con `normKey` solo para los cuatro pares indicados y para letras, dígitos, espacios, guion bajo y puntuación ASCII. Añadir tests en `tests/matching/test_matching_explicit.py` y una línea en `CHANGELOG.md` bajo `## 0.1.13 — not released yet`. Límites: no tocar `normalize_key`, `_title_aliases`, la plantilla JS del catálogo, el emparejamiento difuso ni la otra tarea citada. Validación: `TMPDIR=/dev/shm pytest -q tests/matching/`.

## AMBIGUEDADES

1. «deskops message send --to <repo>»: el input no identifica `<repo>`; obligaría a inventar el identificador del repositorio destinatario del aviso.
2. «runs/subagents/<run-dir>/result-summary.md»: `<run-dir>` no viene concretado; obligaría a inventar el directorio del run.
3. «bajo el encabezado "## 0.1.13 — not released yet"»: no se indica qué hacer si ese encabezado no existe; obligaría a decidir si crearlo o detenerse.

## DRY-RUN

Lecturas: `atom_keys.py` (localizar `label_key` por nombre), `tests/matching/test_matching_explicit.py`, `CHANGELOG.md`, y `grep "label_key"` en `src/sldb`. Cambios previstos: sustituir el regex interno de `label_key` por `[\W_]+`; añadir el test de `"post_published"` y el parametrizado con los cuatro pares exactos; añadir la entrada de changelog. Dependencias: helpers/fixtures existentes del archivo de test y el encabezado de versión del changelog. Validaciones futuras: ejecutar `TMPDIR=/dev/shm pytest -q tests/matching/`; si cambia algún golden, comparar su diff y actualizarlo solo si la única diferencia es `_` convertido en espacio; en caso contrario, detenerse y anotar el diff en el informe. No se ejecuta nada ahora.

## FUTURO

El coordinador decide el `<repo>` del aviso y el mensaje de commit, ejecuta `deskops closeout commit` y no hace push; el arnés aporta `<run-dir>`. Si el diff de un golden no es exclusivamente la separación de `_`, un humano decide la parada.
