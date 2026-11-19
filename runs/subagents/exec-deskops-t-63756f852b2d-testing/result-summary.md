PASA

# Tester deskops-t-63756f852b2d: resultado

Task: `task-la-escritura-por-campos-save-document-payload-y-el-update-de-apply-batch-falla-nombrando-el-contenid`
Commit revisado: `6a4e5ec5b53cef87912df4667c67f133bed54c95` — `save_document_payload refuses to drop undeclared headings/frontmatter`
Archivos del commit: `CHANGELOG.md`, `src/sldb/api/documents/lossy_overwrite.py` (nuevo), `src/sldb/api/documents/payload_save.py`, `tests/api/test_structural_noise.py`, `tests/api/test_transaction.py`.

## Veredicto

**PASA.** La guarda se aplica antes de renderizar y escribir. `refuse_lossy_overwrite` lee el texto actual del documento (con `guarded_text`) y corre `refuse_structural_noise` y `refuse_undeclared_frontmatter`, las mismas guardas de `docs create`/`docs track`, con `SLDBValidationError` y un mensaje que nombra los encabezados o claves que se perderían. `save_document_payload._save` la llama como primer paso, de modo que el `update` de `apply_batch` (vía `transaction_ops.update`) también queda cubierto. Los tests nuevos comprueban que el archivo queda byte a byte intacto y que un documento limpio se sigue escribiendo.

No hay tests de módulo dedicados para `lossy_overwrite.py` ni `payload_save.py`; los casos quedan cubiertos por `tests/api/test_structural_noise.py` y `tests/api/test_transaction.py`, como pedía el Scope.

## Validación ejecutada

Detalle completo en `validation.log`. `/tmp/ws-venv` no existe en este entorno; se usó el venv del proyecto (`.venv/bin/python`, Python 3.13), el mismo intérprete con el que corren las puertas.

| Comando | rc | Resultado |
|---|---|---|
| `pytest -q tests/api/test_structural_noise.py` | 0 | 13 passed |
| `pytest -q tests/api/test_transaction.py` | 0 | 16 passed |
| `pytest -q tests/api/test_api_documents.py` | 0 | 17 passed |
| `pytest -q tests/api/test_write_paths_validate.py` | 0 | 5 passed |
| `pytest -q tests/test_clean_code_rules.py` | 0 | 1212 passed |
| `pytest -q tests/api/test_apply_batch_dry_run.py` (extra, camino apply_batch) | 0 | 4 passed |
| `bash tools/check.sh --fast` | 0 | todas las puertas PASAN |

## Observaciones (no bloqueantes)

- Se creó `src/sldb/api/documents/lossy_overwrite.py` en vez de poner el helper directamente en `payload_save.py`: el Scope nombraba `payload_save.py`/`payload_save_steps.py`, pero el helper es pequeño, está en el paquete correcto y `check.sh --fast` (capas, ejes, núcleo aislado) pasa.
- La guarda no se ejecuta en la prevalidación de `apply_batch(..., dry_run=True)`, así que un `dry_run` sobre un archivo sucio devuelve `planned` y solo el apply real falla. Queda fuera del Goal de esta tarea ("falla antes de escribir"), que se cumple; si se quiere que `dry_run` anticipe también este error, sería un cambio aparte.
