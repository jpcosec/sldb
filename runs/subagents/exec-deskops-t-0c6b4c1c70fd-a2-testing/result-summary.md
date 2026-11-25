FALLA

# Testing — matching: attach_atom_edges carga el índice una vez por store

Commit verificado: `9d09537c8dc4a8cc3786a8a1bd9415db4bd3e12a` — `matching: attach_atom_edges carga el índice de aristas una vez por store`, con el trailer `Task-Id` correcto. Archivos: `src/sldb/api/matching/store_reader.py`, `src/sldb/api/matching/store_edges.py`, `tests/matching/test_matching_refs.py`, `CHANGELOG.md`.

## Veredicto

**FALLA.** El cambio de producción sí logra la meta (una carga del índice por store y por llamada: verificado, 1 llamada con 10 refs), pero **el test contador exigido no cuenta las llamadas del camino nuevo y pasa aunque se elimine la caché**. Además, `bash tools/check.sh --fast` sale rc 1 por `identidad` (`workbench_demo` sin clasificar); el prompt del tester dice que rc ≠ 0 implica FALLA. Esa roja es preexistente y ajena al commit (también falla en el commit padre), pero se registra porque la regla es explícita.

## Motivo principal: el test contador es vacuo en el camino nuevo

`tests/matching/test_matching_refs.py::test_attach_atom_edges_loads_the_edge_index_at_most_twice_for_ten_refs` hace:

```python
from sldb.api.edges import edge_reading
real = edge_reading.load_edge_index
monkeypatch.setattr(edge_reading, "load_edge_index", lambda *a, **k: calls.append(a) or real(*a, **k))
```

Pero `src/sldb/api/matching/store_edges.py` hace `from sldb.api.edges.edge_reading import load_edge_index` (binding en tiempo de import) y `load_index()` llama a **ese** nombre local. Por eso el monkeypatch de `edge_reading.load_edge_index` no intercepta el camino nuevo: `calls` queda vacío y `0 <= 2` siempre.

Comprobaciones empíricas (mismo store de prueba de 10 átomos y 3 tareas que el test):

- Con el patch en el lugar correcto (`sldb.api.matching.store_edges.load_edge_index`), el commit nuevo hace **1** llamada.
- En el commit padre (vía `edges_of`/`edge_reading`) hace **20** llamadas (2 por ref), como describe la tarea.
- **Mutación**: en un worktree del commit, quité el caché `self._index` de `StoreReader._read_edges` para que llame a `load_index` una vez por referencia. El test del commit **sigue pasando** (`1 passed`), porque todas esas llamadas son invisibles para el contador. Es exactamente la regresión que el test debía detectar.

Por tanto no se cumple el requisito del alcance: un test que "falla si `load_edge_index` se llama más de 2 veces para 10 referencias". El test falla contra el código viejo (que va por `edge_reading`), pero no protege la implementación nueva.

Arreglo esperado: monkeypatchear `sldb.api.matching.store_edges.load_edge_index` (o `load_index`) con el contador y mantener la comparación de aristas como conjuntos; conviene además exigir `>= 1` para que un contador en cero no pase inadvertido.

## Lo que sí cumple

- Implementación: `StoreReader` carga el índice y los títulos una vez por store (`self._index`) y resuelve cada ref con `edges_of_index`; medí 1 llamada real para 10 refs. `composed_reading.py` no se tocó (el paso 3 no hizo falta).
- "Mismo resultado": el test compara las aristas como conjuntos contra `store_edges.edges_of` y pasa.
- `CHANGELOG.md`: hay una línea en español bajo `## 0.1.13 — not released yet`, con el estilo vecino.
- Informe del ejecutor (`runs/subagents/exec-deskops-e-3617fe0f6a32/result-summary.md`): medición antes (`timeout 300`, rc 124) y después (**54,9 s**, rc 0) con `tests/visual/fixtures/catalog/examples/catalog/project.yml` de IR, bajo los 60 s.

## Tests ejecutados (secuenciales, `TMPDIR=/tmp`, basetemp propio por corrida)

`/tmp/ws-venv` no existe en este contenedor; se usó `/workspace/sldb/.venv` (Python 3.13.18, pytest 9.1.1).

| Comando | rc | Resultado |
|---|---|---|
| `python -m pytest -q tests/matching/` | 0 | 33 passed |
| `python -m pytest -q tests/api/test_api_edges.py` | 0 | 17 passed |
| `python -m pytest -q tests/store/test_live_stale_security.py` | 0 | 8 passed |

No hay `tests/test_store_reader.py` ni `tests/test_store_edges.py` en el repo, así que no había tests de módulo adicionales que correr; el archivo de test del commit queda cubierto por `tests/matching/`.

## Gate rápido

    PATH=/workspace/sldb/.venv/bin:$PATH bash tools/check.sh --fast  -> rc 1

    PASS: núcleo aislado, capas, ejes, superficie
    FAIL: identidad — "directorio versionado sin clasificar en la raíz: workbench_demo"

Verifiqué que el mismo gate falla en un worktree del commit padre, sin los cambios de la tarea; `workbench_demo` es preexistente y el commit no lo toca. Aun así, según el prompt, rc ≠ 0 ya implica FALLA.
