REFORMULACION
Propósito: portar a sldb la cobertura de pruebas de spec2viz sobre notaciones, paletas, vista resuelta y ViewDoc, ya que sldb posee esos modelos y al retirar spec2viz se perdería. Resultado: archivos `tests/notations/test_ported_from_spec2viz_<tema>.py` que pasan e importan solo sldb; docstrings con casos no portados y motivo; fixtures en `tests/notations/fixtures`; línea en `CHANGELOG.md`; informe en `runs/subagents/<run-dir>/result-summary.md`. Repo: `/mnt/ssd/proyectos/SLDB_1` (sldb), leyendo `/mnt/ssd/proyectos/SLDB_1/spec2viz/tests`. Límites: no modificar spec2viz ni `src/sldb`; no portar renderers; fallo en sldb → xfail y aviso, no arreglo; no push; commit del coordinador. Nodo ejecutable, no agregado.

AMBIGUEDADES
1. “se marca xfail con el motivo y se manda una nota al inbox de sldb” frente a “el aviso va como línea "Aviso a <repo>: ..." en el informe”. ¿El fallback equivale a “se mandó nota al inbox” para `Done When`? Obliga a inventar si el xfail es válido sin mensaje real.
2. “La nota al inbox por un xfail se manda con deskops message send --to sldb --title "Paridad con spec2viz: <caso>"” frente a “Un aviso con deskops message send --to <repo> lleva como título el de la tarea”. ¿Qué título prevalece? Obliga a inventar jerarquía.
3. “por cada caso decidir si prueba algo que existe en sldb” y “en duda, se porta”: no define casos con varios símbolos, unos existentes y otros no. Obliga a inventar granularidad: caso completo o aserción.
4. “Fixtures copiadas van a una carpeta fixtures dentro de tests/notations, con el nombre original”: no prevé colisiones. Obliga a inventar renombrado o subcarpetas.

DRY-RUN
Lecturas: doc de tarea; siete tests de spec2viz; `src/sldb` (`api.notations`, `notations`, `models.notation`); `tests/notations` y helpers; `CHANGELOG.md`. Cambios previstos: inventario y mapa símbolo→equivalente; crear siete archivos y fixtures; docstrings; xfail/avisos; CHANGELOG; result-summary. Dependencias: spec2viz legible, helpers/`sldb.api`, deskops registrado. Validaciones futuras: `pytest -q tests/notations/ -k ported_from_spec2viz`; grep de imports spec2viz; revisar docstrings, xfail y avisos.

FUTURO
El coordinador ejecuta `deskops closeout commit` y no hace push. Los destinatarios de avisos deciden corregir paridad. La retirada de spec2viz queda condicionada a esta cobertura. El humano valida el commit.
