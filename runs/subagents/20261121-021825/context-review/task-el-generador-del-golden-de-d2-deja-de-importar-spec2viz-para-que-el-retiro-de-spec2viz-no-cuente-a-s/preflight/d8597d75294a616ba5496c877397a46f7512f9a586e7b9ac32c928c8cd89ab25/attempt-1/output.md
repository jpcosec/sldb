## REFORMULACION

**Propósito:** eliminar la única dependencia de `spec2viz` en el repo sldb, para que el gate IR13 del retiro de spec2viz no cuente a sldb como consumidor.

**Resultado:** `runs/subagents/20261116-exec-oraculo-d2/gen_golden.py` deja de importar `spec2viz.generators.python_ast`; el golden de D2 (ce0bd384) y sus tests permanecen intactos; se commitea con trailer `Task-Id` y se avisa al desk de IR con `deskops message send --to IR`.

**Repo:** sldb (workspace `desk`), rutas relativas a la raíz del repo.

**Límites:** dentro, el script `gen_golden.py` y, opcionalmente, un `README.md` en esa carpeta. Fuera: el golden y los tests de D2.

## AMBIGUEDADES

1. **Borrar o conservar con README.** Cita: «o se borra (el golden ya está commiteado en ce0bd384 y el script no lo usa ningún test), o se deja un README en esa carpeta que diga cómo se generó, sin el import». El Goal ofrece alternativas; Implementation Path asume ambas («git rm del script, y un README.md»). Obliga a inventar cuál es la opción canónica.
2. **Contenido y destinatario del aviso.** Cita: «el desk de IR recibe un aviso con el commit, con deskops message send --to IR». No se especifica texto, asunto ni si «IR» es el identificador exacto del destinatario.
3. **Intérprete de Python.** Cita: «TMPDIR=/tmp python -m pytest». No aclara si `python` existe en el entorno o debe ser `python3`.

## DRY-RUN

**Lecturas:** `gen_golden.py`; `grep -rn gen_golden src tests`; `git log`/`git show ce0bd384`; `tests/notations/test_component_spec_python.py`; `docs/spec2viz/acta-de-retiro.md`.

**Cambios previstos:** `git rm runs/subagents/20261116-exec-oraculo-d2/gen_golden.py`; alta de `README.md` (3 líneas) en la misma carpeta; commit con `git commit -- <rutas>` y trailer `Task-Id`.

**Dependencias:** repo git limpio, `deskops` disponible, conexión con el desk de IR.

**Validaciones futuras:** `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider tests/notations/test_component_spec_python.py` en verde; `grep` sin coincidencias de `spec2viz` en el script/ruta; aviso enviado a IR.

## FUTURO

Otro nodo o humano debe: resolver la ambigüedad 1 (borrar vs. README), confirmar el identificador `IR` y el texto del aviso, verificar el commit y el paso del gate IR13, y registrar la respuesta de IR en el acta de retiro.
