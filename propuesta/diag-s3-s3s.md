# S3 regulación

## Veredicto

**PRESENTE SIN MECANISMO.** El reglamento existe (standards.md, 22 reglas) y una fracción mínima — 3 reglas de forma — está realmente bloqueada por una prueba. Las 19 restantes, incluidas todas las arquitectónicas (capas, ciclos, imports ocultos, fronteras Pydantic, tipado), no tienen ningún mecanismo que las recorra y rechace. La sección "Toolchain Configuration" del propio estándar declara un mecanismo que ya no existe: ruff, mypy y docstring-coverage no están configurados ni en dependencias ni en CI.

## Evidencia

- CI (`/.github/workflows/ci.yml:25,28,30`): exactamente 3 pasos verificadores — `pytest`, `selfdoc check`, `build`. Sin linter, sin pre-commit (gobernanza.json: `pre_commit_existe: false`, `linter_configurado: false`).
- `pyproject.toml`: sin `[tool.ruff]`, sin `[tool.mypy]`; `dev` = scipy, build, pytest, pytest-cov. Ninguna de las 3 herramientas prometidas por standards.md:50-52 está instalada. Los directorios `.ruff_cache`/`.mypy_cache` sobran de ejecuciones manuales.
- **Contrapunto (importante):** `tests/test_clean_code_rules.py` existe y corre. Parametrizado sobre los 586 archivos de `src/` (586 de las 1207 pruebas, el 48% de la suite), rechaza —no avisa— si: un archivo tiene >1 clase (línea 25), una función supera 10 líneas de lógica (línea 41), un archivo supera 80 líneas efectivas (línea 49). Veredicto parcial: 1207 collected, el archivo aporta 586.
- **El hallazgo central — qué fluye absorbe esa masa de pruebas:** ninguna prueba valida estructura de imports. `grep 'find_cycle|strongly|topolog|circular' tests/` solo encuentra `tests/store/test_graph_analysis.py` y `test_semantic_dag_walk.py`, que verifican el aciclismo del **grafo de documentos del store** (`sldb.store.edge_index.acyclic`), no el del propio código. El sistema le exige a sus datos una condición (DAG) que no se exige a sí mismo: BUNDLE reporta 5 ciclos entre paquetes hoy y 91 imports dentro de funciones hoy, y ninguna prueba los vería fallar. Si mañana alguien mete un ciclo entre paquetes, lógica pesada en un `__init__` o rompe el layering, las 1207 pruebas siguen en verde.
- Los 586 archivos pasan las 3 reglas de forma (la suite está verde), lo que confirma que la atención del autor las sostuvo hasta mecanizarlas. Las otras 19 nunca llegaron a ese estado.

## Reglas sin mecanismo

Standards.md enuncia 22 reglas (Layer 0: 4, Layer 1: 8, Layer 2: 4, Layer 3: 2, Layer 4: 4).

| Regla | Dónde se enuncia | Qué la aplica |
|---|---|---|
| 1 clase por archivo | standards.md L1.5 | ✅ `test_clean_code_rules.py:25` (bloquea) |
| Función ≤10 líneas | standards.md L1.3 | ✅ `test_clean_code_rules.py:41` (bloquea) |
| Archivo ≤100 líneas | standards.md L1.2 | ✅ subsumida por ≤80 efectivas, `test_clean_code_rules.py:49` (bloquea) |
| No legacy / zero noise | standards.md L0.1 | ❌ nada detecta código muerto o carpetas compat |
| Code as Truth | standards.md L0.2 | ❌ nada |
| Visualizabilidad estructural | standards.md L0.2 | ❌ el "health check" sería `map_architecture.py`: manual, solo visibilidad, nadie lo corre |
| Step 0 compliance | standards.md L0.3 | ❌ depende de memoria del autor |
| AST-first refactoring | standards.md L1.1 | ❌ regla de proceso, nada |
| Single purpose per file | standards.md L1.4 | ❌ nada |
| SRP por clase | standards.md L1.6 | ❌ nada |
| Consolidación utilitaria | standards.md L1.5b | ❌ nada detecta duplicación |
| Función compleja → clase | standards.md L1.6b | ❌ nada |
| Fronteras Pydantic | standards.md L2.1 | ❌ nada |
| No type erosion (dict/Any) | standards.md L2.2 | ❌ mypy prometido, no configurado |
| Field(description=…) | standards.md L2.3 | ❌ nada |
| `__future__ annotations` + hints | standards.md L2.4 | ❌ nada |
| Docstrings Google-style | standards.md L3.1 | ❌ docstring-coverage prometido, no instalado |
| Docstring de módulo | standards.md L3.2 | ❌ nada |
| Excepciones de dominio | standards.md L4.1 | ❌ nada verifica la ubicación |
| Catch tipado | standards.md L4.2 | ❌ nada prohíbe `except Exception` |
| No `pass` silencioso | standards.md L4.3 | ❌ nada |
| `raise … from e` | standards.md L4.4 | ❌ nada |

