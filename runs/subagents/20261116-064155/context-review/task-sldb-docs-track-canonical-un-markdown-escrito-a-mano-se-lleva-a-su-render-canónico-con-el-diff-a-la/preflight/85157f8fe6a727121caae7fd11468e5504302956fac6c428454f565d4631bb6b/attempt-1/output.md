## REFORMULACION

Propósito: que un Markdown escrito a mano se lleve a su render canónico antes de trackearlo, mostrando el diff, para dar algo visible a cambio de usar la API. Resultado: flag `--canonical` en `sldb docs track`; parámetro `canonical: bool=False` en `track_document_file` que, antes de `_refuse_unfit`, sustituye el texto por `render_model_markdown(extract_model_data(texto))` y devuelve `canonical_diff`; tres tests; línea en skill y CHANGELOG. Repo: el de `src/sldb` (no se nombra explícitamente). Límites: fuera hook PreToolUse, autocarga de skill y POST /docs; el ejecutor no hace push y el commit es del coordinador.

## AMBIGUEDADES

1. «`render_model_markdown(extract_model_data(texto))`» no indica cómo entra `--model`; obliga a inventar firma y orden de argumentos.
2. «campo `canonical_diff` opcional, "" si no hubo cambios» no fija tipo/default con `canonical=False` ni impacto en serialización; obliga a inventar el contrato.
3. «que el render normaliza a uno» presupone que el render colapsa dos espacios; no lo verifica; obliga a inventar el campo o el caso.
4. «sale con 1 mostrando el error» y «error en stderr» no fijan formato; obliga a inventar el texto.
5. «`difflib.unified_diff`» omite `fromfile`/`tofile`/`lineterm`; obliga a inventar cabeceras.
6. «`deskops message send --to <repo>`» deja `<repo>` sin resolver; obliga a inventar el identificador.
7. «El commit lo hace el coordinador» frente a Done When «commit»: contradicción sobre quién commitea.

## DRY-RUN

Lecturas: `docs1.py` (`_track`), comando (grep `track_document_file`), `track_document_file.py`, `runtime/validation.py`, `tests/test_cli_v2.py`, skill y CHANGELOG. Cambios previstos: API con extracción→render→validación→escritura y diff; parser `--canonical`; impresión de `canonical_diff` o «already canonical»; tres tests; textos de skill/CHANGELOG. Dependencias: firmas reales de extract/render, modelo obligatorio, helpers de test existentes. Validaciones futuras: `pytest -q tests/test_cli_v2.py`, `pytest -q tests/api/test_on_write_entering.py`, `--help`, y revisión de que sin flag no cambia nada.

## FUTURO

El coordinador ejecuta `deskops closeout commit` (mensaje con título corto) y no hay push por el ejecutor. Un nodo/task.decision aparte cubre hook y autocarga. El aviso al repo lo envía quien pueda; si no está registrado, va como línea en `runs/subagents/<run-dir>/result-summary.md`.
