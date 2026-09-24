---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: setup
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-09-23T13:03:22'
# open | closed
status: open
# project identity that acknowledged the note
acknowledged_by: ⸢rev•acknowledged_by⸥
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: ⸢rev•acknowledged_at⸥
---

# Documentar el patron de modelo repo-local, cerrar el reporte de hash_b y definir la familia de modelos de evidencia

_Describe the incoming message with enough evidence to triage._

Tres puntos, en orden de costo creciente. El (2) ya esta resuelto en el codigo y solo
necesita cierre formal; el (1) es documentacion; el (3) es una consulta de diseno que
bloquea trabajo en deskops.

## 1. El patron de modelo repo-local no esta documentado en ninguna parte de sldb

`.pi/skills/use-sldb/SKILL.md`, bloque "Common commands" (lineas 42-76): de los 29
ejemplos, 12 referencian `AtomDoc` (lineas 49-57 y 70-72) y 4 usan el model_ref completo
`deskops.models:AtomDoc` (lineas 49, 70, 71, 72). **Ningun ejemplo muestra un model_ref de
otro repo.** El efecto de lectura es que los modelos viven en deskops y que registrar uno
propio no es una operacion soportada.

El patron real, funcionando hoy en /home/jp/setup:

- Declaracion: `external-resources/models.py` -> `class ExternalResourceDoc(StructuredNLDoc)`.
- Registro: `sldb models add external-resources.models:ExternalResourceDoc --store .sldb --pythonpath .`
- Resultado en `.sldb/core/models/ExternalResourceDoc.yaml`:
  `model_ref: external-resources.models:ExternalResourceDoc`,
  `path: external-resources/models.py` (relativo), `documents_count: 26`, `hash_b` poblado.
- **setup no tiene `pyproject.toml`**: no es paquete Python ni es pip-installable. La
  resolucion ocurre por `--pythonpath .`, que cumple el rol que en un repo empaquetado
  cumplirian `pip install -e` + entry points. El store guarda la referencia y un path
  memoizado, nunca el codigo.

Hoy esto solo existe como conocimiento tacito en el store y en tres atoms locales de setup
(`atom-any-repo-can-declare-structured-doc-models`, `atom-model-ref-resolves-via-pythonpath-not-packaging`,
`atom-models-live-where-their-content-lives`). En el repo sldb no hay nada: `README.md:228`
menciona "repo-local skill file" y `docs/requests/sldb-postulator-integration-guide.md:19`
menciona "repo-local `.sldb/`", pero ninguno cubre el model_ref repo-local.

Sugerencia: un ejemplo no-deskops en el bloque "Common commands" (basta cambiar uno de los
cuatro model_refs), mas un parrafo corto que diga las tres cosas que hoy hay que descubrir
sola: (a) el modelo se declara en el repo dueno del contenido, no en el repo de la
herramienta; (b) `--pythonpath` es el mecanismo de resolucion, no el packaging; (c) un repo
sin `pyproject.toml` puede registrar modelos.

## 2. `hash_b` vacio al registrar un modelo con cero documentos: YA CORREGIDO, cerrar el reporte

Reporte original, en el feature doc de deskops
(`desk/drawer/features/feature-herdr-supervised-execution-runtime.md`, linea 22, seccion
`### RunDoc` en linea 113): registrar un modelo con cero documentos trackeados dejaba
`hash_b: ''` en `.sldb/core/models/<Name>.yaml` en vez del hash de un indice vacio, y
`sldb stores check` FALLABA hasta correr `sldb models update <Name>` una vez.

**Verificado contra el HEAD actual: no se reproduce.** Sandbox en `/home/jp/setup/.tmp/gap2-repro`,
modelo `gap2repro.models:VoidDoc` sin documentos:

```
sldb stores init --path .
sldb models add gap2repro.models:VoidDoc --store .sldb --pythonpath .   # Registered 'VoidDoc'
cat .sldb/core/models/VoidDoc.yaml
#   hash_b: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
#   documents_count: 0
sldb stores check --store .sldb                                         # PASS: store integrity
sldb models update VoidDoc --store .sldb --pythonpath .                 # no-op, hash_b identico
```

