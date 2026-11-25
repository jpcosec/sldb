## REFORMULACION
Encargo ejecutable (`task.code`) en el repo `/mnt/ssd/proyectos/SLDB_1`: portar a `tests/notations/` los casos de siete pruebas de `spec2viz` que correspondan a código ya existente en `sldb` (notaciones, paletas, vista resuelta y ViewDoc). Resultado: archivos nuevos `tests/notations/test_ported_from_spec2viz_<tema>.py`, con imports solo de `sldb`, docstrings que listen casos no portados y su motivo, `CHANGELOG.md` actualizado y commit. Límites: no modificar `spec2viz` ni `src/sldb`; no portar pruebas de renderers; si un caso falla en `sldb`, no corregir código, sino marcar `xfail` y enviar nota al inbox con `deskops message send`.

## AMBIGUEDADES
1. «por cada caso decidir si prueba algo que existe en sldb»: no fija criterio de equivalencia; obligaría a inventar el umbral de aplicabilidad.
2. «quedan listados con su motivo en el docstring del archivo portado»: no aclara si es un docstring por archivo nuevo o uno consolidado; obligaría a inventar la distribución.
3. «se marca xfail con el motivo y se manda una nota al inbox»: no precisa formato, asunto ni contenido exacto de la nota; obligaría a inventarlos.
4. «datos de prueba copiados a tests/notations/fixtures/ si hacen falta»: no define nombres, estructura ni limpieza; obligaría a inventar convención.
5. «commit.»: no indica mensaje, rama ni alcance; obligaría a inventar esos datos.

## DRY-RUN
Lecturas: los siete archivos de `spec2viz/tests/` citados, módulos `sldb.api.notations`, `sldb.notations`, `sldb.models.notation`, pruebas existentes en `tests/notations/` y `CHANGELOG.md`. Cambios previstos: inventario y mapeo símbolo a símbolo; creación de archivos portados con `tmp_path` y fixtures si fueran necesarios; docstrings con exclusiones; posible `xfail` y nota al inbox; entrada en `CHANGELOG.md`. Dependencias: código fuente de `spec2viz` disponible, `pytest`, `sldb` importable, `deskops`, `TMPDIR=/dev/shm`. Validaciones futuras, sin ejecutar: `TMPDIR=/dev/shm pytest -q tests/notations/ -k ported_from_spec2viz`, grep de ausencia de imports de `spec2viz`, revisión de docstrings y commit.

## FUTURO
El ejecutor producirá los tests, fixtures, `xfail`, nota y commit. Un nodo de validación ejecutará las comprobaciones y revisará la cobertura portada. Un humano decidirá si los `xfail` y las exclusiones son aceptables.
