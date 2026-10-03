# A corte

## Veredicto

**PRESENTE SIN MECANISMO.**

El corte existe como **señal** (CI en rojo) pero no como **interrupción**: nada
impide que un commit defectuoso ya esté en `main`. Ese es el hallazgo central.

Evidencia:

- `.github/workflows/ci.yml:3-5` — corre `on: push` **y** `on: pull_request`.
  Con push directo a main, el CI falla EN ROJO **después** de que el commit ya
  entró. Eso es un aviso posterior, no un corte.
- No hay protección de rama verificable en el repo: no existe `CODEOWNERS`
  (`find . -name CODEOWNERS` → vacío), no hay archivos de rulesets/settings en
  `.github/` (solo `workflows/`, `ls .github/` lo confirma). El historial
  confirma el flujo observado: los últimos 8 commits de `main` en first-parent
  (`git log --oneline --first-parent main`) son commits directos, no merges de PR.
- Sin pre-commit, confirmado: no hay `.pre-commit-config.yaml`, `git config
  core.hooksPath` no está fijado (exit 1), `.git/hooks/` solo tiene samples.
  Consecuencia: **nada corre ANTES de un commit local**. Un commit roto se
  descubre en el push, o nunca. El autor puede acumular N commits rotos locales
  y detectarlos en bloque, cuando ya son difíciles de separar.
- `propuesta/evidencia/gobernanza.json`: `pre_commit_existe: false`,
  `linter_configurado: false`.
- standards.md:3 declara «Compliance with these rules is mandatory for all
  contributions» y standards.md (sección *Toolchain Configuration*) afirma que
  «the project uses ruff, mypy, docstring-coverage for enforcement». Falso:
  `pyproject.toml` no tiene `[tool.ruff]` ni `[tool.mypy]`, y el CI no ejecuta
  ninguno. Los caches `.mypy_cache/` (May 15) y `.ruff_cache/` (May 4) son
  fósiles de que el autor corrió esas herramientas **a mano, alguna vez** —
  exactamente el patrón «la función se cumple por atención humana y nadie lo
  declaró».

Las tres puertas del CI sí **rechazan** dentro del workflow (pytest con exit
code, `selfdoc check`, `python -m build`). Pero rechazar dentro de un workflow
post-push solo bloquea si hay protección de rama detrás. Sin ella, el rechazo
no recupera el estado del repositorio: ya entró.

## Las puertas que existen

| puerta | qué rechaza | qué deja pasar | corta o avisa |
|---|---|---|---|
| `pytest` (ci.yml:25, matrix 3.10–3.13) | código que falla los 1.207 tests | todo lo que los tests no cubren (semántica, rendimiento, stores legacy) | corta el workflow; **avisa** respecto a `main` (sin protección de rama, el commit ya entró) |
| `python -m sldb selfdoc check` (ci.yml:27-28, solo Python 3.13) | deriva entre la referencia CLI autogenerada y el código | todo lo demás; y en 3.10–3.12 no corre siquiera como aviso | igual: corta workflow, avisa respecto a main |
| `python -m build` (ci.yml:30) | paquete que no se construye | código instalable pero roto en ejecución | igual |
| hooks locales de git | **no existen** — nada corre antes del commit | absolutamente todo | ausente |
| linter / type check (ruff, mypy) | **no existe** pese a standards.md declararlo como «enforcement» | `except Exception` pelado (≥12 sitios sin `noqa`: `core/handlers/yaml.py:65`, `core/renderer_engine/python_expr.py:19`, `cli/commands/models_validate.py:36`, `cli/commands/lint.py:60`, `cli/serve/sections_routes.py:49`, `cli/serve/segments_routes.py:39`…), archivos de 138 líneas contra la regla de 100 (standards.md:15) | ausente |
| protección de rama / CODEOWNERS | **no existen** (no hay evidencia en el repo; pushes directos a main observados) | commits directos a main sin revisión ni gating | ausente |
| standards.md | declara reglas «mandatory» (capa 0–4) | todo: nadie recorre el conjunto y rechaza | aspiracional |

