PASA

# Tester deskops-t-03790f9a4d76: resultado

Task: `task-el-guard-de-escritura-por-campos-refuse-lossy-overwrite-rechaza-headings-no-declarados-que-viven-den`
Commit revisado: `9e168c33deac9f077bfed425cd4a37df0127b1d2` — `Field-write guard refuses only content that is lost`
Archivos del commit: `src/sldb/api/documents/lossy_overwrite.py`, `src/sldb/api/documents/payload_save.py`, `tests/api/test_structural_noise.py`, `CHANGELOG.md`.

## Veredicto

**PASA.** `refuse_lossy_overwrite` recibe el texto renderizado y compara los headings no declarados del archivo actual contra los del texto nuevo: solo rechaza los que no sobreviven. Las claves de frontmatter no declaradas se someten a la misma comparación (solo se rechazan las ausentes del render). El guard se ejecuta después de renderizar en `save_document_payload`.

Comprobado el caso reportado:

- Un `### Sub` dentro del valor de un campo sobrevive a la escritura y ya no bloquea el `save`.
- Un heading no declarado fuera de todo campo (el caso de 6a4e5ec5, `## Extra`) se sigue rechazando con el mensaje que lo nombra y el archivo queda intacto.
- La clave de frontmatter no declarada (`stray`) se sigue rechazando.
- El test de deskops `tests/test_promotion_nesting.py::test_advance_task_keeps_nested_h3_sections_inside_scope` pasa con este sldb.

No se cambió `refuse_structural_noise` de `docs track`/`docs create`, como pide el Scope.

## Validación ejecutada

`/tmp/ws-venv` no existe en este entorno; se usó el venv del proyecto (`/workspace/sldb/.venv/bin/python`). No se corrió la suite completa.

| Comando | rc | Resultado |
|---|---|---|
| `TMPDIR=/tmp .venv/bin/python -m pytest -q -p no:cacheprovider tests/api/test_structural_noise.py tests/api/test_transaction.py` | 0 | 31 passed |
| `TMPDIR=/tmp .venv/bin/python -m pytest -q -p no:cacheprovider tests/api/test_api_documents.py tests/api/test_write_paths_validate.py tests/api/test_transaction_rules_dirty.py` | 0 | 30 passed |
| `cd /workspace/deskops && TMPDIR=/tmp SLDB_SRC=/workspace/sldb/src /workspace/sldb/.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_promotion_nesting.py` | 0 | 2 passed |
| `PATH=/workspace/sldb/.venv/bin:$PATH TMPDIR=/tmp bash tools/check.sh --fast` | 0 | todas las puertas PASAN |

No existe `tests/test_lossy_overwrite.py` ni `tests/test_payload_save.py`; la cobertura de los módulos tocados está en `tests/api/test_structural_noise.py`, `tests/api/test_transaction.py` y `tests/api/test_api_documents.py`.

## Evidencia de los tests nuevos

`test_save_keeps_a_heading_that_lives_inside_a_field_value` guarda dos veces un `body` con `### Sub`, verifica que el heading sigue en el archivo y que el segundo cambio de `title` se escribe.

`test_save_still_refuses_a_heading_outside_every_field` añade `## Extra` al archivo y verifica que el save falla nombrando `## Extra`.

## Observaciones no bloqueantes

- No hay un test dedicado a una clave de frontmatter no declarada que sobreviva al render; el comportamiento existente de rechazar una clave perdida sí está cubierto por `test_save_refuses_a_file_with_undeclared_frontmatter`.
- El guard ahora corre después de `check_rules_on_write` y `render_checked`; si el render falla, el error es de round-trip antes que el de pérdida. No afecta al Goal ni a la validación pedida.
