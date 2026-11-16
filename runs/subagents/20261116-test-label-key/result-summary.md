# result-summary — tester deskops-t-9741372cd8e8

Task: `task-label-key-de-sldb-api-matching-trata-el-guion-bajo-como-separador-igual-que-normkey-del-catálogo`. Pills: ninguno. Evidencia completa en `validation.log`.

**Veredicto global: PASA**

## Validation
| Comando | Resultado |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/matching/` | **PASA**: 31 passed, rc 0 (1 warning preexistente de config `asyncio_default_fixture_loop_scope`). `uv` funcionó; `uv.lock` intacto (md5 igual antes/después). |

## Done When
| Punto | Veredicto | Evidencia |
|---|---|---|
| `pytest -q tests/matching/` pasa | PASA | 31 passed, rc 0 |
| incluye el test `label_key("post_published") == "post published"` | PASA | `-k label_key -v`: 6 passed (`test_label_key_underscore_is_a_separator`, 4 casos de `test_label_key_matches_normkey`, `test_label_key_matches_template_normkey` previo) |
| CHANGELOG.md tiene la entrada | PASA | una línea en español, primera bajo `## 0.1.13 — not released yet (no tag, not on PyPI)`, estilo de las vecinas |
| commit con esos archivos | N/A para el tester | lo hace el coordinador con `deskops closeout commit`; hoy sin commitear, como corresponde |

## Scope
- Regex exactamente `re.sub(r"[\W_]+", " ", ...)`; pipeline intacto (strip+lower antes, `\s+`→" ", strip después): PASA (diff).
- Pares exactos del parametrizado coinciden con el contrato: PASA.
- `normalize_key` y `_title_aliases` no tocados: PASA (el único hunk del diff es `label_key`; `normalize_key("post_published")` sigue dando `"post_published"`).
- Goldens: no hay goldens en `tests/matching/`; nada que actualizar.

## Caso extra (no cubierto por el ejecutor) — `/dev/shm/tlk/edge.py`
1. Paridad contra `normKey` real ejecutado en node (`/[^\p{L}\p{N}\s]+/gu`, minúsculas, colapso, trim) sobre 212 entradas: cada carácter ASCII imprimible entre letras (`a{c}b`) y repetido en bordes (`{c}{c}x{c}`), más `_lead_`, `__`, `_`, `""`, `Ñandú_42 ok`, `Straße_ß`, `ÉLAN_vital`, tab/newline con `_`: **0 diferencias**. (Fuera del contrato pero también iguales: `٣_x`, `x²_y`.)
2. Extremo a extremo con `collect_explicit_atoms` (spec `component`, colección `nodes`): elemento sin label con id `post_published` queda bajo la clave `"post published"` y ya no bajo `"post_published"`; elemento `Otro_Id` con label `Mi_Label` queda bajo `"mi label"` y `"otro id"`: PASA.

## Archivos fuera del contrato
Tocados por el ejecutor: solo `src/sldb/api/matching/atom_keys.py`, `tests/matching/test_matching_explicit.py`, `CHANGELOG.md` (+ su entrega en `runs/subagents/20261116-exec-label-key/`). Ajenos ya listados en el brief: no revisados. Además aparecen modificados `.sldb/core/models/RunDoc.yaml`, `.sldb/core/store_index.yaml`, `.sldb/store.yaml` y nuevos `.sldb/core/documents/RunDoc/run-deskops-{e-2edd3c6307c2,t-9741372cd8e8}.yaml`: son el registro de los RunDoc de este despacho (executor y tester) que hace el coordinador, no cambios del ejecutor. Se anotan para que el closeout decida si entran.

## Comandos del tester
Ninguna edición del repo; solo escribí en `runs/subagents/20261116-test-label-key/` y `/dev/shm/tlk/`.
