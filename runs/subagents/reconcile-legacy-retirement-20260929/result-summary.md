# Reconciliación: tres tasks de retiro legacy ya ejecutadas, desk desincronizado

Run: reconcile-legacy-retirement-20260929
Estado: el código ya estaba borrado en `main`. El desk seguía diciendo `draft`.

## Qué se encontró

Auditando el manual de usuario surgió que tres tasks del board en `status: draft`
y `current_node: ...-execution-ready` ya tenían su trabajo hecho y commiteado:

| Task (estaba en `draft`) | Commit que la ejecutó |
|---|---|
| `task-retirar-core-ingest-isla-muerta-que-sostiene-el-ciclo-kgdb-sldb` | `d0df139` |
| `task-retirar-cli-graph-y-cli-graph-old-copias-fosiles-de-un-refactor-interrumpido` | `6389d55` |
| `task-retirar-modulos-sueltos-sin-importadores` | `e17abfe`, `32ba946`, `5561534`, `d524b01`, `10dc5c1` |

La tercera se ejecutó como cinco commits, uno por módulo, coincidiendo con su
Implementation Path ("Uno por uno: censo AST de importadores, borrar, correr suite").

## Verificación hecha antes de tocar nada

Censo AST sobre `src/` contando `ast.Import` e `ast.ImportFrom` por módulo, no grep:

```
sldb.core.ingest                     exact=0 submodules=0
sldb.cli.graph                       exact=0 submodules=0
sldb.cli.graph_old                   exact=0 submodules=0
sldb.cli.commands.doc_helpers        exact=0 submodules=0
sldb.cli.commands.predicates_format  exact=0 submodules=0
sldb.cli.commands.model_update       exact=0 submodules=0
sldb.cli.commands.model_source       exact=0 submodules=0
sldb.cli.federated_utils             exact=0 submodules=0
```

El censo AST era necesario: un `grep -c import` previo dio 20 falsos positivos para
`cli/graph` (matcheaba `cli.graph_ops`) y 15 para `commands/model_source`
(matcheaba `api.model_drafts.model_source`, que es el módulo VIVO al que migraron
los consumidores). Ambas tasks lo advertían — `graph_ops` es el árbol que ganó,
`api/model_drafts/source_location.py` es el destino de la migración — y ambos
falsos positivos habrían hecho parecer que el borrado rompía importadores.

## Qué se hizo en este run

Residuo físico: `src/sldb/core/ingest/` y `src/sldb/cli/graph_old/` seguían
existiendo como directorios con solo `__pycache__` adentro. Se borraron.

No se borró código fuente: ya no quedaba ninguno.

## Validación

- `PYTHONPATH=src python -m pytest -q` → **1077 passed**, 0 failed (`validation.log`).
- Misma cuenta que el último closeout (`83efddc`): el residuo no sostenía ningún test.

## Hallazgo de proceso

Este es el tercer caso de desincronización desk↔repo encontrado en la misma sesión:

1. `docs/user-manual.md` §13/§14 describen tres limitaciones ya resueltas
   (`ast show` ya no ensucia stdout; `__containment__`/`__references__` sí generan
   aristas vía `declared_references.py`; `Corpus` sí se exporta en `sldb.api`).
2. `task-expand-sldb-composition-modes` está en `current_node: completed` mientras
   `docs/composition_modes.md:42` dice que su scope "were proposals. They are not
   advertised as supported operations in this checkout."
3. Estas tres tasks en `draft` con el código ya borrado.

El patrón: el trabajo se hace, el commit se escribe, el estado del desk no se mueve.
Lo mismo que el closeout anterior registró como desviación de proceso
("la implementación se hizo en la sesión principal, sin despachar Executor/Tester").

Corregir los tres estados no arregla la causa. Hace falta un chequeo que falle
cuando el desk afirma algo que el repo contradice.
