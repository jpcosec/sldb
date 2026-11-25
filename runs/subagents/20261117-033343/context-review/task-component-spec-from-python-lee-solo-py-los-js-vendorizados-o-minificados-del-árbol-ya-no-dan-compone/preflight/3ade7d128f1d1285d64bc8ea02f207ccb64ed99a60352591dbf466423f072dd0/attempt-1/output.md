## REFORMULACION

Nodo ejecutable (`task.code`), no agregado. Propósito: corregir la regresión de B2 (600b51a9): `component_spec_from_python`, al usar `scan_tree`, recorre también `.ts/.tsx/.js/.jsx`, y un `.js` vendorizado/minificado genera `component-spec/syntax-error`, rompiendo dos pruebas de paridad de IR. Resultado: que el spec se construya solo desde archivos `.py` y ningún otro lenguaje produzca hallazgos. Repo: `SLDB_1`. Superficie: `src/sldb/api/notations/component_spec_python.py`, `tests/notations/test_component_spec_python.py`, `CHANGELOG.md`. Límites: no cambiar `scan_tree` para `code_facts` ni anclas; no excluir `vendor/` ni `*.min.js` globalmente. Entregable: cambio, test de equivalencia (árbol Python solo vs. con `.js` minificado ilegible, cero hallazgos), CHANGELOG, commit y aviso a IR.

## AMBIGUEDADES

1. «filtrar por extensión los archivos que recorre, o pedir a sldb.code un escaneo limitado a Python con la API que ya existe»: ofrece dos rutas sin elegir; obliga a inventar qué API existente usar y dónde aplicar el filtro.
2. «como antes de B2»: no se aporta el comportamiento previo; obliga a inferir el contrato exacto.
3. «un .js minificado ilegible»: no define contenido ni criterio de ilegibilidad; obliga a inventar el fixture.
4. «el spec de src/sldb no cambia respecto de HEAD»: no indica método de comparación; obliga a inventar golden, hash o diff.
5. «aviso a IR»: no especifica canal ni formato; obliga a inventar destinatario.

## DRY-RUN

Sin ejecutar. Lecturas: los tres archivos declarados, `sldb.code` (`scan_tree`, `scan_file`), `files.py`/`find_files` y la nota de inbox. Cambios previstos: limitar el recorrido del generador a `.py`, sin tocar `scan_tree`; añadir test de equivalencia; entrada CHANGELOG. Dependencias: API de `sldb.code`, fixtures, extras `code`/`dev`, `uv --frozen`, `TMPDIR=/dev/shm`. Validaciones futuras: los cuatro comandos de Validation, `check.sh --fast` y comparación del spec de `src/sldb` con HEAD.

## FUTURO

Un ejecutor materializará diff, test y CHANGELOG; la CI/`check.sh` devolverá resultado; IR recibirá el aviso y ejecutará sus pruebas de paridad; un humano revisará/aprobará commit o PR y resolverá la ruta si la ambigüedad persiste.
