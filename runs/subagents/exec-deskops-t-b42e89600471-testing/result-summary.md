PASA

# Verificación: _check_store_document a <=10 líneas de lógica

**Commit del ejecutor:** `fb321318b5972d07ea9109477024036c5f5c4d04`
`notations validate: split _check_store_document and validate_target (clean code rules)`

**Archivos tocados (solo 2):**
- `src/sldb/cli/commands/notations_validate.py`
- `src/sldb/cli/commands/notations_validate_store.py` (nuevo)

## Resultado de tests (de a uno, `TMPDIR=/tmp`)

| Test | Resultado |
|---|---|
| `tests/test_clean_code_rules.py` | 1234 passed, rc=0 |
| `tests/notations/test_notations_validate_cli.py` | 11 passed, rc=0 |
| `tests/notations/test_notations_sync_spec_cli.py` | 4 passed, rc=0 |
| Comando de Validation combinado (clean_code + validate_cli) | 1245 passed, rc=0 |

## Regla de código limpio

- `_check_store_document` en `notations_validate_store.py`: **10 líneas de lógica** (máximo 10).
- `validate_target`: 5 líneas de lógica.
- `notations_validate.py`: 78 líneas efectivas (máximo 80).
- `notations_validate_store.py`: 36 líneas efectivas.

## Comportamiento

La lógica de store (`_store_has`, búsqueda de payload y validación de paleta) se movió a un módulo hermano con extracciones mecánicas (`_store_payload`, `_check_palette_payload`). `validate_target` conserva el orden de hallazgos (alerta de ambigüedad antes del finding) y la misma ramificación archivo/nombre. Los tests de CLI cubren nombres solo en store, paleta inválida en store y notación inválida en store: todos verdes.

## Gate rápido del desk

`bash tools/check.sh --fast` termina rc=1, pero **el único gate que falla es `identidad` por `workbench_demo`**, la excepción autorizada explícitamente en la tarea. `núcleo aislado`, `capas`, `ejes` y `superficie` pasan. No hay fallas nuevas atribuibles al cambio.

## Veredicto

**PASA.** Los tres archivos de tests pasan, la función cumple el límite de 10 líneas y no se detecta cambio de comportamiento.
