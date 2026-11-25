## REFORMULACION
**Propósito:** corregir la incoherencia entre `docs list` y `docs show`: si `docs list` devuelve un nombre, `docs show` debe resolverlo o listarlo como no resoluble con causa.
**Resultado:** código y test que alineen ambas lecturas; `result-summary.md` con el origen del nombre fantasma; `CHANGELOG` y commit; aviso a `sldb-ui`.
**Repo:** `/mnt/ssd/proyectos/SLDB_1/sldb`; superficie declarada: `src/sldb/cli/commands/docs.py`, `tests/test_cli_v2.py`, `CHANGELOG.md`.
**Límites:** no cambiar el formato de salida de `docs list` salvo el marcado de no resoluble. No es agregado ni paquete: es un TaskDoc ejecutable.

## AMBIGUEDADES
1. “docs list y docs show leen la misma fuente” choca con “el nombre no está en .sldb/core/store_index.yaml”. Obliga a inventar cuál es la fuente real y si `store_index.yaml` participa.
2. “o docs list lo marca como no resoluble con su causa” no define marcador, campo ni esquema. Obliga a inventar representación sin cambiar el formato.
3. “un documento declarado o derivado que no está en el índice” no distingue ambos casos ni el fixture. Obliga a inventar la reproducción.
4. “y la API que llaman” no indica si la API está en este repo ni dónde. Obliga a inventar su ubicación y alcance.
5. “aviso a sldb-ui” no fija canal, responsable ni evidencia. Obliga a inventar el mecanismo.
6. “result-summary.md” no indica ruta. Obliga a inventar ubicación.

## DRY-RUN
Lecturas futuras: `docs.py`, test CLI, `CHANGELOG`, índice de store y API implicada. Cambios previstos: reproducir en `tmp_path` un documento listado pero no resoluble; alinear listado/resolución o añadir marcado con causa; test nuevo. Dependencias: CLI, API y fuente del índice. Validaciones futuras: los cuatro comandos de `Validation` y `tools/check.sh --fast`. Sin ejecutar nada.

## FUTURO
El ejecutor implementa y documenta. CI/revisión valida. Un humano decide commit, ubicación final de `result-summary.md` y aviso a `sldb-ui`; el equipo de `sldb-ui` actúa sobre el aviso.
