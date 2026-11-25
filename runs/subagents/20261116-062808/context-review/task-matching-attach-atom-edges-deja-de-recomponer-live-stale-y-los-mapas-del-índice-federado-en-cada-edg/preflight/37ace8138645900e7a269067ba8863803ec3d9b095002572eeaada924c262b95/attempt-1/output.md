## REFORMULACION
Encargo ejecutable de depuración/rendimiento en el repo SLDB_1: hacer que `attach_atom_edges` cargue el índice de aristas una vez por store y llamada, sin recomponer `live-stale` ni los mapas del índice federado por cada referencia. Resultado: test contador que limite `load_edge_index` a 2 llamadas para 10 referencias, validaciones pytest, medición del `catalog build` de IR con después <60 s y mismas aristas, CHANGELOG e informe. Límites: no cambia la semántica de stale, no toca la configuración de federación de IR ni hace push; el commit es del coordinador. No es agregado ni paquete.

## AMBIGUEDADES
1. «la ruta exacta se copia de la nota de origen (references)»: el input solo da la ruta de la nota, no su contenido; obligaría a inventar el `project.yml` exacto o asumir acceso a otro archivo.
2. «El commit lo hace el coordinador con deskops closeout commit» frente a «commit.» en Done When: obligaría a decidir si el ejecutor debe commitear o solo dejar listo.
3. «deskops message send --to <repo>» y «Aviso a <repo>: ...»: no se nombra el repo destinatario; obligaría a inferir que es IR.
4. «Medición antes y después con el comando de IR de la nota (cd al repo IR, timeout 300)»: si el “antes” no termina en 300 s, obligaría a inventar cómo registrarlo (por ejemplo, “>300 s”).

## DRY-RUN
Lecturas: `store_reader.py`, `store_edges.py`, `edge_reading.py`, `compose.py`, `composed_reading.py`, `edge_index.py`, `tests/matching/test_matching_refs.py`, CHANGELOG y nota de origen si está disponible. Cambios previstos: test contador; carga única del índice en `StoreReader`; memoización condicional en `composed_reading.py` solo si no se alcanza la meta; entrada de CHANGELOG; informe con mediciones. Dependencias: fixtures/helpers del test, ruta del `project.yml` de IR, entorno de medición y contadores por monkeypatch. Validaciones futuras: los tres pytest indicados, comparación de conjuntos de aristas y medición antes/después.

## FUTURO
El coordinador ejecuta `deskops closeout commit` y decide el cierre; un humano o nodo de IR aporta/confirma la ruta del `project.yml` y acepta la medición; si el repo del aviso no está registrado, queda constancia en el informe.
