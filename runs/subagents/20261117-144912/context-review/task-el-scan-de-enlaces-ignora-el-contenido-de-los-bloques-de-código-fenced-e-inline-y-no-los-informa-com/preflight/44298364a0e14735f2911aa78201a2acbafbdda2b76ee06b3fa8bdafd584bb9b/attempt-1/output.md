REFORMULACION
Tarea ejecutable (no agregado) en el repo `/mnt/ssd/proyectos/SLDB_1`: localizar el parser de enlaces usado por `src/sldb/cli/commands/links.py` y hacer que `sldb links` y su API no cuenten como enlaces el contenido de bloques cercados (backticks o tildes) ni código inline, manteniendo la detección de enlaces reales. Debe cubrir aperturas en la misma línea de un ítem de lista y cierres indentados según las precisiones, añadir tests en `tests/test_links.py` con los cuatro casos indicados, actualizar `CHANGELOG.md`, hacer commit y avisar a sldb-ui. Fuera de alcance: otros tipos de referencia. La validación son los cuatro comandos listados; el cierre exige que pasen con los tests nuevos.

AMBIGUEDADES
1. “los cuatro casos de runs/subagents/20261116-test-lk-c1/result-summary.md”: el input no incluye su contenido; obligaría a inventar documentos y aserciones exactas si no se puede leer.
2. “cada uno contrastado con markdown-it-py commonmark si está instalado”: no define si omitir, fallar o degradar cuando falte; obligaría a inventar la política condicional.
3. “No entra: otros tipos de referencia”: no delimita qué son (wikilinks `[[...]]`, autolinks, footnotes); obligaría a inventar el alcance.
4. “aviso a sldb-ui”: no indica canal, formato ni responsable; obligaría a inventar medio y mensaje.
5. “CHANGELOG y commit”: no fija mensaje, alcance ni rama; obligaría a inventar convenciones.

DRY-RUN
Lecturas hipotéticas: `links.py`, módulo del parser, `tests/test_links.py`, `result-summary.md`, `CHANGELOG.md` y reglas de `check.sh`. Cambios previstos: excluir fences e inline en el parser o en su entrada, preservar enlaces reales, añadir tests de los cuatro casos y bordes de listas/cierres, actualizar changelog. Dependencias: entorno `uv` con extras code/dev, `markdown-it-py` opcional, pytest y `tools/check.sh`. Validaciones futuras: ejecutar los cuatro comandos de Validation y comprobar recuentos de enlaces reales/rotos sin regresiones.

FUTURO
Otro nodo ejecutará lecturas, cambios y validaciones; un humano decidirá commit, publicación del CHANGELOG y aviso a sldb-ui.