## Patología

La que el BUNDLE predice para A ausente-como-interrupción: **un daño en curso
espera a que alguien lo discuta**. Caso concreto ya consumado: los 5 ciclos
entre paquetes y los 91 imports dentro de funciones conviven con tests verdes y
CI verde — pasaron por todas las puertas existentes. La única cosa que los
detectó fue una auditoría manual (`docs/architecture/superseded-code-audit.md`),
hecha una vez, sin mecanismo que impida que el número vuelva a crecer. El daño
no está en curso porque alguien lo cortó: está en curso porque nadie puede
cortarlo, y el último corte fue humano.

Segunda patología, más engañosa: la puerta existe y funciona, así que **quien
construye encima cree estar protegido**. Pero la garantía real del CI es «el
workflow va a ponerse rojo», no «main va a quedar limpio». La diferencia entre
ambas frases es exactamente la protección de rama ausente.

---

# Salud prestada

## Cifras

- **Autores**: 3 cadenas de autor, 1 persona. `jp_ruiz <juanpablo.ruiz.r@gmail.com>`
  311 commits; `c <a@b>` 5 commits; `jp <jp@local>` 1 commit. Los emails `a@b`
  y `jp@local` son configs desechables, y sus fechas se intercalan con las de
  jp_ruiz en los mismos días de septiembre 2026. Lectura con evidencia: **una
  sola persona escribe el 100% del código**.
- **Commits**: 317 totales (`git log --oneline | wc -l`).
- **Ritmo** (commits por mes): 2026-04: 11 · 05: 23 · 06: 14 · 07: 2 · 08: 38 ·
  **09: 224** · 10: 5. Septiembre concentra el **71% de todo el historial** en
  un mes. El sistema no tiene ritmo sostenido: tiene un sprint reciente de una
  persona. Todo lo que existe fue pensado hace semanas, por la misma cabeza, y
  nunca fue sostenido por nadie más.

## Conocimiento sin respaldo

| decisión | donde vive | donde debería vivir |
|---|---|---|
| import tardío para que `sldb.store` nunca cargue `sldb.api` (rompe un ciclo de paquetes en el punto exacto) | comentario: `src/sldb/store/edge_index/model_contribution.py:41` | en una regla de dependencias con mecanismo (mapa de aristas rechazado en CI); hoy ni standards.md ni specs lo enuncian |
| «PLAN 15 capa 5»: shards por documento en sections/semantic, con fallback de lectura legacy que la migración elimina | comentarios: `src/sldb/store/io/__init__.py:117`, `src/sldb/store/io/sections_index.py:8-12` (citado en `docs/architecture/superseded-code-audit.md` fila 13, un doc de auditoría histórica, no una spec viva) | en el spec del store con su plan de migración y estado actual |
| carrera de descriptores bajo concurrencia (el SO recicla el número de fd; el cleanup no debe cerrar dos veces) | comentario: `src/sldb/store/io/utils.py:45,65` | en la spec de IO del store o en un test que fije el contrato |
| tolerancia a stores escritos antes de `field_hashes`: «absent is unknown, never no-fields» | comentarios: `src/sldb/store/query_engine/models.py:25`, `src/sldb/store/models/document_entry.py:13` | en el contrato del store (`sldb_store_cascade.spec.yaml` existe pero no cubre esto verificado) |
| aliases deprecados (`cascade_hash_a`, `hash_b_of`) que alguien aún consume | comentarios: `src/sldb/store/ops.py:71`, `src/sldb/store/documents_hash.py:102` | en el CHANGELOG con fecha de retiro, y un mecanismo que rechace su uso nuevo |
| re-export por compatibilidad: el contrato de datos se movió a `sldb.api` | comentario: `src/sldb/cli/serve/routes.py:8` | en la spec de límites api/cli; hoy ni `sldb_architecture.spec.yaml` describe `api` (gobernanza.json: 6 nodos declarados no existen y 10 paquetes reales no se declaran) |

