REFORMULACION
PK01 es un agregado no ejecutable: no se promueve ni corre; termina cuando terminan GO01, GO02 y GO03. Su encargo es dejar fijados en sldb (i) la frontera sldb/deskops y su atom (GO01), (ii) la semántica, gramática y firma de evaluación del lenguaje de reglas (GO02) y (iii) el protocolo GraphBackend sobre networkx (GO03), antes de cambiar el comportamiento observable del store. Resultado: G_BOUNDARY, G_SEMANTICS y G_SEAM satisfechos. Límites: no cambia salidas de comandos existentes sobre stores existentes; no toca código de deskops salvo la nota de inbox; quedan fuera auth, motores externos y migración a kimun.

AMBIGUEDADES
ninguna.

DRY-RUN
Hipotéticamente, GO01 parte de la pill reescrita y D1; crea el atom, lo enlaza en la pill (commit 1), escribe la nota en deskops/desk/inbox con ruta y D1, y en commit 2 cambia solo gates.G_BOUNDARY a satisfied con el hash del commit 1. Transfiere G_BOUNDARY satisfecho.

GO02 parte de G_BOUNDARY y D6; escribe docs/architecture/rules-language.md (gramática, caminos, semántica estratificada/Kleene, explicación, __contract__, firma eval) y tests de spec xfail; su revisión en frío aceptada produce G_SEMANTICS. Transfiere a GO03 la firma eval y el subconjunto sin caminos.

GO03 parte de esa firma y G_BOUNDARY; implementa GraphBackend (load/eval/analyze), envuelve networkx, enruta los seis comandos graph y api/graph por analyze, añade graph_backend a store.yaml, docs y CHANGELOG; eval sin caminos y NotImplementedError con caminos. Su revisión en frío aceptada produce G_SEAM. Transfiere el protocolo para GO04 (proyección) y GO05 (caminos).

Validación conjunta: tres gates satisfechos; goldens idénticos; tests api/graph sin cambios; backend espía; carga del índice; finding con forma de GO02; error de clave inválida; pytest verde en el host indicado; disposiciones en reviews/rN.md sin ambigüedad abierta.

FUTURO
El operador del desk promueve los hijos con add task --from-drawer y preflight; el dueño/host fija dónde corre pytest; revisores en frío aceptan GO02 y GO03; el hash del commit 1 fija G_BOUNDARY. GO04 y GO05 consumirán costura y firma.
