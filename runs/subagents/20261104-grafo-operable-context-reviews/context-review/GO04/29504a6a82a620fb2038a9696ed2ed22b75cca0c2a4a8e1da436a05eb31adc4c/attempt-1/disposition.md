# Disposición GO04 (ronda 3)

- 1 corregido: firma canónica como JSON canónico de nombres.
- 2 corregido: shard con versión menor se marca stale al abrir y se reconstruye en la siguiente reconstrucción.
- 3 corregido: el executor es src/sldb/store/graph/executor.py, el de StructuredQuery.
- 4 corregido: __indexed__ sustituye; ausente se omite; no proyectable = error al cargar.

Estado: input corregido; requiere ronda 4.
