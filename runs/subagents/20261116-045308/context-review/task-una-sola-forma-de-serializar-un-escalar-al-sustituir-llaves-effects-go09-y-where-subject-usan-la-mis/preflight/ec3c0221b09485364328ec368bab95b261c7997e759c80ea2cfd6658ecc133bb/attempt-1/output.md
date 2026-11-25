## REFORMULACION
**Propósito:** unificar en una sola función la serialización de escalares al sustituir llaves `{campo}` en reglas, para que `edge_effects` y `where_subject` produzcan el mismo texto.
**Resultado:** `brace_text(value) -> str` en `src/sldb/store/query_engine/where_literal.py`, usada por `edge_effects._written` y por `scalar_literal`/`fill_braces`; salidas exactas para `int`, `Decimal`, `float`, `bool`, `datetime.date` y `str`; `TypeError` para el resto; tests parametrizados en ambos caminos; `CHANGELOG.md` y commit.
**Repo:** `/mnt/ssd/proyectos/SLDB_1`, proyecto Python validado con `pytest`.
**Límites:** no cambiar la gramática del lenguaje de reglas ni los literales que acepta el parser; el alcance son los archivos listados y los tres comandos de validación.

## AMBIGUEDADES
1. «float con repr más corto sin exponente cuando sea posible (0.5 -> 0.5)»: no define qué hacer cuando el exponente sea inevitable (p. ej. `1e-7`, `1e300`). Obligaría a inventar umbral y formato de respaldo.
2. «int y Decimal sin exponente (1e20 -> 100000000000000000000)»: no cubre `Decimal` fraccionario, negativo, con ceros finales ni `NaN`/`Infinity`. Obligaría a inventar la representación.
3. «cualquier otro tipo lanza TypeError con el tipo»: no fija el texto del mensaje. Obligaría a inventar el mensaje y, si se testea, su contrato.
4. «datetime.date -> ISO 8601 (2026-11-16)»: `datetime.datetime` es subclase de `date`, y `bool` es subclase de `int`; no fija el orden de despacho. Obligaría a inventar prioridades.
5. «cambiar _written y scalar_literal/fill_braces para usarla»: no aclara si `scalar_literal` permanece como alias/wrapper o desaparece. Obligaría a inventar la superficie pública.
6. «el commit lo dice»: no especifica formato del mensaje de commit. Obligaría a inventar su redacción.

## DRY-RUN
Un ejecutor futuro leería `edge_effects.py` 30-50, `where_literal.py` 40-60, `where_subject.py` 1-40, los tests citados y `CHANGELOG.md`. Añadiría `brace_text` con despacho `bool` antes de `int`; sustituiría `yaml.safe_dump` en `_written` y haría que `fill_braces`/`scalar_literal` la usen. Añadiría tests parametrizados con los cinco casos por ambos caminos y actualizaría expectativas antiguas y `CHANGELOG.md`. Dependencias: imports existentes, posible retirada de `yaml.safe_dump` y `pytest`. Validaciones futuras, sin ejecutar: los tres comandos `pytest`, el `grep` de `safe_dump`, la igualdad de los cinco textos por ambos caminos y la presencia de CHANGELOG/commit.

## FUTURO
El nodo de implementación producirá el diff, tests y commit; CI o un revisor ejecutará la validación; un humano aprobará la redacción del commit/CHANGELOG y resolverá los criterios de formato no fijados.
