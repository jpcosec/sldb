# REFORMULACION

**Propósito:** que un merge o rebase de dos ramas que tocaron `.sldb` termine sin intervención, regenerando índices derivados en vez de marcar conflicto.

**Resultado:** (1) `sldb stores rebuild-index` que reconstruye `store_index.yaml` y `models/*.yaml` desde los shards ignorando los índices ilegibles; (2) `sldb stores merge-driver %O %A %B %P` que conserva `%A` para índices derivados, une `include` de `.sldb/store.yaml` y sale 1 para el resto; (3) `--install` idempotente en `.gitattributes`/`.git/config`; (4) error exacto en `load_store_index`/`load_models_index` ante marcadores `<<<<<<<`; (5) aviso en `stores init`; (6) AGENTS.md, docs y help; (7) tests y CHANGELOG; (8) nota a mepu.

**Repo:** sldb (`src/sldb/store`, `api/stores`, `cli`, `tests/store`, `docs`, `CHANGELOG.md`).

**Límites:** fuera H1, H3, H4; no cambiar qué se versiona; `stores build` no reemplaza a `rebuild-index`.

# AMBIGUEDADES

1. "sin leer los índices derivados actuales (los ignora si tienen marcadores o no parsean)" frente a "desde los shards […] y el contrato de cada modelo": no dice de dónde enumerar los modelos si no se leen `models/*.yaml`; obligaría a inventar la fuente (¿`store.yaml`? ¿directorio?).
2. "avisa con una alerta si `git ls-tree` de otra rama local del mismo repo ya tiene .sldb/store.yaml": no dice qué rama(s) ni cómo elegirlas; obligaría a inventar el criterio.
3. "deja en %A la versión de la rama actual" para `models/*.yaml`: a diferencia de `store.yaml`, no aclara si ese archivo debe unirse o solo conservarse; obligaría a asumir el contrato exacto del driver.
4. `pills: []` y `depends_on: []` con `current_node: ritual-execution`: el ritual exige pills ligadas y pre-gate; obligaría a inventar qué conocimiento las cubre.

# DRY-RUN

**Lecturas:** `store/io/__init__.py`, `api/stores/update_store_indexes.py`, `cli/parsers/stores.py`, comandos de stores, `documents_hash`, `hashing`, `ops`, `store.yaml`, tests nombrados.

**Cambios:** módulos nuevos en `api/stores/` (rebuild y merge-driver), subparsers, error en las cargas, aviso en init, escritura de `.gitattributes`/`.git/config`, AGENTS.md, docs, tests, CHANGELOG.

**Dependencias:** funciones de hash existentes, formato de `include` en `store.yaml`, git.

**Validaciones futuras:** los tres `pytest`, prueba manual en `/dev/shm` (con y sin driver), `stores check` verde, `--help`.

# FUTURO

Responder la nota a mepu, commit de cierre y closeout; si persiste la ambigüedad 2, un humano decide el alcance del aviso en `init`.
