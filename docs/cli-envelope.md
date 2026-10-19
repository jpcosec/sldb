# CLI envelope and typed exit codes

Estado (2026-10-19): opcional. `sldb --envelope <comando> ...` envuelve cualquier comando; sin
la opción, la CLI imprime y sale como siempre, porque deskops y otros consumidores parsean esa
salida (`models list`, `stores list` y `stores check` con `--format json`). El paso a envelope
por defecto se coordina por inbox con cada consumidor; hasta entonces es opt-in.

## Forma

Un solo valor JSON en stdout por corrida:

```json
{"ok": true, "command": "stores list", "store": {"path": "/repo/.sldb"},
 "revision": "<store_hash>", "data": {...}, "warnings": []}
{"ok": false, "command": "docs show", "store": {...}, "revision": "...",
 "error": {"type": "docs/missing", "message": "Unknown document target: x"}, "exit": 1}
```

- `data` es el JSON que imprimió el comando (pasar `--format json` donde el comando lo tiene); si
  imprimió texto, `{"text": ...}`.
- `store` y `revision` (el `store_hash`) son los del store contra el que corrió, o `null`.
- `command` es el grupo y el subcomando.
- Un exit distinto de 0 siempre va con `ok: false` y repite `exit` en el envelope.

## Códigos de salida

| exit | tipo | cuándo |
|---|---|---|
| 0 | — | ok |
| 1 | `*/missing` | algo nombrado no existe (`docs/missing` <!-- gone -->, `fields/missing`, `links/missing`, `io/missing`) |
| 2 | `*/ambiguous` | un selector nombra más de una cosa (`docs/ambiguous` <!-- gone -->) |
| 3 | `*/rejected` | la entrada se rechaza (`models/`, `validate/`, `docs/`, `graph/rejected`) |
| 4 | `store/busy` | otro proceso escribe el store (`--wait` espera) |
| 5 | `store/error`, `markdown/runtime`, `sldb/error` | el store o el runtime fallaron |
| 6 | `cli/usage` | uso incorrecto (argparse) |
| 70 | `cli/unexpected` | cualquier otra cosa |

Un comando que corre y reporta hallazgos (por ejemplo `stores check` en FAIL) es
`<grupo>/failed`, con el código de salida del propio comando y su salida en `data`.

La tabla vive en `src/sldb/cli/error_types.py`, y el envelope, en `src/sldb/cli/envelope.py`.
