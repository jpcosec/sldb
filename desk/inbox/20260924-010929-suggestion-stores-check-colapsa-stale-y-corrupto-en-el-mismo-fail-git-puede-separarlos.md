---
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: deskops
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-09-24T01:09:29'
# open | closed
status: open
# project identity that acknowledged the note
# ISO 8601 timestamp, set when acknowledged
---

# stores check colapsa stale y corrupto en el mismo FAIL: git puede separarlos

_Describe the incoming message with enough evidence to triage._

`sldb stores check` colapsa dos condiciones distintas en el mismo FAIL, y git tiene la informacion para separarlas.

## Lo que pasa

`stores check` devuelve una sola linea: `FAIL: store integrity`. Sin detalle, sin nombre del documento, sin decir que hash fallo.

En `src/sldb/api/stores/store_check.py:23` el veredicto es `{"ok": not summary["mismatched"], ...}`: cualquier `hash_c`/`hash_d` que no calce entra a la misma lista `mismatched` (`_collect_mismatches`, :41-44). El resumen distingue `kind`, `expected` y `actual`, pero el `ok` los aplasta a todos por igual.

## Por que importa: son dos cosas opuestas

- **STALE**: el `.md` cambio legitimamente (alguien lo edito, un comando lo reescribio) y el indice quedo atras. El arreglo es `stores update`. Es trabajo pendiente, no daño.
- **CORRUPTO**: el indice no corresponde a ninguna version real del archivo. El arreglo es investigar. Es daño.

Hoy las dos dan exactamente la misma salida, asi que el usuario no puede saber si corre `stores update` tranquilo o si tiene que parar a investigar.

## Evidencia de este episodio

Reparando la deriva de `desk/` en el repo sldb, `deskops doctor` reportaba "Legacy desk detected: sldb stores check failed". El check decia `FAIL: store integrity` y nada mas. Hubo que despachar un subagente a leer el codigo de `diagnose_store` para averiguar QUE registro estaba roto, porque el comando no lo dice. Resulto ser stale puro: `stores update` + re-track lo dejo en `PASS: store integrity` sin que nada estuviera corrupto. Se perdio tiempo tratando como posible corrupcion algo que era desactualizacion.

## La propuesta: es calculable, no heuristico

Para un documento trackeado con `path` y `hash_c` esperado, git ya sabe:

1. Si el archivo esta limpio en el working tree y su blob actual no calza con el `hash_c` del indice -> el indice quedo atras: **STALE**.
2. Si el archivo tiene modificaciones sin commitear -> **STALE por edicion local**, y se puede decir contra que commit calzaba.
3. Si el `hash_c` del indice no corresponde a NINGUNA version del archivo en la historia (`git log --follow` sobre esa ruta) -> nadie escribio nunca ese contenido: **CORRUPTO**.
4. Si el archivo no existe en disco ni en la historia reciente -> **HUERFANO**, otra categoria distinta.

El caso (3) es el unico que merece alarma, y hoy se confunde con los otros tres.

## Done when

- `stores check` distingue al menos `stale` / `corrupt` / `orphan` en su salida, no un booleano.
- La salida nombra los documentos afectados y su categoria, en vez de una linea.
- Para stale, sugiere el comando de arreglo (`stores update`) en el propio mensaje.
- El caso corrupto se apoya en la historia de git, con el comando exacto que lo determino, y degrada con gracia cuando el store no esta en un repo git (ahi todo mismatch es "indeterminado", no "corrupto").
- `deskops doctor` puede consumir esa distincion en vez de reportar "stores check failed" a secas.

## Nota de alcance

Esto NO es pedir que sldb dependa de git para funcionar. Es usar git como fuente de evidencia CUANDO esta disponible, para clasificar un fallo que hoy no se clasifica. Sin git, el comando debe seguir funcionando exactamente igual que hoy, solo que diciendo "no puedo determinar si es stale o corrupto" en vez de fingir un veredicto unico.
