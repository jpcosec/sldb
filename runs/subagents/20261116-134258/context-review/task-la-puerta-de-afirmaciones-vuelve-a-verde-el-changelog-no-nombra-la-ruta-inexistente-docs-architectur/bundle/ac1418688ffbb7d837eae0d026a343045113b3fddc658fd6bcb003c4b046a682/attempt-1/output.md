## REFORMULACION

**Propósito:** devolver a verde la puerta de afirmaciones corrigiendo una ruta inexistente en `CHANGELOG.md`. **Resultado:** `tests/test_clean_code_rules.py` y `bash tools/check.sh --fast` pasan; solo cambia la línea del CHANGELOG que nombra la copia de `vistas.yml`, escribiendo `tests/notations/fixtures/docs/architecture/vistas.yml`; los tests de comportamiento no cambian. **Repo:** sldb. **Límites:** solo `CHANGELOG.md`; no se añaden líneas ni se tocan otras; no se modifica código ni tests; otras afirmaciones falsas se anotan en `result-summary.md` y no se corrigen. El nodo es una tarea ejecutable, no un agregado.

## AMBIGUEDADES

1. “se anotan en result-summary.md del run”: no se indica la ruta concreta ni el formato del archivo; obligaría a inventar dónde y cómo registrar las otras afirmaciones falsas.
2. “CHANGELOG y commit”: no se especifica mensaje, tipo ni alcance del commit; obligaría a inventar el mensaje.
3. “los tests de la tarea original siguen verdes sin cambios”: no enumera aquí esos tests; obligaría a decidir cuáles son si no se usara el átomo ligado, que sí menciona los siete `tests/notations/test_ported_from_spec2viz_*.py`.

## DRY-RUN

**Lecturas previstas:** `CHANGELOG.md`, `tests/test_clean_code_rules.py`, `tools/check.sh`, el átomo ligado y los fixtures bajo `tests/notations/fixtures/docs/architecture/`. **Cambios previstos:** una única sustitución de ruta en la línea indicada del CHANGELOG. **Dependencias:** entorno `uv` con extras `code` y `dev`, `TMPDIR=/dev/shm`, git limpio y acceso al repo. **Validaciones futuras:** ejecutar primero `pytest -q tests/test_clean_code_rules.py` y después `bash tools/check.sh --fast`; comprobar con `git diff` que solo cambia esa línea y que no se tocaron tests de comportamiento.

## FUTURO

El nodo de testing producirá la evidencia de ejecución de ambas validaciones. El nodo de closeout actualizará el CHANGELOG si corresponde, hará el commit atómico, cerrará la tarea con `deskops closeout` y dejará el árbol limpio. Un humano o un nodo posterior decidirá qué hacer con las demás afirmaciones falsas anotadas en `result-summary.md`.
