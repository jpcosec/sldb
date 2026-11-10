REFORMULACION
Propósito: ejecutar GD25 (task.code, no agregado): tipar y validar ViewDoc compuesta y servirla. Resultado: `sldb.api.run_view(store,name,params)`→`{view,params,revision,sections}`; CLI `sldb views run|list` con envelope; `GET /views` y `GET /views/<name>` con ETag e If-None-Match→304; validadores pydantic; tests, `docs/architecture/views.md` y CHANGELOG. Repo: sldb, worktree aparte en robocop2. Límites: solo OUTPUT_SCOPE; fuera register_view_provider y computed, cambiar `/views/projection*` de SV02 y nombres del caso deskops en src/.

AMBIGUEDADES
1. "Sin punto de extensión en Python (DA1)": DA1 no se define; obligaría a inventar qué prohíbe además del grep de register_view_provider/computed.
2. "sldb views run NAME [--param k=v ...] y sldb views list, con envelope": la forma del envelope no se declara; obligaría a inventar sus claves.
3. "--param k=v": el tipo del valor no se especifica; obligaría a inventar coerción string/JSON/bool.
4. "revision = sha256 de los source_hash ordenados de todos los documentos leídos": no acota si cuentan los vecinos leídos por edges; obligaría a inventar ese límite.
5. "{relation, direction out|in, as} que agrega a cada fila los export_id vecinos": no dice bajo qué clave van ni si findings/holding/blocked son claves de fila; obligaría a inventar la forma de row.

DRY-RUN
Lecturas: view_doc.py, notation_models.py, api/__init__.py, edge_reading.py, edges_holding/edges_blocked, api/rules, select_documents, shard_signature.py, cli parsers/commands/dispatcher/public, serve/routes.py y views_routes.py, tests citados. Cambios previstos: tipado y validadores en ViewDoc; módulos nuevos `sldb/api/views` (run_view, list_views, rows/groups/edges/rules/transitions/revision); reexport en api/__init__.py; grupo CLI views; `GET /views` y `GET /views/<name>` con ETag antes de `/views/projection*`; tests; docs; CHANGELOG. Dependencias: GD21/GD23 en main, SV01 ViewDoc en main, gates GO05/06/08/09/10 y precisiones q2/q5/q8/q9/q10/q11/q12. Validaciones futuras: los pytest listados, greps, medición de 200 Items, rebase y nota a deskops. Sin ejecutar nada.

FUTURO
El dueño decide las hipótesis q5/q7 (rules al escribir frente a run_view) y q9 (firma por shards); SV01 debe estar en main o GD25 espera. El coordinador poda files no usados y copia la cifra de tiempo a Validation; el supervisor corre la suite completa sobre lo integrado; deskops recibe la nota de cierre (regla 7). Un nodo posterior consume run_view.
