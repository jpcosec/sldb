## REFORMULACION

Propósito: quitar el coste por referencia de `attach_atom_edges`, que recompone live-stale y los mapas del índice federado en cada `edges_of`. Resultado: con 10 referencias, `load_edge_index` se llama ≤2 veces por llamada (con y sin enlaces), sin recalcular live-stale ni mapas por referencia; el catalog build de IR pasa de >300 s a <60 s con aristas iguales como conjunto. Repo: sldb. Superficie: `store_reader.py`, `store_edges.py`, `composed_reading.py` (solo si el paso 2 no basta), `tests/matching` (nuevo test contador y `test_matching_refs.py`) y `CHANGELOG.md`. Límites: no cambia semántica de stale, no toca `compose.py` salvo que (3) lo exija, no toca la federación de IR; el ejecutor no hace push.

## AMBIGUEDADES

1. "la ruta exacta se copia de la nota de origen (references)": la nota no está en el input; obliga a inventar la ruta del `project.yml`.
2. "runs/subagents/<run-dir>/result-summary.md": `<run-dir>` no viene dado; obliga a inventar el directorio del informe.
3. "bajo el encabezado '## 0.1.13 — not released yet'": no dice si ya existe; obliga a decidir si se crea.
4. "igualdad de las aristas ... comparadas como conjuntos": no define qué campos identifican una arista; obliga a inventar el criterio.
5. "por firma de shards y stats de fuentes" / "archivos trackeados": no define esos conjuntos; obliga a inventar la clave exacta.
6. "10 referencias": no dice cuáles ni sobre qué datos; obliga a elegirlas.

## DRY-RUN

Lecturas: los archivos del Implementation Path, `edge_index.py` y el test citado. Cambios: (a) test contador con monkeypatch de `load_edge_index`/`stale_of_facts` que falla hoy; (b) `StoreReader` carga el índice una vez por store y resuelve `edges_from`/`edges_to` sobre él; (c) memoización condicional en `with_live_stale` si (b) no alcanza; (d) línea de CHANGELOG. Dependencias: helpers de `test_matching_refs.py`, nota de origen, repo IR accesible. Validaciones futuras: los tres `pytest`, medición antes/después en el informe y comparación de aristas como conjuntos.

## FUTURO

El coordinador hace `deskops closeout commit` (sin push) y el aviso `deskops message send` al repo IR, o la línea "Aviso a <repo>: ..." si no está registrado. La nota de origen aporta la ruta del `project.yml`. Un humano decide si no se alcanzan los 60 s o si (3) compromete la semántica de stale.
