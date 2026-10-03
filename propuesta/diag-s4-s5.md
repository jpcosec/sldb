# S4 anticipacion

## Veredicto

**PRESENTE SIN MECANISMO.** Hay anticipación real hecha a mano (política de deprecación
escrita, aliases de hash mantenidos por compatibilidad, una puerta de frescura de docs en
CI), pero no existe ningún mecanismo que sostenga la promesa central — qué parte de la
superficie pública es estable — y una promesa de compatibilidad ya se evaporó sin que
nada lo detectara.

## Evidencia

- **No hay contrato de versión vivo.** `pyproject.toml:3` declara `version = "0.1.0"`.
  `CHANGELOG.md:3` lo desdice por escrito: las entradas son "historical development
  records, not a verified registry release inventory" y "No new package version or
  release is created". No hay regla de semver, no hay changelog que comprometa.
- **El freeze es una nota, no un estado.** `README.md:1` congela v1 (2026-09-07) y
  autoriza solo "the explicitly authorized self-documentation slice". El log de main
  muestra trabajo muy por encima de ese corte hasta 2026-10-01: servidor HTTP (`serve`
  con rutas de edges, corpus, auth), features de grafo (`39f1a57`), migraciones de store
  (`a4d6325`). Tres semanas y media de features sobre un sistema "frozen", sin bump de
  versión ni respuesta contractual.
- **La promesa de deprecación se apagó en silencio.** `README.md:97` promete que los
  alias singulares "emit deprecation warnings" y que `SLDB_SUPPRESS_DEPRECATION=1` los
  suprime. En `src/` no existe ningún lector de esa variable y ningún emisor de
  warnings de deprecación (`grep -rni DEPRECATION src/` no devuelve código; solo el
  texto de ayuda en `src/sldb/cli/help_texts_other2.py:54`). El único lector vivo está
  en el artefacto rancio `build/lib/sldb/cli/main.py:29` (directorio ignorado por git).
  `tests/conftest.py:5` todavía setea la variable para un mecanismo que ya no existe.
  Los alias hoy se resuelven callados: `src/sldb/cli/dispatcher.py:72-76` redirige
  `store`/`model`/`doc`/`ls`/`get` a legacy sin aviso.
- **Compatibilidad cuidada a mano, sin contrato.** `src/sldb/store/documents_hash.py:102`
  (`hash_b_of = roster_hash_of  # deprecated alias`) y `src/sldb/store/ops.py:71`
  mantienen aliases viejos "so versioned KBs keep loading" (`README.md:332`). Es
  anticipación real, pero sostenida por atención del autor: nada marca cuánto tiempo
  viven esos aliases ni qué pasa al retirarlos.
- **Sin niveles de estabilidad.** `grep 'deprecat|breaking|stable|experimental' src/`
  solo devuelve usos incidentales ("stable order", "stable IDs"). Ningún símbolo público
  está marcado estable/experimental. Para el consumidor, los ~800 nombres públicos
  (store 336 + api 253 + cli 234) son todos igual de comprometidos o igual de frágiles.
- **La única puerta corriendo cubre otra cosa.** `gobernanza.json -> ci_pasos[2]`:
  `python -m sldb selfdoc check` en CI — recorre la superficie argparse completa y
  rechaza docs de CLI rancias. Es un mecanismo bloqueable real, pero de frescura
  documental, no de compatibilidad de API.
- **TASK-*.md: planes completados, nunca cerrados.** Ambos archivos describen trabajo
  YA ejecutado y mergeado: `TASK-store-generalize.md` (Codec + excepciones propias →
  existe `src/sldb/store/codec.py` y `src/sldb/store/exceptions.py`; commit `49b9d49`,
  merge `9502ad8`) y `TASK-sldb-serve.md` (existe `src/sldb/cli/commands/serve.py`,
  `src/sldb/cli/serve/` con ~30 módulos, y `tests/test_serve*.py`). Ambos quedaron
  versionados en la raíz (git ls-files: 1 c/u) citando líneas base muertas ("sldb 411",
  "sldb 414" frente a 1.207 pruebas actuales) y un worktree ajeno (`iso-lab/worktrees/
  sldb`). Son intención sin cierre: un lector nuevo no puede saber que ya pasaron.

## La superficie publica