Ese hash es `sha256("[]")`, es decir `hash_documents_index(DocumentsIndex())`. El fix esta en
`src/sldb/cli/commands/model_add.py`, `_create_models_index` (lineas ~54-64), con un
comentario que describe el fallo exacto ("...until someone happens to run `models update`
once... it is not the empty string"); `git blame` lo atribuye a **1b04515e** (2026-09-15).
La regresion esta cubierta en `tests/store/test_cli_store.py:298`
(`assert models_idx.hash_b == hash_documents_index(DocumentsIndex())`) y el caso queda
explicado en el docstring de `test_store_check_json_format` (linea ~157).

Accion pedida: solo cierre formal. Si el CHANGELOG no lo menciona, agregarlo, porque el
reporte sigue vivo en el drawer de deskops y alguien lo va a volver a levantar.

## 3. Consulta de diseno: familia de modelos de evidencia

Contexto: deskops va a necesitar un tipo de documento de evidencia ejecutable (un
`ProofDoc`: comando, `exit_code`, `duration_ms`, hash de salida, `head_sha`) para que sus
condiciones dejen de evaluar campos auto-reportados. Ya existen dos vecinos: `RunDoc`
(`deskops/models/run.py`, definido y registrado pero sin escritor todavia) y el par
`TestDoc`/`StressTestDoc` disenado en el analisis de setup.

Antes de crear tres modelos de evidencia sueltos, la pregunta para sldb es de convencion:

- ¿`base_models` + herencia Python es el mecanismo recomendado para una jerarquia de
  evidencia, o conviene `family` (como usa pron con `knowledge` / `relation`)? deskops hoy
  tiene `family: null` en todos sus modelos.
- ¿Hay costo en el store al tener un modelo base abstracto registrado con cero documentos?
  (relacionado con el punto 2: ese es exactamente el flujo de registro vacio).
- ¿Recomendacion para campos de evidencia hasheada, dado que `hash_c`/`hash_b` ya son
  conceptos del store y reusar el nombre en un payload puede confundir?

No es bloqueante para sldb, pero si lo es para deskops: definir la jerarquia una vez sale
mas barato que crear `ProofDoc`, `RunDoc` y `TestDoc` por separado y unificarlos despues.

## Por que esta nota llego como archivo y no por `deskops inbox`

El intake cross-repo esta roto en ambos extremos. Comandos ejecutados desde `/home/jp/setup`
el 2026-09-23:

- `deskops inbox list --root /home/jp/setup` -> exit 0, pero **no lista**: interpreta `list`
  como el mensaje posicional (el flag real es `--list`) y entrega una nota basura de setup a
  si mismo: `Delivered inbox note from setup to setup at /home/jp/setup/desk/inbox/20260923-115256-unclear-list.md`
  + `Tracked '20260923-115256-unclear-list'`.
- `deskops inbox list --root /home/jp/proyectos/hum-ecosystem/tools/deskops` -> exit 1:
  `Error: Repository id 'deskops' not found in registry at '/home/jp/setup/desk/registry'. Supported path: run 'deskops repo register <name> --path <abs>' or add an entry to the ecosystem registry.`

Causa: `resolve_canonical_project_identity` valida la identidad del repo destino contra el
registro del ecosistema derivado del store del **CWD** (`find_local_store()` ->
`/home/jp/setup/.sldb` -> `/home/jp/setup/desk/registry`), no contra `--root`. En ese
registro no estan `sldb`, `deskops`, `spec2viz` ni `kgdb`: solo `hum-ecosystem` como
monorepo. Por lo tanto `deskops inbox ... --repo sldb` tampoco habria funcionado.

Cuando el intake funcione, el envio equivalente es:

```
deskops repo register sldb --path /home/jp/proyectos/hum-ecosystem/tools/sldb
deskops inbox "<cuerpo>" --repo sldb --kind suggestion \
  --title "Documentar el patron de modelo repo-local, cerrar el reporte de hash_b y definir la familia de modelos de evidencia"
```

Este archivo queda sin trackear en el store, igual que las dos notas agregadas en 258c1be.
