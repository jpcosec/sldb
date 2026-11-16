# Ejecutor deskops-e-a5fa67d6c1db — task-sldb-api-template-anchors

Resultado: LISTO 0.

## Qué cambió

- `src/sldb/api/model_registry/template_anchors.py` (nuevo): `template_anchors(model_type) -> dict[str, str]`.
  - Lanza `TypeError` si `model_type` no es una subclase de `StructuredNLDoc`.
  - Las recetas salen de `sldb.runtime.validation._recipes(model_type.__template__)`, la misma llamada que hace `Validator(model).extract` (vía `_get_recipes`, con su caché `lru_cache`). No hay parseo propio de la plantilla.
  - Por cada par de recetas consecutivas: si la anterior es una receta `anchor: True` con `outer_type == "paragraph"` (y no vacía) y la siguiente está en el bloque inmediatamente siguiente (`outer_index + 1`), cada campo de esa receta (`props_info`, `marker` o `markers`) recibe el texto del párrafo. Un heading en medio es un bloque propio, así que el ancla siempre es de la misma sección.
  - El texto se obtiene deshaciendo el `re.escape` de la regex del ancla (`^…$`), que el extractor arma con `get_text(node).strip()`: es el párrafo tal como está en `__template__`, cursivas incluidas, sin espacios al final.
- `src/sldb/api/__init__.py`: import de `template_anchors` y entrada en `__all__`.
- `tests/test_literal_paragraph_anchor.py`: modelo `Anchored` con dos campos anclados por párrafos en cursiva (`goal`, `implementation_path`) y uno sin ancla (`notes`), más el título. Tests: el dict tiene exactamente las dos claves con el texto literal (y `Note` da `{"body": "_Describe the message._"}`); el texto es lo que render escribe y extract consume (roundtrip); `TypeError` para instancia, clase ajena y string.
- `CHANGELOG.md`: una línea bajo `## 0.1.13 — not released yet`.
- `src/sldb/core/template_extractor.py`: no se tocó; no hizo falta.

## Done When

- `from sldb.api import template_anchors` funciona: lo usan los tests (rc 0).
- El test del modelo de prueba pasa: 8 passed (rc 0).
- `check.sh --fast` pasa: TODAS LAS PUERTAS PASAN (rc 0).
- CHANGELOG: hecho. Commit y aviso a deskops (`deskops message send --to deskops`): los hace el coordinador en el closeout según las Convenciones; el ejecutor no hace commit (prohibido por el brief). Texto propuesto del aviso: título de la tarea; cuerpo "sldb.api.template_anchors(model_type) devuelve {campo: párrafo ancla literal} desde las recetas del extractor; deskops puede dejar de usar AST_Handler/TemplateExtractor para detectar placeholders. Commit: <sha del closeout>".

## Comandos (salida completa en validation.log)

- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_literal_paragraph_anchor.py` → rc 0 (8 passed)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast` → rc 0

## Archivos tocados

- src/sldb/api/model_registry/template_anchors.py (nuevo)
- src/sldb/api/__init__.py
- tests/test_literal_paragraph_anchor.py
- CHANGELOG.md
- runs/subagents/20261116-exec-template-anchors/validation.log, result-summary.md

## Desvíos y dudas

- Se importa el helper privado `_recipes` de `sldb.runtime.validation` porque es literalmente la llamada que usa `Validator.extract` (lo pide la Precisión). Alternativa equivalente: `Validator(model_type)._get_recipes()`. La capa api→runtime ya existe (p. ej. `api/documents/create_document.py`) y la puerta de capas pasa.
- El texto se reconstruye deshaciendo `re.escape` de la regex del ancla, porque la receta no guarda el texto suelto; es exacto (re.escape solo antepone barras).
- Sin pills atados; no hubo choque pill/contrato.
