# Resultado — executor deskops-e-08683ea7876c

Tarea: `task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari`. Resultado: **LISTO, rc 0** en todos los comandos de Validation.

## Qué cambió

- `src/sldb/core/renderer_engine/base.py`
  - `BaseRenderer.replace_markers`: el valor de un marcador ya no se pega en el texto fuente. Cada marcador se reemplaza por `{{ _sldb_marker_values[i] }}` (constante de módulo `_REF`), y la lista de valores se pasa en el contexto del render (`render({**data, "_sldb_marker_values": values})`). Jinja imprime el valor y nunca lo compila. Así lo decidió el coordinador en (1): una variable de contexto por marcador. Ninguna salida dependía de un filtro de Jinja aplicado al valor (los valores ya llegaban como texto formateado por `_resolve_marker`), así que no se aplica ningún filtro.
  - `BaseRenderer._bind` (nuevo): llama a `_sub_marker` (el recorder envuelve el valor igual que antes), guarda el resultado en la lista y devuelve la referencia de Jinja.
  - El salto de línea final: Jinja (`keep_trailing_newline=False`) solo descarta el salto final del **texto fuente**. Antes, el salto final de un valor que cerraba el bloque era parte de ese texto y se perdía; ahora es salida de una expresión y Jinja lo conservaría. Para dar los mismos bytes, cuando el texto fuente termina en la referencia del último valor, a ese valor se le aplica `unshield_trailing_newline` (que no hace nada si no lleva centinelas) y se le quita un `\n`. Eso reemplaza el `unshield_trailing_newline(source)` que se aplicaba solo en modo recorder.
  - `_is_absent_optional_line` (optrev) no cambió: las líneas ausentes se descartan antes, igual que antes.
  - Clean code: 80 líneas efectivas (el máximo), `replace_markers` 6 líneas de lógica y `_bind` 2.
- `tests/test_list_items_round_trip.py`: el modelo `Scoped` y `test_a_value_is_never_compiled_as_jinja`, con 11 valores: la reproducción de la nota (`{{.State...}}`), dos llaves, tres llaves, tres llaves al final, expresión más comentario, `{% if %}`, `{% for %}{{ i }}`, `{% raw %}`, llaves de cierre sueltas y `%} #}`, un valor con `⸢rev•title⸥` y `{%- x -%}`. Cada uno va en el título, en un campo escalar y en un ítem de lista. El test exige que extract devuelva los datos exactos y que el valor aparezca literal 3 veces en el Markdown. Con el `replace_markers` de HEAD (cargado con un plugin de pytest, sin tocar el árbol): 9 fallan y 2 pasan (llaves de cierre y `⸢marcador⸥`, que la nota ya daba por literales).
- `CHANGELOG.md`: una entrada en 0.1.13.

## Comparación con HEAD (punto 4 del coordinador)

Un plugin de pytest (`scratchpad/plug/rmrec.py`, fuera del repo) registró la entrada y la salida de cada llamada a `BaseRenderer.replace_markers`, con HEAD y con el cambio, sobre los 22 archivos de `tests/` que renderizan (grep de `replace_markers|render_model_markdown|render_markdown|.render(`, sin `test_apply_batch_lock`) más los 3 de Validation. Hubo 58469 entradas distintas con cada versión; 58452 son comunes y las 58452 dan **0 diferencias de bytes**, con y sin recorder. Las 17 que no coinciden entre corridas son entradas con datos que cambian en cada ejecución (rutas temporales o marcas de tiempo), así que no se pueden emparejar. En esa corrida combinada hay 14 errores `fixture 'api_store' not found` en `tests/api/test_api_documents.py`, iguales con HEAD y con el cambio: salen de mezclar archivos en una sola invocación. Corrido solo, ese archivo pasa 17/17.

## Done When

- Los comandos de Validation pasan con los tests nuevos de roundtrip: sí, todos con rc 0 (abajo).
- Los casos de la nota se guardan literales: sí, todos están en `JINJA_LOOKALIKES` y vuelven byte a byte en extract.
- CHANGELOG: sí. **Commit y aviso a deskops: no**, por la decisión (5) del coordinador. Los dejo al coordinador e integrador (deskops tiene que quitar su `xfail(strict=True)` de `tests/test_message_cli.py`).

## Comandos (salida completa en validation.log)

| comando | rc |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py` | 0 (43 passed) |
| `... pytest -q tests/api/test_api_documents.py` | 0 (17 passed) |
| `... pytest -q tests/api/test_structural_noise.py` | 0 (10 passed) |
| `... pytest -q tests/test_clean_code_rules.py` | 0 (1202 passed) |
| `... bash tools/check.sh --fast` | 0 (todas las puertas pasan) |
| `... pytest -q tests/test_list_items_round_trip.py` | 0 (24 passed) |
| `PYTHONPATH=src ... python3 tools/check_claims.py` (extra, informativo) | 1: 11 afirmaciones falsas, **todas ya en HEAD**. Las 3 del CHANGELOG (`docs/missing`, `docs/ambiguous`, `sldb query`) son entradas viejas; ninguna está en la línea nueva |

La suite completa y `sldb stores build --check` no se corrieron: quedan delegados al integrador.

## Archivos tocados

- `src/sldb/core/renderer_engine/base.py`
- `CHANGELOG.md`
- `tests/test_list_items_round_trip.py` (lo autorizan el Scope, "en un archivo de tests del renderer existente", y el punto 3 del coordinador)
- `runs/subagents/20261116-exec-jinja/validation.log`, `runs/subagents/20261116-exec-jinja/result-summary.md`

No toqué `desk/`, `.sldb/` ni los archivos ajenos; las modificaciones de `.sldb/` en `git status` ya estaban. No hice add, commit ni stash.

## Dudas y desvíos

- Cambio de comportamiento deliberado: si una plantilla rodea un marcador con control de espacios de Jinja (`{%- ... %}` justo después de un valor), antes se recortaba el espacio del final del valor y ahora no: el valor es literal. Ningún test ni modelo de los comparados lo usa (0 diferencias).
- Un marcador escrito dentro de una expresión Jinja de la plantilla (`{{ ⸢x⸥ }}`) dejaría de funcionar; el grep en `src`, `tests` y `.sldb` no encontró ninguno.
- El nombre `_sldb_marker_values` tapa un campo de datos con ese mismo nombre en el render; ningún modelo usa ese nombre.
- No hay pills en el bundle y no hubo choque con el contrato.
