---
status: open
priority: p2
assigned_to: sldb-team
created: 2026-09-30
labels:
  - store-index
  - portability
  - model-registry
  - cross-repo
---

# `ModelEntry.path` filtra rutas absolutas de la máquina al repositorio

## Resumen

Cuando se registra un modelo cuyo archivo fuente vive **fuera** del repositorio del
store, SLDB escribe su ruta **absoluta** en `store_index.yaml`. Ese archivo se
versiona, así que la ruta local de quien corrió el comando queda en el repo y viaja
a todas las demás máquinas, donde no existe.

Medido en el repo `AgentsKBs`: **84 entradas con ruta absoluta**, de **dos máquinas
distintas** (`/home/jp` y `/home/user`), repartidas en las seis KBs.

| KB | rutas absolutas |
|---|---|
| `knowledge_antonia-cobranza` | 28 |
| `knowledge_ejemplo` | 28 |
| `knowledge_test` | 16 |
| `knowledge_psp` | 5 |
| `knowledge_vitali` | 5 |
| `knowledge_grifo` | 2 |

## Dónde pasa

`src/sldb/api/model_registry/model_index_writes.py:21`

```python
def relative_model_path(path: Path, root: Path) -> str:
    """Model source path relative to the project root when inside it, else absolute."""
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path.resolve())   # <- la ruta local entra al store
```

`Path.relative_to` solo resuelve cuando el archivo está **dentro** de `root`: no
genera rutas con `..`. Un modelo importado desde otro proyecto siempre cae en el
`except`.

Tres llamadores comparten el defecto:

- `api/model_registry/add_model.py:47` — registrar un modelo.
- `api/edges/relation_models.py:32` — registrar los modelos de aristas.
- `cli/commands/model.py:43` — la ruta equivalente del CLI.

## Cómo se reproduce

Basta registrar en un store un modelo que viva fuera del repo:

```bash
python -m sldb models add pron.models:AnchorDoc --store KB/.sldb --pythonpath .
grep "path:" KB/.sldb/core/store_index.yaml
#   path: /home/<quien-lo-corrio>/proyectos/pron/src/pron/models/anchor.py
```

Verificado: `Path('/a/b/c').relative_to('/a/x')` levanta `ValueError`; no existe
valor de `root` que haga a `relative_to` devolver un `..`.

En AgentsKBs esto ocurre sin que nadie lo pida: `python3 -m worlds mount MUNDO`
llama a `pron.world.world_init`, que registra `AnchorDoc`, `ProjectionDoc` y
`MoveDoc` — tres modelos que viven en el repo de pron, no en el de la KB.

Cadena completa:

```
worlds mount
  └─ pron.world_init.WorldInit.__call__
       └─ store.register_model("pron.models:AnchorDoc")
            └─ sldb.api.add_model
                 └─ relative_model_path  ← escribe la ruta absoluta
```

**pron nunca pasa un path.** Pasa un `model_ref`. Quien decide el formato de la
ruta es SLDB. El defecto es de SLDB; en pron y en `worlds mount` solo se ve el
síntoma.

## Por qué importa poco… y por qué igual importa

El dato decisivo: **`ModelEntry.path` no se usa para importar el modelo.** La
resolución va por `model_ref` + `pythonpath` (`model_registry/model_reference.py`),
que no mira `path` en ningún momento. Los consumidores son informativos:

- `models list` / `describe_model` — lo muestran.
- `federated_lookup.py:57` — único uso funcional, y lo resuelve contra el root del
  store **enlazado**, no contra el propio.

O sea: SLDB versiona en un archivo compartido un dato **no portable y casi no
consumido**. Nada se rompe hoy, pero:

1. El repo acumula rutas de máquinas ajenas; el diff de cada `mount` mezcla ruido
   de entorno con cambios reales y hace ilegible la revisión.
2. Es fuga de información del entorno (nombre de usuario, layout del disco) hacia
   un repositorio que puede ser compartido.
3. `federated_lookup` sugiere que el campo *aspira* a ser resoluble. Mientras
   pueda ser absoluto-de-otra-máquina, esa aspiración es falsa.

## Qué debería pasar

Una ruta que no se puede expresar relativa al root **no es un dato del store**.
Tres opciones, en orden de preferencia:

**A. `path: null` cuando el modelo es externo.** Honesto: el store declara que no
sabe dónde vive el archivo, y quien lo necesite lo resuelve por `model_ref` +
`pythonpath`, que es como ya funciona el import. Requiere `path: str | None` en
`ModelEntry`.

**B. Relativo con `..` vía `os.path.relpath`.** Genera `../../../proyectos/pron/...`.
Es el formato que ya tiene `knowledge_grifo` (escrito a mano o por una versión
anterior). Sigue siendo frágil: se rompe si el store se mueve de profundidad, y
asume que ambos repos están en la misma posición relativa en cada máquina.

**C. Dejar el absoluto pero no versionarlo.** Mover `path` a un índice derivado
fuera de `store_index.yaml`. El más invasivo.

Recomendación: **A**. Es la única que no miente.

## Alcance del arreglo

- `relative_model_path` y sus tres llamadores.
- `ModelEntry.path` a opcional si se elige A.
- Migración: los 84 valores ya versionados en AgentsKBs. Se limpian solos cuando
  `mount` vuelva a escribirlos, si el arreglo es idempotente.
- Consumidores a revisar: `models list`, `describe_model`, `federated_lookup`.

## Defecto derivado, en AgentsKBs

`worlds/mount.py` promete en su docstring:

> Normalizar el `store_index.yaml` — refs a `kb_models` y paths relativos, para que
> el store sea cargable desde donde esté clonado el repo.

`normalize_store_index` solo reescribe un mapa fijo de rutas legadas
(`LEGACY_PATHS`); no convierte los absolutos que SLDB acaba de escribir. Una vez
arreglado SLDB, conviene decidir si `mount` debe además sanear lo ya versionado o
si alcanza con que deje de generarse.

## Procedencia

Encontrado el 2026-09-30 moviendo el modelo `CompleteSystemPrompt` entre ramas de
AgentsKBs: `worlds mount antonia-cobranza` ensuciaba el árbol con entradas nuevas
de `AnchorDoc` y `MoveDoc` apuntando a `/home/jp/proyectos/pron/...`, mientras las
mismas entradas en `knowledge_grifo` eran relativas.
