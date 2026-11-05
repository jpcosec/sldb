REFORMULACION
PK01 "Fundamentos" es un agregado de planificación (`node_role: aggregate`, no ejecutable; termina cuando terminan sus hijos) que deja escritas las bases del plan grafo-operable antes de alterar el store: (1) frontera sldb/deskops commiteada, (2) semántica, gramática y firma de evaluación del lenguaje de reglas, (3) costura `GraphBackend` con networkx. Repo dueño: sldb; única escritura fuera permitida: `deskops/desk/inbox` vía `deskops message send` (D3). Límites: no cambia la salida observable de comandos existentes sobre stores existentes (goldens idénticos); una clave nueva en `store.yaml` con validación propia es comportamiento nuevo admitido; sin auth ni motores externos. Aceptación: G_BOUNDARY, G_SEMANTICS y G_SEAM satisfechos.

AMBIGUEDADES
ninguna.

DRY-RUN (hipotético, sin ejecutar)
Orden GO01 → GO02 → GO03 (aristas `depends_on`; GO02 y GO03 requieren G_BOUNDARY).
- GO01: lee la pill ya editada y D1; produce commit 1 (pill + atom enlazado vía `where`/`how`) y commit 2 (`gates.G_BOUNDARY` satisfied con hash del commit 1), más nota a inbox de deskops. Transfiere: frontera commiteada y G_BOUNDARY.
- GO02: con G_BOUNDARY satisfecho, escribe `docs/architecture/rules-language.md` (gramática, caminos `campo`/`rel:tipo`/`^`, clausura `+`, trivaluada de Kleene, `__contract__`, explicación, firma `eval(predicado, sujeto) → findings` con `node, holds, clause, seen`), tabla de equivalencias y tests de spec `xfail` (no skipped). Transfiere: G_SEMANTICS y la firma que GO03 implementa.
- GO03: con GO02 hecho, define `GraphBackend` (`load`, `eval`) y lo implementa sobre networkx; enruta los seis comandos graph y `api/graph`; añade `graph_backend` a `store.yaml`; `eval` solo de un documento (sin caminos); goldens idénticos; docs y CHANGELOG. Transfiere: G_SEAM.
- Validación conjunta: tres gates satisfied; goldens de los seis comandos idénticos; tests de `api/graph` sin cambios; test con backend espía; carga del índice del repo; `eval has(id)` devuelve finding con forma de GO02; `store.yaml` sin clave = networkx, valor inválido falla listando `["networkx"]`; spec `xfail`, no skipped.

FUTURO
GO04 produce la proyección de payloads; GO05 produce caminos y evaluación consumiendo firma y G_SEAM; quien opera el desk de sldb acepta la revisión en frío y escribe disposición en `reviews/rN.md` (D3); deskops produce G_CONSUMER en su propio plan; la promoción se hace con `deskops add task --from-drawer` y preflight TaskDoc-only; pytest corre en robocop2.