Patrón transversal: el conocimiento está en **comentarios y en la cabeza**, no
en el modelo. Los comentarios son de alta calidad (explican *por qué*), pero un
comentario no es consultable por un mecanismo: el día que alguien refactoriza
`model_contribution.py` y «limpia» el import tardío, el ciclo vuelve y **nada lo
rechaza**.

## Pronostico

Las cifras que sostienen todo lo que sigue: **224 de 317 commits (71%) son de
septiembre 2026**, escritos por **una sola persona real** (`jp_ruiz`; los otros
dos strings de autor son configs desechables de la misma persona), y **4
decisiones de arquitectura viven solo en comentarios de codigo** (tabla
anterior: import tardio, PLAN 15 capa 5, carrera de descriptores, tolerancia a
stores pre-`field_hashes`). El conocimiento del sistema entero cabe en una
cabeza y en 6 comentarios.

### 1 semana sin su autor

**Que se degrada primero: la capacidad de decidir, no la de ejecutar.** Los
1.207 tests siguen verdes y el CI corre solo. Pero cualquier cambio en el store
exige saber que firma cada hash (`source_hash`/`content_hash`/`field_hashes`,
nombres semanticos — los commits `bbae77c`, `5d76539` y `15e3c38` de septiembre
son ese conocimiento condensado, 71% del historial en un mes, todo del mismo
autor). Un reemplazo que toque `store/edge_index/model_contribution.py` y
«limpie» el import tardio del comentario en la linea 41 restaura el ciclo
store→api: pytest lo deja pasar, `selfdoc check` no mide imports, y nadie puede
explicarle por que esa linea es sagrada — la explicacion esta en la cabeza que
se fue.

### 1 mes sin su autor

**Que se degrada primero: el contrato del store.** Es el codigo mas reciente
(backfill de `field_hashes` y migracion de layout legacy, commits `15e3c38` y
`a4d6325`), el mas delicado, y su conocimiento vive solo en comentarios:
`store/io/__init__.py:117` («PLAN 15 capa 5»), `store/io/sections_index.py:8-12`
(fallback de lectura legacy), `store/io/utils.py:45,65` (carrera de
descriptores: el SO recicla el numero de fd bajo concurrencia). Un reemplazo
que migre un store sin conocer PLAN 15 capa 5 borra el fallback de lectura y
deja **stores de usuarios existentes ilegibles** — no hay test que lo tape
porque el caso depende de datos escritos antes de la migracion, y quien lo
tope no podra arreglarlo: la razon por la que el fallback existe esta en un
comentario, no en ninguna spec ni en `sldb_store_cascade.spec.yaml`. Ademas,
standards.md se declara obsoleto a si mismo («Historical assessment, not a
current audit»): con el autor fuera, nadie sabe que parte miente.

### 6 meses sin su autor

**Que se degrada primero: la navegabilidad, y es danio ya medible hoy.** 5
ciclos entre paquetes, 91 imports dentro de funciones, 12+ `except Exception`
pelados, archivos de 138 lineas contra la regla de 100 de standards.md — todo
paso por el CI verde, porque ninguna puerta lo rechaza. Y la spec de
arquitectura declara 6 nodos que no existen y omite los 10 paquetes reales
(gobernanza.json): sin el autor, **nadie sabe que esa spec miente**, y cualquier
persona nueva que navegue por `sldb_architecture.spec.yaml` aterriza en una
arquitectura fantasma. El sistema seguira *funcionando* (tests + CI como
congelador del comportamiento) y dejara de ser *modificable con confianza*:
cada cambio sera una excavacion arqueologica de 6 comentarios escritos por una
persona. Ese es el pronostico: **no colapso, sino congelacion** — el punto
donde nadie fuera del autor se atreve a tocar el store, y el proyecto queda
vivo pero parado.
