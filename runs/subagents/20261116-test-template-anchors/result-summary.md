# Tester deskops-t-54ea165c28be: task-sldb-api-template-anchors

**Veredicto: PASA**

La salida completa está en `validation.log`, en este mismo directorio. `uv run --frozen` funcionó sin usar el respaldo `uvx`, y `uv.lock` ya venía modificado de antes (es un cambio ajeno).

## Validation

| Comando | Resultado |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_literal_paragraph_anchor.py` | PASA: 8 passed, rc 0 |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast` | PASA: "TODAS LAS PUERTAS PASAN", rc 0. La puerta de capas da 0 violaciones con api → runtime |

## Done When

| Punto | Veredicto | Evidencia |
|---|---|---|
| `from sldb.api import template_anchors` funciona | PASA | `python -c` imprime la función, y `'template_anchors' in sldb.api.__all__` da True |
| El test del modelo de prueba pasa | PASA | `Anchored` (con `goal` y `implementation_path` anclados y `notes` sin ancla) devuelve exactamente las dos claves con el texto en cursiva. También pasan el roundtrip render/extract y los TypeError |
| check.sh --fast pasa | PASA | Ver arriba |
| CHANGELOG | PASA | Hay una línea en español bajo `## 0.1.13 — not released yet`, al estilo de las entradas vecinas |
| Commit y aviso a deskops | Fuera de mi alcance | Según las Convenciones, los hacen el coordinador y el closeout. Aún no están hechos |

## Cumplimiento de las precisiones del Scope

- Las recetas salen de `sldb.runtime.validation._recipes(model.__template__)`. Es la misma llamada que hace `Validator._get_recipes`, así que no hay un parseo propio de la plantilla. Lo único propio es deshacer `re.escape` sobre la regex `^…$` del ancla, que arma `_add_anchor_recipe` (`get_text(node).strip()`).
- Una entrada que no es una clase lanza TypeError. Lo probé con una instancia, `dict`, un str, `None` y `3`.
- `src/sldb/core/template_extractor.py` no cambió: `git diff` sale vacío.

## Bordes no cubiertos por el ejecutor

Script en `/dev/shm/tta/edge.py` y `edge2.py`, sin tocar el repo. Todos dan el resultado esperado y cada ancla aparece literal en lo que produce `render_model_markdown`:

- **Dos párrafos literales seguidos:** solo cuenta el inmediatamente anterior (`_Second._`).
- **Párrafo en la sección previa con un heading en medio:** no hay ancla, `{}`.
- **Caracteres especiales de regex** `( | [ ] $ ^ ? + { }` y `*…*`: el texto sale exacto.
- **Backslashes literales** (`C:\\path`) y backticks: el texto sale exacto y el roundtrip da `{'title':'T','a':'X'}`.
- **Espacios al final del párrafo:** se recortan.
- **Campo inline** (`Status: ⸢rev•status⸥`) tras un párrafo literal: se ancla.
- **Lista literal antes del campo:** no es ancla de párrafo, `{}`.
- **Unicode** (`qué — ñ`): el texto sale exacto.
- **Párrafo con salto suave:** conserva el `\n` del template.
- **`StructuredNLDoc` base:** devuelve `{}` sin error. Es aceptable, porque es un `type[StructuredNLDoc]`.

Observación menor, que no bloquea: el módulo importa el helper privado `_recipes`. El contrato lo pide así de forma implícita ("la misma llamada que hace Validator(model).extract") y la puerta de capas lo acepta.

## Archivos fuera del contrato

Los únicos archivos que tocó el ejecutor son los del contrato: `template_anchors.py` (nuevo), `api/__init__.py`, `tests/test_literal_paragraph_anchor.py` y `CHANGELOG.md`, además de su directorio de run. El resto de `git status` es ajeno:

- Los cambios que ya listaba el brief.
- En `.sldb/` (`store.yaml`, `core/models/RunDoc.yaml`, `core/store_index.yaml` y los dos `RunDoc/run-deskops-{e,t}-*.yaml` nuevos): son el registro de los RunDoc del despacho de este ejecutor y este tester (el include de `runs/subagents/20261116-{exec,test}-template-anchors/run.md`), no código de la tarea.
- `tests/api/test_apply_batch_lock.py`, que es ajeno.
