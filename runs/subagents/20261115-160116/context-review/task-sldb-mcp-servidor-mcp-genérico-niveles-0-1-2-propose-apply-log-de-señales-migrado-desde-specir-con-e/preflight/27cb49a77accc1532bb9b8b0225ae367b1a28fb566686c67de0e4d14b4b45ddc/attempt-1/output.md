## REFORMULACION
El nodo debe planificar la migración del servidor MCP genérico de specIR al repo `sldb` (`/mnt/ssd/proyectos/SLDB_1/sldb`), sin reescribirlo: tools de lectura nivel 0, `propose_changes`/`apply_changes` niveles 1/2 sobre `sldb.api.apply_batch`, comando `sldb mcp --store --level --actor` por stdio, extra opcional `mcp`, log de señales con `list_signals`, punto de extensión para consumidores y tests portados con cliente MCP real. Límites: nada específico de specIR; los modelos como código nunca se sirven; el nivel lo fija el operador; leer —incluido registrar señales— no escribe el store; deshacer queda pendiente, no se implementa el inverso en `sldb.api`.

## AMBIGUEDADES
1. «El worker decide dónde vive (runtime o caché del store…)»: no fija ruta, formato, retención ni concurrencia; obliga a inventar el contrato del log.
2. «sugiere nombres cercanos con `sldb.api.matching` (no un matcher nuevo)»: no define umbral, orden ni forma de sugerencias; obliga a inventar comportamiento visible.
3. «un punto de extensión… (por ejemplo `build_server` con un registro de extensiones)»: no fija firma, registro ni herencia efectiva; obliga a inventar API pública.
4. «el nivel lo fija el operador al arrancar» y «según el nivel»: no hay matriz nivel→tools permitidas; obliga a inventar qué se expone en 0/1/2.
5. «sin literales que repitan la respuesta»: no concreta qué aserciones sustituyen a los tests de specIR; obliga a inventar criterios de portabilidad.
6. «dejar el punto preparado y declarado como pendiente»: no indica artefacto verificable; obliga a inventar si basta documentación, TODO o test omitido.

## DRY-RUN
Lecturas: módulos y tests de specIR en `82c79d6`/`14f6f24`, `sldb.api`, `matching`, CLI, `pyproject`, `contracts/layers.toml`, docs y CHANGELOG. Cambios previstos: copiar módulos mínimamente modificados, registrar subcomando y extra, añadir log/`list_signals`, extensión y tests portados. Dependencias: `apply_batch`, `matching`, `mcp>=2.2` opcional, cliente stdio y copia aislada del store. Validaciones futuras: pytest por archivo con `TMPDIR=/dev/shm`, `tools/check.sh`, `sldb stores build --check`, `deskops graph missing`, digest antes/después y rechazo stale/reglas.

## FUTURO
Otro nodo resolverá el pedido de deshacer del inbox `20261115-123855`; entonces se expondrá `undo_changes`. El worker justificará la ubicación del log. specIR registrará sus tools de dominio sobre el servidor de sldb.
