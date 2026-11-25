## REFORMULACION

Propósito: recuperar en sldb la cobertura de pruebas que aún vive en spec2viz para modelos que sldb ya posee (notaciones, paletas, resolvedor de vistas y ViewDoc, SV01-SV04); IR13c se retiró y al retirar spec2viz esa cobertura se perdería. Origen: segunda petición de la nota de inbox citada.

Resultado: en `tests/notations/` de sldb, un archivo nuevo por cada uno de los siete `test_*.py` de spec2viz (`test_ported_from_spec2viz_<nombre original sin test_>.py`), con equivalentes que importan solo sldb, docstring que lista casos no portados y su motivo, xfail más nota al inbox donde falle, y una línea en `CHANGELOG.md`.

Repo: sldb (`/mnt/ssd/proyectos/SLDB_1`); tarea `task.code` ejecutable (no agregado).

Límites: no tocar spec2viz ni `src/sldb`; no portar pruebas de renderers; el ejecutor no hace push; el commit lo hace el coordinador con `deskops closeout commit`.

## AMBIGUEDADES

1. "misma firma y comportamiento documentado" — obliga a inventar cuál es la documentación de referencia (docstrings de spec2viz, docs de sldb, o los propios tests).
2. "Fixtures copiadas van a una carpeta fixtures dentro de tests/notations, con el nombre original" — no dice qué hacer si dos archivos traen fixtures homónimas de contenido distinto; hay que inventar política de colisión.
3. "se marca xfail con el motivo" — no fija si el xfail es `strict` ni el formato del motivo; "pasan" en Validation admite un xpass no strict sin definirlo.
4. "bajo el encabezado '## 0.1.13 — not released yet'" — no aclara si el encabezado ya existe o debe crearse.
5. "Los números de línea citados son orientativos a HEAD 7288d93e" — el input no cita números de línea; hay que inventar a qué se refiere.

## DRY-RUN

Lecturas (hipotéticas): los siete tests de spec2viz citados; `src/sldb` (`sldb.api.notations`, `sldb.notations`, `sldb.models.notation`); `tests/notations/` existente; `CHANGELOG.md`; Board y rituales; nota de inbox de origen.

Cambios previstos: siete archivos `tests/notations/test_ported_from_spec2viz_{notation,notation_view,style_palette,catalog_notation,catalog_resolved_views,view_contract_resolved,view_doc}.py`; `tests/notations/fixtures/` con fixtures copiadas; una línea en `CHANGELOG.md`; posibles `deskops message send --to sldb` por cada xfail; `result-summary.md`. Dependencias: pytest, `tmp_path`, helpers de store vía `sldb.api`, deskops.

Validaciones futuras: correr cada archivo nuevo uno a uno; luego `TMPDIR=/dev/shm pytest -q tests/notations/ -k ported_from_spec2viz` y el grep de no-import de spec2viz; revisar docstrings; confirmar notas enviadas.

## FUTURO

El coordinador ejecuta `deskops closeout commit` y `closeout verify`, decide si acepta los xfails; si el repo no está registrado, el aviso pasa a `result-summary.md`; un humano valida la cobertura antes de retirar spec2viz.
