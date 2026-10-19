# Qué del store es fuente y qué se deriva

Estado (2026-10-19): frontera aprobada por el dueño. `stores declare` y `stores build`
están implementados y `.sldb/store.yaml` es la declaración de este store; sacar lo derivado
de git es el paso siguiente, después de reconstruirlo en un clon limpio con `stores check` en
PASS. Retoma la decisión del dueño del 2026-10-07 (nota del inbox 20261007-133032).

## 1. Medición (2026-10-19, este repo)

En git hay 2.816 archivos bajo `.sldb/` (2.781 entradas en `core/documents/`, 34 índices de
modelo en `core/models/` y `core/store_index.yaml`) y 2.648 bajo `knowledge/`. Un cambio de un
campo derivado reescribe miles: 66dac43b tocó 5.045 archivos por agregar un hash.

| Contenido | Archivos | De dónde sale |
|---|---|---|
| `knowledge/symbols/*.md` | 2.522 | AST y docstrings de `src/` (`selfdoc python-sync`). Ningún tag ni `architecture` escrito a mano; los 1.078 `purpose` son el primer párrafo de su docstring. |
| `knowledge/commands/*.md`, `knowledge/surfaces/*.md` | 101 + 25 | Mixto: la sinopsis y los argumentos salen del parser, pero 59 y 19 tienen `Purpose`/`How It Works` escritos a mano, que la regeneración preserva. |
| `.sldb/core/documents/<Model>/*.yaml` | 2.781 | Cada entrada une una declaración (este archivo se trackea con este modelo) con hashes calculados del archivo y del modelo. |
| `.sldb/core/models/*.yaml` | 34 | Hashes, roster y conteos, calculados de la clase y de los documentos. |
| `.sldb/core/store_index.yaml` | 1 | Declaraciones (modelos registrados con `model_ref` y `path`, `canonical`; links a otros stores; 15 predicados) mezcladas con valores calculados (`semantics`, `family`, `store_hash`). |

## 2. La frontera

**Fuente (queda en git):** los Markdown escritos o editados por personas y agentes (`docs/`,
`desk/`, `ledger/`, `sldb/relation_types/`, `knowledge/commands/`, `knowledge/surfaces/`), el
código y los modelos Python, y un archivo nuevo de declaraciones del store,
`.sldb/store.yaml`:

```yaml
models:            # lo que hoy se registra con models add
  - {name: TaskDoc, model_ref: deskops.models:TaskDoc, inherited_from: deskops}
  - {name: CliCommandDoc, model_ref: sldb.models.knowledge_surface:CliCommandDoc, path: src/sldb/models/cli_command_doc.py}
links: [{name: deskops, path: ../deskops/.sldb}]
predicates: [...]  # los 15 de hoy, tal cual
include:           # qué archivo se trackea con qué modelo
  - {model: PythonSymbolDoc, glob: "knowledge/symbols/*.md", generated_by: "selfdoc python-sync"}
  - {model: CliCommandDoc, glob: "knowledge/commands/*.md"}
  - {model: PillDoc, glob: "desk/contexts/pill-*.md"}
  - {model: DeskSpecDoc, path: desk/SPEC.md}
```

Las globs cubren las carpetas de un solo modelo; donde una carpeta mezcla modelos o tiene
archivos no trackeados (`docs/`, `docs/architecture/`, `desk/tasks/`, `desk/lifecycle/`) se
listan rutas.

**Derivado (sale de git):** `.sldb/core/documents/`, `.sldb/core/models/`,
`.sldb/core/store_index.yaml` y `knowledge/symbols/`. Su formato en disco no cambia: quien lee
`.sldb/` lee las mismas claves (`tests/store/test_export_contract_frozen.py`), después de
construirlo.

## 3. Reconstrucción

`sldb stores build` lee `.sldb/store.yaml`, registra los modelos y los links, corre
`selfdoc python-sync` para lo generado, trackea cada `include` y reconstruye los índices.
Es idempotente. En un clon limpio, `stores build` seguido de `stores check` tiene que dar
PASS. `stores build --check` construye una copia de los fuentes (lo que git versiona, sin lo derivado: `.sldb/core/`, `.sldb/runtime/` y lo que la declaración lista en `derived`) en un directorio temporal, con los stores enlazados alcanzables por symlink, y falla si la copia no pasa `stores check`, si algo trackeado no está declarado o si lo que trackea difiere del store local. `stores declare --write` escribe la declaración que el índice actual implica, para adoptar este layout. Una glob solo cubre una carpeta donde rastrearía exactamente lo trackeado, con nombres iguales al archivo, y nunca la raíz del proyecto.

El CI no commitea (ya no lo hace: los commits firmados `github-actions[bot]` salen de un
`~/.gitconfig` local). Pasa a correr `stores build --check` y falla si los fuentes no generan
lo esperado.

## 4. Lo que bloquea un clon limpio hoy

- 15 modelos (48 documentos del desk) se heredan del store de deskops por el link
  `../deskops/.sldb`. Un clon solo de sldb no los resuelve: el CI necesita deskops al lado,
  con la misma ruta relativa.
- 3 modelos de pron (AnchorDoc, ProjectionDoc, MoveDoc, con 37 documentos en `ledger/`): por
  decisión del dueño viven en el store de pron y sldb los hereda por `../pron/.sldb` (106ed3c0);
  `ledger/*.md` queda en sldb como fuente. pron no versiona su `.sldb/` y lo construye con su
  propio CLI (`make world`); por decisión del coordinador queda así, y el CI de sldb corre
  `make world` en el checkout hermano de pron antes de reconstruir el de sldb. Un generador de
  `store.yaml` solo corre subcomandos de sldb, a propósito: un store que ejecuta comandos
  arbitrarios es más superficie de la necesaria.

## 5. Los otros repos

deskops (225 archivos), spec2viz (23) y graph_ui (311) también versionan `.sldb/`. Cada uno necesita su
`.sldb/store.yaml`, el `.gitignore` de lo derivado y el `stores build --check` en su CI. sldb
migra primero.
