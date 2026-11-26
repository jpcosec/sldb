PASA

# Tester exec-deskops-t-5cbfa34b77c2: NotationDoc declara el estándar que implementa

Task: `task-una-notationdoc-declara-que-estandar-implementa-y-sldb-notations-validate-lo-muestra`
Commit revisado: `318a353d9a75f6f47b929e78c1994b679821d64f` — `feat: a NotationDoc declares the standard it implements; notations list/validate show it`.
El commit no lleva `Task-Id`, como pide el encargo; se localizó por mensaje y fecha (2026-11-26T00:33:57Z).
Archivos: `docs/architecture/notations-and-views.md`, `src/sldb/api/notations/notation_listing.py`, `src/sldb/api/notations/notation_payloads.py`, `src/sldb/cli/commands/notations_validate.py`, `src/sldb/models/notation/notation_doc.py`, `src/sldb/notations/notation_spec.py`, `tests/test_notation_declares_standard.py` (+187/−3).

## Veredicto

**PASA.** El campo opcional `standard: {name, version}` existe en el modelo `NotationDoc`, se carga y valida desde el YAML de la notación, se guarda en el payload del store y se muestra al listar y validar. Sin el campo la notación sigue siendo válida. Un nombre vacío, un nombre de solo espacios o una versión sin nombre se rechazan con un mensaje que nombra la notación y el campo. La documentación de notaciones describe el campo y su relación con los tags semánticos.

## Validación ejecutada

Entorno: `/tmp/ws-venv` no existe en este contenedor; usé el venv del repo `/workspace/sldb/.venv` (Python 3.13.18) primero en `PATH`, con `TMPDIR=/tmp` y `PYTEST_ADDOPTS=--basetemp=/tmp/pytest-deskops-t-5cbfa34b77c2`.

| Comando | rc | Resultado |
|---|---:|---|
| `python -m pytest -q tests/test_notation_declares_standard.py` | 0 | **10 passed** |
| `python -m pytest -q tests/notations/test_notations_validate_cli.py tests/notations/test_notation_models_and_builtins.py` | 0 | **26 passed** |
| `python -m pytest -q tests/notations/test_notation_view_and_routes.py tests/notations/test_notations_sync_spec_cli.py` | 0 | **13 passed** |
| `python -m pytest -q tests/notations/test_ported_from_spec2viz_notation.py tests/notations/test_ported_from_spec2viz_style_palette.py` | 0 | **57 passed** |
| `bash tools/check.sh --fast` | 0 | todas las puertas pasan (núcleo aislado, capas, identidad, ejes, superficie) |

No se corrió la suite completa. No existe `tests/test_<modulo>.py` para `notation_listing`, `notation_payloads`, `notation_doc` ni `notation_spec`; los tests existentes que ejercitan esas rutas son los de `tests/notations/` corridos arriba. `tests/notations/test_notations_validate_cli.py` cubre el comando tocado.

Comprobación manual adicional en un store temporal (fuera del repo): sync de una notación con `standard: {name: BPMN, version: 2.0}` → `notations list` devuelve `standards: {"NotationDoc:flujo": {"name": "BPMN", "version": "2.0"}}` y `notations validate flujo --store ...` imprime `standard: BPMN 2.0` con rc 0. Validar una notación builtin sin estándar (`activity`) no imprime nada y sale rc 0.

## Revisión del cambio

- `StandardSpec` valida `name` no vacío y `version` no vacía si está presente; `NotationSpec` rechaza además `standard` que no sea un mapa o que traiga versión sin nombre, nombrando la notación (`notation 'mi-notacion': ...`). El mensaje nombra el campo (`standard.name` / `standard.version`).
- `notation_payload` persiste el estándar en el `NotationDoc`, y `notation_standards` lo recoge tanto de builtins como de documentos del store.
- `notations list` agrega la clave `standards` solo si alguna notación lo declara; `notations validate` imprime `standard: <name> [<version>]` solo para una notación válida que lo declare, y con `--json` devuelve `{findings, standard}`. Sin estándar mantiene la salida anterior (lista de findings / sin línea).
- `docs/architecture/notations-and-views.md` documenta el campo, por qué los tags semánticos no sirven para esto y que no hay reglas de cobertura del estándar.

## Observaciones no bloqueantes

- En `NotationDoc` el campo se guarda como `dict | None`, igual que `layout` y `markers`; la validación fuerte vive en `NotationSpec` (la carga desde YAML), que es el camino que pide el encargo. Un `NotationDoc` editado a mano en el store con un `standard` inválido no se rechaza al cargar el payload; queda fuera del alcance declarado, pero conviene tenerlo presente si más adelante se valida el store entero contra el modelo.
- `notation_standards` silencia cualquier excepción al leer builtins o el store y simplemente omite esa notación; es coherente con `store_notation_refs`, pero puede ocultar un fallo de carga en el listado.
