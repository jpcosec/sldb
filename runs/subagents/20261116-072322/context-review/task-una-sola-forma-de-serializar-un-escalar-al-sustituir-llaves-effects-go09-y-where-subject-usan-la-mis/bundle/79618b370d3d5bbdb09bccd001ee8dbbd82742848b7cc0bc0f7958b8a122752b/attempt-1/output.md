REFORMULACION
Propósito: unificar la serialización de escalares al sustituir `{campo}`, hoy divergente entre edge_effects._written (yaml.safe_dump) y where_subject/scalar_literal (Decimal sin exponente, None para bool). Resultado: `brace_text(value)->str` en where_literal.py usada por ambos caminos, con salidas exactas (int/Decimal sin exponente, float sin exponente cuando posible, bool true/false, date ISO 8601, str tal cual, resto TypeError "cannot write {tipo} into braces"), tests parametrizados en ambos archivos y CHANGELOG. Repo: src/sldb (SLDB_1), archivos del TaskDoc. Límites: no cambia gramática ni literales del parser; commit del coordinador vía deskops closeout; sin push.

AMBIGUEDADES
1. "scalar_literal se queda y llama a brace_text ... (sigue devolviendo None para los tipos que hoy no maneja, salvo bool...)" frente a "los cinco casos dan el mismo texto por effects y por where_subject" y "datetime.date -> ISO 8601". Hoy scalar_literal no maneja Decimal ni date: con None, fill_braces pone `"?"`. Obligaría a inventar si debe devolver brace_text para ellos.
2. "str tal cual" frente a "scalar_literal ... llama a brace_text" y su uso en `--where`. Hoy devuelve `quote(value)`; un str sin comillas rompe el parser. Obligaría a inventar si scalar_literal recomilla o si fill_braces cambia de contrato.
3. "Decimal ... NaN e Infinity lanzan ValueError" y "float -> repr(f) si no contiene 'e'". No dice qué ocurre con float inf/nan ('inf'/'nan', sin 'e'). Obligaría a inventar esa salida.

DRY-RUN
Lecturas: edge_effects.py 30-50, where_literal.py 40-60, where_subject.py 1-40, tests nombrados, CHANGELOG. Cambios: brace_text en where_literal.py (orden bool, datetime, date, int, Decimal, float, str); _written delega (posible retirada de yaml); scalar_literal/fill_braces la usan; tests parametrizados mismo valor/mismo texto; actualizar 1.0e+20 y None de bool; línea CHANGELOG bajo "## 0.1.13 — not released yet". Dependencias: decimal/datetime y fixtures del test o sldb.api en tmp_path. Validaciones futuras: los tres pytest con TMPDIR=/dev/shm, grep "safe_dump" fuera de _written, contraste effects/where_subject de los cinco casos. Sin ejecutar.

FUTURO
Coordinador: commit con deskops closeout (mensaje título corto), sin push; aviso a <repo> con deskops message send o como "Aviso a <repo>: ..." en runs/subagents/<run-dir>/result-summary.md si no está registrado. Humano/otro nodo resuelve ambigüedades 1-2 y aprueba float inf/nan.
