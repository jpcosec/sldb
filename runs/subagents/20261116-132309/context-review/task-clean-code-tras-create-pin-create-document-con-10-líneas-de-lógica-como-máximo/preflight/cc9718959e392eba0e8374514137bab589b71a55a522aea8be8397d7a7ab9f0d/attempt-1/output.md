## REFORMULACION

Corregir una violación de clean code introducida por task-create-document-pinnea (e82d62ba): `create_document` en `src/sldb/api/documents/create_document.py` tiene 12 líneas de lógica (máximo 10). Repo: `/mnt/ssd/proyectos/SLDB_1`, workspace desk. Resultado: `tests/test_clean_code_rules.py` y `bash tools/check.sh --fast` pasan; comportamiento y API pública idénticos; tests de comportamiento originales verdes sin cambios; una línea en CHANGELOG bajo 0.1.13 y commit. Límites: no cambiar comportamiento ni tests; no tocar otras violaciones (solo anotarlas); extracción en el mismo archivo o módulo vecino del mismo paquete, con reexport.

## AMBIGUEDADES

1. «pin_payload, _rendered, pin_provenance»: nombres no uniformes (pin_payload sin guion bajo). Obliga a inventar la convención exacta de nombres.
2. «en el mismo archivo si este sigue bajo 80 líneas»: no aclara si se mide antes o después de extraer. Obliga a inventar el criterio de conteo.
3. «Los nombres que hoy se importan desde el módulo original»: no se enumeran. Obliga a inventar la lista de reexports.
4. «bajo '## 0.1.13 — not released yet'»: no consta que esa sección exista. Obliga a inventar qué hacer si falta.
5. «se anotan en result-summary.md»: ruta y formato no definidos. Obliga a inventar ubicación y formato.

## DRY-RUN

Un ejecutor futuro leería `create_document.py`, `tests/test_clean_code_rules.py`, los tres tests de API de Validation, `CHANGELOG.md` y `tools/check.sh`. Cambios previstos: extraer función(es) privada(s) de pinneo/render/provenance o de escritura, reexportar nombres públicos desde el módulo original y añadir la línea de CHANGELOG. Dependencias: `uv` con extras code/dev, `TMPDIR=/dev/shm`, `check.sh`. Validaciones futuras: los cinco comandos de Validation más `git diff` para confirmar que los tests de comportamiento no cambiaron. No se ejecuta nada.

## FUTURO

Un humano u otro nodo decide: si la extracción va en el mismo archivo o en módulo vecino y con qué nombre; la lista definitiva de reexports; si las otras violaciones detectadas se abren como tareas aparte; el mensaje de commit.
