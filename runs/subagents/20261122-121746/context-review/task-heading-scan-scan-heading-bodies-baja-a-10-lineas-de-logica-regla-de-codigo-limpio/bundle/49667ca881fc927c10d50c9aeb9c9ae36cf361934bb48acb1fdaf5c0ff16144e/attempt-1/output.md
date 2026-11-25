## REFORMULACION

Encargo de refactor de código limpio en el repo sldb: en `src/sldb/api/documents/heading_scan.py`, partir `scan_heading_bodies` extrayendo una función auxiliar privada del mismo archivo, de modo que la original quede en ≤10 líneas de lógica según el conteo del test (del primer al último statement del cuerpo, sin docstring), sin cambiar comportamiento. Resultado: `tests/test_clean_code_rules.py` pasa y el integrate de sldb se desbloquea. Límites: solo ese archivo; fuera cambiar tests o comportamiento; commit acotado a ese archivo con trailer `Task-Id`.

## AMBIGUEDADES

1. "bash tools/check.sh --fast en verde salvo 'identidad' por workbench_demo (excepción f055723d)" — el bundle no define qué es el check `identidad` ni la excepción `f055723d`; obligaría a inventar cómo interpretar su salida y si el resto de check.sh debe estar verde.
2. "p4: commit desde el worktree que dispatch te da" — el worktree no aparece en el input; obligaría a inventar su ruta.
3. Validación lista solo dos archivos, pero Done When dice "Los tres archivos de tests pasan" y p2 nombra además `tests/test_extraction_segments.py`; obligaría a inventar cuál es el conjunto exigido.
4. "partiéndola en una auxiliar privada del mismo archivo" — nombre y firma no se especifican; no obliga a inventar comportamiento, pero sí una decisión de diseño.

## DRY-RUN

Lecturas: `heading_scan.py`, `tests/test_clean_code_rules.py` (para replicar el conteo), los tres tests nombrados. Cambios previstos: extraer la auxiliar privada y reemplazar el cuerpo por la llamada, sin alterar semántica. Dependencias: worktree provisto por dispatch, entorno pytest con `TMPDIR=/tmp`. Validaciones futuras: pytest de `test_clean_code_rules.py`, `test_lossy_overwrite_content.py` y `test_extraction_segments.py`; `tools/check.sh --fast`; commit con `Task-Id`. No se ejecuta nada.

## FUTURO

Dispatch entrega el worktree; un nodo ejecutor realiza el refactor y las validaciones; un humano u otro nodo resuelve la discrepancia de archivos de test y el significado de la excepción `f055723d`, y closeout retira la tarea del Board.
