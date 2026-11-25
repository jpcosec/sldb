## REFORMULACION

Encargo: corregir una única línea de `CHANGELOG.md` que afirma como ruta del repo un `vistas.yml` inexistente; la copia real está en `tests/notations/fixtures/docs/architecture/vistas.yml`. Propósito: que la puerta de afirmaciones vuelva a verde sin alterar comportamiento. Resultado: `tests/test_clean_code_rules.py` y `bash tools/check.sh --fast` pasan, los tests de comportamiento no cambian y `git diff` solo toca esa línea. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: solo `CHANGELOG.md`; no se añaden líneas ni se tocan código, tests u otras afirmaciones; afirmaciones falsas ajenas solo se anotan en `result-summary.md` del run.

## AMBIGUEDADES

1. «escribir la ruta real tests/notations/fixtures/docs/architecture/vistas.yml en lugar de la ruta sin el prefijo tests/notations/fixtures» — no cita el texto literal actual de la línea (el título lo trunca como «docs-architectur»); obliga a inventar el string exacto a reemplazar.
2. «los tests de la tarea original siguen verdes sin cambios» — no enumera cuáles son; obliga a inferirlos del diff.
3. «se anotan en result-summary.md del run» — no da ruta ni formato de ese archivo; obliga a inventar ubicación y estructura.
4. «CHANGELOG y commit» — no especifica mensaje ni firma del commit; obliga a inventar convención.

## DRY-RUN

Lecturas: `CHANGELOG.md` (localizar la línea que empieza «Las pruebas de spec2viz…»), `tests/test_clean_code_rules.py` (regla que detecta rutas), `tools/check.sh` (si incluye esa regla). Cambios previstos: reemplazo del token de ruta en esa única línea; ninguna otra edición. Dependencias: `uv`, extras `code` y `dev`, `pytest`, `bash`, `TMPDIR=/dev/shm`. Validaciones futuras: ejecutar los dos comandos de Validation y `git diff` para confirmar que no cambian archivos de tests. Sin ejecutar nada.

## FUTURO

Otro nodo o un humano decide el mensaje/commit, confirma que el diff es de una sola línea y revisa/archiva las anotaciones de otras afirmaciones falsas en el `result-summary.md` del run.
