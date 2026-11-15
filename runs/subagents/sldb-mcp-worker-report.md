# Informe: sldb mcp (servidor MCP genérico migrado de specIR)

## Qué migré (origen IR main 82c79d6, lectura 14f6f24; destino `src/sldb/mcp/`)

Regla del repo que obligó a trocear: `tests/test_clean_code_rules.py` exige por archivo de `src/` una sola clase, funciones de 10 líneas de lógica y 80 líneas efectivas. El código de IR (módulos de 150-240 líneas) no cabía, así que cada módulo se partió en archivos y funciones pequeñas; la lógica, los textos y los nombres de los métodos son los de IR.

| IR `src/specir/mcp/` | sldb `src/sldb/mcp/` | Cambio |
| --- | --- | --- |
| `paging.py` | `paging.py` | igual; `check_window` extraído |
| `addresses.py` | `addresses.py` | copia literal (solo `sldb.api`) |
| `mutability.py` | `mutability.py` | copia; quito referencias IR02/pron del docstring; matriz de niveles intacta |
| `changes.py` | `changes/` (`base`, `create_document`, `update_document`, `delete_document`, `assert_edge`, `retract_edge`, `batch_change`, `proposal`, `sealer`, `typed`) | una clase por archivo; mismos nombres de clase y esquema JSON |
| `read_tools.py` | `read/` (`tools.py` con `ReadTools`, `models`, `documents`, `graph`, `views`, `integrity`, `miss`) | métodos pasan a funciones por tema; `ReadTools` delega. Cada rama "no existe" añade una marca `signal` vía `miss.missing` (única lógica nueva) |
| `write_tools.py` | `write/` (`tools.py` con `WriteTools`, `propose`, `apply`, `findings`, `pending`, `pendings`) | métodos privados a funciones; `DEFAULT_ACTOR = agent:sldb-mcp`; `PENDING` conserva las notas del inbox de sldb y suma `undo`. No migré `claims_verified` (solo está en IR HEAD, regla IR05 de specIR) |
| `server.py` | `server.py`, `signal_server.py`, `guard.py`, `registry.py`, `unmet.py`, `context.py`, `extension.py` | `build_server` ya no define 11 tools anidadas: `registry.py` las registra desde las mismas funciones. `run()` de IR es `guard.guarded` |
| `__init__.py` | `__init__.py` | igual |

Nuevo (no existía en IR): `signals/` (catálogo cerrado, log, suggest, candidates, settle, `list_signals`), `context.py`, `extension.py`, `unmet.py`, `signal_server.py` (subclase de `MCPServer`).
CLI: `src/sldb/cli/parsers/mcp.py`, `src/sldb/cli/commands/mcp.py` (import perezoso de `sldb.mcp.server`; sin el extra sale con rc 2 y dice `pip install 'structuredLanguageDB[mcp]'`), registro en `parsers/core.py`, `dispatcher.py` (sin añadir líneas: el archivo estaba en 80) y `help_texts_short.py`.
Contratos: `pyproject.toml` extra `mcp = ["mcp>=2.2"]`; `contracts/layers.toml` (`mcp` en la capa de transporte, eje y unidad `mcp`, contadores de `persistencia`, `recuperacion` y `operacion` al día); `contracts/identity.toml` (paquete de producto); `tools/check_axes.py` (módulo `mcp` del eje). Docs: `docs/architecture/mcp.md`; CHANGELOG.

`mcp` no estaba en `/mnt/ssd/proyectos/SLDB_1/.venv`: lo instalé con `uv pip install --python .../.venv/bin/python 'mcp>=2.2'` (resolvió mcp 2.3.0). No toqué `uv.lock` (su cambio ya estaba). No añadí `mcp` al extra `dev`: haría falta regenerar `uv.lock`; los tests hacen `importorskip("mcp")`.

