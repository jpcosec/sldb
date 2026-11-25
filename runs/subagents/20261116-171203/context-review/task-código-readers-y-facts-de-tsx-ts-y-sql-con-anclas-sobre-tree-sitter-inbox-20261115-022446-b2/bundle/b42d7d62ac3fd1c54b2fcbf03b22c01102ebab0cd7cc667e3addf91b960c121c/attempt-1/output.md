## REFORMULACION

**Propósito:** ampliar `sldb.code` para leer TypeScript/TSX con tree-sitter (readers, facts, fingerprints, imports, scan) y anclar símbolos con `code:<ruta>::<qualified_name>`, reutilizando la maquinaria de Python, con las gramáticas como extras opcionales.

**Resultado:** `tree-sitter-typescript` en el extra `code`; runtime por lenguaje; módulo `lang_ts.py`; dispatch por extensión en `scan_file`/`find_files`; `parse_code_ref` acepta `.ts`/`.tsx`; `recorded_with` informa la gramática; fixtures y tests de intact/changed/lost/reconnected que se saltan sin gramática.

**Repo:** `structuredLanguageDB` (`/mnt/ssd/proyectos/SLDB_1`), paquete `src/sldb/code`, `models/code_ref.py`, `api/anchors/record_anchor.py`, tests y `pyproject.toml`/`uv.lock`.

**Límites:** TS/TSX únicamente; SQL va en tarea hermana; mapeo a dominio es de specIR; no duplicar la maquinaria Python; sin ejecutar nada en esta revisión.

## AMBIGUEDADES

1. Alcance SQL contradictorio: «El paquete sldb.code lee TS/TSX y SQL» frente a «esta tarea cubre TS y TSX; SQL va en la tarea hermana»; Done When exige «Fixtures reales de TSX y de SQL». Obligaría a inventar si SQL entra o no.
2. Detección de componente: «component (función o const que devuelve JSX, nombre en mayúscula)». No define retorno explícito/implícito, anidado ni reexportaciones; obliga a inventar heurística.
3. JSDoc: «el comentario JSDoc /** */ inmediatamente anterior». No define distancia (línea contigua, blancos, decoradores/`export`); obliga a inventar la regla.
4. Colisión de módulos: «la ruta sin extensión con '.' como separador, igual que py_module_name». No dice qué ocurre con `a.ts` y `a.tsx` coexistentes; obliga a inventar desambiguación de ids.
5. Disponibilidad parcial: «si falta la gramática, TreeSitterUnavailable nombra el extra» y «find_files incluye .ts/.tsx solo si la gramática está». No define el caso Python presente y TypeScript ausente, ni cómo se consulta; obliga a inventar política.
6. `recorded_with`: «informa la gramática del archivo». Formato y nombre exacto no especificados; obliga a inventar el string.

## DRY-RUN

**Lecturas:** `pyproject.toml`, `uv.lock`, `src/sldb/code/{runtime,scan,readers,imports,facts,fingerprints,ids}.py`, `models/code_ref.py`, `api/anchors/record_anchor.py`, tests y fixtures citados.

**Cambios previstos:** añadir `tree-sitter-typescript>=0.23` al extra `code` y `uv lock`; runtime seleccionable por extensión; `lang_ts.py` con query, readers JSDoc e imports; dispatch en `scan_file` y filtro en `find_files`; aceptar `.ts`/`.tsx` en `parse_code_ref`; `recorded_with` por gramática; fixtures `.tsx` y tests condicionados.

**Dependencias:** instalación del extra `code` con la gramática nueva; lock actualizado; `uv run --frozen`.

**Validaciones futuras:** los siete comandos de la sección Validation, `tools/check.sh --fast`, y el `stores build --check` citado en Done When.

No es un agregado: es una tarea ejecutable.

## FUTURO

La tarea hermana de SQL depende de esta y consume su dispatch/runtime. El coordinador decide cómo commitear `uv.lock` si llega sucio. El cierre corresponde a los rituales de testing y closeout (commit atómico, CHANGELOG, Board), no a esta revisión.
