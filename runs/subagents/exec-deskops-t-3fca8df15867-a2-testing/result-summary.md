FALLA

El guard sigue aceptando la pérdida de encabezados no declarados setext e indentados cuyo cuerpo no sobrevive.

## Evidencia

- Commit del ejecutor (único con el Task-Id): `291910691e0904df644b876c836f1104f749bb13`.
- Los tests añadidos por el commit pasan: `tests/api/test_lossy_overwrite_content.py` → 2 passed.
- `tests/test_extraction_segments.py` → 6 passed.
- `bash tools/check.sh --fast` → rc=1 por la puerta `identidad` (workbench_demo, excepción autorizada f055723d), no usado como motivo del veredicto.

## Bloqueante reproducido

Con `TicketDoc` (`## Tags` declarado) más un encabezado setext no declarado:

```markdown
Lost Section
------------

content only here
```

y con un encabezado indentado no declarado:

```markdown
  ## Indented Lost

content only here
```

`save_document_payload(... title="Lost" ...)` **no lanza** `SLDBValidationError`; el cuerpo se pierde. Ambos tests de reproducción fallaron con `DID NOT RAISE`.

Causa: `scan_headings` usa el AST y ve los tres encabezados, pero `_heading_bodies` solo reconoce ATX en columna 0. Para setext/indentado cae en el default `[""]`, y `all(body in target ...)` con `""` siempre es verdadero. Falta el cambio pedido en el Intento 2 (cuerpos desde el mismo escaneo AST, fallar cerrado si no se calculó el cuerpo) y faltan sus tests.

## Archivos

`validation.log` contiene los comandos, salidas y la comparación `scan_headings` vs `_heading_bodies`.
