## REFORMULACION
Propósito: eliminar dos fricciones de `sldb` al renderizar/extraer marcadores `rev` con valor `None` y al actualizar un campo `optrev` que vale `None`. El nodo es `task.code` ejecutable, no un agregado.

Resultado esperado: `rev=None` renderiza el literal `null` y `extract` lo devuelve como `None` (round-trip); un `optrev=None` puede volver a fijarse con `fields update <doc> <campo> <valor>`; se añade `tests/test_rev_optrev_none.py`.

Repo: `sldb` (workspace `desk`). Límites: dentro, render/extract de `rev`/`optrev` y `fields update` de un path con valor `None`, con tests. Fuera: tablas, `BaseModel`/dict tipado y `docs create` con rutas relativas.

## AMBIGUEDADES
1. “Arreglo en render/extract y fields update” no nombra archivos, módulos ni funciones. Obliga a inventar dónde vive cada comportamiento.
2. “Correr solo ese test” contradice parcialmente el ritual de testing: “then the full suite when shared behavior changed”. Obliga a decidir si el arreglo es cambio compartido y exige suite completa.
3. “igual con una clave null dentro de un dict tipado” aparece en Rationale, pero Scope dice “Fuera: tablas, BaseModel, docs create”. Obliga a decidir si el caso dict/null queda incluido o solo se documenta.
4. El título incluye “tablas vacias, dict de BaseModel y rutas relativas de docs create”, mientras Scope las excluye. Aunque Scope parece resolverlo, obliga a decidir si el título es aspiracional o contrato.
5. “fields update <doc> <campo> <valor>” no precisa cómo se representa `None` en la CLI ni si `valor='x'` debe ser string. Obliga a inventar el parser y la semántica exacta.

## DRY-RUN
Lecturas hipotéticas: TaskDoc, Board, rituales execution/testing/closeout, pills/átomos ligados, código de render/extract y `fields update`, tests existentes y estado git.

Cambios previstos: crear `tests/test_rev_optrev_none.py` con modelo mínimo; ajustar render para emitir `null` cuando `rev is None`; ajustar extract para devolver `None` desde `null`; permitir que `fields update` escriba un `optrev` previamente `None`. Sin tocar tablas, `BaseModel` ni `docs create`.

Dependencias: localizar las funciones reales, el modelo/CLI de fields update y el entorno pytest indicado.

Validaciones futuras: ejecutar exactamente `TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_rev_optrev_none.py`; decidir si aplica suite completa por cambio compartido. Nada se ejecuta ahora.

## FUTURO
Otro ejecutor implementará y correrá las pruebas; el closeout humano/deskops decidirá commit, CHANGELOG y salida del Board. Si las ambigüedades no se resuelven, corresponde solicitar contexto antes de ejecutar.