Además, docs/*.md contienen reglas propias también sin mecanismo: `docs/packaging instructions.md` exige una checklist de verificación ("Verify at least…") sin nada que la recorre; `docs/versionado-y-colaboracion.md` declara invariantes de hashes y locking con fecha fija (2026-09-21) y nada las re-verifica contra el código.

## Patología

**Estándares sin mecanismo**, con un agravante: el documento de estándares miente sobre su propio mecanismo. La sección "Toolchain Configuration" (standards.md:50-52) afirma que ruff/mypy/docstring-coverage hacen cumplir las reglas; ninguna existe en el repo. La única regla de arquitectura que importaría (capas, ciclos, fronteras) es la que nada mira — y el sistema falla esa regla hoy (5 ciclos, 91 imports ocultos) en silencio. Mientras tanto, el 48% de la suite gasta su variedad en 3 reglas de forma ya estabilizadas. Si el autor se va: las 19 reglas sin mecanismo se degradan en el primer PR sin.signal alguno.

---

# S3* auditoría

## Veredicto

**PRESENTE SIN MECANISMO.** Existe un canal propio real — `selfdoc check` corre en CI y bloquea — pero su variedad cubre solo los hechos del parser CLI. Los dos instrumentos propios declarados en gobernanza.json son scripts manuales de solo-visibilidad que nadie corre, y el inventario que debería anclar la auditoría estructural (sldb_architecture.spec.yaml) envejeció: 16 de sus 17 nombres ya no corresponden con el sistema real, sin que nada lo detecte.

## Evidencia

- El canal normal: `pytest` (1207 pasan) + `selfdoc check` + `build` (ci.yml:25-30). Todos miran comportamiento y frescura de referencia CLI.
- `selfdoc check` (ci.yml:28) → `src/sldb/cli/commands/selfdoc.py:63-68`: re-escanea el parser CLI (`ParserScanner`), re-materializa los documentos de referencia de comandos/superficies, y compara contra lo trackeado en el store; drift → `report.ok=False` → exit 1 → CI rojo. **Esto sí es auditoría real y bloqueable — de un solo objeto:** la referencia generada de comandos CLI. `docs/self-documentation.md` y el parser (`cli/parsers/selfdoc.py:11-16`) muestran que existe también `python-check` ("Report static Python documentation drift without writing") — **y CI no lo corre**. La mitad basada en AST del canal propio depende de que alguien se acuerde.
- `herramientas_propias` (gobernanza.json): ambos scripts existen, ambos son manuales, ninguno aparece en CI ni tests (grep de referencias: cero resultados fuera de sí mismos):
  - `scripts/map_architecture.py` (61 líneas): recorre el AST de `src/`, extrae imports internos y **imprime un mapa markdown**. No detecta ciclos, no devuelve código de error, no compara contra nada. Visibilidad pura, sin consumidor.
  - `tools/generate_vistas_html.py` (66 líneas): renderiza `docs/vistas.yml` <!-- gone --> (diagramas mermaid) a `docs/architecture.html` <!-- gone -->. No verifica nada contra el código; solo compone HTML.
- `spec_arquitectura` (gobernanza.json → `sldb_architecture.spec.yaml`): declara 7 nodos (CLI, AST_Handler, TemplateExtractor, DataExtractor, SLDBRenderer, StoreManager, LinkManager); existen 11 paquetes reales (api, assets, cli, core, examples, links, models, runtime, selfdoc, store, templates). **Divergencia exacta: 6 declarados que no existen + 10 reales que no se declaran = 16 de 17 nombres mal.** El único que matchea es CLI. Peor: `selfdoc` usa ese spec como ancla de verdad — `python_materialize.py:49-54` no lo valida: solo graba `ruta; sha256=…` como referencia en cada documento. El hash certifica que el archivo no cambió, no que sea cierto.

## Lo que el canal normal no ve

1. **Estructura.** Las pruebas ejercitan comportamiento; ningún test importa el grafo de paquetes. Los 5 ciclos y los 91 imports dentro de funciones son invisibles para los 1207 verdes. El único instrumento que miraría eso (map_architecture.py) es un script muerto: nadie lo corre y, si se corriera, solo imprimiría.
2. **La verdad de los 70 docs.** `selfdoc check` verifica exactamente una cosa: que la referencia CLI regenerada coincida con la trackeada. No pasa por los 70 markdown de docs/ (ni siquiera los que afirman hechos verificables: `current-source-tree.md`, `current-cli-tree.md`, `architecture_map.md`). Un doc que describa un módulo eliminado sigue "pasando" para siempre. La única excepción estructural es `tests/test_store_readme_doc.py:33-34`, que hace roundtrip del README del store — un caso, no un canal.
3. **El inventario de arquitectura.** El spec declara un sistema de 7 componentes estilo mainframe (AST_Handler, DataExtractor…) que no existe; el real (11 paquetes) vive sin declaración. El antipatrón «existencia como prueba» en estado puro: el spec envejeció en silencio y conserva su autoridad — es el archivo que `selfdoc` cita como `architecture_spec` con su sha256.

## Patología

**Solo se ve lo que el canal de reportes fue diseñado para ver.** El sistema construyó un canal propio genuino (selfdoc) pero lo apuntó al objeto más fácil de verificar — la referencia de sus propios comandos CLI — y dejó sin observador exactamente lo que puede degradarse sin romper pruebas: estructura de paquetes, verdad de la documentación en prosa y correspondencia spec↔código. El único mecanismo que recorre el conjunto completo de archivos (`test_clean_code_rules.py`, 586 casos) mira 3 reglas de estilo y ninguna relación entre partes. La auditoría que existe es parcial y lo parcial no se declara: CI en verde comunica "todo auditado" cuando solo se audita un slice.
