# REFORMULACION

Encargo (nodo `task.code`, ejecutable —no agregado—): ampliar el paquete `sldb.code` para leer **TS/TSX** con `tree-sitter-typescript` como parte del extra `code`, publicando facts (component, hook, type, function, module) con la misma forma que los de Python y soportando anclas `code:<ruta>.ts|.tsx::<símbolo>` (fingerprints, estados, reconexión). **Repo:** sldb (`structuredLanguageDB`, `/mnt/ssd/proyectos/SLDB_1`). **Resultado:** runtime por lenguaje, módulo `lang_ts.py` con query/readers/imports, `scan_file`/`find_files` despachando por extensión, `parse_code_ref` aceptando `.ts/.tsx`, `recorded_with` informando la gramática; `.py` intacto (NORMALIZATION igual); sin gramática, sldb sigue escaneando `.py`. **Límites:** mapear a dominio queda fuera (specIR); SQL en tarea hermana; reutilizar maquinaria Python sin duplicarla.

# AMBIGUEDADES

1. "Alcance: TS/TSX (...) y SQL (tablas, columnas, vistas, DDL y migraciones)" vs "esta tarea cubre TS y TSX; SQL va en la tarea hermana": ¿SQL entra o no? Obligaría a inventar si implementar readers SQL aquí.
2. "component (función o const que devuelve JSX, nombre en mayúscula)": detección de "devuelve JSX" no definida (arrow implícita vs return). Obligaría a inventar heurística.
3. "el comentario JSDoc /** */ inmediatamente anterior": "inmediatamente" no acota líneas en blanco. Obligaría a inventar tolerancia.
4. "tree-sitter-typescript>=0.23" y "la versión 0.23.2 está en PyPI": suelo vs pin exacto.
5. "un runtime por lenguaje elegido por extensión (.py, .ts, .tsx)": tree-sitter-typescript trae dos gramáticas (typescript/tsx); mapeo `.tsx`→gramática TSX no explicitado.
6. "find_files incluye .ts/.tsx solo si la gramática está": comportamiento al faltar (¿excluir en silencio?).
7. Validación cita `test_fingerprints.py`, `test_treesitter_agreement.py`, `test_component_spec_python.py`, `test_clean_code_rules.py`, ausentes de `files:`; ¿se actualizan o solo se ejecutan?
8. "NORMALIZATION no cambia si la salida de .py es la misma": no dice acción sobre la constante.

# DRY-RUN

Lecturas previstas: los archivos listados en `files:` y, para reutilizar, los módulos Python ya existentes (`readers`, `imports`, `facts`, `fingerprints`, `ids`), no nombrados. Cambios: dep en `pyproject.toml`; `uv lock`; `runtime.py` por lenguaje; nuevo `lang_ts.py`; `scan.py` dispatch+`find_files`; `code_ref.py`; `record_anchor.py`; fixtures + tests; `CHANGELOG`. Dependencias: `uv`, red para lock/wheels. Validaciones futuras: los siete comandos de Validation (pytest por archivo y `tools/check.sh --fast`), sin ejecutar aquí.

# FUTURO

La tarea hermana de SQL depende de este resultado. El coordinador decide cómo commitear `uv.lock` si aparece sucio. IR se avisa vía `result-summary.md` (no está en el registro). Closeout humano/deskops verifica commits, Board y CHANGELOG.
