# Coordinator status (robocop2) — 2026-11-05

## Nodo GO03 — Costura GraphBackend sobre networkx — BLOQUEADO en el cold-bundle

### Estado
- TaskDoc promovido con deskops (sin commitear, en el clon principal `~/proyectos/SLDB_1/sldb`, sobre main `573fda56`): `desk/tasks/task-go03-costura-graphbackend-sobre-networkx.md`, task_type code, `files` con 11 rutas (paquete nuevo `src/sldb/store/graph/backend/`, `api/graph/analyze.py` y `__init__.py`, parser y comando `graph_analysis`, `store_declaration.py`, `docs/architecture/graph-backend.md`, CHANGELOG, `tests/store/test_graph_backend.py`).
- Preflight (attempt-1, technical_ok): 4 ambigüedades, todas corregidas en el Scope del TaskDoc con `deskops edit task` como precisiones p1–p4:
  - p1 goldens: hoy no existen; el primer commit del ejecutor los captura desde main (stdout de los seis `sldb graph` sobre el store de la fixture `world` de `tests/api/test_api_graph_analysis.py`) en `tests/fixtures/graph_goldens/<comando>.txt`. Los comandos graph no tienen `--format json`.
  - p2 índice del propio repo = `compose_edge_index(<repo>/.sldb)`, cargado con `load(índice, None)`.
  - p3 inventario del espía: las diez funciones de `api/graph/analyze.py` y los seis subcomandos; `execute/neighborhood/snapshot/traverse` fuera.
  - p4 forma del finding: `node`, `holds`, `clause`, `seen` (rules-language.md §4/§6).
  - FUTURO: sin hallazgo.
- Cold-bundle: **tres timeouts de 900 s** (attempt-1/2/3, 00:02–00:47 del 2026-11-05; input.md de 79.427 bytes). pi responde en 3 s a un prompt corto, así que el transporte está bien: el input es demasiado grande para 900 s en deepseek-flash. Fallos técnicos, no cuentan como intento de revisión.

### Nota sobre la regla nueva (CLI-only)
Antes de recibirla escribí a mano `disposition.md` y edité `receipt.json` del preflight de GO03 (runs/, sin commitear en el clon principal). Desde la regla no escribo ninguno de los dos.

### Bloqueo — decide el supervisor
No puedo seguir sin tocar `desk/drawer/plans/grafo-operable/context_review.py` (TIMEOUT = 900), que ahora está fuera de mi alcance. Opciones:
1. Subir TIMEOUT (p.ej. 1800 s) o añadir un flag `--timeout` al driver, y yo relanzo el bundle.
2. Recortar lo que el bundle mete para GO03 (79 KB; GO02 era bastante menor).
3. Aceptar GO03 con solo el preflight dispuesto (contra la regla "dos revisiones dispuestas"; decisión tuya).
Además: el TaskDoc de GO03 y los artefactos de revisión están sin commitear en el clon principal; dime si los commiteo yo (en main local no pusheo) o los commiteas tú como hiciste con GO02.

Rama `wt/go03` creada desde main solo para este estado; sin código todavía.
