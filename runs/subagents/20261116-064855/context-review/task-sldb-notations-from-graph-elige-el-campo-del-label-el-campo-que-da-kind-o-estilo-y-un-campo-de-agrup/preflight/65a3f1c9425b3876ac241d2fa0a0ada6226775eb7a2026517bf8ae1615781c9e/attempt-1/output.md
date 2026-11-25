REFORMULACION
Propósito: que `sldb notations from-graph` permita elegir qué campo del payload da el label, cuál da el kind y cuál agrupa nodos. Resultado: flags `--label-field`, `--kind-field` y `--group-field` en parser, comando y función de API que compila grafo a spec; tests y CHANGELOG. Repo: SLDB_1 (`/mnt/ssd/proyectos/SLDB_1`), archivos `src/sldb/cli/...` y `tests/notations/...`. Límites: sin estilos/paletas nuevas; `--snapshot` sin payload sigue usando id/modelo; sin flags la salida no cambia; el ejecutor no hace push; el commit lo hace el coordinador; entrada en CHANGELOG bajo `## 0.1.13 — not released yet`.

AMBIGUEDADES
1. “los nodos con el mismo valor de agrupación quedan dentro de un nodo contenedor con aristas contains”: no define id, label, kind, orden del contenedor ni qué hacer con valor de agrupación ausente; obligaría a inventar esa convención.
2. “deskops message send --to <repo>” / “Aviso a <repo>: ...”: no identifica el repo destinatario; obligaría a inventar cuál es.
3. “la función de API que compila el grafo a spec (localizarla desde notations_from_graph.py)”: no nombra la función ni aclara si es API pública o helper interno; obligaría a inferir el límite de la superficie.
4. “un store en tmp_path con dos RepositoryDoc-like (title y tags system:a / system:b)”: no fija el modelo ni el payload mínimo; obligaría a inventar la fixture si los helpers existentes no cubren ese caso.

DRY-RUN
Lecturas: TaskDoc, `notations_from_graph.py`, `parsers/notations.py`, test CLI nombrado, test de component spec y CHANGELOG. Cambios previstos: añadir flags y filtros; aplicar label/kind/group al construir nodos; crear contenedores con `contains`; tests de label/kind, agrupación y golden sin flags; línea de CHANGELOG. Dependencias: compilador de grafo a spec, helpers de test o `sldb.api`, pytest y deskops para aviso. Validaciones futuras: los dos comandos pytest indicados, comprobación del golden sin flags y revisión del informe en `result-summary.md`. Sin ejecutar nada.

FUTURO
El ejecutor produce cambios, tests, CHANGELOG e informe. El coordinador hace `deskops closeout commit` sin push. El aviso al repo lo emite el ejecutor o queda anotado en el informe si el repo no está registrado. La aceptación final y la decisión sobre el commit corresponden al humano/coordinador.
