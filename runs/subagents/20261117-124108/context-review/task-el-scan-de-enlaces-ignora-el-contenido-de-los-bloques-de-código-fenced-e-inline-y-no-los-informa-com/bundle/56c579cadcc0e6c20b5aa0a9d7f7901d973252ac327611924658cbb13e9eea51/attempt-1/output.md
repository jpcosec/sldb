## REFORMULACION

Propósito: que el scan de enlaces de sldb (comando `sldb links` y API `recover_links`) no trate como enlaces el contenido de bloques de código cercados (backticks o tildes) ni de código en línea, manteniendo la detección de enlaces reales. Resultado esperado: parser corregido, tests nuevos en `tests/test_links.py`, entrada en `CHANGELOG.md`, commit y aviso a sldb-ui. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: solo el parser usado por `src/sldb/cli/commands/links.py` y esos tests; fuera de alcance “otros tipos de referencia”.

## AMBIGUEDADES

1. “encontrar el parser de enlaces que usa src/sldb/cli/commands/links.py”: ese archivo solo importa `recover_links`/`parse_links` desde `sldb.links`; el parser real no figura en `files:` — obligaría a inventar si se modifica `src/sldb/links.py` (y su ruta exacta).
2. “ni de un código en línea”: no define delimitadores múltiples (``` `` ```), backticks escapados ni spans multilínea — obligaría a inventar la gramática exacta.
3. “bloques de código cercados (con backticks o tildes)”: no especifica cierre por longitud coincidente ni qué hacer con bloques sin cerrar al EOF — obligaría a inventar la política.
4. “no cuenta como enlace nada que esté dentro”: no aclara si aplica también a `predicate_link` y transclusiones; los tests actuales cubren `parse_links` con predicados — obligaría a inventar el alcance.
5. “aviso a sldb-ui”: no indica canal, nodo ni formato — obligaría a inventar el mecanismo.

## DRY-RUN

Lecturas: `links.py` (ya visto), localizar `sldb/links.py` y `parse_links`/`recover_links`, revisar tests de predicados existentes y `CHANGELOG.md`. Cambios previstos: enmascarar/quitar spans de código (inline y fenced) antes del regex de enlaces en el extractor; añadir test con documento mixto (enlaces reales + ejemplos en bloques); entrada en CHANGELOG. Dependencias: confirmar si ya existe utilidad de Markdown o hay que implementarla; verificar que `recover_links` reutilice el mismo extractor. Validaciones futuras: los cuatro comandos listados (`test_links.py`, `test_links_batch_cli.py`, `test_clean_code_rules.py`, `tools/check.sh --fast`).

## FUTURO

Decisión humana/otro nodo: ubicación definitiva del parser si no está en `files:` y política de bloques sin cerrar. `deskops closeout`: commit, retirada del Board y verificación. Notificación a sldb-ui: nodo o humano que la ejecute.
