# Informe de la prueba de concepto: indice federado en un motor Datalog embebido

Fecha: 2026-11-24. Repo: sldb, commit de partida 3ba12f65. Host: robocop2 (6 cpu, 31 GB, ~22 GB disponibles).
Codigo de produccion intacto: todo vive en `poc/poc_datalog.py`.

## Motor elegido para la prueba

| Motor | Cliente Python | Datalog | Embebido | Veredicto para la prueba |
|---|---|---|---|---|
| Datalevin (candidato de `docs/architecture/graph-backend.md`) | no hay paquete en PyPI (`pydatalevin` no existe en el registro); se usa desde JVM o binario nativo | si (Datalog, estilo Datomic) | solo en JVM/nativo | descartado para la prueba: obligaria a un proceso aparte con protocolo propio |
| CozoDB (`cozo-embedded` 0.7.6, wheel en PyPI) | si, API `CozoDbPy.run_script` | si, con recursion, negacion estratificada, agregados | si, motor en Rust; almacenamiento `mem`, `sqlite` o `rocksdb` | elegido |
| pyDatalog 0.22 | si | Datalog en memoria, sin almacenamiento propio | en proceso | sin persistencia ni indices: no sirve como duenio del almacenamiento |
| clingo 5.8 | si | ASP, no Datalog de consulta | en proceso | otro paradigma (resolucion, no consulta incremental) |
| Kuzu / Neo4j | si | no: Cypher | si / no | fuera: JP pidio Datalog; ademas D6 fija Datalog estratificado |

Salvedad: la tabla de motores se armo con lo que resuelve `uv pip install --dry-run` hoy y con lo que
documenta cada proyecto; la actividad reciente de Cozo (ultima version publicada 0.7.6) no la verifique
y es un riesgo propio de la decision de motor.

## Datos

Indice federado real de sldb con sus links (deskops, pron y los que ellos encadenan): 4 stores, 39.639 nodos,
230.655 aristas, 7.829 documentos, 337 `AtomDoc`. Primera composicion tras invalidar el cache en disco:
40,0 s (el "28 s" de la nota de JP es de otro dia; el orden de magnitud se confirma).

## Como repetirlo

Desde la raiz de sldb, con el venv del repo mas `uv pip install cozo-embedded`:

    P=desk/drawer/plans/grafo-datalog-daemon/poc/poc_datalog.py
    python $P facts   .sldb /tmp/facts.pkl                       # compone el indice y vuelca hechos
    python $P current .sldb /tmp/facts.pkl /tmp/cur.json         # camino actual
    python $P cozo    /tmp/facts.pkl /tmp/cozo-mem.json mem      # Cozo en memoria
    python $P cozo    /tmp/facts.pkl /tmp/cozo-sqlite.json sqlite
    python $P reopen  /tmp/facts.pkl                             # reabrir la base sqlite ya cargada
    python $P report  /tmp/cur.json /tmp/cozo-mem.json /tmp/cozo-sqlite.json

Cada paso corre en su proceso para que el RSS sea el suyo. Los JSON de esta corrida estan en `poc/resultado-*.json`.

## Resultados

| Medida | Camino actual | Cozo mem | Cozo sqlite |
|---|---|---|---|
| Carga del indice federado (s) | 3,04 (con cache compuesto en disco valido) | 2,60 | 4,74 |
| Aristas de un nodo (2.557 aristas), mejor de 5 (s) | 0,0005 | 0,0066 | 0,0066 |
| Recorrido: 68 descendientes por `implements` (s) | 0,0003 | 0,0006 | 0,0014 |
| Atomos: aristas de los 337 en lote (s) | 0,0022 | 0,0117 | 0,0157 |
| Atomos: 50 consultas sueltas, como `attach_atom_edges` hoy (s) | 49,08 | 0,0084 | 0,0147 |
| Stale: escaneo de stats y comparacion (s) | 0,99 con hechos en memoria; 27,06 leyendo los shards | 0,99 | 1,06 |
| RSS tras la carga, incremento sobre el arranque (MB) | 604 | 552 | 385 |
| Pico RSS (MB) | 1.146 | 780 | 689 |
| Reabrir la base ya cargada y pedir las aristas de un nodo | n/a | n/a | 0,007 s, +5,7 MB, base de 319 MB en disco |

Las mismas respuestas en los tres: 2.557 aristas del nodo, 68 descendientes, 0 documentos stale.

## Lectura honesta

1. **Las consultas en proceso no mejoran.** Con el indice ya en memoria, el camino actual (diccionarios Python) responde
   aristas, recorrido y atomos en microsegundos; Cozo tarda milisegundos. Cozo no gana por consultar mas rapido.
2. **Lo que cuesta es recomponer, no consultar.** Las 50 consultas sueltas del camino actual tardan 49 s porque cada una
   vuelve a pasar por `compose_edge_index` y su live stale (~1 s cada una); con el indice residente (Cozo o el dict en un
   daemon) cuestan 8 a 15 ms en total. Es el mismo defecto que ataca `task-matching-attach-atom-edges-deja-de-recomponer-live-stale`;
   esa tarea lo arregla sin motor nuevo, y va primero.
3. **Persistir el motor quita la carga en frio.** Reabrir la base sqlite ya cargada y consultar cuesta 7 ms y 5,7 MB, contra 3 s
   (cache en disco valido) o 40 s (cache invalido) de componer. Este es el argumento fuerte a favor de un motor duenio de las aristas,
   incluso sin daemon.
4. **Stale no mejora con Datalog.** El costo (0,99 s) es el escaneo de stats y las comprobaciones de seguridad
   (`unreadable_reason`), que son las mismas en ambos caminos; la comparacion en Datalog cuesta 0,09 s. Lo que quita ese segundo
   es un daemon que no reescanea (invalidacion por evento o por git), no el motor.
5. **Memoria.** Un proceso residente con el indice cargado ocupa del orden de 0,4 a 0,6 GB sobre su arranque (pico 0,7 a 1,1 GB),
   muy por debajo del tope de 8 GB libres de robocop2; pero no se midio con varios proyectos a la vez.
6. **Limites de la prueba.** La carga a Cozo parte de hechos ya compuestos (`compose_edge_index` se ejecuto antes, en `facts`);
   la composicion desde shards no se movio al motor y su costo (3 a 40 s) no esta en la fila "Carga" de Cozo.
   No se midieron proyeccion de payload ni `eval` de reglas, ni escrituras incrementales ni concurrencia de lectores.
   El stale de la columna Cozo comparo mtime y tamano en Datalog y leyo y hasheo en Python solo los archivos movidos,
   igual que hoy. Una sola maquina, una corrida por medida.
