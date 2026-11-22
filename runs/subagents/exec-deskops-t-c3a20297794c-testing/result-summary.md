PASA

# Testing — heading_scan: scan_heading_bodies a 10 líneas de lógica

Commit del ejecutor: `8d69e3a1f8caefa9174ad76b0358b50faf36715d` (`heading_scan: split scan_heading_bodies into _heading_spans helper`), con el trailer `Task-Id` correcto. Toca solo `src/sldb/api/documents/heading_scan.py`.

## Evidencia

- `tests/test_clean_code_rules.py` → **1235 passed** (rc 0). La regla de 10 líneas para `scan_heading_bodies` queda satisfecha.
- `tests/api/test_lossy_overwrite_content.py` → **6 passed** (rc 0).
- `tests/test_extraction_segments.py` → **6 passed** (rc 0).
- No existe `tests/test_heading_scan.py`; el commit no añade ni modifica tests.
- `bash tools/check.sh --fast` → rc 1 **solo** por la puerta `identidad`: `directorio versionado sin clasificar en la raíz: workbench_demo`. Es la excepción autorizada f055723d; núcleo aislado, capas, ejes y superficie pasan.

## Revisión del cambio

`scan_heading_bodies` delega la recolección de encabezados en una auxiliar privada del mismo archivo (`_heading_spans`) y conserva el cálculo de cuerpos y su salida. Refactor sin cambio de comportamiento.

Log completo: `validation.log`.
