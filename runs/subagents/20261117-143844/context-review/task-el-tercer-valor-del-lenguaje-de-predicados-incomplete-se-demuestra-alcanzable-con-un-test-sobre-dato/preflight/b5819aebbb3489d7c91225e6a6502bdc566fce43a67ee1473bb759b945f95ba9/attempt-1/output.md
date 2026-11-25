## REFORMULACION
**Propósito:** determinar si el valor `incomplete` del lenguaje de predicados es alcanzable con datos reales; si lo es, demostrarlo con un test; si no, retirarlo del lenguaje, la API y la documentación.

**Resultado:** un test sobre un store real creado en `tmp_path` que obtenga `incomplete` desde una evaluación pública (`where` o `rules check`) y documente cuándo ocurre, **o** la retirada de `incomplete` sin alterar los resultados `true/false` existentes. Además: `result-summary.md` con la decisión y evidencia, tests en `tests/test_predicates_cli.py` o `tests/api/test_rules_evaluation.py`, actualización de `docs/architecture/rules-language.md`, `CHANGELOG` y commit.

**Repo:** `/mnt/ssd/proyectos/SLDB_1` (SLDB_1).

**Límites:** solo `incomplete`; quedan fuera otros cambios del lenguaje. `depends_on: []`.

## AMBIGUEDADES
1. “O hay un test […] o incomplete se retira del lenguaje” — no define el criterio de suficiencia de la evidencia para elegir; obligaría a inventar el umbral de prueba.
2. “decidir con evidencia en result-summary.md” — no indica ruta ni formato; obligaría a inventar ubicación y estructura.
3. “con un store real armado en tmp_path” y “datos reales” — no aclara qué hace “real” a un store sintético; obligaría a inventar la fixture.
4. “evaluación pública (where o rules check)” — no fija si basta una u obliga a ambas; obligaría a inventar cobertura.
5. “sin cambiar los resultados true/false existentes” — no define baseline ni oráculo de regresión; obligaría a inventar comparative.
6. `files` omite `predicate_explain.py`, `predicate_reach.py` y `src/sldb/api/rules/`, citados en Rationale; obligaría a inventar si son editables.
7. “CHANGELOG y commit” — sin convención de mensaje ni estado de rama; obligaría a inventar formato.

## DRY-RUN
**Lecturas:** TaskDoc; `docs/architecture/rules-language.md`; `src/sldb/api/where.py`; `predicate_explain.py`; `predicate_reach.py`; `src/sldb/api/rules/`; tests citados; `tools/check.sh`; `CHANGELOG.md`. Grep de `incomplete`.  
**Cambios previstos:** añadir test/fixture y documentar el caso, o retirar `incomplete` de código/API/doc; escribir `result-summary.md`; actualizar `CHANGELOG`; commit.  
**Dependencias:** `uv run --frozen --extra code --extra dev`, `tmp_path`, pytest, `bash tools/check.sh --fast`.  
**Validaciones futuras:** los cuatro comandos de Validation. Sin ejecutar nada.

## FUTURO
Un nodo ejecutor produce `result-summary.md`, tests, cambios de doc/código y commit. Un humano o nodo revisor aprueba la elección entre demostrar o retirar `incomplete`, y valida el commit. El nodo de validación ejecuta los comandos y reporta resultados.
