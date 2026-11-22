FALLA

# Resultado — testing del guard de sobrescritura con pérdida

Commit evaluado: `291910691e0904df644b876c836f1104f749bb13` — *refuse_lossy_overwrite accepts dropping an undeclared heading whose text survives*
(`Task-Id: task-el-guard-de-sobrescritura-con-perdida-acepta-quitar-un-encabezado-no-declarado-si-su-contenido-queda`).

## Archivos del ejecutor

- `src/sldb/api/documents/lossy_overwrite.py`
- `tests/api/test_lossy_overwrite_content.py`
- `CHANGELOG.md`

## Tests del commit y vecindad (uno por archivo, `TMPDIR=/tmp`, venv del repo)

| Archivo | Resultado |
|---|---|
| `tests/api/test_lossy_overwrite_content.py` (nuevo) | 2 passed |
| `tests/api/test_rewrite_loss.py` | 3 passed |
| `tests/api/test_structural_noise.py` | 15 passed |
| `tests/api/test_policy.py` | 14 passed |
| `tests/api/test_write_paths_validate.py` | 5 passed |
| `tests/api/test_field_blocks.py` | 2 passed |
| `tests/api/test_api_documents.py` | 21 passed |
| `tests/api/test_tags.py` | 37 passed |
| `tests/api/test_replace_text.py` | 16 passed |

Total: **115 passed, 0 failed**. Los dos tests nuevos pasan y los tests de lossy existentes siguen
verdes. También verifiqué con el `AtomDoc` real de deskops
(`desk/atoms/atom-desk-health-delegates-store-diagnostics-to-sldb.md`): al plegar ATX
`## Boundary Rationale`, `## Delegation Pattern`, `## Evidence` y `## Tags` en `answer`/`tags`,
el guard deja de rechazar y, si borro el cuerpo de `Evidence`, sigue rechazando.

## Gate rápido

`bash tools/check.sh --fast` (PATH con `/tmp/ws-venv/bin`, symlink a `/workspace/sldb/.venv`) termina **rc=1** únicamente por
la puerta `identidad`:

```
ERROR  directorio versionado sin clasificar en la raíz: workbench_demo
FAIL: identidad — ... 1 violaciones
```

Es la excepción autorizada (`f055723d`), preexistente y ajena al commit. Las demás puertas pasan:
`núcleo aislado`, `capas`, `ejes` y `superficie`. No uso esta roja como motivo del veredicto.

## Bloqueante: todavía se pierde contenido con encabezados que el escáner sí ve pero el helper no

`_heading_bodies` sólo reconoce encabezados ATX que empiezan en la columna 0
(`_HEADING_LINE = ^(#{1,6})...`), mientras que `scan_headings` (el que alimenta
`report.undeclared`) usa el AST de Markdown y sí reconoce encabezados setext y ATX indentados.
Para esos encabezados, `bodies.get(line, [""])` cae en el default `[""]`, y `all(body in target ...)`
con `""` siempre es verdadero: el guard los considera «contenido conservado» y permite perder su
cuerpo. Esto contradice el Goal: «Sigue rechazando si se pierde contenido».

Reproducción con `TicketDoc` (ATX `## Tags` declarado, encabezado no declarado setext h2):

```text
documento actual:
# Old
Status: open
## Tags
- auth

Lost Section
------------

content only here

escritura: save_document_payload(..., {"title": "New", "status": "open", "tags": ["auth"]})
resultado: SAVE ALLOWED (BUG): content lost
archivo final: pierde «Lost Section» y su cuerpo «content only here»
```

El mismo agujero se reproduce con un ATX indentado válido (`   ## Lost Section`):

```text
scan_headings -> [(1, 'T'), (2, 'Lost Section')]
_heading_bodies -> {'# T': ['## Lost Section content only here']}   # no mapea el encabezado
lost -> ['## Lost Section']
_without_kept_content -> []                                          # lo deja pasar
```

Antes del cambio, `_lost_headings` devolvía `['## Lost Section']` y el guard rechazaba. Es una
regresión funcional, no cubierta por los dos tests nuevos (ambos usan ATX en columna 0).

## Observación secundaria de calidad

`src/sldb/api/documents/lossy_overwrite.py` contiene **duplicados accidentales**: `import re` dos
veces y el bloque `_HEADING_LINE` / `_squash` / `_heading_bodies` / `_without_kept_content`
definido dos veces (la segunda definición pisa a la primera). No rompe los tests, pero confirma que
el commit necesita otra pasada.

## Veredicto

**FALLA**: los tests pedidos pasan, pero el objetivo explícito de seguir rechazando cuando se
pierde contenido no se cumple para encabezados setext o ATX indentados; una escritura de campo
puede borrar su cuerpo en silencio. Corregir el mapeo de cuerpos (usar el mismo escáner/AST o
normalizar la línea) y no defaultear a `[""]`; añadir el test de contenido perdido con al menos un
encabezado no-ATX-en-columna-0.
