# Alcance: motor Datalog duenio de las aristas y daemon residente de sldb

Fecha: 2026-11-24. Repo duenio: sldb. Estado: plan en drawer, `execution_authorized: false`.
Origen: notas 20261123-142527 (JP revierte D5) y 20261123-142553 (JP pide ver ahora el daemon).

## Estado de partida (verificado 2026-11-24)

- `GraphBackend` (`src/sldb/store/graph/backend/protocol.py`) tiene `load`, `eval`, `analyze`, y solo existe `NetworkXBackend`.
  El backend recibe el indice ya compuesto: **compose queda fuera del backend** (`docs/architecture/graph-backend.md`).
- El indice se compone a mano: shards YAML en `.sldb_cache/edges` (110 MB, 4.797 archivos en este repo), `compose_edge_index`
  (`store/edge_index/compose.py`), cache compuesto en `.sldb_cache/composed` (varios archivos de 100 a 150 MB) y `with_live_stale`
  en cada llamada. Medido en la prueba de concepto: 40 s la composicion con cache invalido, 3 s con cache valido, ~1 s por
  llamada de live stale, 49 s para 50 consultas sueltas de aristas de atomos.
- No hay proceso residente: cada invocacion de CLI, `sldb serve`, deskops y specir recompone o relee el indice.
- Una prueba de concepto con CozoDB sobre el indice federado real esta en `poc/informe.md`.

## Entra

1. Un motor Datalog embebido como duenio del almacenamiento y la consulta de aristas (hoy: shards YAML y dict en memoria).
2. Un daemon sldb residente con el indice y el store cargados, y su cliente con respaldo sin daemon.
3. Invalidacion del indice con git y con las escrituras de sldb.
4. Las tareas de codigo que salen del DAG (`dag.yaml`).

## Queda fuera

- Cambiar `GraphBackend` o el codigo de produccion en este plan: eso lo hacen las tareas del DAG, cuando JP decida.
- El lenguaje de reglas (D6): sigue siendo Datalog estratificado; el motor nuevo debe poder evaluarlo, no redefinirlo.
- `task-matching-attach-atom-edges-deja-de-recomponer-live-stale...`: va primero y este plan ni lo reemplaza ni lo bloquea
  (gate `G_MATCHING_FIRST`).
- Autenticacion, multiusuario o red: el daemon es local a un proyecto y a un usuario.

## Reglas comunes de ejecucion

1. Cada nodo se promueve con `deskops add task --from-drawer`, con `--task-type` y `files` completos.
2. Paridad antes que mejora: un nodo que sustituye un camino deja los goldens de `graph`, `edges` y `where` identicos.
3. Sin daemon todo sigue funcionando (CLI, tests, contenedores de ejecutor): el daemon es una aceleracion, nunca un requisito.
4. Toda medicion que un nodo exige se registra con unidad, metodo, fecha y comando repetible; la de este plan es `poc/poc_datalog.py`.
5. Nada del plan se ejecuta mientras `execution_authorized` sea `false`; cada decision abierta es una `task.decision` para JP.