Cifras de `superficie.json -> superficie_por_paquete`. La columna de cobertura es
conteo propio (AST, nombres públicos de módulo vs entradas `__all__` en todo el
paquete, `src/sldb` al 2026-10-03).

| paquete | defs publicas | declara __all__ | es diseno o residuo |
|---|---|---|---|
| store | 336 | sí | **Mezcla.** Núcleo diseñado (cascade Merkle, codec, facade, query) + residuo de compat sin contrato (`hash_b_of`, `cascade_hash_a`). El `__all__` cubre ~68 de ~354 nombres públicos medidos: la punta declarada y el mar de debajo. |
| api | 253 | sí | **Diseño amplio sin jerarquía.** `contracts/layers.toml` la declara "la frontera pública para quien integra", pero 253 defs sin marca de estabilidad: frontera sin tapiar. |
| cli | 234 | sí | **Residuo.** Es capa de transporte; su `__all__` cubre 2 entradas y los ~267 nombres públicos son clases de comando internas expuestas por accidente, no por diseño. |
| core | 67 | no | **Diseño** (excepciones, handlers, render engine), pero superficie implícita: sin `__all__`, nadie firmó qué es público. |
| selfdoc | 33 | no | **Diseño** — producto declarado en README (`selfdoc scan|sync|check`) y gate de CI. Sin `__all__`. |
| runtime | 12 | no | **Diseño** (config, validation) sin `__all__`; pequeño y coherente. |
| links | 7 | sí | **Diseño.** El único paquete chico con `__all__` completo (7/7 medidos). |
| models | 9 | sí | **Diseño.** Tipos base; `__all__` mínimo (2). |
| examples | 2 | no | **Diseño** — respalda `sldb example .`, declarado en README. |
| assets | 0 | no | Derivado sin código público. |
| templates | 0 | no | Derivado sin código público. |

Lectura: la superficie grande (store/api/cli) es en parte diseño y en parte todo lo
que quedó sin guion bajo. Nadie puede distinguir cuál es cuál, porque no hay marca
alguna de estabilidad y el `__all__` que sí existe no recorre el conjunto.

## Patologia

