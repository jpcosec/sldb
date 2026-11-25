## REFORMULACION

Propósito: que quien escribió Markdown a mano reciba, al trackearlo, el render canónico y el diff visible en vez de un rechazo seco. Resultado: `sldb docs track <ruta> --model <M> --canonical` extrae el payload, lo renderiza, imprime el diff unificado, reescribe el archivo canónico y lo trackea; si la extracción o validación falla, no escribe y sale con 1. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: fuera el hook PreToolUse, la autocarga de skill y POST /docs de `sldb serve`; sin `--canonical`, track se comporta como hoy.

## AMBIGUEDADES

1. "imprime el diff unificado entre el archivo y el render canónico" y "devuelve el diff en el DocumentReference (campo canonical_diff opcional, \"\" si no hubo cambios)": no dice si la CLI imprime desde ese campo ni qué muestra con diff vacío. Obliga a inventar el contrato de salida.
2. "un archivo con un campo escrito con espacios de más": no concreta campo, espacios ni criterio de "canónico". Obliga a inventar el fixture.
3. "antes de _refuse_unfit, reemplaza el texto por render_model_markdown(extract_model_data(texto))": no aclara si `_refuse_unfit` valida el texto original o el canónico; el caso "no valida" queda indefinido. Obliga a inventar el orden semántico.
4. "`sldb docs track <ruta> --model <M> --canonical`": no dice si `--canonical` exige `--model` ni si hay default. Obliga a inventar la validación de flags.
5. "sale con 1 mostrando el error": no especifica canal ni formato del error. Obliga a inventar el mensaje.
6. "la línea correspondiente en la skill `src/sldb/assets/skills/sldb.md`": no identifica línea ni redacción. Obliga a inventar el texto.

## DRY-RUN

Lecturas: `src/sldb/cli/parsers/docs1.py` (`_track`), comando docs track, `track_document_file.py`, `src/sldb/runtime/validation.py` (`extract_model_data`, `render_model_markdown`), `tests/test_cli_v2.py`, `tests/api/test_on_write_entering.py`, skill y CHANGELOG. Cambios previstos: parámetro `canonical: bool = False` con diff vía `difflib.unified_diff`; flag en parser; impresión, reescritura y trackeo; tres tests; docs. Dependencias: firmas reales de extracción/render y del modelo; forma de `DocumentReference`. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py`, `TMPDIR=/dev/shm pytest -q tests/api/test_on_write_entering.py` y `--help`.

## FUTURO

Otro nodo o un humano ejecuta la implementación y el commit, decide la redacción final de skill/CHANGELOG y confirma el contrato de salida del diff. Las partes (a) y (c) del drawer quedan en una task.decision aparte.
