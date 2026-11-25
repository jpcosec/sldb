## REFORMULACION
Propósito: que `sldb.code` emita facts sintácticos genéricos de Python, sin conocer frameworks, para que specIR derive Django/DRF. Resultado: relación `extends` hacia cada base; `attrs.decorators` {name,args,kwargs}; relación `calls` desde funciones/métodos (sin resolver tipos) con `attrs.calls` y línea; nuevo kind `assignment` para asignaciones de módulo/clase (incluida una `Meta` anidada) con `attrs.call`/`attrs.items`/`attrs.value`; todo normalizado con `py_norm`; fixture Django/DRF mínimo, tests y CHANGELOG. Repo: `src/sldb/code/scan.py`, `readers.py`, módulos nuevos del paquete, `tests/selfdoc/test_treesitter_symbols.py`, `tests/fixtures/treesitter/`, `CHANGELOG.md`. Límites: no interpretar Django/DRF, no resolver tipos ni imports, no TS/JS, no alterar anclas existentes.

## AMBIGUEDADES
1. "si cambia la forma de los facts existentes, se sube y se dice en el CHANGELOG": no indica valor ni ubicación de NORMALIZATION; obligaría a inventar número y criterio de ruptura.
2. "attrs.calls con línea de cada llamada": no define su forma (¿lista de {name,line}?), a diferencia de `relations`; obligaría a inventar esquema.
3. "El hecho call de módulo se nombra por su func con sufijo ~N si se repite": `func` es texto calificado con puntos (`router.register`); no dice cómo forma id/qualified_name; obligaría a inventar su limpieza.
4. "Fixture de Django/DRF mínimo en tests/fixtures/treesitter/": `files:` no lista esos archivos ni el directorio; obligaría a inventar ruta y contenido.
5. "por la regla de 80 líneas": la regla no se cita; obligaría a inventar umbral y reparto de módulos nuevos.
6. "las anclas existentes no cambian de estado": no define "estado" ni su comprobación (solo `tests/api/test_anchors.py`); obligaría a inventar el criterio.

## DRY-RUN
Lecturas: `scan.py`, `readers.py`, `facts.py`, `fingerprints.py`, tests selfdoc, fixture treesitter, `tools/check.sh`. Cambios previstos: readers nuevos para bases, decoradores, llamadas y asignaciones; integrarlos en `scan_file` para `.py`; añadir attrs/relaciones/kinds sin tocar ids existentes; fixture Django/DRF y tests; CHANGELOG; subir NORMALIZATION si procede. Dependencias: `py_norm`, `fact`/`rels`/`Ids`, gramática Python de tree-sitter vía `runtime()`, `py_signature`. Validaciones futuras: los siete comandos listados; `agreement`, `fingerprints` y `anchors` detectan regresiones; cierre con `check.sh --fast`.

## FUTURO
specIR consumirá los facts e interpretará rutas, acciones, campos, serializers y cadenas de llamadas; un humano decide la versión de NORMALIZATION y acepta el resultado; deskops cierra, commitea y actualiza el Board; otro nodo notifica a IR.