## Dónde vive el log y por qué
`<proyecto>/.sldb_cache/signals.jsonl` (`sldb.store.layout.cache_dir(store)/signals.jsonl`; el preflight decía `<store>/.sldb_cache`, pero la caché de sldb es hermana de `.sldb`, junto a `rules/` y `composed/`). Es caché derivada, ignorada por git, no estado del store: ningún documento trackeado ni store enlazado se escribe, así que funciona en nivel 0 y la prueba de que leer no escribe (digest del store sin `.sldb_cache`) sigue verdadera; hay un test que lo comprueba. Una línea por señal con un único `O_APPEND`; sin rotación.

## Ejemplo real de una línea (corrida a mano de `sldb mcp --actor agent:manual` sobre una copia en /dev/shm)
```
{"at": "2026-11-15T16:41:50.885Z", "tool": "describe_model", "arguments": {"model": "Itm", "offset": 0, "limit": 50}, "signal_class": "unknown_model", "suggestions": ["Item", "Stage", "RelationTypeDoc", "ViewDoc", "RelationDoc"], "actor": "agent:manual"}
```

## Tests (de a uno, con el comando indicado)
`tests/mcp/` (sin mocks: cliente MCP real por stdio contra `python -m sldb mcp`, sobre copia aislada de un store real construido con la API pública; `mcp_world.py`, `mcp_session.py`, `mcp_helpers.py`, `conftest.py`).
- test_read_tools.py: 14 passed
- test_no_writes.py: 2 passed
- test_dry_run.py: 1 passed
- test_mutability.py: 7 passed
- test_write_tools.py: 8 passed, 1 xfailed (el xfail estricto de IR: SLDB valida aristas tras escribir)
- test_signals.py: 10 passed (catálogo, clases, formato de línea, `list_signals` paginada y filtrada, tool y argumento desconocidos, `undo_changes` not_implemented, el log no es estado del store)
- test_extension.py: 5 passed (tools de ejemplo, paginación, nivel/actor, herencia del log, `--extension` inválido)
- test_cli_mcp.py: 3 passed (sin el extra; el resto de sldb no lo necesita)
- tests/test_clean_code_rules.py: 1013 passed; tests/test_cli_every_command_has_a_handler.py: 1 passed
- `tools/check.sh --fast` (con el venv en PATH): todas las puertas pasan.
No pude correr `tests/store/test_graph_backend.py` ni `tests/test_cli_format_coverage.py`: el lock `/dev/shm/sldb1-tests.lock` lo tenía otro proceso; solo tocan `build_parser`. Tampoco corrí `sldb selfdoc check` ni `stores build --check` (del coordinador): el comando nuevo y los módulos nuevos pueden regenerar `knowledge/` y `.sldb`; no lo regeneré ni lo commiteé. `docs/architecture/mcp.md` puede entrar en el glob del store.

## Dudas
1. Matriz de niveles: el preflight (4) dice nivel 1 = propose, nivel 2 = apply; el bundle manda "como mutability.py de IR" y los tests portados; seguí IR (nivel 1 sirve propose y apply sobre contenido, nivel 2 suma reglas como dato).
2. "Copia aislada del store": no copié el store vivo de sldb (30 MB, federado con deskops y pron, cambia mientras se trabaja). Los tests construyen un store real pequeño (Item/Stage, RelationDoc, RuleDoc, ViewDoc) con la API y comparan contra los archivos de la copia. Se perdió el test de federación spec2viz (sin reemplazo con store enlazado).
3. Una llamada a una tool no servida en ese nivel (p. ej. `propose_changes` en nivel 0) ya no es error: es señal `unknown_tool` con explicación del nivel.
4. El `--actor` global de la CLI lo consume `main` antes del subparser; el handler lo recupera del proceso (si es el `agent` por defecto, el actor es null).
5. Sugerencias con `Matcher.rank` y umbral por defecto (0.0): siempre devuelve hasta 5 aunque ninguna se parezca.
6. `mcp` falta en el extra `dev` y en `uv.lock`.
