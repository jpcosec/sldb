## REFORMULACION

Nodo único ejecutable (`task.debug`, `current_node: ritual-execution`, sin átomos ni hijos): no es agregado. Propósito: cerrar el resto de H11 y que `sldb views run board`, con store construido y en proceso nuevo, baje de 1,6 s a menos de 1 s (mediana de 3), sin cambiar resultado ni `revision`, y con invalidación al escribir o cambiar un documento. Repo: sldb (`src/sldb/api/documents/select_documents.py`, `api/views/`, `store/io/`, `store/edge_index/`, `tests/`, `docs/architecture/views.md`, `CHANGELOG.md`, `contracts/layers.toml`). Límites: fuera el índice de aristas y su caché (H11), el costo propio de deskops, H12 y H13; b3 se abandona si el recorte seguro es menor a 0,1 s.

## AMBIGUEDADES

1. "una caché de disco, en el .sldb_cache del store que llama": no se define la ruta ni el nombre del archivo; obligaría a inventar ubicación y esquema.
2. "mtimes y tamaños de core/documents más la versión del índice y el contrato de cada modelo" frente a "un documento escrito o cambiado se nota en la siguiente corrida": si un cambio preserva mtime y tamaño, ambas afirmaciones se contradicen; obligaría a elegir qué garantía vale.
3. "el script del benchmark vive en tests/perf de esa tarea": no se nombra el archivo; obligaría a adivinar cuál es la línea base.
4. "sin cambiar la superficie pública ni el orden de los efectos": "orden de los efectos" no está definido; obligaría a inventar qué efectos se auditan.
5. "una caché corrupta o de otra versión se ignora sin error": no se dice qué identifica la versión de la caché; obligaría a definirla.

## DRY-RUN

Lecturas: Board, este TaskDoc, rituales execution/testing/closeout, `select_documents.py`, `views.md`, `layers.toml`, `repro.log` de H11, script de `tests/perf`, git log para confirmar H11 en main. Cambios previstos: módulo de caché JSON en `store/io/` (o bajo `api/documents`), clave por mtimes/tamaños/versión de índice/contratos, lectura y escritura tolerante a corrupción; import perezoso en `sldb.api` solo si supera 0,1 s; tests de equivalencia, invalidación y caché corrupta; docs, CHANGELOG, eje en `layers.toml` si el archivo es nuevo. Dependencias: H11 integrada, `.sldb_cache` escribible, `-X importtime` y `cProfile`, `tools/check.sh --fast`. Validaciones futuras: benchmark frío/caliente antes y después, clean-code rules, suite por archivo desde `/dev/shm`, 7 pasos en clon limpio.

## FUTURO

Verificar la precondición de H11 y correr los 7 pasos corresponde al coordinador; si la meta no se alcanza, el informe con la medición decide humano; deskops view board y H12/H13 son otras tareas.
