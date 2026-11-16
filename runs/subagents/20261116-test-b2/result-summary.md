# Tester deskops-t-9d06b59a722f — B2, parte TS: **PASA**

Task: `task-código-readers-y-facts-de-tsx-ts-y-sql-con-anclas-sobre-tree-sitter-inbox-20261115-022446-b2`. Pills: ninguno.
Cambio revisado: el diff sin commitear de los archivos del contrato y los módulos nuevos sin trackear `src/sldb/code/{files,lang_ts,ts_readers,ts_fingerprints}.py` más `tests/fixtures/treesitter/frontend/` (aclaración 2 del coordinador). La salida completa está en `validation.log`, y los scripts de las pruebas propias en `/dev/shm/tb2/s/`.

## Validation (corrida por mí con `uv run --frozen --extra code --extra dev`; uv no falló)
| Comando | Resultado |
|---|---|
| pytest tests/api/test_anchors.py | PASA (10 passed, rc=0) |
| pytest tests/selfdoc/test_treesitter_symbols.py | PASA (9 passed) |
| pytest tests/selfdoc/test_fingerprints.py | PASA (4 passed) |
| pytest tests/selfdoc/test_treesitter_agreement.py | PASA (2 passed) |
| pytest tests/notations/test_component_spec_python.py | PASA (5 passed) |
| pytest tests/test_clean_code_rules.py (también obligatorio por el brief) | PASA (1177 passed) |
| bash tools/check.sh --fast (también obligatorio por el brief) | PASA ("TODAS LAS PUERTAS PASAN", rc=0) |

Validation no pide la suite completa ni `sldb stores build --check`, y no los corrí: quedan **delegados al integrador**.

## Done When, punto por punto
- **Los comandos de Validation pasan**: PASA (tabla de arriba).
- **El ancla .tsx de un componente queda intact, changed, lost y reconnected**: PASA. Lo probé por mi cuenta sobre el fixture real `App.tsx::Button` (copiado a /dev/shm), no solo con el test del ejecutor:
  - sin cambios da intact;
  - cambiar el cuerpo da changed `['body']`, y cambiar el JSDoc da changed `['docstring']`;
  - renombrarla a Boton da reconnected `code:src/App.tsx::Boton`;
  - borrar la declaración da lost;
  - moverla a `Moved.tsx` da reconnected `code:src/Moved.tsx::Button`.
- **El ancla .js del fixture JS se registra y queda intact**: PASA. `code:src/util.js::double`, tomada del fixture real, sale kind function e intact. `Panel.jsx::Panel` sale component e intact.
- **Sin tree-sitter-typescript se sigue escaneando .py**: PASA. Bloqueé el import de `tree_sitter_typescript` con un meta_path finder: `scan_tree` devuelve los mismos ids de .py y omite b.ts. `record_anchor` sobre un .ts da `TreeSitterUnavailable`, que nombra `[code]`.
- **La salida de los .py no cambia (NORMALIZATION igual)**: PASA.
  - (3b) Comparé `scan_file` y `scan_tree` sobre `src/` y `tests/` de `git archive HEAD`, con el código de HEAD contra el código nuevo. Los hechos son idénticos: 5564 en src, 2561 en tests y 5 archivos sueltos. NORMALIZATION sigue en 1.
  - (3a) `node_modules`: el conjunto de .py que escanea el repo sldb es idéntico al de HEAD (1173 rutas en src y 255 en tests). En el árbol actual solo aparecen de más los 4 módulos nuevos de `sldb/code` y los 4 fixtures TS/JS, y no falta ninguna ruta.
- **CHANGELOG**: PASA. Hay entrada en 0.1.13, y la puerta de afirmaciones de check.sh pasa.
- **Commit y aviso a IR**: no aplican al tester. El brief prohíbe el commit y el aviso lo manda el coordinador (aclaración 7 al ejecutor).

## uv.lock (aclaración 1)
Corrí `uv lock` sobre una copia del pyproject de HEAD en /dev/shm, que reproduce el relock previo de los extras code y mcp. Comparado con el uv.lock actual, el **único paquete nuevo es `tree-sitter-typescript` 0.23.2**. La única otra diferencia es de versión: `tree-sitter` es 0.26.0 en el lock y 0.26.1 en mi relock de hoy. Es una resolución anterior, no un paquete nuevo. Las corridas con `--frozen` no modificaron uv.lock.

## Caso no cubierto por el ejecutor (script `/dev/shm/tb2/s/edge.py`)
Armé un `Edge.tsx` con bordes de Scope y casos negativos. Todos salen según las reglas y las aclaraciones:
- `memo(function Inner(){<div/>})`, `forwardRef((p,r)=><input/>)`, `let X = function(){<></>}` y un declarador múltiple (`const a = 1, Multi = () => <i/>`) dan component. `a` no da hecho.
- `NoJsx = () => 42` da function.
- `useThing` da hook aunque su JSX esté anidado. `user` y `use` dan function.
- Un generador async exportado da function.
- `export default App;` (un identificador), el reexport `export {..} from`, `enum`, `class` y la función anidada `Nested` no crean hechos.
- Comentarios:
  - con dos `/** */` seguidos cuenta el último;
  - un `/* */` sin el segundo asterisco no cuenta;
  - un JSDoc separado por una línea en blanco no cuenta.
- `export default () => <div/>` en Anon.tsx da `src.Anon.Anon` (component), y `export default function(){}` en .js da `AnonFn`.
- Con a.js y a.ts en la misma carpeta, los módulos salen `src.a` y `src.a~2`, y los símbolos `src.a.f` y `src.a.f~2`. Es la misma forma que Python con a.py y a/__init__.py: `a.f` y `a.f~2`.
- Un .ts roto da el módulo con `has_error: True`, sin excepción.
- `node_modules/` no se recorre, ni sus .py ni sus .js.
- `parse_code_ref` rechaza `.mjs`, `.TSX` y `../`.

## Fuera del contrato
No hay cambios del ejecutor fuera de la lista `files` y de los módulos y fixtures nuevos que autoriza Implementation Path. Los cambios de `.sldb/` y `desk/reviews/` (bundle-4 y preflight-4, RunDoc), `desk/runtimes/`, `.herdr-coordination.md` y `runs/subagents/*` son del coordinador o ajenos. No los toqué ni los revisé.

## Regresiones vecinas
Los módulos de src cambiados son runtime, scan, code_ref y record_anchor. Sus importadores, los de `sldb.code` y `sldb.api.anchors`, y los tests de selfdoc corrieron archivo por archivo, todos con rc=0:
- tests/notations: test_component_spec_graph y test_notations_from_graph_cli;
- tests/security: test_guard_selfdoc;
- tests/selfdoc: test_docstring_metadata, test_import_context, test_parser, test_preflight, test_python_doc_ids, test_python_purpose, test_python_scanner, test_reexports, test_sync y test_tag_inheritance;
- tests/test_store_seams.

Como no hubo ninguna falla, no hizo falta compararlos contra HEAD.

## Observaciones (no bloquean)
- `qualified_name` de un símbolo TS es el nombre a secas, y el `module.nombre` va en el id. Es la misma convención que Python, y el ejecutor lo declaró como desvío.
- `foo.d.ts` da el módulo `foo.d`, porque `py_module_name` solo quita la última extensión.
- Un .ts con error de sintaxis puede perder sus declaraciones; el módulo marca `has_error`.
- El span de un componente con `const` empieza en el declarador, no en la línea del `export`.