La de la columna "si falta S4": **el sistema reacciona, nunca prevé** — con un caso
demostrativo ya consumado. La promesa de deprecación (README + CHANGELOG 0.2.0: "old
singular commands emit deprecation warnings") existió como mecanismo, murió en una
refactorización, y nada la extrañó: el README sigue prometiéndola, `tests/conftest.py:5`
sigue configurándola, y el único rastro del mecanismo vive en un `build/` ignorado por
git. Eso es la forma exacta del daño: una anticipación que existía se degradó
sin señal, porque nada recorre el conjunto. Hoy el consumidor de store(336)/api(253)/
cli(234) no tiene forma de saber qué es promesa y qué es incidental; y si el autor se
va, hereda planes raíz (TASK-*.md) que parecen vigentes y están ejecutados, con
líneas base de pruebas que ya no existen.

# S5 clausura

## Veredicto

**PRESENTE SIN MECANISMO.** La identidad está declarada con contenido negativo real
(puede rechazar en principio) y existe una puerta de capas que obliga a decidir dónde
va un paquete nuevo — pero esa puerta está sin versionar y sin cablear a nada, y a
nivel de repositorio no hay mecanismo alguno: los sistemas ajenos ya están dentro,
versionados como si pertenecieran.

## Evidencia

- **Identidad declarada, con bordes.** `README.md:7-8`: biblioteca de extracción y
  mapeo Markdown↔Pydantic con store y CLI. `README.md:9` fija el borde negativo dentro
  del ecosistema: "it should not compete with `specyaml/` as the semantic
  source-of-truth contract". `README.md:11`: "The workflow-domain example layer now
  lives in the sibling `opsys` repo, not inside `sldb` itself" — el README SÍ sabe
  decir "esto no va acá". Es una identidad que podría rechazar una propuesta.
- **Una puerta existe y sabe rechazar.** `tools/check_layers.py` (docstring: rechaza
  import que cierra ciclo, import que sube de capa, y "un paquete sin capa asignada —
  para que agregar uno obligue a decidir dónde va"; implementado en
  `tools/check_layers.py:109`). Recorre todo `src/sldb/**/*.py`, incluidos imports
  diferidos. Es la pieza de clausura más honesta del repo.
- **Pero la puerta no está instalada.** `git status`: `contracts/layers.toml` y
  `tools/check_layers.py` están **sin trackear** (`??`). No aparecen en `.github/
  workflows/ci.yml` (pasos: pytest, selfdoc check, build), ni en pre-commit
  (`gobernanza.json: pre_commit_existe: false`), ni son invocados por tests o scripts
  (grep sin resultados). Un clone fresco ni siquiera tendría el contrato. Corre solo
  si alguien se acuerda: por la regla del marco, aspiracional.
- **La puerta misma declara su límite.** `contracts/layers.toml:77`: "mientras esta
  lista tenga entradas, el orden de capas es aspiracional, no bloqueable" — con 3
  excepciones vigentes (`core→store`, `store→api`, `selfdoc→cli`) y 5 ciclos pendientes
  R1–R5. Honestidad ejemplar; bloqueabilidad, ninguna.
- **El resto del repo no tiene puerta.** Los 11 paquetes de `src/sldb` son del sistema
  (incluidos `selfdoc`, `links` y `examples`: el primero es producto declarado en
  README y gate de CI, los otros dos respaldan federación y `sldb example`). El
  problema está en la raíz, donde conviven y se versionan árboles de otros sistemas
  (tabla abajo).

## Que pertenece y que no

Versionado = archivos bajo git (git ls-files; `git check-ignore desk kgdb knowledge
ledger runs surface contracts` → ninguno ignorado; solo `build` y `dist` lo están).

| directorio o paquete | versionado | pertenece a la identidad |
|---|---|---|
| `src/sldb` (11 paquetes) | sí (593 archivos) | **Sí** — el producto. |
| `tests`, `docs` | sí (87 / 116) | **Sí.** |
| `.sldb/` | sí (1.588; `runtime/` ignorado) | **Sí** — el store aplicado al propio repo (dogfooding). |
| `contracts/` | sí (9; `layers.toml` **sin trackear**) | **Parcial** — fixtures del handoff kgdb + el contrato de capas (que sería identidad y no está versionado). |
| `knowledge/` | sí (**1.368**) | **No** — es el proyecto sucesor; el propio README.md:1 dice que vive en `github.com/jpcosec/knowledge`. El repositorio sucesor está DENTRO del repo congelado. |
| `surface/` | sí (140) | **No** — app npm/Vite propia (`@sldb/surface`, `package.json`, `vite.config.ts`). Derivado real, pero ausente de la identidad del README: las únicas 3 menciones de "surface" en README.md:60,86,97 son la superficie de direcciones, no este frontend. |
| `desk/` | sí (149) | **No** — escritorio deskops con SPEC.md, METHODOLOGY.md, inbox, tasks propios: el harness de workflow, otro sistema. |
| `kgdb/` | sí (14) | **No** — documentación de `relation_types` de kgdb, otro sistema del ecosistema. |
| `sldb/` (raíz) | sí (1) | **Ambiguo** — `sldb/relation_types/composes.md` duplica el propósito de `kgdb/relation_types/`. Un directorio con el nombre del paquete, en la raíz, con un archivo. |
| `ledger/` | sí (37) | **No** — bitácoras `move-*.md` de movimientos de archivos. |
| `runs/` | sí (17) | **No** — salidas de subagentes (`runs/subagents/`). |
| `.serena/` | sí (6) | **No** — estado de una herramienta externa. |
| `build/`, `dist/` | **no** (ignorados) | Artefactos; correctamente fuera. |

## Patologia

La de la columna "si falta S5": **nadie puede decidir si algo pertenece** — y el repo
ya muestra la forma consumada del daño. El README enuncia bordes ("not inside sldb
itself", "should not compete") que nadie bloquea: junto a ellos viven versionados el
proyecto sucesor (1.368 archivos de `knowledge/`), el harness deskops (`desk/`), docs
de kgdb, un frontend npm, bitácoras de agente y estado de herramienta. La regla
"existencia como prueba" está invertida acá: el README declara un dentro y un fuera,
y el árbol de git dice otro. El único mecanismo que sabría rechazar (`check_layers.py`
+ `contracts/layers.toml`) no está versionado: la pieza que fijaría la clausura es
ella misma una pieza fuera del sistema. Si el autor se va, un contribuyente nuevo no
tiene forma de saber si agregar código a `knowledge/` o una vista a `surface/` es
trabajo de este repo o de otro.
